---
title: Harbor
type: design
updated: 2026-06-16
---

# Harbor

Harbor is booking software for a small marina, and the claim it makes is that one sentence holds the whole product: **this boat has that berth from this day to that day.** Everything else — the invoice, the card payment, the calendar on the office wall, the check-in on the pontoon — hangs off that sentence being true and being in one place.

What it replaces is a wall planner: one sheet of paper, a season's berths down the side, the weeks across the top, and pencil. The planner is not primitive. It is readable from across the room by four people at once, it works when the wifi does not, and everybody in the harbour office already knows how to use it. Anything we build is measured against it.

## The flows

**Booking.** Someone asks for a berth for a range of dates. Harbor answers which berths are free for that range — by length, draught and shore power, because a nine-metre boat does not fit a seven-metre berth — holds one for twenty minutes while the guest pays, and confirms it. The hold is what stops two people buying the same berth while one of them is typing a card number, and it is the reason availability and the write cannot be two separate reads.

**Money.** Confirmation takes a card payment, and cancellation gives it back. An invoice goes to the guest priced at the rate that applied on the day the booking was made, not today's rate, so that a marina which raises its prices in August does not reissue June's invoices at August's money.

**The calendar.** A month of every berth on one screen, readable across the office. Arrivals, departures, and the slip that has been empty for a fortnight, without clicking anything.

**Check-in.** A guest arrives at a pontoon with one bar of signal and a wet phone. Harbor finds the booking, confirms the boat, photographs the papers, and shows the office all of it whenever the phone next has a network.

## The vocabulary

A **berth** is a physical place a boat is tied to; it has a length, a depth, and shore power or not. A **booking** is one boat in one berth for a range of nights. A **hold** is a booking that has not been paid for yet and expires. **Check-in** is the arrival, which is a different event from the booking and can happen weeks later. A **season** booking is priced by the month rather than the night, and is the thing most likely to be cut short.

The word we avoid is "reservation", because half the marinas use it for a hold and half for a confirmed booking, and the ambiguity is exactly where double-bookings live.

## What this costs, and what is not built

Holding availability and the booking write together is what makes the hold correct and it is also the slowest thing in the product; the month view needs a cache to stay usable on a four-hundred-berth marina. Group bookings, a waiting list for a full week, and printing the week for the office wall are all unbuilt. So is anything to do with the winter: Harbor currently assumes boats are in the water.
