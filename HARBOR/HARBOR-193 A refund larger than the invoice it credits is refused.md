---
type: test
automated: true
key: HARBOR-193
title: A refund larger than the invoice it credits is refused
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:00:00Z
updated: 2026-09-04T15:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-004
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-190 A refund larger than the invoice total is accepted]]"]
run_by: ["[[HARBOR-213 A refund larger than the invoice it credits is refused]]", "[[HARBOR-238 A refund larger than the invoice it credits is refused]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  Given H-1001 is confirmed for 18000 cents with intent conf-1
  When 25000 cents are refunded to H-1001
  Then the refund is refused because more than was charged
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-190 — the commit that wrote it
