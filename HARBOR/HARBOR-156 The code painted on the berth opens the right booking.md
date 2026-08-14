---
type: test
automated: true
key: HARBOR-156
title: The code painted on the berth opens the right booking
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-14T16:00:00Z
updated: 2026-08-14T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-CHK-003
parent: "[[HARBOR-21 Checking a guest in from the pontoon]]"
tests: ["[[HARBOR-143 Scan the berth's QR code to open the right booking]]", "[[HARBOR-153 A check-in made offline arrives with the phone's wrong clock]]"]
run_by: ["[[HARBOR-167 The code painted on the berth opens the right booking]]"]
included_in: ["[[HARBOR-21 Checking a guest in from the pontoon]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  And berth A1 is painted with code NL-A1
  When the crew scan NL-A1 on 2026-07-02
  Then the scan opens booking H-1001
```

From `Checking a guest in from the pontoon` in `checkin.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-143 — the commit that wrote it
- HARBOR-153 — the commit that wrote it
