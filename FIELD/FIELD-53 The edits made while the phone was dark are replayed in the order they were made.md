---
type: test
automated: true
key: FIELD-53
title: The edits made while the phone was dark are replayed in the order they were made
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-05T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-GEN-2F9367
generated: true
parent: "[[FIELD-11 Putting a phone back together with the board]]"
tests: ["[[FIELD-48 Queue every edit the crew makes while the phone is dark]]", "[[FIELD-50 Offline edits are lost when the server's version wins the merge]]"]
run_by: ["[[FIELD-57 The edits made while the phone was dark are replayed in the order they were made]]", "[[FIELD-73 The edits made while the phone was dark are replayed in the order they were made]]", "[[FIELD-109 The edits made while the phone was dark are replayed in the order they were made]]"]
included_in: ["[[FIELD-11 Putting a phone back together with the board]]"]
---

## Scenario

```gherkin
  Given the board has these jobs
  | id  | crew  | status  |
  | J-1 | north | planned |
  And the phone queued these edits
  | id  | field  | value      |
  | J-1 | status | on the way |
  | J-1 | status | done       |
  When the queued edits are replayed onto the board
  Then J-1 comes back as done
```

From `Putting a phone back together with the board` in `sync.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@FIELD-GEN-2F9367` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-48 — the commit that wrote it
- FIELD-50 — the commit that wrote it
