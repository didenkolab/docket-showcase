---
type: test
automated: true
key: HARBOR-45
title: The guest comes back from the bank's page to their own booking
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-09-04T15:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-8DD76D
generated: true
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-35 Carry the 3-D Secure redirect back to the booking]]", "[[HARBOR-39 Store the provider's payment reference on the booking]]"]
run_by: ["[[HARBOR-56 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-75 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-97 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-113 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-136 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-171 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-207 The guest comes back from the bank's page to their own booking]]", "[[HARBOR-231 The guest comes back from the bank's page to their own booking]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  Given H-1001 sends the guest away to pay with token tok-9
  And H-1002 sends the guest away to pay with token tok-4
  When the guest comes back with token tok-9
  Then they are put back on booking H-1001
```

From `What a stay costs and who pays for it` in `payments.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-8DD76D` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-35 — the commit that wrote it
- HARBOR-39 — the commit that wrote it
