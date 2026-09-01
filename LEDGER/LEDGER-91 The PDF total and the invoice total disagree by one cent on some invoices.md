---
key: LEDGER-91
title: The PDF total and the invoice total disagree by one cent on some invoices
type: bug
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]", "[[tax]]"]
created: 2026-08-27T11:20:00Z
updated: 2026-09-01T10:30:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 2
relates: ["[[LEDGER-83 Round the tax per line or per invoice, whichever the country says]]"]
---

The invoice screen adds each line's tax and rounds once; the PDF rounds each line's tax and then adds. On most invoices the two agree, and on an invoice with seven lines at a reduced rate they are a cent apart — which means the document we send and the document we keep say different things.

## Acceptance

- [ ] The screen, the PDF and the stored total are computed once and shared
- [ ] The invoices in the demo data that disagree are listed and corrected

## Comments

**mateo · 2026-08-27 11:30** — A florist in Aalesund noticed before we did, which is the embarrassing part. Seven lines, two rates, screen says 4 218.60 and the PDF says 4 218.59. It is not the rounding rule that is wrong, it is that we have two of them.
