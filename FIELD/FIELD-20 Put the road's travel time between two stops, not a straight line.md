---
key: FIELD-20
title: Put the road's travel time between two stops, not a straight line
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[FIELD-2 Route planning]]"
labels: ["[[routing]]"]
created: 2026-07-13T10:00:00Z
updated: 2026-07-21T16:05:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 3]]"
estimate: 5
blocks: ["[[FIELD-19 Order a crew's stops so the day is driveable]]"]
---

Two addresses eight kilometres apart are twelve minutes or fifty depending on which side of the water they are on, and a planner that measures in straight lines will confidently build a day nobody can drive. The times are asked for once per pair and kept, because the roads do not move.

## Acceptance

- [x] A pair of addresses gets a driving time that accounts for the water between them
- [ ] Times already asked for are reused rather than asked again
- [ ] A pair we cannot get a time for is planned pessimistically, not optimistically

## Comments
