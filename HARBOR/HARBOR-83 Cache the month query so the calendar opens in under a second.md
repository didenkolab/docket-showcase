---
key: HARBOR-83
title: Cache the month query so the calendar opens in under a second
type: task
status: In review
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: []
created: 2026-07-13T10:20:00Z
updated: 2026-07-17T15:40:00Z
aliases: []
tags: [area/api]
sprint: "[[Sprint 3]]"
estimate: 3
---

The month query is the one request the office makes forty times a day, and on a four-hundred-berth marina it takes two and a half seconds. Bookings change rarely enough that the answer can be kept until one does.

## Acceptance

- [x] A month opens in under a second on a four-hundred-berth marina
- [x] A new or moved booking invalidates the month it touches

## Comments
