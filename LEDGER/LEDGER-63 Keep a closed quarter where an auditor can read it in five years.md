---
key: LEDGER-63
title: Keep a closed quarter where an auditor can read it in five years
type: task
status: Ready
status_category: todo
priority: normal
assignee: '[[ola]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-11T11:20:00Z
updated: 2026-09-01T11:35:00Z
aliases: []
tags: []
duplicates: ["[[LEDGER-85 Close a quarter so nothing can be booked into it afterwards]]"]
---

A closed quarter has to still be readable long after the software that produced it has been rewritten twice, which usually means a file somewhere rather than a row in a database that has since been migrated.

## Acceptance

- [ ] A closed quarter is written out in a form that outlives the schema
- [ ] The written form can be read back and checked against the live data

## Comments

**ola · 2026-09-01 11:30** — Folding this into closing the period rather than doing it beside it. Writing the quarter out is what closing a quarter should mean — a close that leaves no artefact behind is a flag on a row, and a flag on a row is exactly the thing an auditor in five years cannot read. Tomasz has put it in that story's acceptance and I would rather it lived there than here.
