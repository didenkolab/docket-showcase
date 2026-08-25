---
type: risk
likelihood: possible
impact: severe
owner: aiko
reviewed_on: 2026-08-03
key: FIELD-7
title: A crew loses a day's work again and Nordic Field stop using the phone
status: Backlog
status_category: todo
priority: normal
assignee: '[[aiko]]'
created: 2026-06-22T11:30:00Z
updated: 2026-08-25T14:20:00Z
labels: ["[[offline-sync]]"]
tags: []
aliases: []
threatens: ["[[FIELD-3 Offline mobile]]"]
mitigated_by: ["[[FIELD-91 The sync holds when a whole depot comes back into signal at once]]"]
---

## What could happen

A crew loses a day's work again and Nordic Field stop using the phone.

## Why we think so

Eleven crews lost an afternoon on 29 July and rang the office about it. The fix went in within a week, and the thing that has not been tested is the case that produced it: a whole depot coming back into signal at once, at half past four, with a day of queued edits each. Dispatchers do not give software a third chance with their crews' time.

## What we would do

Hold the sync under a depot's worth of reconnections before the next season, and give the crew the conflict rather than resolving it for them.
