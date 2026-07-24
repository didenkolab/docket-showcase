---
type: test
automated: true
key: LEDGER-42
title: A late invoice is chased twice and then left alone
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-07-24T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-502246
generated: true
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-31 Chase a late invoice twice and then stop chasing it]]"]
run_by: ["[[LEDGER-49 A late invoice is chased twice and then left alone]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  Given an invoice fell due on 2026-07-01
  When it is 2026-07-09 and nothing has been chased yet
  Then a reminder goes out
  When it is 2026-08-05 and 1 reminder has been sent
  Then a reminder goes out
  When it is 2026-09-01 and 2 reminders have been sent
  Then no reminder goes out because chased twice already
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-502246` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-31 — the commit that wrote it
