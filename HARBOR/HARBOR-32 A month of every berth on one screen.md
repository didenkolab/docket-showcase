---
key: HARBOR-32
title: A month of every berth on one screen
type: story
status: QA
status_category: doing
priority: normal
assignee: '[[priya]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: ["[[bookings]]"]
created: 2026-06-29T09:50:00Z
updated: 2026-07-17T10:20:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 3]]"
blocks: ["[[HARBOR-81 Drag a booking to another berth]]"]
---

This is the wall planner. Berths down the side, days across the top, one cell per berth-night, and it has to be legible from the other side of the harbour office. It is also the screen the office will keep open all day, which makes how it scrolls a feature rather than a detail.

## Acceptance

- [x] Every berth and every day of a month fit on one screen
- [x] A booking reads as one bar across the nights it holds
- [x] Scrolling a month of forty berths does not stutter

## Comments

**tomasz · 2026-07-15 09:30** — Back to you: it is lovely on forty berths and unusable on four hundred, and Sandholm have four hundred and six. The month query returns every cell rather than every booking, so the payload grows with the marina.
