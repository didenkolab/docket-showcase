---
key: FIELD-102
title: A job sent twice from a phone appears twice on the board
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[FIELD-3 Offline mobile]]"
labels: ["[[offline-sync]]"]
created: 2026-08-28T11:20:00Z
updated: 2026-08-28T11:20:00Z
aliases: []
tags: []
---

A phone that sends its queue, loses the signal before it hears the answer and sends again produces two of the same finished job, and the office invoices one of them and wonders about the other. The queue is ordered and retried; what it is not is idempotent, which is the same lesson the payments work learned in July.

## Acceptance

- [ ] The same queued change sent twice is applied once
- [ ] A duplicate that already reached the board can be merged into the original

## Comments
