---
type: test
automated: true
key: HARBOR-192
title: A stay of a month or more is priced by the month
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-B9965B
generated: true
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-142 Price a season booking by the month, not by the night]]", "[[HARBOR-190 A refund larger than the invoice total is accepted]]"]
run_by: ["[[HARBOR-208 A stay of a month or more is priced by the month]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  Given the marina charges 90000 cents a month from 2026-01-01
  And Kittiwake has berth A1 from 2026-06-01 to 2026-07-01 as H-2001
  When the invoice for H-2001 is made out as 2026-0044
  Then the invoice totals 90000 cents
```

From `What a stay costs and who pays for it` in `payments.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-B9965B` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-142 — the commit that wrote it
- HARBOR-190 — the commit that wrote it
