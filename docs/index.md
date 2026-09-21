---
title: Northlight
type: page
updated: 2026-09-04
---

# Northlight

Three products for the same stretch of coast, built by six people between 15 June and today: Harbor for marinas, Ledgerline for the businesses that invoice for them, and Fieldnote for the crews who service the boats. One vault, one board, one key space — HARBOR, LEDGER and FIELD — and the reason for that is [[0001-one-vault-for-three-products|ADR-0001]], which is also the first thing to read if you are wondering why the backlog is this long.

## If you are new

Start with the product you are going to touch: [[Harbor|Harbor]], [[Ledgerline|Ledgerline]] or [[Fieldnote|Fieldnote]]. Each says what the product is, the flows it has, the words it uses for things, and what it costs — and each was rewritten once this quarter when something happened that made the first version wrong. [[Architecture|The architecture page]] says what the three share, which is less than people expect.

Then read [[Documents]], which is normative: the five kinds of page, where each lives, and what a decision must contain. `docket check` enforces the half of it that a program can.

## The arguments

Six decisions were taken this quarter and they are in `docs/decisions/`, numbered in the order they were made. Two of them explain most of what is surprising in the code: [[0004-the-phone-is-the-source-of-truth-for-a-job|ADR-0004]], which is why Fieldnote keeps two versions of a job rather than merging them, and [[0006-refunds-are-credit-notes|ADR-0006]], which is why a refund in Harbor goes through Ledgerline at all. Both were bought expensively.

## The work

Sprints are pages in `docs/sprints/`, one per fortnight, each with the goal it started with and the retrospective it ended with; the tasks that were in one are its backlinks rather than a list. Sprint 6 finished today and Sprint 7 is planned.

The labels — [[bookings]], [[payments]], [[offline-sync]] and the rest — each have a page saying what they mean, and everything carrying one is in that page's backlinks.

## The apps, and the pages they brought

This vault runs twelve packs on top of the board, and five of them brought a document explaining how the thing they add is meant to be kept: [[How objectives are kept]] on why progress is not a percentage of finished tasks, [[How risks are kept]] on why a risk has two words rather than a score, [[How incidents are kept]] on why an incident and its postmortem are two tasks, [[How requests are kept]] on why a request is not a backlog item, and [[How time is logged]] on why an hour is a note rather than a number on a card. [[How testing works here]] is the largest of them and says how a test plan, a test and a run relate.

Everything those five describe is in this vault with real data in it: three objectives and seven key results for the quarter, six risks reviewed twice, two incidents with their postmortems, eight customer requests, and thirty worklogs from the last two sprints.

## Where the quarter got to

Harbor launched check-in on the pontoon in August and the whole check-in epic is finished. Ledgerline is closing its first quarter this week. Fieldnote lost eleven crews an afternoon in July, and the work that came out of that is most of what is on the board now. The one thing nobody has settled is what happens to a season berth that is cut short, which is why `HARBOR-142` has been in review since the middle of August.
