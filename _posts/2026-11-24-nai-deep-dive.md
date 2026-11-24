---
layout: post
title:  "Under the Hood of Nutanix Enterprise AI 2.8"
date: 2026-11-24 14:38:29 -0800
tags: [kubernetes, genai]
---

# Nutanix Enterprise AI Deep Dive: What Happens on Kubernetes When You Click "Create"

> A behind-the-scenes look at the Kubernetes resources Nutanix Enterprise AI (NAI) creates for each feature — Agent Gateway and AI Inference.

## Introduction

Nutanix Enterprise AI (NAI) is a Kubernetes-native platform. Every action you take in the NAI UI — creating a provider, deploying a model, exposing an MCP server — translates into concrete Kubernetes resources. This post maps each NAI feature to the exact CRDs, Deployments, Services, and other resources that appear in your cluster.

All observations are from a live NKP 2.19 cluster running NAI 2.8.1, with NAI deployed in the `nai-system`, `nai-admin`, and `nai-admin-extensions` namespaces.

In this example environment, we have the following entities created:

### Agent Gateway
1. Provider: shared-nai
2. Unified endpoint: uep-chat
3. MCP server (local): demo-crm
4. MCP server (remote): weather
5. An MCP connector: weather-forecast

### AI Inference
1. A model: llama-32-1b
2. A local endpoint serving that model: llama-32-1b

## Architecture Overview

NAI spans three namespaces:

| Namespace | Purpose |
|-----------|---------|
| `nai-system` | NAI control plane: API server, UI, IAM, Envoy Gateway, AI Gateway controller |
| `nai-admin` | User-created resources: providers, models, unified endpoints, local endpoints |
| `nai-admin-extensions` | MCP servers (local deployments + remote backends) |

The Envoy Gateway (in `envoy-gateway-system`) handles all external traffic. The AI Gateway controller (in `nai-system`) extends Envoy with AI-specific routing.

**[Interactive Diagram: Overview](../html/nai-combined.html#overview)**

---

## Agent Gateway

### 1. Provider (e.g., "shared-nai")

A Provider connects NAI to an external LLM backend (e.g. OpenAI, Anthropic, or Nutanix AI Inference).

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| Secret | `nai-admin` | Opaque | Stores the provider API key |
| AIGatewayProvider | `nai-admin` | `iep.nai.nutanix.com/v1alpha1` | NAI CR tracking the provider config |
| Backend | `nai-admin` | `gateway.envoyproxy.io/v1alpha1` | Envoy backend pointing to provider hostname |
| AIServiceBackend (×2) | `nai-admin` | `aigateway.envoyproxy.io/v1alpha1` | OpenAI + Cohere API format backends |
| BackendTLSPolicy | `nai-admin` | (auto) | TLS config for provider connection |

**Key spec fields:**
- `backend.hostname`: The external LLM provider hostname
- `backend.port`: 443 (TLS)
- `schemaVersion.OpenAI.prefix`: `enterpriseai/v1`
- `schemaVersion.Cohere.version`: `enterpriseai/v2`
- Credentials reference the Secret by name

**[Interactive Diagram: Provider](../html/nai-combined.html#provider)**

### 2. Unified Endpoint (e.g., "uep-chat")

A Unified Endpoint is a load-balanced entry point that routes requests to one or more models from a provider.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| AIGatewayRoute | `nai-admin` | `aigateway.envoyproxy.io/v1alpha1` | Envoy AI Gateway route with model-based routing |
| HTTPRoute (auto) | `nai-system` | `gateway.networking.k8s.io/v1` | Created by Envoy Gateway from AIGatewayRoute |

**Key spec fields:**
- `parentRefs`: References the Gateway (`nai-ingress-gateway` in `nai-system`)
- `rules.matches`: Header `x-ai-eg-model` must equal the endpoint name
- `rules.backendRefs`: List of models with weights and priorities for load balancing
- `llmRequestCosts`: Tracks input/output/total tokens for usage monitoring
- `timeouts.request`: 300s

**Example:** The "uep-chat" endpoint load-balances 50/50 between `gemma-4-31b-it-w4a16` and `gpt-oss-120b`, both served by the same provider backend.

**[Interactive Diagram: Unified Endpoint](../html/nai-combined.html#unified-endpoint)**

### 3. MCP Server — Local (e.g., "demo-crm")

A local MCP server runs a container image inside the cluster.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| Deployment | `nai-admin-extensions` | `apps/v1` | Runs the MCP server container |
| Service | `nai-admin-extensions` | `v1` | ClusterIP on port 3000 |
| Backend | `nai-admin-extensions` | `gateway.envoyproxy.io/v1alpha1` | Envoy backend → service FQDN |
| MCPRoute | `nai-admin-extensions` | `aigateway.envoyproxy.io/v1beta1` | Exposes at `/enterpriseai/gateway/mcp/<name>` |

**Key details:**
- Image: `registry.nutanixdemo.com/bootcamps/demo-mcp-server:latest`
- Port: 3000 (configurable)
- Resources: 1 CPU, 1Gi RAM (configurable)
- Readiness probe: TCP socket on port 3000
- NAI labels: `nai.nutanix.com/feature: mcp`, `nai.nutanix.com/mcp-server-type: local`

**[Interactive Diagram: MCP (Local)](../html/nai-combined.html#mcp-local)**

### 4. MCP Server — Remote (e.g., "weather")

A remote MCP server proxies to an external endpoint. No pods are created.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| Backend | `nai-admin-extensions` | `gateway.envoyproxy.io/v1alpha1` | Envoy backend → external FQDN:443 |
| MCPRoute | `nai-admin-extensions` | `aigateway.envoyproxy.io/v1beta1` | Exposes at `/enterpriseai/gateway/mcp/<name>` |

**Key details:**
- Backend type: `Endpoints` with FQDN (e.g., `nws.caseyjhand.com:443`)
- No Deployment, Service, or Pod created
- Envoy proxies requests directly to the remote server over TLS
- `toolSelector.include` filters which tools are exposed

**[Interactive Diagram: MCP (Remote)](../html/nai-combined.html#mcp-remote)**

### 5. MCP Connector (e.g., "weather-forecast")

An MCP Connector creates a filtered view of an existing MCP server, exposing only specific tools.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| MCPRoute | `nai-admin-extensions` | `aigateway.envoyproxy.io/v1beta1` | Filtered route with toolSelector |
| Backend (auto) | `nai-admin-extensions` | `gateway.envoyproxy.io/v1alpha1` | MCP proxy backend (extproc sidecar) |

**Key details:**
- The MCPRoute references the source MCP server's Backend
- `toolSelector.include` specifies which tools to expose (e.g., only `nws_get_forecast`)
- A proxy Backend is auto-created pointing to the extproc sidecar (`192.0.2.42:9856`)
- The connector gets its own path: `/enterpriseai/gateway/mcp/<connector-name>`
- No new pods — reuses the existing MCP server backend
- Multiple connectors can filter different tool subsets from the same server

**[Interactive Diagram: MCP Connector](../html/nai-combined.html#mcp-connector)**

---

## AI Inference

### 1. Model (e.g., "llama-32-1b" from HuggingFace)

A Model downloads weights from HuggingFace (or NVIDIA NGC) and stores them in a PVC.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| Model | `nai-admin` | `iep.nai.nutanix.com/v1alpha1` | Tracks download status and storage URL |
| PVC | `nai-admin` | `v1` | 10G storage on `nai-nfs-storage` |
| Job/Pod (one-time) | `nai-admin` | `batch/v1` | Downloads model weights to PVC |

**Model CR spec:**
- `modelSize`: 10G (determines PVC capacity)
- `outputFormat`: hf
- `provider.hf.repoId`: `meta-llama/Llama-3.2-1B-Instruct`
- `provider.hf.repoVersion`: Git commit hash
- `provider.secretName`: Secret containing HuggingFace token
- `storage.sc`: `nai-nfs-storage`

**Status progression:** Pending → Processing → Active

**[Interactive Diagram: Model Download](../html/nai-combined.html#model-download)**

### 2. Local Endpoint (e.g., "llama-32-1b" served via vLLM)

A Local Endpoint deploys a model for inference using KServe with vLLM.

**What gets created:**

| Resource | Namespace | Kind | Purpose |
|----------|-----------|------|---------|
| InferenceService | `nai-admin` | `serving.kserve.io/v1beta1` | Manages full serving lifecycle |
| Deployment | `nai-admin` | `apps/v1` | Runs vLLM container |
| Service | `nai-admin` | `v1` | ClusterIP on port 80 |
| HPA | `nai-admin` | `autoscaling/v2` | Autoscaling (min 1, max 1) |

**InferenceService spec highlights:**
- Image: `registry.nutanixdemo.com/bootcamps/nutanix/nai-vllm:v0.26.0`
- Command: `vllm serve /mnt/models`
- Args: `--served-model-name`, `--max-model-len=4096`, `--enable-auto-tool-choice`, `--tool-call-parser=llama3_json`
- Resources: 12 CPU, 12Gi RAM
- Node selector: `cpu-cpuid.AMXBF16: "true"` (Intel AMX required)
- STORAGE_URI: `pvc://<model-pvc>/model-files`
- Port: 8000 (OpenAI-compatible API)

**[Interactive Diagram: Local Endpoint](../html/nai-combined.html#local-endpoint)**

---

## Summary: Resource Mapping

| NAI Feature | Primary K8s Resource | Supporting Resources |
|-------------|---------------------|---------------------|
| Provider | `AIGatewayProvider` | Secret, Backend, AIServiceBackend (×2), BackendTLSPolicy |
| Unified Endpoint | `AIGatewayRoute` | HTTPRoute (auto), Backend refs |
| MCP Server (local) | `MCPRoute` | Deployment, Service, Backend |
| MCP Server (remote) | `MCPRoute` | Backend (external FQDN) |
| MCP Connector | `MCPRoute` | Backend (extproc proxy, auto-created) |
| Model | `Model` | PVC, Download Job |
| Local Endpoint | `InferenceService` | Deployment, Service, HPA |

## Common Patterns

1. **Every NAI feature creates CRDs** — NAI is fully Kubernetes-native
2. **Envoy Gateway is the traffic layer** — all external access goes through the Gateway
3. **The AI Gateway controller extends Envoy** — AIGatewayRoute/MCPRoute are reconciled into HTTPRoutes
4. **The extproc sidecar** (`ai-gateway-extproc`) handles AI-specific processing (token counting, tool filtering)
5. **Labels** (`nai.nutanix.com/feature`, `nai.nutanix.com/mcp-server-type`) enable resource discovery
6. **Owner references** link child resources to their parent (e.g., Backend → MCPRoute → Gateway)
7. **Namespaces** separate concerns: `nai-admin` (user resources), `nai-admin-extensions` (MCP), `nai-system` (platform)

## NAI Operator Architecture

NAI uses several operators/controllers:

| Controller | Manages | Namespace |
|-----------|---------|-----------|
| NAI IEP Operator | AIGatewayProvider, Model, AIGatewayRoute | `nai-system` |
| Envoy Gateway Controller | Gateway, HTTPRoute, Backend, MCPRoute | `envoy-gateway-system` |
| AI Gateway Controller | Extends Envoy with AI routing, extproc injection | `nai-system` |
| KServe Controller | InferenceService, Deployment, Service, HPA | `nai-admin` |
| NAI API Server | REST API, database, business logic | `nai-system` |

All controllers watch their respective CRDs and reconcile the desired state into concrete Kubernetes resources. When you delete a resource in the NAI UI, the controller cleans up the dependent resources (via ownerReferences and finalizers).
