---
key: HARBOR-33
title: Take the card payment when a booking is confirmed
type: story
status: QA
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-06-29T10:00:00Z
updated: 2026-07-13T10:10:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 2]]"
tested_by: ["[[HARBOR-28 The rate on the day of the booking, not today's]]", "[[HARBOR-44 The card is charged when the booking is confirmed]]"]
---

The sprint goal in one story: a guest confirms a booking, a card is charged, and the booking is only confirmed if the charge was. Everything awkward about payments — the redirect, the retry, the reference the accountant needs — is a child of this one.

## Acceptance

- [x] Confirming a booking charges the card once and only on success
- [x] A failed charge leaves the berth free and tells the guest why
- [x] The provider's payment reference is on the booking afterwards

## Comments

**mateo · 2026-07-09 09:30** — Failing it in QA. Card declined on a real sandbox card leaves the booking in 'confirmed' with no payment on it — the failure path rolls back the charge and not the booking, so the berth is held for a guest who never paid. The happy path is fine and the redirect works on a phone.
