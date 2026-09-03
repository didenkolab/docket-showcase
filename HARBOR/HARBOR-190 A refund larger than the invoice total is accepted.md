---
key: HARBOR-190
title: A refund larger than the invoice total is accepted
type: bug
status: In progress
status_category: doing
priority: high
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-08-28T11:10:00Z
updated: 2026-09-03T16:15:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 3
tested_by: ["[[HARBOR-192 A stay of a month or more is priced by the month]]", "[[HARBOR-193 A refund larger than the invoice it credits is refused]]"]
found_in: ["[[HARBOR-213 A refund larger than the invoice it credits is refused]]"]
---

The refund endpoint checks that the booking was paid and not how much it was paid. A refund of four hundred against an invoice of ninety is accepted and sent to the provider, which happily sends the money.

## Acceptance

- [x] A refund larger than what is left on the invoice is refused
- [ ] Several partial refunds cannot add up to more than the invoice

## Comments

**mateo · 2026-08-28 11:20** — Found by the payments scenarios rather than by a marina, thankfully: HARBOR-PAY-004 refunds 400 against an invoice for 90 and passes. Nobody has done it in the wild because the number is typed by us and not by a guest, but it will be typed by a harbour master the moment refunds ship.
