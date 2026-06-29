---
key: HARBOR-33
title: Take the card payment when a booking is confirmed
type: story
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-06-29T10:00:00Z
updated: 2026-06-29T10:20:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 2]]"
---

The sprint goal in one story: a guest confirms a booking, a card is charged, and the booking is only confirmed if the charge was. Everything awkward about payments — the redirect, the retry, the reference the accountant needs — is a child of this one.

## Acceptance

- [ ] Confirming a booking charges the card once and only on success
- [ ] A failed charge leaves the berth free and tells the guest why
- [ ] The provider's payment reference is on the booking afterwards

## Comments
