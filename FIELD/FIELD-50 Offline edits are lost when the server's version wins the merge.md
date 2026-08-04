---
key: FIELD-50
title: Offline edits are lost when the server's version wins the merge
type: bug
status: In progress
status_category: doing
priority: critical
assignee: '[[tomasz]]'
parent: "[[FIELD-3 Offline mobile]]"
labels: ["[[offline-sync]]"]
created: 2026-07-29T14:10:00Z
updated: 2026-08-04T16:05:00Z
aliases: []
tags: [regress]
definition_of_done: hotfix
sprint: "[[Sprint 4]]"
found_in: ["[[FIELD-45 Work done with the phone offline survives the sync]]"]
estimate: 8
causes: ["[[FIELD-51 Eleven crews' offline work was overwritten when their phones reconnected]]"]
relates: ["[[HARBOR-103 Check a guest in from the pontoon with no signal]]"]
---

When a job comes back from a phone and the server's copy has also changed, the merge keeps the server's fields and drops the phone's. A day in a dead zone is exactly the case where the phone is right and the server is a stale copy from seven in the morning, so the rule throws away the only version of the work that anybody actually did.

## Acceptance

- [x] A field the phone changed while offline is never overwritten by an older server value
- [x] Anything the server cannot reconcile is kept somewhere a person can read it
- [ ] The eleven crews' lost notes are recovered from the request logs where they exist
- [ ] The merge rule is written down as a decision rather than living in the code

## Comments

**mateo · 2026-07-29 14:20** — Eleven crews, one afternoon. The Storelva crew rang the office to ask why their morning was empty and it went from there. Every job they finished in the eastern valley is back to the state it was in when they left the depot: no notes, no parts, no photographs, and two of them marked unfinished. This is everything four people did today.

**tomasz · 2026-07-29 15:10** — Found it. The merge is last-writer-wins on the whole job and the server counts as the writer whenever it has touched the row since the phone last saw it — and the planner touches every row at seven when it builds the day. So the phone always loses, and it loses hardest for the crews that were offline longest. I am taking it now; nothing else I have is worth a crew's day.

**ingrid · 2026-07-29 16:30** — What we are telling Nordic Field: we lost this afternoon's write-ups for eleven crews, we know exactly which jobs, and we are asking those crews to write them again tomorrow morning rather than pretending we can recover them all. Tomasz thinks the notes are in the request logs and is looking. Nobody rings a crew to ask what they did today twice — so the second half of this card is the decision about who wins a merge, written down where somebody can disagree with it.
