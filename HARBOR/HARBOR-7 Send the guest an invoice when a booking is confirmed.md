---
key: HARBOR-7
title: Send the guest an invoice when a booking is confirmed
type: story
status: In progress
status_category: doing
priority: normal
assignee: '[[tomasz]]'
parent: "[[HARBOR-1 Season bookings]]"
labels: ["[[invoicing]]"]
created: 2026-06-15T09:50:00Z
updated: 2026-06-24T16:00:00Z
aliases: []
tags: []
definition_of_done: team
sprint: "[[Sprint 1]]"
estimate: 5
tested_by: ["[[HARBOR-27 An invoice for the nights that were booked]]", "[[HARBOR-28 The rate on the day of the booking, not today's]]"]
---

A marina's season is sold on invoices, and the sprint goal is only met when one comes out of a booking without anybody retyping it. The invoice carries the boat, the berth, the nights and the rate that applied on the day it was booked, because a rate that changes in August must not change what June already agreed.

## Acceptance

- [x] Confirming a booking produces an invoice with the nights and the rate on it
- [x] The rate on the invoice is the one that applied on the day of booking
- [ ] The invoice number is unique and never reused

## Comments
