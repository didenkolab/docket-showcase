---
key: LEDGER-28
title: A refund is booked as a credit note against the invoice it came from
type: story
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]", "[[payments]]"]
created: 2026-07-14T10:00:00Z
updated: 2026-07-14T10:07:00Z
aliases: []
tags: []
definition_of_done: team
---

Money going back to a customer is not an invoice with a minus sign in front of it. It is its own document, with its own number, that points at the invoice it reverses and carries the same tax rates that invoice carried — because the quarter the refund lands in and the quarter the invoice landed in are usually not the same quarter, and the tax has to unwind where it was charged.

## Acceptance

- [ ] A credit note has its own number and names the invoice it reverses
- [ ] A partial refund credits part of an invoice and leaves the rest owing
- [ ] The credit note carries the tax rates of the invoice, not today's

## Comments
