---
key: LEDGER-31
title: Chase a late invoice twice and then stop chasing it
type: story
status: Cancelled
status_category: done
priority: normal
assignee: '[[ingrid]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-07-20T11:20:00Z
updated: 2026-08-18T11:30:00Z
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

**ingrid · 2026-08-18 11:20** — Cancelling this rather than carrying it a fourth sprint. Two of the three accountants we sat with chase late payers by ringing them, and the third does it from her own mail client with a template she likes better than anything we would write. Nobody asked for this; we wrote it down because it sounded like something an invoicing product has. The half worth building is knowing which invoices are late, and that is already on the invoice list.
