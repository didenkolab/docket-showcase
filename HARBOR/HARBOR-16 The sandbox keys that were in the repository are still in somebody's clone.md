---
type: risk
likelihood: possible
impact: major
owner: ola
reviewed_on: 2026-06-22
key: HARBOR-16
title: The sandbox keys that were in the repository are still in somebody's clone
status: Backlog
status_category: todo
priority: normal
assignee: '[[ola]]'
created: 2026-06-22T10:50:00Z
updated: 2026-07-01T14:30:00Z
labels: ["[[payments]]"]
tags: []
aliases: []
threatens: ["[[HARBOR-3 Card payments]]"]
mitigated_by: ["[[HARBOR-37 Move the payment provider's keys out of the repository]]"]
---

## What could happen

The sandbox keys that were in the repository are still in somebody's clone.

## Why we think so

The provider's sandbox keys were committed in the first sprint and taken out in the second, which removes them from the working tree and from nothing else. They are in the history, in every clone, and in whatever search index has been over this repository since June. Sandbox keys are not money, but the habit that put them there is the habit that will put live ones somewhere.

## What we would do

Rotate what was committed, keep secrets in the deployment's own store, and make the person who needs a key ask for it rather than find it.
