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
updated: 2026-07-01T14:41:00Z
aliases: []
tags: [regress]
sprint: "[[Sprint 2]]"
estimate: 3
---

Two browsers, same berth, same week, confirm within the same second: both holds are created and both guests are told the berth is theirs. The availability check and the write are two separate reads of the same table with nothing between them.

## Acceptance

- [ ] Two simultaneous holds on one berth leave exactly one winner
- [ ] The loser is told the berth went, not shown an error page

## Comments

**mateo · 2026-07-01 14:30** — Reproduced eight times out of ten with two tabs and a stopwatch: berth A12, week of 10 August, both confirmations say 'held for you'. The second hold overwrites the first rather than being refused, so the first guest keeps a confirmation for a berth they do not have.
