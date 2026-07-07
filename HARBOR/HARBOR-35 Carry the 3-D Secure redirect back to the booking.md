---
key: HARBOR-35
title: Carry the 3-D Secure redirect back to the booking
type: subtask
status: Done
status_category: done
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-33 Take the card payment when a booking is confirmed]]"
labels: []
created: 2026-06-29T11:05:00Z
updated: 2026-07-07T15:10:00Z
aliases: []
tags: []
estimate: 5
tested_by: ["[[HARBOR-44 The card is charged when the booking is confirmed]]", "[[HARBOR-45 The guest comes back from the bank's page to their own booking]]"]
---

The bank sends the guest away to its own page and back again, and whatever we were holding in memory is gone by the time they return. The booking has to be findable from the redirect alone, on a phone that may have changed network.

## Comments
