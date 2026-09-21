---
title: Harbor
type: design
updated: 2026-08-21
---

# Harbor

Harbor is booking software for a small marina, and the claim it makes is that one sentence holds the whole product: **this boat has that berth from this day to that day.** Everything else — the invoice, the card payment, the calendar on the office wall, the check-in on the pontoon — hangs off that sentence being true and being in one place.

What it replaces is a wall planner: one sheet of paper, a season's berths down the side, the weeks across the top, and pencil. The planner is not primitive. It is readable from across the room by four people at once, it works when the wifi does not, and everybody in the harbour office already knows how to use it. Anything we build is measured against it, and the one thing it still does better is print.

## The flows

**Booking.** Someone asks for a berth for a range of dates. Harbor answers which berths are free for that range — by length, draught and shore power — holds one for twenty minutes while the guest pays, and confirms it. The hold is what stops two people buying the same berth while one of them is typing a card number: `HARBOR-38` was two separate reads with nothing between them, and fixing it properly meant changing how a hold is created rather than adding a lock.

**Money.** Confirmation takes a card payment, and cancellation gives it back. An invoice is priced at the rate that applied on the day of the booking, not today's. Anything that spends money is idempotent by construction and says so in its acceptance — that rule was bought with eleven duplicate charges in July, and the reasoning is in [[0003-bank-imports-are-idempotent-by-statement-hash|ADR-0003]]. Which provider takes the money, and why there is only one, is [[0002-payments-go-through-one-provider|ADR-0002]].

**The calendar.** A month of every berth on one screen, readable across the office. The month query is cached because the honest version took two and a half seconds on Sandholm's four hundred and six berths, which is a screen nobody leaves open.

**Check-in.** This is the part that changed. A guest arrives at a pontoon with one bar of signal and a wet phone; the dockhand scans the sticker on the cleat, which opens that berth's booking, confirms the boat, photographs the papers, and queues the lot. The office sees it when the phone next has a network. Two dockhands ran a whole weekend on their own phones in the rain in August, which is the only test of this that counts.

## The vocabulary

A **berth** is a physical place a boat is tied to; it has a length, a depth, and shore power or not. A **booking** is one boat in one berth for a range of nights. A **hold** is a booking that has not been paid for yet and expires. **Check-in** is the arrival, which is a different event from the booking and can happen weeks later — a queued check-in carries the time the phone thought it was, which is why `HARBOR-153` put arrivals in the future. A **season** booking is priced by the month rather than the night.

The word we avoid is "reservation", because half the marinas use it for a hold and half for a confirmed booking, and the ambiguity is exactly where double-bookings live.

## What this costs, and what is not built

The queue on the phone is the price of the pontoon working at all: every screen that shows an arrival now has to be able to show one that has not reached us yet. Group bookings, a waiting list, and printing the week for the office wall are all unbuilt, and the last of those is a customer request that has been waiting since June. What happens to a season booking that is cut short is not decided, which is why the season-rate story has sat in review since the middle of August. Harbor still assumes boats are in the water: there is nothing here about winter storage.

What Harbor shares with the other two products, and what it deliberately does not, is [[Architecture|the architecture page]].
