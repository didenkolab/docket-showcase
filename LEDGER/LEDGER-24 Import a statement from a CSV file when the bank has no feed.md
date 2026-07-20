---
key: LEDGER-24
title: Import a statement from a CSV file when the bank has no feed
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[priya]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-07-13T09:45:00Z
updated: 2026-07-20T15:25:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 3]]"
estimate: 3
---

Three banks is not every bank, and the fourth one a business banks with will always be a small one that exports a CSV and nothing else. Dropping that file on a page has to produce the same statement the feeds produce, including the part where the columns are in an order nobody has seen before.

## Acceptance

- [x] A dropped CSV becomes the same statement shape the bank feeds produce
- [ ] The columns are mapped by the person importing, and the mapping is remembered
- [ ] A file that is not a statement is refused before anything is written

## Comments
