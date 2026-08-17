---
key: LEDGER-59
title: Email an invoice and know whether it arrived
type: story
status: In review
status_category: doing
priority: normal
assignee: '[[priya]]'
parent: "[[LEDGER-1 Invoices and credit notes]]"
labels: ["[[invoicing]]"]
created: 2026-07-30T11:00:00Z
updated: 2026-08-17T16:10:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 5]]"
estimate: 3
tested_by: ["[[LEDGER-42 A late invoice is chased twice and then left alone]]", "[[LEDGER-66 An invoice that bounced is not an invoice that arrived]]"]
---

An invoice nobody received is an invoice nobody is going to pay, and today the only evidence that it was sent is the sender's own memory of pressing the button. Sending has to be a thing the invoice remembers, with the address it went to, the moment it went, and whatever the mail server said afterwards.

## Acceptance

- [x] Sending records the address, the moment, and what the mail server answered
- [x] A bounce is visible on the invoice rather than in somebody's inbox
- [x] The same invoice can be sent again without becoming a second invoice

## Comments
