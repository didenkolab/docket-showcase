---
title: Fieldnote
type: design
updated: 2026-06-16
---

# Fieldnote

Fieldnote is job scheduling for crews who work where there is no signal. The claim is one sentence and the whole product rests on it: **take the phone into the valley, do a day's work, come back, and everything you did is there.**

Every scheduling tool our first customer has tried assumed a connection. Each one worked in the depot car park and quietly lost the afternoon somewhere past the second stop, and each time the crews went back to paper dockets and the dispatcher went back to the telephone. Offline is not a feature here. It is the premise, and everything else is negotiable.

## The flows

**The day.** A dispatcher puts jobs on crews from a board. Before a crew leaves, the phone takes the whole day — jobs, addresses, what happened last time somebody went to that address, and the route between them — and holds it locally. Nothing after that point needs a network.

**The job.** A crew arrives, does the work, and writes it up from the van while it is fresh: what was wrong, what was used, photographs, and the customer's signature. All of it is queued on the handset.

**The route.** The stops are ordered so the day is driveable, using the road's travel time rather than the distance between two dots, with the depot and the last stop as fixed ends. When a job overruns, the rest of the day should move rather than the crew improvising.

**Coming back.** The phone finds a signal, sends its queue oldest first, and the office sees the day. This is the part with the hard problem in it, and this page will be wrong about it before the quarter is out.

## The vocabulary

A **job** is one visit to one address for one customer; it is the unit everything else is about. A **crew** is the people in one van, and it is the thing work is assigned to rather than a person. A **stop** is a job seen from the route's point of view. A **day** is a crew's list, in order, and it is what the phone holds. A **conflict** is one job with two versions that disagree.

We say **crew** and not "technician" because the van holds two people and the work belongs to the van.

## What this costs, and what is not built

Everything is harder because of the premise. Data has to be complete on the phone before it leaves, which means downloading things the crew will probably not need. Every edit is a queued intention rather than a write, so the phone holds a history rather than a state. And the moment the phone reconnects is the moment everything can go wrong at once.

What happens when the phone and the server disagree about the same job is not decided. That is the largest unanswered question in the product and it is currently answered by whatever the sync code happens to do.
