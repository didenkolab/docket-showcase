---
key: LEDGER-28
title: A refund is booked as a credit note against the invoice it came from
type: story
status: Ready
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]", "[[payments]]"]
created: 2026-07-14T10:00:00Z
updated: 2026-09-03T17:33:00Z
aliases: []
tags: []
definition_of_done: team
tested_by: ["[[LEDGER-40 Two invoices numbered from the same reading do not get the same number]]", "[[LEDGER-41 A refund is a credit note against the invoice it undoes]]"]
blocks: ["[[HARBOR-183 Refund a cancelled booking to the card it came from]]"]
logged: ["[[LEDGER-92 Reading what a credit note has to be]]", "[[LEDGER-119 Credit note against an invoice, on paper]]", "[[LEDGER-120 What a credit note looks like in the PDF]]", "[[LEDGER-121 Harbor's refund against a Ledgerline credit note]]"]
---

Money going back to a customer is not an invoice with a minus sign in front of it. It is its own document, with its own number, that points at the invoice it reverses and carries the same tax rates that invoice carried — because the quarter the refund lands in and the quarter the invoice landed in are usually not the same quarter, and the tax has to unwind where it was charged.

## Acceptance

- [ ] A credit note has its own number and names the invoice it reverses
- [ ] A partial refund credits part of an invoice and leaves the rest owing
- [ ] The credit note carries the tax rates of the invoice, not today's

## Comments

**ingrid · 2026-08-25 11:40** — Leaving this unsized on purpose until planning. Harbor's refunds story is now waiting on it, which means the two have to be estimated in the same room: the half of this that Harbor needs is a credit note produced by a refund, and the half Bergstrom asked for is a credit note somebody writes by hand against an invoice nobody is refunding. They may not be the same story.
