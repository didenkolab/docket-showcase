---
type: test
automated: true
key: HARBOR-42
title: Two guests clicking at the same moment do not both get the berth
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-08-05T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-E016AC
generated: true
parent: "[[HARBOR-19 Berth booking]]"
tests: ["[[HARBOR-38 Two guests can hold the same berth if they click at the same second]]", "[[HARBOR-6 Show which berths are free for a chosen week]]"]
run_by: ["[[HARBOR-57 Two guests clicking at the same moment do not both get the berth]]", "[[HARBOR-76 Two guests clicking at the same moment do not both get the berth]]", "[[HARBOR-98 Two guests clicking at the same moment do not both get the berth]]", "[[HARBOR-114 Two guests clicking at the same moment do not both get the berth]]", "[[HARBOR-137 Two guests clicking at the same moment do not both get the berth]]"]
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  Given Puffin holds berth A2 from 2026-07-01 to 2026-07-03 as H-1003 at 10:00
  When Guillemot holds berth A2 from 2026-07-02 to 2026-07-04 as H-1004 at 10:01
  Then the hold is refused because berth held
```

From `Berth booking` in `booking.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-E016AC` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-38 — the commit that wrote it
- HARBOR-6 — the commit that wrote it
