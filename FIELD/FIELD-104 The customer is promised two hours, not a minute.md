---
type: test
automated: true
key: FIELD-104
title: The customer is promised two hours, not a minute
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-JOB-005
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-96 Promise the customer a two-hour arrival window and keep it]]"]
run_by: ["[[FIELD-114 The customer is promised two hours, not a minute]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address    |
  | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
  When the arrival window for J-1 is worked out
  Then the window runs from 13:00 to 15:00
```

From `A crew's day` in `jobs.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-96 — the commit that wrote it
