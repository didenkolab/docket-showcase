---
key: LEDGER-4
title: Number invoices in one unbroken sequence per business year
type: story
status: QA
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-06-15T09:55:00Z
updated: 2026-06-22T10:30:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 1]]"
estimate: 3
---

An invoice number is the only thing about an invoice that the tax office cares about before it cares about anything else: the sequence has to start at one each business year, have no gaps in it, and never give the same number to two documents. A gap has to be explainable and a duplicate is not explainable at all, which is why this is the first thing Ledgerline does rather than the last.

## Acceptance

- [x] Each business gets its own sequence, starting again at the turn of its year
- [x] Two invoices issued at the same moment get two different numbers
- [x] A number is allocated when the invoice is issued, not when it is drafted

## Comments
