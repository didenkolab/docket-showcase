---
key: FIELD-94
title: The arrival time texted to the customer is the one from before the replan
type: bug
status: In progress
status_category: doing
priority: high
assignee: '[[priya]]'
parent: "[[FIELD-2 Route planning]]"
labels: ["[[routing]]"]
created: 2026-08-24T14:20:00Z
updated: 2026-08-26T16:10:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 3
---

The message to the customer is composed from the day as it was planned in the morning, and the day is replanned every time a job overruns. The customer is told half past one, the crew arrives at four, and the firm is the one that looks disorganised for a number nobody at Nordic Field ever typed.

## Acceptance

- [x] The message is composed when it is sent, from the day as it stands then
- [ ] A replan that moves a stop more than an hour offers to tell the customer
- [ ] The office can see what was sent and when

## Comments

**mateo · 2026-08-24 14:30** — Found it against the replanning branch, so it is not in front of a customer yet. The estimate is read once when the day is planned and carried in the message queue for hours.
