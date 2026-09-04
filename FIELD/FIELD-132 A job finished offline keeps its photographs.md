---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: [''P-1'', ''P-2'']'
key: FIELD-132
title: A job finished offline keeps its photographs
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:40:00Z
updated: 2026-09-04T15:50:00Z
labels: []
tags: []
aliases: []
parent: "[[FIELD-131 Cucumber on production at a000419]]"
automation_id: FIELD-GEN-04E49B
runs: ["[[FIELD-106 A job finished offline keeps its photographs]]"]
---

## What happened

**Failed** on production at `a000419`.

```
ASSERT FAILED: ['P-1', 'P-2']
```

Case `FIELD-GEN-04E49B`, from the Cucumber report — nothing here was typed by hand.

## Comments

**mateo · 2026-09-04 15:50** — Off by one photo again, on the release candidate. Nobody has picked it up because it is not written down; that is the lesson rather than the bug.
