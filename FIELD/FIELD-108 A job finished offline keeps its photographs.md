---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: [''P-1'', ''P-2'']'
key: FIELD-108
title: A job finished offline keeps its photographs
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T17:00:00Z
updated: 2026-08-28T17:20:00Z
labels: []
tags: []
aliases: []
parent: "[[FIELD-107 Cucumber on staging at 2f5065b]]"
automation_id: FIELD-GEN-04E49B
runs: ["[[FIELD-106 A job finished offline keeps its photographs]]"]
---

## What happened

**Failed** on staging at `2f5065b`.

```
ASSERT FAILED: ['P-1', 'P-2']
```

Case `FIELD-GEN-04E49B`, from the Cucumber report — nothing here was typed by hand.

## Comments

**mateo · 2026-08-28 17:20** — Off by one photo, see the story: the newest picture on the phone is held back on the theory that it may still be uploading, so a job with six comes back with five. No bug filed yet — it is a five-minute fix and a very bad demo.
