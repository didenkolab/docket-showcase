---
key: LEDGER-64
title: A statement with the bank's own character set imports the names as question marks
type: bug
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-08-13T14:30:00Z
updated: 2026-08-13T14:30:00Z
aliases: []
tags: []
---

The third bank's CSV is not UTF-8 and does not say so, and the importer assumes it is. Every Norwegian and Swedish letter in a payer's name comes through as a question mark, which means the matcher cannot match on the name and Bergstrom cannot read the ones it failed on.

## Acceptance

- [ ] A statement file's encoding is detected rather than assumed
- [ ] A file whose encoding cannot be established is refused with the reason

## Comments
