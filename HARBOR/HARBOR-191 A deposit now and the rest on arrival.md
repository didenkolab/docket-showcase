---
type: test
automated: true
key: HARBOR-191
title: A deposit now and the rest on arrival
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-006
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-178 Take a deposit now and the rest on arrival]]", "[[HARBOR-142 Price a season booking by the month, not by the night]]"]
run_by: ["[[HARBOR-215 A deposit now and the rest on arrival]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  When 18000 cents is split into a 30 per cent deposit
  Then 5400 cents is taken now and 12600 cents on arrival
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-178 — the commit that wrote it
- HARBOR-142 — the commit that wrote it
