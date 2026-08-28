---
type: test
automated: true
key: FIELD-31
title: A crew cannot be in two places at two o'clock
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-JOB-002
parent: "[[FIELD-9 A crew's day]]"
tests: ["[[FIELD-24 Two jobs can be booked into the same crew's two o'clock]]", "[[FIELD-13 Put a job on a crew from the dispatcher's board]]"]
run_by: ["[[FIELD-40 A crew cannot be in two places at two o'clock]]", "[[FIELD-59 A crew cannot be in two places at two o'clock]]", "[[FIELD-75 A crew cannot be in two places at two o'clock]]", "[[FIELD-111 A crew cannot be in two places at two o'clock]]"]
included_in: ["[[FIELD-9 A crew's day]]"]
---

## Scenario

```gherkin
  Given these jobs are on the board
  | id  | crew  | day        | start | minutes | address    |
  | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
  When J-2 is put on the north crew for 2026-07-16 at 14:30 for 30 minutes
  Then the job is refused because the crew is already out
  And the job in the way is J-1
```

From `A crew's day` in `jobs.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-24 — the commit that wrote it
- FIELD-13 — the commit that wrote it
