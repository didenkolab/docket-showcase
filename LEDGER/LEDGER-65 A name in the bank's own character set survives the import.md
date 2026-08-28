---
type: test
automated: true
key: LEDGER-65
title: A name in the bank's own character set survives the import
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-14T16:30:00Z
updated: 2026-08-28T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-128989
generated: true
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-64 A statement with the bank's own character set imports the names as question marks]]"]
run_by: ["[[LEDGER-73 A name in the bank's own character set survives the import]]", "[[LEDGER-104 A name in the bank's own character set survives the import]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  When the bank's bytes are decoded as latin-1
  Then the name reads Sørensen
```

From `Importing a bank statement` in `bankimport.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-128989` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-64 — the commit that wrote it
