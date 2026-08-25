---
key: FIELD-91
title: The sync holds when a whole depot comes back into signal at once
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[FIELD-3 Offline mobile]]"
labels: ["[[offline-sync]]"]
created: 2026-08-24T10:05:00Z
updated: 2026-08-25T14:21:00Z
aliases: []
tags: [area/api]
definition_of_done: team
sprint: "[[Sprint 6]]"
estimate: 8
mitigates: ["[[FIELD-52 Postmortem - the afternoon eleven crews lost]]", "[[FIELD-7 A crew loses a day's work again and Nordic Field stop using the phone]]"]
---

Half of the sprint goal. The merge rule from the incident is right and slow: it reads every change a phone made before it decides anything, and four crews driving into the depot yard at the same time is forty days of changes arriving in one minute. It has to hold up under that with the phones on the yard's own weak signal, which is the shape the next customer will have four times over.

## Acceptance

- [ ] Four crews' full days sync together without a phone timing out
- [ ] A phone that loses the signal mid-sync resumes rather than starting again
- [ ] The reconciliation is measured, so we find out from a graph rather than a crew

## Comments
