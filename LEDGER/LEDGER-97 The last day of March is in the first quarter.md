---
type: test
automated: true
key: LEDGER-97
title: The last day of March is in the first quarter
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-1E865C
generated: true
parent: "[[LEDGER-12 Tax rates, quarters, and closing one]]"
tests: ["[[LEDGER-90 An invoice dated the last day of the quarter falls into the next one]]"]
run_by: ["[[LEDGER-105 The last day of March is in the first quarter]]", "[[LEDGER-129 The last day of March is in the first quarter]]"]
included_in: ["[[LEDGER-12 Tax rates, quarters, and closing one]]"]
---

## Scenario

```gherkin
  When the quarter of 2026-03-31 is worked out
  Then the quarter is 2026-Q1
```

From `Tax rates, quarters, and closing one` in `tax.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-1E865C` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-90 — the commit that wrote it
