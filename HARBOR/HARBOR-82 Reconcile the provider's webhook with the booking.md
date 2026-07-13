---
key: HARBOR-82
title: Reconcile the provider's webhook with the booking
type: story
status: Backlog
status_category: todo
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-07-13T09:45:00Z
updated: 2026-07-13T09:49:00Z
aliases: []
tags: [area/api]
---

The provider tells us what happened twice: once as the answer to our request and once, minutes or hours later, as a webhook. When those two disagree the webhook is right, and today nothing is listening to it.

## Acceptance

- [ ] A webhook the provider sends twice is applied once
- [ ] A charge the webhook reports and the booking does not know about raises an alert
- [ ] A webhook for a booking that no longer exists is kept, not dropped

## Comments
