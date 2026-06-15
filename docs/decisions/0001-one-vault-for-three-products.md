---
title: One vault for three products
type: decision
updated: 2026-06-15
status: accepted
date: 2026-06-15
---

# ADR-0001 — One vault for three products

## Context

Northlight is six people building three products for the same stretch of coast: Harbor for marinas, Ledgerline for the accountants who bill for them, and Fieldnote for the crews who service the boats. The three are separate products with separate customers, and everybody on the team works on at least two of them in any given fortnight.

We had to decide, before anything was written down, whether that is three projects or one. It is not a question we can defer: the first week produces keys, and a key is the thing people say out loud for the rest of the product's life. Two dependencies were already visible on the whiteboard on day one. A refund in Harbor has to become a credit note in Ledgerline or the marina's accountant cannot explain it. And the hardest problem in Fieldnote — a phone that works for a day with no signal — is the same problem as checking a boat in from a pontoon, which is Harbor's.

## Decision

**All three products live in one vault, on one board, in one key space, separated by a project prefix: HARBOR, LEDGER and FIELD.**

A relation crosses projects like any other link, so the refund story can say it is blocked by the credit-note story and both cards show it. A sprint is the team's fortnight rather than a product's, because the team is one team and pretending otherwise would mean three planning sessions for six people. The prefix carries which product something belongs to, and it carries it in the one place everybody reads: the key.

This also settles where cross-cutting things go. A risk that threatens Harbor's payments is a HARBOR task; an objective about closing a quarter is a LEDGER one. There is no fourth project for the team itself, and there should not be — work that belongs to everybody belongs to nobody, and the board that filters by product is the one people actually open.

## What this costs

One backlog is longer than any one person wants to read. Somebody who only cares about Fieldnote scrolls past two products' worth of tax and berths to find their own work, and the default view of this vault is not useful to anybody — filtering stops being a convenience and becomes the only way in. Every board here is a saved filter for that reason.

The sprint goal is the sharper cost. A fortnight that serves three products either gets one sentence that is true of all of them, which is usually vague, or three sentences wearing one coat. Sprint 3 was "bank import for Ledgerline" and Harbor did a sprint's work underneath it that the goal did not mention.

And a customer conversation is now harder to have from the board. Nothing here says which marina is waiting for what; that lives in requests and in people's heads, which is fine at four customers and will not be at forty.

## Alternatives considered

**Three vaults, one per product.** Rejected because the two dependencies that hurt most cross the boundary. A link between repositories is a URL in a comment: it does not appear in a backlink, a graph or a board, and it rots the first time something is renamed. We would have discovered the refund and credit-note pair by having the argument twice.

**One vault, one project, and a label per product.** Rejected because the key is what people say. "HARBOR-41" tells you which product you are talking about with no lookup, in a commit message, in a corridor and in a phone call to a marina; a label does not appear in a key and a numbering shared across three products makes the number meaningless.

**One vault now, split when it hurts.** This is the one to revisit, and it is worth saying why we did not simply plan for it: splitting later means renumbering, and a key that moves is not a name. If this becomes wrong it will be because the team has grown into three teams, and at that point the split is worth its price rather than free.
