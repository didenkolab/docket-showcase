---
key: LEDGER-22
title: Two invoices issued in the same minute get the same number
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-07-06T14:30:00Z
updated: 2026-07-06T14:34:00Z
aliases: []
tags: [regress]
---

The next number is read, then written, and two issues that overlap read the same number before either writes it. The sequence is the one thing in the product that was supposed to be impossible to get wrong, and it is wrong in the ordinary way: a read and a write with nothing holding them together.

## Acceptance

- [ ] Two invoices issued at the same instant are given two different numbers
- [ ] The duplicate pair already in the demo data is renumbered and recorded

## Comments
