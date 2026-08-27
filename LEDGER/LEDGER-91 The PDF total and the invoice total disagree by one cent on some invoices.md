---
key: LEDGER-91
title: The PDF total and the invoice total disagree by one cent on some invoices
type: bug
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]", "[[tax]]"]
created: 2026-08-27T11:20:00Z
updated: 2026-08-27T11:20:00Z
aliases: []
tags: []
---

The invoice screen adds each line's tax and rounds once; the PDF rounds each line's tax and then adds. On most invoices the two agree, and on an invoice with seven lines at a reduced rate they are a cent apart — which means the document we send and the document we keep say different things.

## Acceptance

- [ ] The screen, the PDF and the stored total are computed once and shared
- [ ] The invoices in the demo data that disagree are listed and corrected

## Comments
