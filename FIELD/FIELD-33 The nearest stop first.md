---
type: test
automated: true
key: FIELD-33
title: The nearest stop first
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-RTE-001
parent: "[[FIELD-10 Ordering a crew's day]]"
tests: ["[[FIELD-19 Order a crew's stops so the day is driveable]]", "[[FIELD-20 Put the road's travel time between two stops, not a straight line]]"]
run_by: ["[[FIELD-42 The nearest stop first]]", "[[FIELD-61 The nearest stop first]]", "[[FIELD-78 The nearest stop first]]", "[[FIELD-115 The nearest stop first]]"]
included_in: ["[[FIELD-10 Ordering a crew's day]]"]
---

## Scenario

```gherkin
  When the stops north, west and east are ordered from depot
  Then the order is north, west and east
```

From `Ordering a crew's day` in `routes.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-19 — the commit that wrote it
- FIELD-20 — the commit that wrote it
