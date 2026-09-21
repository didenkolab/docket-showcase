---
title: Payments go through one provider
type: decision
updated: 2026-06-24
status: accepted
date: 2026-06-24
---

# ADR-0002 — Payments go through one provider

## Context

`HARBOR-3` needs to take a card at the moment a berth is booked and hand money back when the weather cancels a weekend, and it needs to do it in eight weeks. `LEDGER-1` will need to take payment for an invoice within the year, against the same businesses.

So the choice is not really which provider. It is whether we build against one of them directly, or build the abstraction that would let us hold two. Marinas take a year's revenue in eight weeks, which means the day a provider stops working for us is a day a marina loses its season — and there is no way to make that day painless. There is only a choice about what we pay in advance to make it less likely.

## Decision

**Both products take money through one provider, called from one internal payments module that Harbor and Ledgerline both use.**

The module exists because two products calling a payment API two different ways is how a refund comes to mean two things. It is not a provider abstraction: it speaks this provider's vocabulary, holds this provider's idempotency rules, and would have to be rewritten rather than reconfigured to speak to another one. That is deliberate.

One provider means one sandbox, one webhook shape, one set of keys to keep out of the repository, one refund model to explain to an accountant, and one set of failure modes for the whole team to learn rather than two sets for half the team each.

What the three products do and do not share, and why this is the one dependency between two of them that was chosen rather than grown, is [[Architecture|the architecture page]].

## What this costs

The day this provider suspends a marina's account, holds funds while it asks about a suspicious eight-week revenue curve, or changes an endpoint with a month's notice, both products stop taking money and there is nothing to fail over to. That is on the risk register with a name against it, and the honest mitigation is a phone number for an escalation contact and a marina taking cards on arrival for a day. It is not a technical answer, because there is not one.

We also lose the ability to negotiate. A provider that knows it is the only one integrated prices accordingly at renewal, and the cost of moving is a rewrite rather than a configuration change.

And the module will read as an abstraction to whoever opens it next. It is not one, and the first person who tries to add a second provider behind it will find that out expensively — which is why it is written here.

## Alternatives considered

**Two providers behind a routing layer from the start.** Rejected because it doubles the integration work in the sprint that has to ship a season, and because the layer would have been designed against two providers we had not yet operated. The failure we are guarding against is rare; the cost of guarding against it lands every fortnight.

**One provider now, behind a real abstraction, so a second is cheap later.** Rejected because an abstraction written against one implementation is that implementation with different words on it. Every seam we would have guessed at — refunds, disputes, the shape of a webhook, when a charge is final — is exactly where two providers actually differ, and we would have guessed them all from one example.

**Take payment through the marina's own provider, whichever it is.** This is the one worth revisiting when we are talking to forty marinas rather than four, because several of them already have a card terminal and a contract. Rejected now because it makes every marina's onboarding a bespoke integration, and we have six people.
