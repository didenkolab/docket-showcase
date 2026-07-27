---
type: test
automated: true
key: FIELD-30
title: The day comes back in the order it is meant to happen
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-07-27T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-JOB-001
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-12 Show a crew the day's jobs in the order they are meant to happen]]", "[[FIELD-24 Two jobs can be booked into the same crew's two o'clock]]"]
run_by: ["[[FIELD-39 The day comes back in the order it is meant to happen]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address      |
  | J-3 | north | 2026-07-16 | 14:00 | 60      | Storgata 4   |
  | J-1 | north | 2026-07-16 | 08:30 | 90      | Havnegata 12 |
  | J-2 | north | 2026-07-16 | 11:00 | 45      | Fjellveien 7 |
  When the north crew's day for 2026-07-16 is read
  Then the day is J-1, J-2 and J-3
```

From `A crew's day` in `jobs.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-12 — the commit that wrote it
- FIELD-24 — the commit that wrote it
