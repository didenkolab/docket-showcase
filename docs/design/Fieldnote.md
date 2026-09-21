---
title: Fieldnote
type: design
updated: 2026-08-04
---

# Fieldnote

Fieldnote is job scheduling for crews who work where there is no signal. The claim is one sentence and the whole product rests on it: **take the phone into the valley, do a day's work, come back, and everything you did is there.**

On 29 July that claim was false for eleven crews, and this page was wrong in the way it said it would be. The section on coming back has been rewritten around the answer the incident forced.

## The flows

**The day.** A dispatcher puts jobs on crews from a board. Before a crew leaves, the phone takes the whole day — jobs, addresses, what happened last time somebody went to that address, and the route between them — and holds it locally. Nothing after that point needs a network.

**The job.** A crew arrives, does the work, and writes it up from the van while it is fresh: what was wrong, what was used, photographs, and the customer's signature. All of it is queued on the handset.

**The route.** The stops are ordered so the day is driveable, using the road's travel time rather than the distance between two dots, with the depot and the last stop as fixed ends.

**Coming back.** The phone finds a signal and sends its queue oldest first. For a job, the phone wins: the server never overwrites a field a phone changed while it was offline, and anything the server cannot reconcile is kept rather than dropped. Where the two genuinely disagree, both versions are held and the crew is shown what disagreed and asked to choose. That is [[0004-the-phone-is-the-source-of-truth-for-a-job|ADR-0004]] now rather than a line in the sync code, which is what `FIELD-50` cost us.

The rule is about jobs. It is not about the schedule: which crew is on which job tomorrow belongs to the dispatcher and the server holds it.

## The vocabulary

A **job** is one visit to one address for one customer; it is the unit everything else is about. A **crew** is the people in one van, and it is the thing work is assigned to rather than a person. A **stop** is a job seen from the route's point of view. A **day** is a crew's list, in order, and it is what the phone holds. A **conflict** is one job with two versions that disagree, and it is now a thing a crew sees rather than a thing the code resolves.

We say **crew** and not "technician" because the van holds two people and the work belongs to the van.

## What this costs, and what is not built

Everything is harder because of the premise. Data has to be complete on the phone before it leaves, which means downloading things the crew will probably not need. Every edit is a queued intention rather than a write. And a job now carries its history rather than its state, so it grows with every conflict and nothing has been decided about when a kept version may be thrown away.

A dispatcher's correction no longer takes effect while a crew is out, and he will find that annoying, correctly.

The conflict screen is unbuilt. So is holding the sync while a whole depot comes back into signal at once, which is the case that produced the incident and the case we have still not tested.
