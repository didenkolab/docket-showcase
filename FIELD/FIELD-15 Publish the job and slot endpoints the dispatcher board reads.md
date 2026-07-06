---
key: FIELD-15
title: Publish the job and slot endpoints the dispatcher board reads
type: task
status: In review
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[FIELD-1 Job scheduling]]"
labels: []
created: 2026-06-29T10:15:00Z
updated: 2026-07-06T16:20:00Z
aliases: []
tags: [area/api]
sprint: "[[Sprint 2]]"
estimate: 3
---

The board, the phone and eventually the customer's own booking page all want the same three questions answered — what is on this crew today, what is unplanned, and is this slot free — and answering them three different ways is how the three screens come to disagree about the same day.

## Acceptance

- [x] One endpoint answers a crew's day and one answers a day's unplanned work
- [x] A slot that is taken is refused with the job that took it, not a bare error

## Comments
