---
key: LEDGER-30
title: A refund on the statement is imported as money coming in
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-07-16T14:20:00Z
updated: 2026-07-16T14:24:00Z
aliases: []
tags: [regress]
---

One of the three banks reports a refund as a credit with a transaction code that says it reverses a debit, and the importer reads the sign and ignores the code. A business that refunded a customer four hundred appears to have been paid four hundred, and the month's turnover is eight hundred out.

## Acceptance

- [ ] A reversal is imported with the direction its transaction code says
- [ ] The demo data's three wrong-way lines are reimported and correct

## Comments
