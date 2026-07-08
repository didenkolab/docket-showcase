---
key: HARBOR-63
title: Guests at three marinas were charged twice for one booking
type: incident
status: QA
status_category: doing
priority: normal
assignee: '[[tomasz]]'
labels: ["[[payments]]"]
created: 2026-07-08T09:50:00Z
updated: 2026-07-08T14:40:00Z
aliases: []
tags: []
severity: sev2
detected_at: 2026-07-08T09:40:00Z
resolved_at: 2026-07-08T13:15:00Z
customers_affected: 3 marinas, 7 guests, 11 duplicate charges
---

Between 09:40 and 10:05 on Wednesday 8 July, eleven card charges were taken for seven bookings across three marinas. Every one of them has the same shape: the confirmation call to the provider took longer than the guest was willing to wait, the guest pressed the button again, and the second press was a second charge against a booking that already had one.

Vik rang at 09:52 to say a guest had been charged twice. Sandholm rang at 10:04. The charges were stopped by taking confirmation off the booking screen at 10:20; the eleven duplicates were refunded by hand from the provider's console by 13:15, and every affected guest was rung by the marina rather than emailed by us.

Found by three customers rather than by us, which is the part of this that should be uncomfortable. The fix, the reconciliation that would have caught it, and what we are doing about the general case are in the postmortem.

## Comments
