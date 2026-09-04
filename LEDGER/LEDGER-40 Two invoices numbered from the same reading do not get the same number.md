---
type: test
automated: true
key: LEDGER-40
title: Two invoices numbered from the same reading do not get the same number
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-BE1942
generated: true
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-22 Two invoices issued in the same minute get the same number]]", "[[LEDGER-28 A refund is booked as a credit note against the invoice it came from]]"]
run_by: ["[[LEDGER-50 Two invoices numbered from the same reading do not get the same number]]", "[[LEDGER-76 Two invoices numbered from the same reading do not get the same number]]", "[[LEDGER-108 Two invoices numbered from the same reading do not get the same number]]", "[[LEDGER-132 Two invoices numbered from the same reading do not get the same number]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  Given 1 invoice is numbered for 2026
  When two invoices are numbered from one reading of the sequence for 2026
  Then the second one is refused because the sequence has moved on
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-BE1942` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-22 — the commit that wrote it
- LEDGER-28 — the commit that wrote it
