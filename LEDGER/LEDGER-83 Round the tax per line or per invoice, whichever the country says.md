---
key: LEDGER-83
title: Round the tax per line or per invoice, whichever the country says
type: story
status: Ready
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-19T11:40:00Z
updated: 2026-08-28T16:30:00Z
aliases: []
tags: []
definition_of_done: team
logged: ["[[LEDGER-88 Which rounding the rules actually want]]", "[[LEDGER-89 Rounding written up for the tax stories]]"]
tested_by: ["[[LEDGER-93 The tax is rounded on every line]]", "[[LEDGER-94 The tax is rounded once, on the total]]"]
---

Norway rounds the tax on the invoice total and Sweden rounds it line by line, and on a seven-line invoice the two answers differ by a cent or two. It has to be a rule of the business's country rather than a habit of whichever function was written first, and it is the same argument as the PDF total bug.

## Acceptance

- [ ] The rounding rule is a property of the business's country, held in one place
- [ ] A business's invoices are consistent with each other whichever rule applies

## Comments
