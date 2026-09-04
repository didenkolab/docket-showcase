---
type: test
automated: true
key: FIELD-129
title: When a job overruns, the rest of the day moves
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:40:00Z
updated: 2026-09-04T15:40:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-GEN-173372
generated: true
parent: "[[FIELD-10 Ordering a crew's day]]"
tests: ["[[FIELD-89 When a job overruns, move the rest of the day rather than break it]]"]
run_by: ["[[FIELD-133 When a job overruns, the rest of the day moves]]"]
included_in: ["[[FIELD-10 Ordering a crew's day]]"]
---

## Scenario

```gherkin
  Given the crew get there at
  | stop | at    |
  | west | 10:00 |
  | east | 11:30 |
  | isle | 13:00 |
  When west overruns by 45 minutes
  Then the crew now get there at 10:00, 12:15 and 13:45
```

From `Ordering a crew's day` in `routes.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@FIELD-GEN-173372` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-89 — the commit that wrote it
