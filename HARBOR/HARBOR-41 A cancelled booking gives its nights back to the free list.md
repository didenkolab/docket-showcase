---
type: test
automated: true
key: HARBOR-41
title: A cancelled booking gives its nights back to the free list
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-08-05T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-GEN-8A6A81
generated: true
parent: "[[HARBOR-19 Berth booking]]"
tests: ["[[HARBOR-31 Cancel a booking and give the berth back]]", "[[HARBOR-38 Two guests can hold the same berth if they click at the same second]]"]
run_by: ["[[HARBOR-55 A cancelled booking gives its nights back to the free list]]", "[[HARBOR-74 A cancelled booking gives its nights back to the free list]]", "[[HARBOR-96 A cancelled booking gives its nights back to the free list]]", "[[HARBOR-112 A cancelled booking gives its nights back to the free list]]", "[[HARBOR-135 A cancelled booking gives its nights back to the free list]]"]
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When booking H-1001 is cancelled
  Then the free berths from 2026-07-02 to 2026-07-04 are A1, A2 and B7
```

From `Berth booking` in `booking.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@HARBOR-GEN-8A6A81` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-31 — the commit that wrote it
- HARBOR-38 — the commit that wrote it
