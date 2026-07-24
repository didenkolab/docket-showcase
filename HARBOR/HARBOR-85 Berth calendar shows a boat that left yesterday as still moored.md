---
key: HARBOR-85
title: Berth calendar shows a boat that left yesterday as still moored
type: bug
status: Done
status_category: done
priority: high
assignee: '[[tomasz]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: ["[[bookings]]"]
created: 2026-07-16T11:40:00Z
updated: 2026-07-24T10:50:00Z
aliases: []
tags: [regress]
sprint: "[[Sprint 3]]"
estimate: 2
---

A booking that ended yesterday is still drawn as occupying its berth today, so the office turns boats away from berths that are empty. The calendar compares the booking's last night with today rather than with the morning after it.

## Acceptance

- [x] A booking that ended yesterday leaves its berth free today
- [x] A booking that ends today still shows the boat as moored until the morning

## Comments

**mateo · 2026-07-16 11:50** — Sandholm rang about this one: pontoon C looked full on Tuesday and had four empty slips on it. Every booking whose last night was Monday was still drawn on Tuesday. It is an off-by-one on the last night, not a caching problem — it survives a hard reload.

**tomasz · 2026-07-22 15:10** — The check was `last_night >= today` where it wants `last_night >= today` on the checkout morning only. Fixed by asking the booking when the berth is free rather than when the guest leaves, which are a night apart on purpose.
