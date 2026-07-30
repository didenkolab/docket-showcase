---
key: FIELD-51
title: Eleven crews' offline work was overwritten when their phones reconnected
type: incident
status: In review
status_category: doing
priority: normal
assignee: '[[aiko]]'
labels: ["[[offline-sync]]"]
created: 2026-07-29T14:20:00Z
updated: 2026-07-30T09:30:00Z
aliases: []
tags: []
severity: sev1
detected_at: 2026-07-29T14:05:00Z
resolved_at: 2026-07-29T18:30:00Z
customers_affected: 11 crews, 34 jobs, one afternoon
---

On Wednesday 29 July the Storelva crew rang the dispatcher at 14:05 to ask why their morning was empty. It was empty because their phones had come back into signal at the depot and the sync had taken the server's version of every job they had touched. By 14:40 the same was true of eleven crews and thirty-four jobs: no notes, no parts used, no photographs, and two jobs back to unfinished after the customer had signed for them.

Sync was turned off for every phone at 14:50, which stopped it spreading and left every crew's work sitting on their own handset. Twenty-nine of the thirty-four jobs were rebuilt from the request logs by 18:30; the remaining five were rung round and retyped by the dispatcher the next morning.

Nobody enjoyed ringing eleven crews to ask what they had done that day. The merge rule that did this was never written down anywhere, so nobody had the chance to disagree with it before it ran; that is the subject of the postmortem and of the decision it produced.

## Comments
