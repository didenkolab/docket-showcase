---
type: test
automated: true
key: FIELD-128
title: A job moved to tomorrow leaves today's list
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:40:00Z
updated: 2026-09-04T15:40:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-GEN-631971
generated: true
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-101 A job moved to tomorrow stays on today's list until the app restarts]]"]
run_by: ["[[FIELD-135 A job moved to tomorrow leaves today's list]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address    |
  | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
  When J-1 is moved to 2026-07-17
  Then the north crew's day for 2026-07-16 holds nothing
  And the north crew's day for 2026-07-17 is J-1
```

From `A crew's day` in `jobs.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@FIELD-GEN-631971` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-101 — the commit that wrote it
