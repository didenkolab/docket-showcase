---
key: LEDGER-62
title: Fetch each business's statements overnight instead of when a page is opened
type: task
status: Backlog
status_category: todo
priority: normal
assignee: '[[ola]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-08-10T10:10:00Z
updated: 2026-08-10T10:30:00Z
aliases: []
tags: []
sprint: "[[Sprint 5]]"
---

Fetching when somebody opens the page means the first page of the morning takes eleven seconds and the banks see ninety businesses arrive at nine o'clock. Overnight, spread out, with the failures visible in the morning rather than in front of the accountant who was trying to work.

## Acceptance

- [ ] Every connected business is fetched once overnight, spread across the window
- [ ] A bank that refused is retried and then reported, not silently skipped

## Comments
