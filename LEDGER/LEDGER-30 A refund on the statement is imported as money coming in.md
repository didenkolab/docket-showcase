---
key: LEDGER-30
title: A refund on the statement is imported as money coming in
type: bug
status: QA
status_category: doing
priority: high
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-07-16T14:20:00Z
updated: 2026-07-22T09:40:00Z
aliases: []
tags: [regress]
sprint: "[[Sprint 3]]"
estimate: 2
---

One of the three banks reports a refund as a credit with a transaction code that says it reverses a debit, and the importer reads the sign and ignores the code. A business that refunded a customer four hundred appears to have been paid four hundred, and the month's turnover is eight hundred out.

## Acceptance

- [x] A reversal is imported with the direction its transaction code says
- [x] The demo data's three wrong-way lines are reimported and correct

## Comments

**mateo · 2026-07-16 14:30** — Caught it against the second bank's test statements, which are the only ones with a reversal in them. Three lines, all credits, all of them reversals of card refunds, all imported as income. The sign on the amount is right and the code beside it says the opposite, and we only read the sign.
