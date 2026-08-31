---
type: key_result
target: 90
current: 78
measure: Share of imported statement lines the matcher settled on its own over the last thirty days
quarter: 2026-Q3
key: LEDGER-7
title: Nine in ten bank lines are matched without a person
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
created: 2026-06-16T09:38:00Z
updated: 2026-08-31T11:12:00Z
labels: []
tags: []
aliases: []
parent: "[[LEDGER-5 Ledgerline closes a quarter without a spreadsheet]]"
advanced_by: ["[[LEDGER-2 Bank import]]"]
---

Matching by hand is the work the spreadsheet was doing. Every line the importer settles is a line nobody reads, and the ones it cannot settle are the ones worth a person's attention.

## Where the number comes from

The import log over the previous thirty days, counting lines rather than statements. A line a person confirmed without changing counts as settled; a line a person corrected does not.
