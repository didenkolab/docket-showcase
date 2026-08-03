---
type: risk
likelihood: unlikely
impact: severe
owner: ola
reviewed_on: 2026-08-03
key: HARBOR-14
title: The payment provider suspends a marina's account mid-season
status: Backlog
status_category: todo
priority: normal
assignee: '[[ola]]'
created: 2026-06-22T10:20:00Z
updated: 2026-08-03T14:10:00Z
labels: ["[[payments]]"]
tags: []
aliases: []
threatens: ["[[HARBOR-3 Card payments]]"]
---

## What could happen

The payment provider suspends a marina's account mid-season.

## Why we think so

Marinas take a season's money in eight weeks, which to a payment provider's fraud model looks like a dormant account that suddenly turns over forty thousand kroner in a fortnight. A provider that decides to hold funds while it asks questions stops a marina taking bookings on the weekend it earns its year, and there is no second provider to fail over to — that is the price the payments decision names and accepts.

## What we would do

Every marina is onboarded with its expected season volume declared up front rather than discovered, and we hold the provider's escalation contact rather than the support form. If it happens, bookings continue and payment is taken on arrival, which is what the marina did before us.
