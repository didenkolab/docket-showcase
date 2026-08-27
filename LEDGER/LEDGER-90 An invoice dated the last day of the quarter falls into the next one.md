---
key: LEDGER-90
title: An invoice dated the last day of the quarter falls into the next one
type: bug
status: Ready
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[LEDGER-3 Tax periods]]"
labels: ["[[tax]]"]
created: 2026-08-27T11:10:00Z
updated: 2026-08-27T14:20:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 2
---

A quarter is held as a start and an end, and the end is compared with a less-than where it wants a less-than-or-equal. Every invoice issued on 31 March, 30 June, 30 September and 31 December is reported in the quarter after the one it belongs to, which is four days a year and, for a business that invoices monthly, four invoices in the wrong return.

## Acceptance

- [ ] An invoice dated the last day of a quarter is reported in that quarter
- [ ] The demo data's misfiled invoices move to the right quarter when reimported

## Comments

**mateo · 2026-08-27 11:20** — Found it while building the quarter-close scenarios rather than in the wild, which is luck. Invoice dated 30 June appears in the July-to-September return. The start of the quarter is inclusive and the end is not, so the two ends of every quarter disagree about which side the boundary is on.
