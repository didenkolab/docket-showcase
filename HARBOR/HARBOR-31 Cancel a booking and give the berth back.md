---
key: HARBOR-31
title: Cancel a booking and give the berth back
type: story
status: QA
status_category: doing
priority: normal
assignee: '[[priya]]'
parent: "[[HARBOR-1 Season bookings]]"
labels: ["[[bookings]]"]
created: 2026-06-29T09:40:00Z
updated: 2026-07-09T11:10:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 2]]"
estimate: 3
tested_by: ["[[HARBOR-40 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-41 A cancelled booking gives its nights back to the free list]]"]
---

Weather cancels more bookings than people do. The office needs one action that ends the booking, frees every night it held and leaves a record of who cancelled it and when — a berth quietly deleted is a berth nobody can explain in October.

## Acceptance

- [x] Cancelling frees every night the booking held
- [x] The cancelled booking is still readable, with who cancelled it and when
- [x] The invoice for it is marked cancelled rather than deleted

## Comments
