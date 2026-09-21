---
title: Tax periods close by decision, not by date
type: decision
updated: 2026-08-18
status: accepted
date: 2026-08-18
---

# ADR-0005 — Tax periods close by decision, not by date

## Context

`LEDGER-3` has to decide when a quarter stops accepting entries, and the obvious answer is wrong in a way that only shows up in October.

A quarter ends on 30 September. The books for that quarter do not: an accountant is still entering September's invoices in the second week of October, with September dates on them, and that is not sloppiness — it is how the work arrives. The return is filed some time after that, and from the moment it is filed the period must not change, because the number in the return and the number in the books have to agree for ever afterwards.

So there are two dates that matter and neither is the end of the quarter: the day the books for it are finished, and the day the return goes. Every accountant we have asked has a different gap between them, and one of them described the invoice that appears in a filed period as the thing that ruins her October.

## Decision

**A tax period is open until somebody closes it. Closing is an act, with the person and the moment recorded on it, and after it nothing can be booked into that period at all.**

A correction to a closed period is a document in the open period that refers to the closed one — never an edit to what is closed. That is what an accountant does on paper and it is what an auditor expects to find.

A period that is closed can be reopened, by a person, and the reopening is recorded the same way the closing was. Refusing to allow it would be pretending nobody ever closes a quarter by mistake at half past four on a Friday.

What a period is made of, and what else this product does with it, is [[Ledgerline|Ledgerline's design page]].

## What this costs

A quarter can stay open indefinitely, and a business that never closes one gets a report that changes underneath it every time somebody enters something old. The software cannot save them from that; the most it can do is say how long a period has been open and how many entries have landed in it since the quarter ended, and then keep saying it.

Two periods being open at once is now a normal state rather than an error, so every query, every report and every screen has to say which period it means. That is a running cost on everything we build in this product from here.

And an entry can be refused for a reason that is nowhere in the entry: the date is fine, the amounts are fine, and the period is shut. That error message has to say who closed it and when, or it reads as a bug.

## Alternatives considered

**Close on the calendar date.** Rejected because it puts the honest work — entering September's invoices in October — outside the period it belongs to, and it would land in the wrong quarter. The software would be forcing an accountant to file a return she knows to be incomplete.

**A grace period of N days after the quarter ends.** Rejected because N is a number nobody can defend. Every accountant we asked gave a different one, the good answer depends on the business's own customers, and a default here silently becomes a policy for everybody who does not change it.

**Allow back-dated entries into a closed period, with an audit trail.** Rejected because a return that has already been filed cannot be un-filed by an audit trail. The trail records that the books and the return stopped agreeing; it does not stop it happening, and the whole value of closing is that it cannot happen.
