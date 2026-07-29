---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: {''id'': ''J-1'', ''crew'': ''north'', ''status'': ''planned''}'
key: FIELD-45
title: Work done with the phone offline survives the sync
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-07-29T14:30:00Z
labels: []
tags: []
aliases: []
parent: "[[FIELD-38 Cucumber on staging at c0d64b8]]"
automation_id: FIELD-SYN-001
runs: ["[[FIELD-36 Work done with the phone offline survives the sync]]"]
found: ["[[FIELD-50 Offline edits are lost when the server's version wins the merge]]"]
---

## What happened

**Failed** on staging at `c0d64b8`.

```
ASSERT FAILED: {'id': 'J-1', 'crew': 'north', 'status': 'planned'}
```

Case `FIELD-SYN-001`, from the Cucumber report — nothing here was typed by hand.

## Comments

**mateo · 2026-07-29 14:30** — This is the run from the Monday afternoon, before we knew what it was. It is the same failure as the bug I have just written down.
