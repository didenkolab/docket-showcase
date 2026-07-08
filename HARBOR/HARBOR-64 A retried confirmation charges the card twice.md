---
key: HARBOR-64
title: A retried confirmation charges the card twice
type: bug
status: Backlog
status_category: todo
priority: critical
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-07-08T11:20:00Z
updated: 2026-07-08T11:27:00Z
aliases: []
tags: [area/api]
definition_of_done: hotfix
---

A guest whose confirmation is slow presses the button again, and the second press makes a second charge for the same booking. Three marinas have refunded a guest this week. The confirmation is not idempotent: nothing on our side says these two requests are the same intention.

## Acceptance

- [ ] Confirming the same booking twice charges the card once
- [ ] A duplicate confirmation returns the first charge rather than a new one
- [ ] The three known double charges are refunded and listed here

## Comments
