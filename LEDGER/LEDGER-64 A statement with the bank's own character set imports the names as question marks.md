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
updated: 2026-08-13T14:51:00Z
aliases: []
tags: [customer/bergstrom]
sprint: "[[Sprint 5]]"
estimate: 3
---

The third bank's CSV is not UTF-8 and does not say so, and the importer assumes it is. Every Norwegian and Swedish letter in a payer's name comes through as a question mark, which means the matcher cannot match on the name and Bergstrom cannot read the ones it failed on.

## Acceptance

- [ ] A statement file's encoding is detected rather than assumed
- [ ] A file whose encoding cannot be established is refused with the reason

## Comments

**mateo · 2026-08-13 14:40** — Bergstrom sent us a real month from the third bank, with permission and with the amounts scrambled, and forty of its four hundred lines have a payer name full of question marks. It is the same failure as reading a marina's berth spreadsheet, so I have linked the two — whatever we do here should be the thing Harbor does as well.
