---
key: LEDGER-22
title: Two invoices issued in the same minute get the same number
type: bug
status: Done
status_category: done
priority: high
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-07-06T14:30:00Z
updated: 2026-07-24T16:30:00Z
aliases: []
tags: [regress]
sprint: "[[Sprint 2]]"
estimate: 2
tested_by: ["[[LEDGER-39 The totals underneath add the lines up]]", "[[LEDGER-40 Two invoices numbered from the same reading do not get the same number]]"]
---

The next number is read, then written, and two issues that overlap read the same number before either writes it. The sequence is the one thing in the product that was supposed to be impossible to get wrong, and it is wrong in the ordinary way: a read and a write with nothing holding them together.

## Acceptance

- [x] Two invoices issued at the same instant are given two different numbers
- [x] The duplicate pair already in the demo data is renumbered and recorded

## Comments

**mateo · 2026-07-06 14:40** — Two invoices, both numbered 2026-0041, issued four seconds apart by the same business. I found it by clicking issue on two tabs, which is not a thing a person does on purpose but is exactly what the batch send will do a hundred times a minute. The sequence is read-then-write with a gap in the middle.
