---
type: test_execution
environment: staging
revision: 9deb136
started:
finished:
key: FIELD-56
title: Cucumber on staging at 9deb136
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-05T17:00:00Z
updated: 2026-08-05T17:00:00Z
labels: []
tags: []
aliases: []
---

# What was run, where

An execution is one pass over a set of tests, on one build, in one environment.
Its runs are its children: a note per test, each with its own result.

Two notes rather than a status on the test, because a test carrying only its
last result cannot answer "did this ever pass on staging" — which is the
question a release asks.

## What was not run, and why

The part nobody writes down, and the part that matters when somebody asks
whether this build was tested.
