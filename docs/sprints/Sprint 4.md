---
title: Sprint 4
type: sprint
updated: 2026-08-07
starts: 2026-07-27
ends: 2026-08-07
---

# Sprint 4

Fieldnote works a whole day offline

## Retrospective

A crew phone now holds its jobs, its route and its photographs for a whole day without a signal and reconciles when it gets one, and Harbor's check-in learned the same trick from it: the queued check-in (`HARBOR-119`) and the flush that empties the queue (`HARBOR-120`) were both written this sprint. Two products sharing one hard problem turned out to be cheaper than two products each having half of it.

On the Wednesday of the first week we lost work that eleven crews had done offline. The merge took the server's version of a job whenever the two disagreed, and a day in a dead zone is exactly the case where the phone is right and the server is stale. It is written up as an incident with a postmortem; the short version is that the rule was never stated anywhere, so nobody could disagree with it before it ran. Nobody enjoyed ringing eleven crews to ask what they had done that day.

The rule is now a decision with a document: for a job, the phone is the source of truth, and anything the server cannot reconcile is kept rather than dropped. Sync now has a scenario per conflict shape instead of one happy-path scenario, and the sync work is on the sprint board rather than being 'nearly done' for a fortnight.
