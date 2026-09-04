---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: {''ok'': True, ''charge'': Charge(reference=''rf-1'', booking_ref=''H-1001'', amount_cents=-25000, intent=''''), ''ledger'': [Charge(reference=''ch-1'', booking_ref=''H-1001'', amou'
key: HARBOR-238
title: A refund larger than the invoice it credits is refused
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-09-04T15:00:00Z
updated: 2026-09-04T15:10:00Z
labels: []
tags: []
aliases: []
parent: "[[HARBOR-218 Cucumber on production at a000419]]"
automation_id: HARBOR-PAY-004
runs: ["[[HARBOR-193 A refund larger than the invoice it credits is refused]]"]
found: ["[[HARBOR-190 A refund larger than the invoice total is accepted]]"]
---

## What happened

**Failed** on production at `a000419`.

```
ASSERT FAILED: {'ok': True, 'charge': Charge(reference='rf-1', booking_ref='H-1001', amount_cents=-25000, intent=''), 'ledger': [Charge(reference='ch-1', booking_ref='H-1001', amount_cents=18000, intent='conf-1'), Charge(reference='rf-1', booking_ref='H-1001', amount_cents=-25000, intent='')]}
```

Case `HARBOR-PAY-004`, from the Cucumber report — nothing here was typed by hand.

## Comments

**mateo · 2026-09-04 15:10** — Still red on the release candidate. The fix is in review, not in the build.
