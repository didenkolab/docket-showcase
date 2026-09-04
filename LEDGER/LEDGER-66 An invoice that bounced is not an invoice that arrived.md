---
type: test
automated: true
key: LEDGER-66
title: An invoice that bounced is not an invoice that arrived
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-14T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-5C3E57
generated: true
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-59 Email an invoice and know whether it arrived]]"]
run_by: ["[[LEDGER-75 An invoice that bounced is not an invoice that arrived]]", "[[LEDGER-107 An invoice that bounced is not an invoice that arrived]]", "[[LEDGER-131 An invoice that bounced is not an invoice that arrived]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  Given these things happened to our messages
  | message_id | state     |
  | m-1        | delivered |
  | m-2        | bounced   |
  When we ask what became of m-2
  Then what became of it is bounced
  When we ask what became of m-3
  Then what became of it is unknown
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-5C3E57` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-59 — the commit that wrote it
