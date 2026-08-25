---
key: HARBOR-189
title: A booking made the night the clocks change is a day short
type: bug
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: []
created: 2026-08-25T11:30:00Z
updated: 2026-08-25T11:30:00Z
aliases: []
tags: []
---

Nights are counted by subtracting two timestamps and dividing by twenty-four hours, which is right for every night of the year except the two the clocks change on. A week over the October change is billed as six nights.

## Acceptance

- [ ] A range over a clock change counts the nights a calendar would count
- [ ] The invoice for such a range charges for every night the boat was there

## Comments
