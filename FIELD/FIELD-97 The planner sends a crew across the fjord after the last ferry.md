---
key: FIELD-97
title: The planner sends a crew across the fjord after the last ferry
type: bug
status: Ready
status_category: todo
priority: high
assignee: '[[tomasz]]'
parent: "[[FIELD-2 Route planning]]"
labels: ["[[routing]]"]
created: 2026-08-26T14:10:00Z
updated: 2026-08-28T17:00:00Z
aliases: []
tags: []
sprint: "[[Sprint 6]]"
estimate: 5
tested_by: ["[[FIELD-35 The depot is both ends of the day]]", "[[FIELD-105 A stop the crew would reach after the last ferry is handed back]]"]
---

The coast-road zone is reached by a crossing that stops at six, and the travel times know how long it takes but not when it runs. A five o'clock job on the far side is planned happily and the crew spends the night on the wrong side of the water or drives two hours round.

## Acceptance

- [ ] A crossing has a timetable and the planner refuses to plan across it after the last one
- [ ] A day that has to cross late is flagged to the office rather than silently reordered

## Comments

**mateo · 2026-08-26 14:20** — The Kvaløya crew found this one for us, politely. Job at seventeen ten on the far side, last crossing at eighteen, and the planner had them leaving the previous job at seventeen forty. They drove round. It has been planning like this since the travel times went in, so it is not new — it is just that nobody had a late job over there until this week.
