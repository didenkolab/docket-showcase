---
title: Ledgerline
type: design
updated: 2026-06-16
---

# Ledgerline

Ledgerline is bookkeeping for a business too small to have a finance department and too real to be run out of a spreadsheet. The claim is narrower than "accounting software": **the quarter closes out of Ledgerline and the spreadsheet stays shut.**

That is a deliberate target. Every accountant we have spoken to already has software, and every one of them also has a spreadsheet beside it where the quarter is actually assembled — numbers gathered by hand from four places and typed into a return. The invoicing they will tolerate anywhere. The fortnight at the end of the quarter is the thing worth paying to be rid of.

## The flows

**Invoicing.** An invoice is written line by line with the tax shown per line, numbered in one unbroken sequence per business year, rendered as a PDF the customer's accountant will accept, and emailed with some idea of whether it arrived. The numbering is not a detail: a gap in the sequence is a question an auditor asks, so the number is allocated once and never reused, even when an invoice is abandoned.

**Bank import.** A statement comes in from the bank — through an API where there is one, as a file where there is not — and each line is matched against the invoice it pays, on amount, date and whatever reference the payer typed. What the importer cannot guess goes to a screen where a person matches it by hand, and that screen is the product's honest half: the matching that cannot be automated is the work the spreadsheet was doing.

**Tax.** Rates that apply on the day rather than today, the rounding rules, and the quarterly return an accountant can hand to the authority without retyping it.

## The vocabulary

An **invoice** is a document that has been sent; before that it is a draft and it has no number. A **credit note** is a document that credits an invoice — it is not a negative invoice and not a state on one. A **statement** is one bank's record of a period; a **line** is one movement on it. **Matching** joins a line to the invoice it pays, and a line may match nothing, which is a normal outcome and not an error. A **period** is a tax quarter, and it is either open or closed.

We say **business** rather than "company" throughout, because half our first customers are sole traders and the word matters to them.

## What this costs, and what is not built

Matching on amount, date and reference is a heuristic, and a heuristic that is right nine times in ten is wrong once a week for a business with fifty invoices a month. Every wrong match is worse than a missing one, so the importer is deliberately conservative and the manual screen is busier than it would need to be if we were braver.

Recurring invoices, chasing a late one, and rounding tax per line versus per invoice are all unbuilt. So is anything an accountant would call double entry: Ledgerline records what happened to a business's money and does not yet keep the books in the form an auditor would want to see them.
