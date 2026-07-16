---
key: HARBOR-85
title: Berth calendar shows a boat that left yesterday as still moored
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: ["[[bookings]]"]
created: 2026-07-16T11:40:00Z
updated: 2026-07-16T11:40:00Z
aliases: []
tags: []
---

A booking that ended yesterday is still drawn as occupying its berth today, so the office turns boats away from berths that are empty. The calendar compares the booking's last night with today rather than with the morning after it.

## Acceptance

- [ ] A booking that ended yesterday leaves its berth free today
- [ ] A booking that ends today still shows the boat as moored until the morning

## Comments
