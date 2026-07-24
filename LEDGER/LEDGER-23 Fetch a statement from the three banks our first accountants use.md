---
key: LEDGER-23
title: Fetch a statement from the three banks our first accountants use
type: story
status: Done
status_category: done
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-07-13T09:40:00Z
updated: 2026-07-24T16:30:00Z
aliases: []
tags: [area/api]
definition_of_done: team
sprint: "[[Sprint 3]]"
tested_by: ["[[LEDGER-32 A statement is imported into the ledger]]"]
---

Three banks cover every business Bergstrom keep the books for, and each of the three has its own idea of what a statement is: one paginates by day, one by transaction, and one will only tell you about the last ninety days and then silently gives you eighty-nine. One door into all three, and the rest of Ledgerline never learns which bank a line came from.

## Acceptance

- [x] A statement can be fetched from each of the three banks for a chosen month
- [x] The three banks' answers become one shape before anything else sees them
- [x] A bank that stops answering is reported rather than treated as an empty month

## Comments
