---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: {''ok'': True, ''charge'': Charge(reference=''rf-1'', booking_ref=''H-1001'', amount_cents=-25000, intent=''''), ''ledger'': [Charge(reference=''ch-1'', booking_ref=''H-1001'', amou'
key: HARBOR-213
title: A refund larger than the invoice it credits is refused
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
parent: "[[HARBOR-194 Cucumber on staging at 2f5065b]]"
automation_id: HARBOR-PAY-004
runs: ["[[HARBOR-193 A refund larger than the invoice it credits is refused]]"]
---

## What happened

**Failed** on staging at `2f5065b`.

```
ASSERT FAILED: {'ok': True, 'charge': Charge(reference='rf-1', booking_ref='H-1001', amount_cents=-25000, intent=''), 'ledger': [Charge(reference='ch-1', booking_ref='H-1001', amount_cents=18000, intent='conf-1'), Charge(reference='rf-1', booking_ref='H-1001', amount_cents=-25000, intent='')]}
```

Case `HARBOR-PAY-004`, from the Cucumber report — nothing here was typed by hand.
