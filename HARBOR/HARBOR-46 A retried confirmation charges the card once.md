---
type: test
automated: true
key: HARBOR-46
title: A retried confirmation charges the card once
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-09-04T15:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-005
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-39 Store the provider's payment reference on the booking]]", "[[HARBOR-178 Take a deposit now and the rest on arrival]]"]
run_by: ["[[HARBOR-61 A retried confirmation charges the card once]]", "[[HARBOR-80 A retried confirmation charges the card once]]", "[[HARBOR-102 A retried confirmation charges the card once]]", "[[HARBOR-118 A retried confirmation charges the card once]]", "[[HARBOR-141 A retried confirmation charges the card once]]", "[[HARBOR-176 A retried confirmation charges the card once]]", "[[HARBOR-214 A retried confirmation charges the card once]]", "[[HARBOR-239 A retried confirmation charges the card once]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  Given H-1001 is confirmed for 18000 cents with intent conf-1
  And H-1043 is confirmed for 9000 cents with intent conf-2
  When H-1001 is confirmed for 18000 cents with intent conf-1
  Then the card has been charged 18000 cents for H-1001
  And the ledger holds 2 charges
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-39 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-178 — the commit that wrote it
