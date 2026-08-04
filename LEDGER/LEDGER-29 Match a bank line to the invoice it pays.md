---
key: LEDGER-29
title: Match a bank line to the invoice it pays
type: story
status: In review
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]", "[[invoicing]]"]
created: 2026-07-16T09:40:00Z
updated: 2026-08-04T16:20:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 4]]"
tested_by: ["[[LEDGER-35 Money leaving the account is a negative line]]", "[[LEDGER-36 A bank line is matched to the invoice it pays]]", "[[LEDGER-37 A line nobody can match is left for a person]]"]
blocked_by: ["[[LEDGER-23 Fetch a statement from the three banks our first accountants use]]"]
---

This is the whole point of importing anything. A line of 4 218.60 arriving on the fourth with the invoice number in its reference is not a puzzle, and a person should never be shown it. What a person should be shown is the twenty per cent the machine could not be sure about, which is what the next story is for.

## Acceptance

- [x] A line whose reference names an invoice is matched to it without being asked
- [x] A line that matches an amount and a date but nothing else is offered, not decided
- [x] A match can be undone, and undoing it puts the invoice back to unpaid

## Comments
