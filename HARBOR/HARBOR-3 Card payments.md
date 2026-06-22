---
key: HARBOR-3
title: Card payments
type: epic
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
labels: []
created: 2026-06-15T09:32:00Z
updated: 2026-06-22T10:55:00Z
aliases: []
tags: []
threatened_by: ["[[HARBOR-14 The payment provider suspends a marina's account mid-season]]", "[[HARBOR-16 The sandbox keys that were in the repository are still in somebody's clone]]"]
---

Marinas take a card at the moment of booking and hand back money when the weather cancels a weekend. Everything under this epic is that one flow and its unhappy halves: a charge that went through and a booking that did not, a refund the accountant has to be able to explain, a provider webhook arriving twice.

## Acceptance

- [ ] A confirmed booking is paid for by card, once
- [ ] A cancelled booking's money goes back to the card it came from
- [ ] Every charge can be matched to the booking it belongs to

## Comments
