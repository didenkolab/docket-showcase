---
key: LEDGER-61
title: Match by hand the lines the importer would not guess
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[priya]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-08-10T09:55:00Z
updated: 2026-08-18T16:10:00Z
aliases: []
tags: [needs-design]
definition_of_done: team
sprint: "[[Sprint 5]]"
estimate: 5
tested_by: ["[[LEDGER-37 A line nobody can match is left for a person]]"]
---

One payment covering three invoices, a payment short by the bank's own fee, a customer who pays two months at once in a round number. This is the screen Bergstrom will live in for two days at the end of every month, so it has to be fast under the hands rather than pretty in a screenshot.

## Acceptance

- [x] A line can be split across several invoices, and the split has to add up
- [x] An unmatched line can be booked as something other than a payment
- [ ] The screen can be worked through with the keyboard alone

## Comments
