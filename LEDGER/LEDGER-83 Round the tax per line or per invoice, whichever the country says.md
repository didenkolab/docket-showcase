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
updated: 2026-08-24T17:13:00Z
aliases: []
tags: []
definition_of_done: team
logged: ["[[LEDGER-88 Which rounding the rules actually want]]"]
---

Norway rounds the tax on the invoice total and Sweden rounds it line by line, and on a seven-line invoice the two answers differ by a cent or two. It has to be a rule of the business's country rather than a habit of whichever function was written first, and it is the same argument as the PDF total bug.

## Acceptance

- [ ] The rounding rule is a property of the business's country, held in one place
- [ ] A business's invoices are consistent with each other whichever rule applies

## Comments
