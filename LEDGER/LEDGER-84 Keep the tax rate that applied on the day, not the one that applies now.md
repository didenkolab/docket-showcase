---
key: LEDGER-84
title: Keep the tax rate that applied on the day, not the one that applies now
type: story
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-24T09:40:00Z
updated: 2026-08-24T09:44:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 5
---

Rates change on a date somebody in a ministry chose, and every document already issued keeps the rate it was issued under for as long as it exists. A rate table with one current value in it is the bug that arrives eighteen months later, when a credit note against an old invoice quietly uses today's number.

## Acceptance

- [ ] A rate is looked up by the date of the document, not by today
- [ ] A rate change is entered once, with the date it takes effect
- [ ] Reissuing a document from last year produces last year's tax

## Comments
