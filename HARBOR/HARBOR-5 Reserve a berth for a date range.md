---
key: HARBOR-5
title: Reserve a berth for a date range
type: story
status: Ready
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-1 Season bookings]]"
labels: ["[[bookings]]"]
created: 2026-06-15T09:40:00Z
updated: 2026-06-15T11:10:00Z
aliases: []
tags: [area/api]
definition_of_done: team
sprint: "[[Sprint 1]]"
estimate: 5
---

Everything else in Harbor hangs off one sentence: this boat has that berth from this day to that one. A reservation is the range, the berth and the boat, and it either exists for every night in the range or it does not exist at all — a berth held for four of five nights is the argument the harbour office has to have on the pontoon on the fifth.

## Acceptance

- [ ] A reservation covers every night of the range or none of them
- [ ] A berth already taken for one night of the range is refused, naming the night
- [ ] The reservation is on the berth calendar the moment it is made

## Comments
