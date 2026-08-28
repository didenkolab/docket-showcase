---
key: FIELD-101
title: A job moved to tomorrow stays on today's list until the app restarts
type: bug
status: Backlog
status_category: todo
priority: normal
assignee: '[[aiko]]'
parent: "[[FIELD-1 Job scheduling]]"
labels: ["[[mobile]]"]
created: 2026-08-28T11:10:00Z
updated: 2026-08-28T11:14:00Z
aliases: []
tags: [device/older-fleet]
---

The phone is told the job has moved and removes it from the server's answer, but the list on the screen was built when the day was opened and nothing tells it to build itself again. The crew sees a job it is no longer going to, which on the older half of the fleet lasts until somebody closes the app properly.

## Acceptance

- [ ] A job moved off the crew leaves the day's list without a restart
- [ ] The same is true of a job moved onto the crew mid-morning

## Comments
