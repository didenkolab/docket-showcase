---
title: Ledgerline
type: design
updated: 2026-09-02
---

# Ledgerline

Ledgerline is bookkeeping for a business too small to have a finance department and too real to be run out of a spreadsheet. The claim is narrower than "accounting software": **the quarter closes out of Ledgerline and the spreadsheet stays shut.**

That is a deliberate target. Every accountant we have spoken to already has software, and every one of them also has a spreadsheet beside it where the quarter is actually assembled. The invoicing they will tolerate anywhere. The fortnight at the end of the quarter is the thing worth paying to be rid of, and as of this week it is the part of the product that exists.

## The flows

**Invoicing.** An invoice is written line by line with the tax shown per line, numbered in one unbroken sequence per business year, rendered as a PDF, and emailed with some idea of whether it arrived. The number is allocated once and never reused, even when an invoice is abandoned, because a gap in the sequence is a question an auditor asks — and `LEDGER-22` showed how easily two invoices issued in the same minute can claim one.

**Bank import.** A statement comes in from the bank — through an API where there is one, as a file where there is not — and each line is matched against the invoice it pays. Importing the same statement twice does nothing, and the rule that makes that true is [[0003-bank-imports-are-idempotent-by-statement-hash|ADR-0003]] rather than a trick in the importer. What the importer cannot guess goes to `LEDGER-61`, which is the product's honest half: the matching that cannot be automated is the work the spreadsheet was doing.

**Tax.** Rates that applied on the day rather than today, and a quarter that closes when somebody closes it rather than when the calendar does — [[0005-tax-periods-close-by-decision|ADR-0005]]. A closed period cannot be booked into at all; a correction is a document in the open period that refers to the closed one. That rule came from an accountant describing the invoice that appears in a filed quarter as the thing that ruins her October.

## The vocabulary

An **invoice** is a document that has been sent; before that it is a draft and it has no number. A **credit note** is a document that credits an invoice — it is not a negative invoice and not a state on one, and since [[0006-refunds-are-credit-notes|ADR-0006]] it is also the only way a refund reaches a card. A **statement** is one bank's record of a period; a **line** is one movement on it. **Matching** joins a line to the invoice it pays, and a line may match nothing, which is a normal outcome and not an error. A **period** is a tax quarter, and it is open until somebody closes it.

We say **business** rather than "company" throughout, because half our first customers are sole traders and the word matters to them.

## What this costs, and what is not built

Matching is a heuristic, and a heuristic that is right nine times in ten is wrong once a week for a business with fifty invoices a month. Every wrong match is worse than a missing one, so the importer is deliberately conservative and the manual screen is busier than it would be if we were braver — the number we watch is the share of lines it settles on its own, and it is short of where it needs to be.

Closing a period cost us the assumption that one period is open at a time; every query in this product now has to say which one it means, for ever.

Recurring invoices and chasing a late one are unbuilt, and the second was cancelled rather than deferred. Rounding per line versus per invoice is still an open question with two national rules disagreeing about it. So is anything an accountant would call double entry.
