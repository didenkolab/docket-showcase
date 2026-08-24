---
key: LEDGER-85
title: Close a quarter so nothing can be booked into it afterwards
type: story
status: Ready
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-24T09:45:00Z
updated: 2026-08-24T11:35:00Z
aliases: []
tags: []
definition_of_done: release
sprint: "[[Sprint 6]]"
estimate: 8
---

Closing is the moment the numbers stop being an opinion. After it, an invoice dated inside the quarter has to be refused rather than accepted quietly, a correction has to become a document of its own in the open quarter, and the closing itself has to be undoable by somebody senior and impossible by accident.

## Acceptance

- [ ] A closed quarter refuses any new entry dated inside it, and says why
- [ ] A correction to a closed quarter becomes a document in the open one
- [ ] Reopening a quarter is recorded with who did it and why

## Comments
