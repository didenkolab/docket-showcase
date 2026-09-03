---
key: LEDGER-85
title: Close a quarter so nothing can be booked into it afterwards
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-24T09:45:00Z
updated: 2026-09-03T15:15:00Z
aliases: []
tags: []
definition_of_done: release
sprint: "[[Sprint 6]]"
estimate: 8
came_from: ["[[LEDGER-21 Can a quarter be locked so nothing new lands in it]]"]
tested_by: ["[[LEDGER-94 The tax is rounded once, on the total]]", "[[LEDGER-95 A closed quarter takes nothing more]]"]
duplicated_by: ["[[LEDGER-63 Keep a closed quarter where an auditor can read it in five years]]"]
---

Closing is the moment the numbers stop being an opinion. After it, an invoice dated inside the quarter has to be refused rather than accepted quietly, a correction has to become a document of its own in the open quarter, and the closing itself has to be undoable by somebody senior and impossible by accident.

## Acceptance

- [x] A closed quarter refuses any new entry dated inside it, and says why
- [ ] A correction to a closed quarter becomes a document in the open one
- [ ] Reopening a quarter is recorded with who did it and why

## Comments
