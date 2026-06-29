---
key: HARBOR-35
title: Carry the 3-D Secure redirect back to the booking
type: subtask
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-33 Take the card payment when a booking is confirmed]]"
labels: []
created: 2026-06-29T11:05:00Z
updated: 2026-06-29T11:05:00Z
aliases: []
tags: []
---

The bank sends the guest away to its own page and back again, and whatever we were holding in memory is gone by the time they return. The booking has to be findable from the redirect alone, on a phone that may have changed network.

## Comments
