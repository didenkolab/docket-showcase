---
key: HARBOR-37
title: Move the payment provider's keys out of the repository
type: task
status: Backlog
status_category: todo
priority: high
assignee: '[[ola]]'
parent: "[[HARBOR-3 Card payments]]"
labels: []
created: 2026-06-30T15:40:00Z
updated: 2026-06-30T15:40:00Z
aliases: []
tags: []
---

The sandbox keys went in with the first payment commit and the live ones would have followed. They belong in the deployment's own secret store, and the old ones have to be rotated because a key that has been in a repository is a key that is public.

## Acceptance

- [ ] No provider key is in the repository or its history going forward
- [ ] The sandbox keys that were committed are rotated

## Comments
