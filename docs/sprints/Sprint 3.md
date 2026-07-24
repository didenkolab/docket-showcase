---
title: Sprint 3
type: sprint
updated: 2026-07-24
starts: 2026-07-13
ends: 2026-07-24
---

# Sprint 3

Bank import for Ledgerline, first three banks

## Retrospective

Ledgerline can pull a statement from the three banks our first accountants actually use, and importing the same statement twice no longer produces two of everything — which is the difference between a feature and a liability. Harbor carried on underneath: the webhook reconciliation (`HARBOR-82`), the month-query cache (`HARBOR-83`) that took the calendar from two and a half seconds to under one, and the calendar bug (`HARBOR-85`) that drew boats which had left the day before as still moored.

The double charge (`HARBOR-64`) on the Wednesday of the first week was the sprint's real event. Three marinas, twenty minutes apart, all with the same shape: a slow confirmation, a guest pressing the button again, two charges and one booking. It is written up as an incident with the refunds against it. What made it possible was that our confirmation had no way of saying 'this is the same intention as the last one', and it was found by three customers rather than by us. The calendar month story (`HARBOR-32`) also came back from review — beautiful on forty berths and unusable on four hundred and six, which is what Sandholm have.

Two changes. Anything that spends money is idempotent by construction and says so in its acceptance. And a screen goes into review with the largest marina's data loaded, not with the demo marina's — the size of the customer is not a detail we get to discover in review.
