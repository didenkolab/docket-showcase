---
key: LEDGER-4
title: Number invoices in one unbroken sequence per business year
type: story
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-06-15T09:55:00Z
updated: 2026-06-15T09:55:00Z
aliases: []
tags: []
---

An invoice number is the only thing about an invoice that the tax office cares about before it cares about anything else: the sequence has to start at one each business year, have no gaps in it, and never give the same number to two documents. A gap has to be explainable and a duplicate is not explainable at all, which is why this is the first thing Ledgerline does rather than the last.

## Acceptance

- [ ] Each business gets its own sequence, starting again at the turn of its year
- [ ] Two invoices issued at the same moment get two different numbers
- [ ] A number is allocated when the invoice is issued, not when it is drafted

## Comments
