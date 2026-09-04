---
type: test
automated: true
key: FIELD-71
title: The crew write the job up from the van
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-14T17:00:00Z
updated: 2026-09-04T15:40:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-JOB-004
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-18 A crew writes up the job from the van, before it drives off]]", "[[FIELD-96 Promise the customer a two-hour arrival window and keep it]]"]
run_by: ["[[FIELD-77 The crew write the job up from the van]]", "[[FIELD-113 The crew write the job up from the van]]", "[[FIELD-139 The crew write the job up from the van]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address    |
  | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
  When J-1 is written up as Replaced the pump and ran it for ten minutes
  Then the job is taken
  And J-1 is done and says Replaced the pump and ran it for ten minutes
```

From `A crew's day` in `jobs.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-18 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-96 — the commit that wrote it
