import asyncio
from typing import Dict, Optional
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def run_streamable_mcp_client(
    server_url: str, 
    headers: Optional[Dict[str, str]] = None
):
    """
    Connects to a remote Streamable HTTP MCP server (e.g., pointing to /mcp).
    
    :param server_url: Full HTTP/HTTPS endpoint URL (e.g., "https://api.example.com/mcp")
    :param headers: Headers such as Bearer tokens, API keys, etc.
    """
    print(f"Connecting to Streamable HTTP server at: {server_url}...")

    # streamablehttp_client manages session headers, connection reuse, 
    # and streaming fallback automatically on a single endpoint.
    async with streamablehttp_client(server_url, headers=headers) as (read_stream, write_stream, session_id):
        
        if session_id:
            print(f"Session established with ID: {session_id}")
            
        async with ClientSession(read_stream, write_stream) as session:
            # Step 1: Handshake
            await session.initialize()
            print("Session initialized successfully!\n")

            # Step 2: Discover capabilities/tools
            print("--- Available Tools ---")
            tools_response = await session.list_tools()
            
            if not tools_response.tools:
                print("No tools returned by this server.")
                return

            for tool in tools_response.tools:
                print(f"• Tool: {tool.name}")
                #print(f"  Description: {tool.description}")
                #print(f"  Schema: {tool.inputSchema}\n")

            total_count = len(tools_response.tools)
            print(f"\n Total Tools Found: {total_count}\n")

            # # Step 3: Example call to a tool
            # target_tool = tools_response.tools[0].name
            # print(f"--- Calling Tool: '{target_tool}' ---")
            
            # # Update with parameters required by your target tool's schema
            # sample_args = {}
            
            # result = await session.call_tool(target_tool, arguments=sample_args)
            
            # print("Response from server:")
            # for content in result.content:
            #     if content.type == "text":
            #         print(f"  [Text]:\n{content.text}")
            #     elif content.type == "image":
            #         print("  [Image received]")


if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Point directly to your remote /mcp endpoint
    REMOTE_MCP_ENDPOINT = "https://your-remote-domain.com/mcp"
    
    # Supply authorization tokens if your remote server requires them
    AUTH_HEADERS = {
        "Authorization": "Bearer YOUR_API_KEY_OR_TOKEN"
    }

    try:
        asyncio.run(
            run_streamable_mcp_client(REMOTE_MCP_ENDPOINT, headers=AUTH_HEADERS)
        )
    except Exception as err:
        print(f"\n[Error] Could not connect to MCP server: {err}")