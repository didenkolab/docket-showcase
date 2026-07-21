---
key: LEDGER-25
title: Importing the same statement twice does not produce two of everything
type: story
status: In review
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[LEDGER-2 Bank import]]"
labels: ["[[bank-import]]"]
created: 2026-07-13T09:50:00Z
updated: 2026-07-21T09:30:00Z
aliases: []
tags: [area/api]
definition_of_done: team
sprint: "[[Sprint 3]]"
estimate: 5
---

Every accountant will import the same month twice, because the first import was before the last few days landed and because the feed will re-send a month on its own. Two of every transaction is worse than none: it doubles a business's turnover and nobody spots it until the quarter will not balance.

## Acceptance

- [x] A line already imported is recognised and left alone on a second import
- [x] A line the bank corrected replaces the old one rather than joining it
- [x] The import says how many lines were new and how many it already had

## Comments

**priya · 2026-07-21 09:30** — Sending it back, sorry. Recognising a line by bank reference plus amount plus date is right until the bank corrects a line, which two of the three do by re-sending the month with the same reference and a different amount — and then we keep both. The correction case is in the acceptance and the import treats it as a new line.
