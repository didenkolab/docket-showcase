---
key: HARBOR-64
title: A retried confirmation charges the card twice
type: bug
status: Done
status_category: done
priority: critical
assignee: '[[tomasz]]'
parent: "[[HARBOR-3 Card payments]]"
labels: ["[[payments]]"]
created: 2026-07-08T11:20:00Z
updated: 2026-07-13T09:48:00Z
aliases: []
tags: [area/api]
definition_of_done: hotfix
found_in: ["[[HARBOR-61 A retried confirmation charges the card once]]"]
causes: ["[[HARBOR-63 Guests at three marinas were charged twice for one booking]]"]
sprint: "[[Sprint 3]]"
---

A guest whose confirmation is slow presses the button again, and the second press makes a second charge for the same booking. Three marinas have refunded a guest this week. The confirmation is not idempotent: nothing on our side says these two requests are the same intention.

## Acceptance

- [x] Confirming the same booking twice charges the card once
- [x] A duplicate confirmation returns the first charge rather than a new one
- [x] The three known double charges are refunded and listed here

## Comments

**mateo · 2026-07-08 11:30** — Three reports this morning, all within twenty minutes of each other: Vik, Sandholm and the small marina at Bergen. Same shape each time — slow confirmation, guest presses again, two charges and one booking. I can reproduce it by throttling the connection to 3G.

**tomasz · 2026-07-09 15:10** — Fixed by giving the confirmation an idempotency key derived from the booking and the guest's attempt, which the provider then honours on its side too. The three charges are refunded; references are on the incident.
