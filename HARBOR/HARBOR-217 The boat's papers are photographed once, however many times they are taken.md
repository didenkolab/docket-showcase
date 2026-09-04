---
type: test
automated: true
key: HARBOR-217
title: The boat's papers are photographed once, however many times they are taken
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:00:00Z
updated: 2026-09-04T15:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-F7B44E
generated: true
parent: "[[HARBOR-21 Checking a guest in from the pontoon]]"
tests: ["[[HARBOR-144 Photograph the boat's papers at check-in]]"]
run_by: ["[[HARBOR-234 The boat's papers are photographed once, however many times they are taken]]"]
included_in: ["[[HARBOR-21 Checking a guest in from the pontoon]]"]
---

## Scenario

```gherkin
  Given the phone has no signal
  When ola checks H-1001 in at 09:40
  And the papers reg-page, reg-page and insurance are photographed for H-1001
  Then the check-in carries the papers reg-page and insurance
```

From `Checking a guest in from the pontoon` in `checkin.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-F7B44E` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-144 — the commit that wrote it
