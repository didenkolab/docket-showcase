---
type: test
automated: true
key: FIELD-106
title: A job finished offline keeps its photographs
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-GEN-04E49B
generated: true
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-92 Upload a job's photographs over a connection that keeps dropping]]"]
run_by: ["[[FIELD-108 A job finished offline keeps its photographs]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  Given the board has these jobs
  | id  | crew  | status  |
  | J-1 | north | planned |
  And the phone has these jobs
  | id  | crew  | status |
  | J-1 | north | done   |
  And the phone has photographs P-1, P-2 and P-3 for J-1
  When the phone and the board are merged
  Then J-1 comes back with photographs P-1, P-2 and P-3
```

From `Putting a phone back together with the board` in `sync.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@FIELD-GEN-04E49B` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-92 — the commit that wrote it
