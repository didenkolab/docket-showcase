---
key: FIELD-102
title: A job sent twice from a phone appears twice on the board
type: bug
status: Ready
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[FIELD-3 Offline mobile]]"
labels: ["[[offline-sync]]"]
created: 2026-08-28T11:20:00Z
updated: 2026-08-28T14:30:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 3
relates: ["[[FIELD-50 Offline edits are lost when the server's version wins the merge]]"]
---

A phone that sends its queue, loses the signal before it hears the answer and sends again produces two of the same finished job, and the office invoices one of them and wonders about the other. The queue is ordered and retried; what it is not is idempotent, which is the same lesson the payments work learned in July.

## Acceptance

- [ ] The same queued change sent twice is applied once
- [ ] A duplicate that already reached the board can be merged into the original

## Comments

**mateo · 2026-08-28 11:30** — Two of the crews' phones did this on the trial week and I have been able to make it happen on demand: send the queue standing in the tunnel entrance, walk in, walk out. Same job, two rows, both finished, both invoiceable. It is the sync loss's cousin — the phone is being careful about not losing work and nothing at the other end is being careful about not counting it twice.
