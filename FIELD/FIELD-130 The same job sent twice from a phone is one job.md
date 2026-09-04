---
type: test
automated: true
key: FIELD-130
title: The same job sent twice from a phone is one job
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:40:00Z
updated: 2026-09-04T15:40:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-SYN-005
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-102 A job sent twice from a phone appears twice on the board]]"]
run_by: ["[[FIELD-149 The same job sent twice from a phone is one job]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  When these sendings are put together
  | id   | client_id | status |
  | J-9  | c-77      | done   |
  | J-10 | c-77      | done   |
  | J-11 | c-78      | done   |
  Then what is left is J-9 and J-11
```

From `Putting a phone back together with the board` in `sync.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-102 — the commit that wrote it
