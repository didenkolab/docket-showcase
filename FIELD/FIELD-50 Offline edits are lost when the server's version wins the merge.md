---
key: FIELD-50
title: Offline edits are lost when the server's version wins the merge
type: bug
status: Backlog
status_category: todo
priority: critical
assignee: '[[tomasz]]'
parent: "[[FIELD-3 Offline mobile]]"
labels: ["[[offline-sync]]"]
created: 2026-07-29T14:10:00Z
updated: 2026-07-29T14:20:00Z
aliases: []
tags: [regress]
definition_of_done: hotfix
---

When a job comes back from a phone and the server's copy has also changed, the merge keeps the server's fields and drops the phone's. A day in a dead zone is exactly the case where the phone is right and the server is a stale copy from seven in the morning, so the rule throws away the only version of the work that anybody actually did.

## Acceptance

- [ ] A field the phone changed while offline is never overwritten by an older server value
- [ ] Anything the server cannot reconcile is kept somewhere a person can read it
- [ ] The eleven crews' lost notes are recovered from the request logs where they exist
- [ ] The merge rule is written down as a decision rather than living in the code

## Comments

**mateo · 2026-07-29 14:20** — Eleven crews, one afternoon. The Storelva crew rang the office to ask why their morning was empty and it went from there. Every job they finished in the eastern valley is back to the state it was in when they left the depot: no notes, no parts, no photographs, and two of them marked unfinished. This is everything four people did today.
