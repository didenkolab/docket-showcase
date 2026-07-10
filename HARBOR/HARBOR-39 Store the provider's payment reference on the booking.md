---
key: HARBOR-39
title: Store the provider's payment reference on the booking
type: subtask
status: Done
status_category: done
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-33 Take the card payment when a booking is confirmed]]"
labels: []
created: 2026-07-02T10:20:00Z
updated: 2026-07-10T11:40:00Z
aliases: []
tags: []
estimate: 2
tested_by: ["[[HARBOR-45 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-46 A retried confirmation charges the card once]]"]
---

Without the provider's own reference on the booking, matching a charge to a berth means reading two lists side by side, which is what the marina's bookkeeper does today and what Harbor is supposed to stop.

## Comments
