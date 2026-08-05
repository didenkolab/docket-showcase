---
type: test
automated: true
key: FIELD-36
title: Work done with the phone offline survives the sync
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-08-05T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-SYN-001
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-26 A crew phone holds a whole day's work with no signal]]"]
run_by: ["[[FIELD-45 Work done with the phone offline survives the sync]]", "[[FIELD-64 Work done with the phone offline survives the sync]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  Given the board has these jobs
  | id  | crew  | status  |
  | J-1 | north | planned |
  And the phone has these jobs
  | id  | crew  | status |
  | J-1 | north | done   |
  When the phone and the board are merged
  Then J-1 comes back as done
```

From `Putting a phone back together with the board` in `sync.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-26 — the commit that wrote it
