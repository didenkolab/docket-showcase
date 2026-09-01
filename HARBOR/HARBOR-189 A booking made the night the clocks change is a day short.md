---
key: HARBOR-189
title: A booking made the night the clocks change is a day short
type: bug
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-2 Berth calendar]]"
labels: []
created: 2026-08-25T11:30:00Z
updated: 2026-09-01T15:55:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 2
---

Nights are counted by subtracting two timestamps and dividing by twenty-four hours, which is right for every night of the year except the two the clocks change on. A week over the October change is billed as six nights.

## Acceptance

- [x] A range over a clock change counts the nights a calendar would count
- [ ] The invoice for such a range charges for every night the boat was there

## Comments

**mateo · 2026-08-25 11:40** — Found it on purpose rather than in the wild: booked 24 to 31 October at Vik and got six nights and six nights' money. It will be real in eight weeks, so it is worth doing now while nobody has been overcharged.
