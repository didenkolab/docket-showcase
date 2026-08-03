---
type: postmortem
key: FIELD-52
title: 'Postmortem: the afternoon eleven crews lost'
status: In progress
status_category: doing
priority: normal
assignee: '[[aiko]]'
created: 2026-08-03T10:30:00Z
updated: 2026-08-03T10:30:00Z
labels: ["[[offline-sync]]"]
tags: []
aliases: []
---

## What happened

07:00 — the planner rebuilds every crew's day, as it does every morning. This touches every job row, including rows for jobs whose crews are already out of signal.

08:10 to 13:50 — eleven crews work in the eastern valley with no signal. Notes, parts, photographs and two customer signatures are written on the phones and queued.

13:55 — the first crew reaches the depot and their phone reconnects. The merge sees that the server has touched every job since the phone last saw it, and keeps the server's version of each field.

14:05 — the Storelva crew ring the dispatcher to ask why their morning is empty.

14:40 — eleven crews, thirty-four jobs. Two jobs the customer had signed for are back to unfinished.

14:50 — sync is turned off for every phone, which stops the loss spreading.

18:30 — twenty-nine jobs rebuilt from the request logs. The remaining five are rung round the following morning and retyped by the dispatcher.

## Why it was possible

The merge was last-writer-wins over the whole job, and the server counted as the writer whenever it had touched the row since the phone last saw it. The planner touches every row at seven in the morning. So the phone always lost, and it lost hardest for the crews who had been offline longest — which is to say, for exactly the people the product exists for.

That rule was never written down. It was a line in the sync code and it read as reasonable there; nobody outside the two people who wrote it ever had the chance to say that a day in a dead zone is the case where the phone is right and the server is a stale copy from seven o'clock.

The tests reached the same conclusion by the same route. There was one sync scenario, it was the happy path, and it was written by the person who wrote the merge.

## What we are changing

The rule is now a decision with a document behind it: for a job, the phone is the source of truth, and anything the server cannot reconcile is kept rather than dropped.

Where the two genuinely disagree, both versions are held and the crew is shown what disagreed and asked to choose. That is a card in Sprint 6, and it is the piece of work this incident bought.

The sync gets a scenario per conflict shape instead of one happy path, and it is held under a whole depot reconnecting at once rather than one phone at a time. That is a second card.

## What we are not changing, and why

We are not stopping the planner touching every row at seven. It is how the day is built and it is not the fault; a merge that cannot cope with the server having a normal morning is the fault.

We are not resolving conflicts automatically by field, however tempting it looks in the code. Two fields of one job merged from two versions produce a job that nobody wrote and that the crew cannot recognise, and the first time that reaches a customer we will have spent the trust this cost us twice over.
