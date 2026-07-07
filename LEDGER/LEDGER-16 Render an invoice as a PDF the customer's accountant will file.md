---
key: LEDGER-16
title: Render an invoice as a PDF the customer's accountant will file
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-06-29T09:45:00Z
updated: 2026-07-07T16:35:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 2]]"
estimate: 5
---

What actually leaves the building is a PDF, and it is read by somebody who has never seen Ledgerline and never will. It has to carry the business's registered name and number, the customer's address as the customer writes it, the lines, the tax rows and the payment details, on one page whenever one page is possible.

## Acceptance

- [x] The PDF carries the registered details of both businesses and the invoice number
- [x] An invoice of twenty lines still prints as a document rather than a spill
- [x] The same invoice rendered twice produces the same bytes

## Comments
