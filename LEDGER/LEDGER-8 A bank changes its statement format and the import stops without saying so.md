---
type: risk
likelihood: possible
impact: moderate
owner:
reviewed_on:
key: LEDGER-8
title: A bank changes its statement format and the import stops without saying so
status: Backlog
status_category: todo
priority: normal
assignee: '[[ola]]'
created: 2026-06-22T10:40:00Z
updated: 2026-06-22T10:40:00Z
labels: ["[[bank-import]]"]
tags: []
aliases: []
---

## What could happen

A bank changes its statement format and the import stops without saying so.

## Why we think so

Two of the three banks we read give us a file rather than an API, and a file format is a promise nobody made. The failure we should expect is not a crash: it is a column that moves, an import that succeeds, and a quarter of lines that are quietly wrong until an accountant notices in October.

## What we would do

The importer refuses a statement it cannot fully account for rather than importing the part it understands, and the manual matching screen is the fallback for a bank that has moved under us.
