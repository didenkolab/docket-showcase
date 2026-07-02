---
key: HARBOR-30
title: Hold a berth for twenty minutes while the guest pays
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-1 Season bookings]]"
labels: ["[[bookings]]", "[[payments]]"]
created: 2026-06-29T09:35:00Z
updated: 2026-07-02T15:45:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 2]]"
estimate: 5
---

Between choosing a berth and the card clearing there is a minute or two in which the berth belongs to nobody, and on a Friday in July that is long enough for two people to buy it. A hold is a reservation with an expiry: the berth is off the market for twenty minutes, and comes back on its own if the payment never lands.

## Acceptance

- [x] A held berth is not offered to anybody else while the hold lasts
- [x] An unpaid hold expires on its own and the berth is free again
- [x] A payment that lands after the hold expired is refunded, not silently kept

## Comments
