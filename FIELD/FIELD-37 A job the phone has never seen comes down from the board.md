---
type: test
automated: true
key: FIELD-37
title: A job the phone has never seen comes down from the board
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-SYN-002
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-26 A crew phone holds a whole day's work with no signal]]", "[[FIELD-48 Queue every edit the crew makes while the phone is dark]]"]
run_by: ["[[FIELD-46 A job the phone has never seen comes down from the board]]", "[[FIELD-65 A job the phone has never seen comes down from the board]]", "[[FIELD-82 A job the phone has never seen comes down from the board]]", "[[FIELD-120 A job the phone has never seen comes down from the board]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  Given the board has these jobs
  | id  | crew  | status  |
  | J-1 | north | planned |
  | J-2 | north | planned |
  And the phone has these jobs
  | id  | crew  | status |
  | J-1 | north | done   |
  When the phone and the board are merged
  Then the merged day is J-1 and J-2
```

From `Putting a phone back together with the board` in `sync.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-26 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-48 — the commit that wrote it
