---
title: Bank imports are idempotent by statement hash
type: decision
updated: 2026-07-15
status: accepted
date: 2026-07-15
---

# ADR-0003 — Bank imports are idempotent by statement hash

## Context

The bank import went in this sprint and the first thing it did on real data was produce two of everything, because an accountant who is not sure whether an import worked imports it again. That is `LEDGER-25`, and it is not a bug in the sense of somebody having made a mistake: nothing in the design said what the same statement twice was supposed to mean.

A week earlier `HARBOR-64` had the same shape from the other end — a guest who was not sure whether a payment had worked pressed the button again, and a system with no way to say "this is the same intention as the last one" charged the card twice. Two products, two weeks, one missing idea.

The three banks our first accountants use make it worse rather than better. One has an API with a transaction id; two send a file. Neither of the two guarantees that a statement fetched twice is byte-identical, and one of them reissues a corrected statement for the same period under the same name.

## Decision

**A statement is identified by the hash of its normalised content, and every line by the hash of that statement plus the line's position in it. Importing a statement whose hash we already hold is a no-op that reports what it skipped.**

Normalisation is the part with the rules in it: line endings, the thousands separator, trailing whitespace and the header rows that carry the fetch time rather than the data. Everything that survives normalisation is content, and content decides identity.

The line's position matters because a business that pays the same supplier the same amount on the same day twice is not making a mistake, and two lines that are identical in every field are two payments.

What the import does with a line once it has one is [[ledgerline|Ledgerline's design page]].

## What this costs

The normalisation rules are where every future bug lives. A bank that adds a column, changes a date format or pads an amount produces a different hash for the same statement, and the import silently duplicates rather than silently skipping — which is the worse of the two failures and the one nobody notices until a quarter is being closed. Every new bank adds a rule to a function that is already the most delicate thing in the importer.

A restated statement cannot be corrected in place. When the bank reissues a period, we import it as a new statement and somebody has to reconcile the two by hand, because we have deliberately made ourselves unable to tell a correction from a fresh document.

And the hash is not readable. When an import does nothing, the message a person gets is that this statement was already imported on a date, which is the best we can do and is not the same as showing them why.

## Alternatives considered

**Match on the bank's own transaction id.** Rejected because two of our three banks do not send one, and the third's is unique per fetch rather than per transaction — the same payment fetched on Tuesday and Wednesday arrives with two different ids. A rule that works for one bank and has to be special-cased for two is not a rule.

**De-duplicate on date, amount and reference together.** Rejected because it makes a genuine second payment invisible. A business that pays two identical invoices to the same supplier on the same day is ordinary, and an importer that swallows the second one is worse than one that duplicates: a duplicate is seen and deleted, a missing line is found in October.

**Ask the person: "you have imported this before, continue?"** Rejected because it is the same question the accountant could not answer in the first place. They import twice precisely because they do not know whether the first one worked, and a dialogue that asks them to know is a dialogue they will click through.
