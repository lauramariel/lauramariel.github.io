---
layout: post
title:  "New Actions in Nutanix X-Play in PC.2021.7"
date:   2021-08-04 20:37:40 -0700
categories: aiops, automation, prism ops, nutanix
render: false
---
With the release of Nutanix Prism Central 2021.7 comes additional actions to Nutanix X-Play. Nutanix X-Play is a simple low-code, no-code automation tool built into Nutanix Prism Central that helps you automate routine operations and tasks.

You can define a set of actions or series of actions called playooks based on a trigger. The trigger can be an event (such as VM creation or update), an alert (such as memory usage on a VM), or an incoming webhook. Then, you can build a series of actions that should be carried out when the trigger is fired, such as increasing memory of the affected resource, running scripts, sending e-mails, calling an API, the list goes on.

With the recent release of PC.2021.7 the following actions have been added:

- **Add to Category** - Add a VM, host, or cluster to a category
- **Remove From Category** - Remove a VM, host, or cluster from a category
- **Microsoft Teams** - Send a message to Microsoft Teams
- **Ansible** - Trigger an Ansible workflow or job template

![New Actions](../images/xplay-new-actions.png)

To see these new playbooks in action, check out this video!

<iframe width="560" height="315" src="https://www.youtube.com/embed/q4HFcGMO11Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
