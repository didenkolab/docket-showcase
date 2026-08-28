---
key: HARBOR-190
title: A refund larger than the invoice total is accepted
type: bug
status: Backlog
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-08-28T11:10:00Z
updated: 2026-08-28T11:10:00Z
aliases: []
tags: []
---

The refund endpoint checks that the booking was paid and not how much it was paid. A refund of four hundred against an invoice of ninety is accepted and sent to the provider, which happily sends the money.

## Acceptance

- [ ] A refund larger than what is left on the invoice is refused
- [ ] Several partial refunds cannot add up to more than the invoice

## Comments
