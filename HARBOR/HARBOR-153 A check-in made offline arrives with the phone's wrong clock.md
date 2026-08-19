---
key: HARBOR-153
title: A check-in made offline arrives with the phone's wrong clock
type: bug
status: In review
status_category: doing
priority: high
assignee: '[[aiko]]'
parent: "[[HARBOR-4 Mobile check-in]]"
labels: ["[[mobile]]"]
created: 2026-08-13T14:20:00Z
updated: 2026-08-19T15:20:00Z
aliases: []
tags: [regress]
sprint: "[[Sprint 5]]"
estimate: 2
tested_by: ["[[HARBOR-156 The code painted on the berth opens the right booking]]", "[[HARBOR-157 A phone with the wrong clock keeps the order it saw]]"]
---

A queued check-in carries the time the phone thought it was, and the older test phone is eleven minutes fast. The office sees arrivals in the wrong order and, twice, in the future.

## Acceptance

- [x] A check-in is stamped with a time the server can trust
- [x] The phone's own idea of the time is kept too, for when they disagree

## Comments

**mateo · 2026-08-13 14:30** — Two check-ins on the old phone arrived stamped eleven minutes ahead of the clock on the wall, which put them above the ones made after them. It is the device clock, not the queue order — the queue is fine.
