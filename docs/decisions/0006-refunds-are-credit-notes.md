---
title: Refunds are credit notes
type: decision
updated: 2026-08-27
status: accepted
date: 2026-08-27
---

# ADR-0006 — Refunds are credit notes

## Context

`HARBOR-183` gives a guest their money back when the weather cancels a weekend, and `LEDGER-28` has to make that explicable to the marina's accountant. The two have been circling each other since June: the refund story is blocked by the credit-note story and has been sitting in Sprint 6 waiting for this.

What forced it now is a question nobody could answer on Tuesday: what stops a refund being larger than the invoice it refunds. Harbor knows what it charged. Nothing on the accounting side knows what may be given back, because there is nothing on the accounting side yet.

There are two coherent ways to record money going back out. It is a negative payment against the invoice, or it is a document of its own that credits the invoice. They look similar until a quarter is closed, and then they are nothing alike.

## Decision

**Every refund is a credit note against the invoice it refunds. The card refund is what the credit note causes, not the other way round.**

So the sequence is one way only: a credit note is issued against an invoice, and issuing it is what tells Harbor to return money to the card the payment came from. A refund cannot exist without one, which is what makes a refund larger than the invoice impossible rather than merely checked for — a credit note cannot credit more than the invoice it is written against, and there is no other path to the card.

A credit note carries its own number in the same unbroken sequence as invoices, its own tax lines, and a reference to what it credits. It is a document the business sends, not a state on another document.

What that sequence has to survive is [[ledgerline|Ledgerline's design page]].

## What this costs

Harbor's refund flow now depends on Ledgerline being up. A marina that wants to refund a guest standing in front of them cannot do it while the accounting side is down, and "refund later" is a poor answer on a pontoon. That is a real coupling between two products we deliberately keep separable, and it is the price of the invoice and the refund telling the same story.

Refunding a booking that was never invoiced — a deposit taken and returned the same week, which happens — now needs an invoice first, or a special case. We have chosen the invoice, so a guest may get paperwork for something they thought was a phone call.

And a partial refund needs line items to credit, which means Harbor has to send an invoice that has them. "One booking, one line" was doing fine until this.

## Alternatives considered

**A negative payment against the invoice.** Rejected because it leaves the invoice saying a total that was never true. An accountant cannot hand in a document whose total has changed since it was sent, and a customer who compares the invoice in their inbox with the one in the system finds two different numbers.

**A refund with no ledger record at all, reconciled from the bank statement.** Rejected because that is the spreadsheet we are replacing. It works right up until the quarter is closed and somebody has to explain a line of money leaving that no document accounts for.

**A credit note only when the invoice has been sent, a plain reversal before that.** Genuinely tempting, and rejected because "sent" is a state that changes: an invoice that was reversed quietly on Tuesday and sent on Wednesday leaves two conflicting histories, and the rule that decides which happened is the kind of rule that produces the next postmortem.
