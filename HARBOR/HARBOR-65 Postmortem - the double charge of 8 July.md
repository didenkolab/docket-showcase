---
type: postmortem
key: HARBOR-65
title: 'Postmortem: the double charge of 8 July'
status: Done
status_category: done
priority: normal
assignee: '[[tomasz]]'
created: 2026-07-10T10:20:00Z
updated: 2026-07-14T15:20:00Z
labels: ["[[payments]]"]
tags: []
aliases: []
explains: ["[[HARBOR-63 Guests at three marinas were charged twice for one booking]]"]
mitigated_by: ["[[HARBOR-64 A retried confirmation charges the card twice]]", "[[HARBOR-82 Reconcile the provider's webhook with the booking]]"]
---

## What happened

09:40 — the first duplicate charge, at Vik. The provider's confirmation call was taking between eight and twenty seconds all morning; the booking screen showed a spinner and no other feedback.

09:52 — Vik ring the office: a guest has two charges on one card for one berth.

10:04 — Sandholm ring with the same thing. By now there are nine duplicates across two marinas.

10:20 — confirmation is taken off the booking screen for every marina. Eleven duplicates in total; no further ones after this.

11:20 — the cause is understood and written up as a bug.

13:15 — all eleven duplicate charges refunded by hand from the provider's console. Each marina rings its own guests.

## Why it was possible

Confirming a booking sent a charge and had no way of saying that this charge was the same intention as the last one. The provider supports an idempotency key on exactly this call and we were not sending one, because the happy path does not need it and the happy path is what we tested.

The second half is that a slow confirmation looked, to a guest, exactly like one that had not been sent. A spinner with no words on it invites a second press, and we had built the button that way in the first sprint without anybody deciding to.

The third half — and this is the one that matters — is that nothing on our side compared what the provider thought had happened with what the booking thought had happened. Eleven charges existed for seven bookings for three and a half hours, and every one of the systems involved was content.

## What we are changing

The confirmation call carries an idempotency key derived from the booking and the attempt, so a retry is the same charge rather than a second one. That is the fix, and it is a card.

The provider's webhook is reconciled against the booking nightly and anything that disagrees is raised rather than logged, so a charge without a booking is found by us within a day. That is a card too, in Sprint 3.

Anything that spends money now has idempotence in its acceptance, in writing, rather than in whoever reviewed it.

## What we are not changing, and why

We are not building an automatic refund for a duplicate charge. Eleven refunds by hand took forty minutes; an automatic refunder that is wrong sends money to the wrong card, and the case is rare enough that a person should look at it.

We are not disabling the confirmation button while the call is in flight and calling that the fix. It is worth doing and it is on the payments story, but it makes the same mistake we made in June: a browser cannot be the thing that guarantees a charge happens once.

## Comments

**mateo · 2026-07-14 10:20** — Checked what this says it is changing against the board: the fix and the reconciliation are both cards with numbers on them, and the acceptance line about idempotence is on the two payment stories in Sprint 3. The provider-side idempotency key is the only one that is prose here and it is inside the fix, so I am happy. Passing it.
