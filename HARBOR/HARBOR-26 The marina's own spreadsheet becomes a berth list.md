---
type: test
automated: true
key: HARBOR-26
title: The marina's own spreadsheet becomes a berth list
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-07-10T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-6C1A63
generated: true
parent: "[[HARBOR-19 Berth booking]]"
included_in: ["[[HARBOR-19 Berth booking]]"]
tests: ["[[HARBOR-8 Import the marina's berth list from a spreadsheet]]", "[[HARBOR-30 Hold a berth for twenty minutes while the guest pays]]"]
run_by: ["[[HARBOR-54 The marina's own spreadsheet becomes a berth list]]", "[[HARBOR-73 The marina's own spreadsheet becomes a berth list]]"]
---

## Scenario

```gherkin
  When the marina's berth spreadsheet is imported
  Then the berths read are A1, A2 and B7
  And berth A1 has shore power
  And berth A2 has no shore power
```

From `Berth booking` in `booking.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-6C1A63` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-8 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-30 — the commit that wrote it
