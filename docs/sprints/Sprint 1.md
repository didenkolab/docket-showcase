---
title: Sprint 1
type: sprint
updated: 2026-06-26
starts: 2026-06-15
ends: 2026-06-26
---

# Sprint 1

A marina can take a booking and send an invoice

## Retrospective

We got the sentence the whole product hangs off — this boat has that berth from this day to that one — and an invoice out of the end of it, which is what we said the sprint was for. Reserving a berth for a date range (`HARBOR-5`), the free-berths answer the harbour office actually asks for (`HARBOR-6`), and importing a real marina's forty-one berths (`HARBOR-8`) all finished inside the two weeks. Ledgerline's invoice numbering landed beside them, so the demo we gave on the Friday was one flow across two products rather than two demos.

The one that hurt was the invoice story (`HARBOR-7`) coming back from review on the Thursday: it priced the booking at today's rate rather than the rate on the day it was booked, and a marina that changes its prices in August would have reissued June's invoices at August's money. Priya caught it reading the code rather than running it, which is luck we should not plan for. It cost us most of a day and it was the right day to spend.

Two things change. Rates are now written down as a decision rather than argued about in each story, because three of us had three answers when it came up. And the spreadsheet import gets a real marina's file before the story is written, not after: half of the import estimate went on a column called 'note2' that turned out to hold shore power.
