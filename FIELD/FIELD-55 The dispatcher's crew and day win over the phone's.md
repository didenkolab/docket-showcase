---
type: test
automated: true
key: FIELD-55
title: The dispatcher's crew and day win over the phone's
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-05T17:00:00Z
updated: 2026-08-05T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-SYN-004
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-50 Offline edits are lost when the server's version wins the merge]]"]
run_by: ["[[FIELD-67 The dispatcher's crew and day win over the phone's]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  Given the board has these jobs
  | id  | crew  | status  |
  | J-1 | south | planned |
  And the phone has these jobs
  | id  | crew  | status |
  | J-1 | north | done   |
  When the phone and the board are merged
  Then J-1 comes back as done
  And J-1 belongs to the south crew
```

From `Putting a phone back together with the board` in `sync.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-50 — the commit that wrote it
