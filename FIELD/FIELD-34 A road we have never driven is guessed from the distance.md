---
type: test
automated: true
key: FIELD-34
title: A road we have never driven is guessed from the distance
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-07-27T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-RTE-002
parent: "[[FIELD-10 Ordering a crew's day]]"
tests: ["[[FIELD-20 Put the road's travel time between two stops, not a straight line]]", "[[FIELD-22 Treat the depot and the last stop as fixed ends of the day]]"]
run_by: ["[[FIELD-43 A road we have never driven is guessed from the distance]]"]
included_in: ["[[FIELD-10 Ordering a crew's day]]"]
---

## Scenario

```gherkin
  Given where the stops are
  | stop  | x  | y  |
  | depot | 0  | 0  |
  | north | 0  | 20 |
  | west  | 30 | 0  |
  | east  | 40 | 40 |
  | isle  | 0  | 60 |
  When the leg from north to isle is worked out
  Then the leg is 52 minutes
```

From `Ordering a crew's day` in `routes.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-20 — the commit that wrote it
- FIELD-22 — the commit that wrote it
