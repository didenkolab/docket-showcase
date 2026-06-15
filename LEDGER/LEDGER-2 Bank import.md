---
key: LEDGER-2
title: Bank import
type: epic
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
labels: []
created: 2026-06-15T09:35:00Z
updated: 2026-06-15T09:35:00Z
aliases: []
tags: []
---

Half of bookkeeping is reading a bank statement and deciding what each line was. Bergstrom Accounting do it for ninety businesses by downloading a CSV a month and typing into a spreadsheet. This epic is the machine doing the typing: statements arrive on their own, the lines that obviously pay an invoice are matched, and a person only sees the ones that need a person.

## Acceptance

- [ ] A month of statements arrives without anybody downloading anything
- [ ] A line that pays an invoice is matched to it without being asked
- [ ] Importing the same statement twice changes nothing the second time

## Comments
