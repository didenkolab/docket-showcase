---
type: test
automated: true
key: LEDGER-41
title: A refund is a credit note against the invoice it undoes
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-08-14T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-INV-005
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-28 A refund is booked as a credit note against the invoice it came from]]", "[[LEDGER-31 Chase a late invoice twice and then stop chasing it]]"]
run_by: ["[[LEDGER-56 A refund is a credit note against the invoice it undoes]]", "[[LEDGER-82 A refund is a credit note against the invoice it undoes]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  Given an invoice 2026-0007 for Bergstrom Accounting
  | description | quantity | unit_cents | tax_percent |
  | Bookkeeping | 10       | 8000       | 25          |
  When 20000 cents are credited against it as 2026-C002
  Then the credit note is made out against 2026-0007
  And crediting 200000 cents is refused because more than the invoice it credits
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-28 — the commit that wrote it
- LEDGER-31 — the commit that wrote it
