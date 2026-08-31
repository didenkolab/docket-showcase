---
key: LEDGER-84
title: Keep the tax rate that applied on the day, not the one that applies now
type: story
status: QA
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-24T09:40:00Z
updated: 2026-08-31T10:20:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 5
definition_of_done: team
blocks: ["[[LEDGER-86 The quarterly return an accountant can hand to the tax office]]"]
tested_by: ["[[LEDGER-95 A closed quarter takes nothing more]]", "[[LEDGER-96 The rate that applied on the day of the invoice]]"]
---

Rates change on a date somebody in a ministry chose, and every document already issued keeps the rate it was issued under for as long as it exists. A rate table with one current value in it is the bug that arrives eighteen months later, when a credit note against an old invoice quietly uses today's number.

## Acceptance

- [x] A rate is looked up by the date of the document, not by today
- [x] A rate change is entered once, with the date it takes effect
- [x] Reissuing a document from last year produces last year's tax

## Comments
