---
key: FIELD-24
title: Two jobs can be booked into the same crew's two o'clock
type: bug
status: Done
status_category: done
priority: high
assignee: '[[tomasz]]'
parent: "[[FIELD-1 Job scheduling]]"
labels: ["[[routing]]"]
created: 2026-07-15T14:20:00Z
updated: 2026-07-27T17:00:00Z
aliases: []
tags: []
sprint: "[[Sprint 3]]"
estimate: 3
tested_by: ["[[FIELD-30 The day comes back in the order it is meant to happen]]", "[[FIELD-31 A crew cannot be in two places at two o'clock]]"]
---

The board asks whether the slot is free and then writes the job, and between the two questions there is nothing stopping the other dispatcher doing the same. Two jobs at two o'clock is one crew, one van, and a customer who was promised an afternoon.

## Acceptance

- [x] A slot that has been taken between the check and the write is refused
- [x] The refusal names the job that took the slot so the dispatcher can move one

## Comments

**mateo · 2026-07-15 14:30** — Reproduced it in ten seconds with two browser windows, which means the office will find it on the first Monday. Both windows accept the drop and the board shows both jobs; refresh and they are still both there. The check and the write are two separate questions with a gap in the middle.
