---
title: 'Offline first: the phone is the source of truth for a job'
type: decision
updated: 2026-07-31
status: accepted
date: 2026-07-31
---

# ADR-0004 — Offline first: the phone is the source of truth for a job

## Context

On Wednesday 29 July eleven crews lost an afternoon's work. Their phones came back into signal at the depot, the merge saw that the server had touched every job since the phone last saw it, and it kept the server's version of every field. Thirty-four jobs went back to how they had looked at seven that morning: no notes, no parts, no photographs, and two jobs the customer had signed for marked unfinished. That is `FIELD-50`; the incident is written up in this vault and the postmortem is being drafted this week.

The rule that did it — last writer wins, and the server counts as the writer whenever it has touched the row — was a line in the sync code. It read as reasonable there. It was never written anywhere a dispatcher, a product person or the other four engineers could see it, so nobody ever had the chance to say the obvious thing: a day in a dead zone is precisely the case where the phone is right and the server is a stale copy from seven in the morning.

The same question is now live in a second product. `HARBOR-103` queues check-ins on a phone with no signal and flushes them later, and it will need an answer to the same conflict within the month. Deciding this once, in writing, is the point.

## Decision

**For a job, the phone is the source of truth. The server never overwrites a field that a phone changed while it was offline, and anything the server cannot reconcile is kept rather than dropped.**

Where the two genuinely disagree — the phone changed a field and a dispatcher changed the same field while the crew was out — both versions are held and the crew is shown what disagreed and asked to choose. Nothing is resolved silently in either direction.

"Kept rather than dropped" is the load-bearing half. A merge that cannot decide must never delete: the version nobody chose stays, attached to the job, until somebody says otherwise. Storage is cheap and a crew's afternoon is not.

This is a rule about jobs. It is not a rule about the schedule: which crew is on which job tomorrow is the dispatcher's to decide and the server holds it.

How the rest of the day fits around that is [[fieldnote|Fieldnote's design page]].

## What this costs

A dispatcher's correction no longer takes effect while a crew is out. If he fixes an address at eleven and the crew has already edited the job, the crew's version wins and he has to say it again — and he will find that annoying, correctly, because he was right and the software preferred somebody else.

Two versions of a job can now exist for hours, so every screen that shows a job has to be able to show that. The conflict screen is real work nobody had planned for and it is the largest thing on the next fortnight.

And a job carries its history rather than its state, so the data grows with every conflict and never shrinks on its own. We have not decided when a kept version may be thrown away, which means for now it never is.

## Alternatives considered

**Last write wins by timestamp.** Rejected because the phone's clock is the thing we trust least in the whole system. A handset that has been off the network since seven in the morning has no better idea what time it is than we do, and two of the test phones already disagree with each other by minutes. Deciding whose work survives with a number the device made up is not a rule, it is a coin.

**Server wins, which is what we had.** Rejected for the reason the incident showed: the server is authoritative about everything except the one thing the crew was actually doing, and the longer a crew is offline — which is to say, the more work they have done — the more of it this throws away.

**Merge per field with no winner.** Rejected because two fields of one job taken from two versions produce a job that nobody wrote. A crew reading it back cannot recognise their own work, and the first time that reaches a customer it costs more than the incident did.

**Lock a job to a crew while they hold it offline.** The closest call. Rejected because a lock has to be released by something, and the thing that would release it is the network the crew does not have.
