---
key: LEDGER-31
title: Chase a late invoice twice and then stop chasing it
type: story
status: Ready
status_category: todo
priority: normal
assignee: '[[ingrid]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-07-20T11:20:00Z
updated: 2026-07-24T16:30:00Z
aliases: []
tags: []
definition_of_done: team
tested_by: ["[[LEDGER-41 A refund is a credit note against the invoice it undoes]]", "[[LEDGER-42 A late invoice is chased twice and then left alone]]"]
---

An invoice goes unpaid for a fortnight and nobody notices until the quarter is being closed. A reminder a week after the due date and a second one a fortnight after that is what a bookkeeper does by hand, badly, when they remember.

## Acceptance

- [ ] A late invoice produces a reminder the business can read before it goes
- [ ] Reminders stop when the invoice is paid, and stop after the second one either way

## Comments
