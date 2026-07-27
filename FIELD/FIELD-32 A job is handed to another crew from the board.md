---
type: test
automated: true
key: FIELD-32
title: A job is handed to another crew from the board
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-07-27T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-JOB-003
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-13 Put a job on a crew from the dispatcher's board]]"]
run_by: ["[[FIELD-41 A job is handed to another crew from the board]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address    |
  | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
  When J-1 is handed to the south crew
  Then the job is taken
  And the south crew's day for 2026-07-16 is J-1
```

From `A crew's day` in `jobs.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-13 — the commit that wrote it
