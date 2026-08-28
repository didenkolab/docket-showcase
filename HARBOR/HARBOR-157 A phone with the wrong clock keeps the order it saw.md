---
type: test
automated: true
key: HARBOR-157
title: A phone with the wrong clock keeps the order it saw
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-14T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-CHK-004
parent: "[[HARBOR-21 Checking a guest in from the pontoon]]"
tests: ["[[HARBOR-153 A check-in made offline arrives with the phone's wrong clock]]"]
run_by: ["[[HARBOR-168 A phone with the wrong clock keeps the order it saw]]", "[[HARBOR-204 A phone with the wrong clock keeps the order it saw]]"]
included_in: ["[[HARBOR-21 Checking a guest in from the pontoon]]"]
---

## Scenario

```gherkin
  Given the phone has no signal
  When ola checks H-1001 in at 09:40
  And ola checks H-1002 in at 10:10
  And the phone's clock is put right by 95 minutes
  And the phone finds a signal
  Then the check-ins are stamped 11:15 and 11:45
```

From `Checking a guest in from the pontoon` in `checkin.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-153 — the commit that wrote it
