---
key: HARBOR-38
title: Two guests can hold the same berth if they click at the same second
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[HARBOR-1 Season bookings]]"
labels: ["[[bookings]]"]
created: 2026-07-01T14:20:00Z
updated: 2026-07-01T14:24:00Z
aliases: []
tags: [regress]
---

Two browsers, same berth, same week, confirm within the same second: both holds are created and both guests are told the berth is theirs. The availability check and the write are two separate reads of the same table with nothing between them.

## Acceptance

- [ ] Two simultaneous holds on one berth leave exactly one winner
- [ ] The loser is told the berth went, not shown an error page

## Comments
