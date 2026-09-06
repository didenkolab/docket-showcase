"""Harbor: what a marina's season looked like between 15 June and 4 September 2026.

Four epics — season bookings, the berth calendar, card payments and check-in on the
pontoon — and the forty-four pieces of work under them, each one a spec that
`common.lifecycle` turns into the events that wrote it, sized it, pulled it into a
sprint, moved it and ticked it off.

Three anomalies are planted here on purpose, because a vault that has none is a vault
nobody can use to demonstrate finding them:

  * **adrift** — `harbor.loose.receipt-footer` has no parent, no label, no tag, no
    sprint, no relation and nothing links to it. Somebody wrote it down and it fell out
    of the plan, which is exactly what `docket anomalies --kind adrift` is for.
  * **only-owner** — every open piece of `harbor.ops.season-runbook` is on ola. The
    runbook is the one thing nobody else can finish, and no board can say so.
  * **one-sided** — the refund-over bug says it blocks the refunds story, and the
    refunds story does not say it is blocked. One card reads as ready to start and the
    other as waiting, from the same pair of files.

The cross-project relation is the awkward one: `harbor.payments.refunds` is blocked by
Ledgerline's credit-notes story, which lives in `ledgerline.py` and is created on
2026-07-14. Both sides of it are written here, under the `with_ledger` guard, so the
pair never disagrees — **ledgerline.py must not set `blocks` on `ledger.invoices.credit-notes`
itself**, or it will overwrite this one. Building Harbor on its own, before Ledgerline
exists, is done with SHOWCASE_NO_LEDGER=1 in the environment, which drops those two
events and leaves everything else identical.
"""
from __future__ import annotations
import os

import story

from . import common

PROJECT = "HARBOR"
PREFIX = "harbor."

# --- the epics ------------------------------------------------------------------------

EPICS = [
    dict(a="booking", t="Season bookings", type="epic", who="ingrid", made="06-15 09:30",
         moves=[("06-15 11:30", "Ready"), ("06-16 09:15", "In progress")],
         why="A marina sells the same forty berths every year and keeps the truth of who has "
             "which one in a wall planner. Harbor's first job is to hold that truth: a guest "
             "or the harbour office reserves a berth for a range of dates, the marina invoices "
             "for it, and nobody has to ring anyone to find out whether a slip is free.",
         ok=["A guest can reserve a berth for a date range and get an invoice for it",
             "Two people cannot hold the same berth for the same night",
             "The harbour office can cancel a booking and see the berth come back"]),
    dict(a="calendar", t="Berth calendar", type="epic", who="priya", made="06-15 09:31",
         moves=[("06-15 11:35", "Ready"), ("06-16 09:16", "In progress")],
         why="The wall planner the bookings replace was one sheet of paper the whole harbour "
             "office could stand in front of. Whatever we build has to be readable from that "
             "distance: a month of every berth on one screen, with the boat that is coming, "
             "the boat that is leaving and the slip that has been empty for a fortnight all "
             "visible without clicking anything.",
         ok=["A month of every berth is one screen the office can read across the room",
             "A booking can be moved to another berth without retyping it",
             "The calendar tells the truth about a boat that has already left"]),
    dict(a="payments", t="Card payments", type="epic", who="tomasz", made="06-15 09:32",
         moves=[("06-15 11:40", "Ready"), ("06-16 09:17", "In progress")],
         why="Marinas take a card at the moment of booking and hand back money when the "
             "weather cancels a weekend. Everything under this epic is that one flow and its "
             "unhappy halves: a charge that went through and a booking that did not, a refund "
             "the accountant has to be able to explain, a provider webhook arriving twice.",
         ok=["A confirmed booking is paid for by card, once",
             "A cancelled booking's money goes back to the card it came from",
             "Every charge can be matched to the booking it belongs to"]),
    dict(a="checkin", t="Mobile check-in", type="epic", who="aiko", made="06-15 09:33",
         moves=[("06-15 11:45", "Ready"), ("07-27 09:20", "In progress"),
                ("08-19 17:10", "In review"), ("08-20 17:20", "QA", "mateo"),
                ("08-21 15:30", "Done", "mateo")],
         why="The pontoon has no signal, a wet phone and a berth holder who wants to be on the "
             "boat rather than in the office. Check-in has to work standing on a finger pier "
             "with one bar and no patience: find the booking, confirm the boat, photograph the "
             "papers, and let the office see all of it whenever the phone gets a signal back.",
         ok=["A berth holder is checked in from the pontoon with no signal",
             "The office sees the check-in as soon as the phone reconnects",
             "The boat's papers are photographed and kept with the booking"]),
]

# --- season bookings ------------------------------------------------------------------

BOOKING = [
    dict(a="booking.week", t="Reserve a berth for a date range", parent="booking",
         who="tomasz", labels="bookings", tags=("area/api",), pts=5,
         made="06-15 09:40", sprint="Sprint 1",
         moves=[("06-15 11:10", "Ready"), ("06-16 09:40", "In progress"),
                ("06-18 16:20", "In review"), ("06-19 11:15", "QA", "priya"),
                ("06-22 14:40", "Done", "mateo")],
         why="Everything else in Harbor hangs off one sentence: this boat has that berth from "
             "this day to that one. A reservation is the range, the berth and the boat, and it "
             "either exists for every night in the range or it does not exist at all — a berth "
             "held for four of five nights is the argument the harbour office has to have on "
             "the pontoon on the fifth.",
         ok=["A reservation covers every night of the range or none of them",
             "A berth already taken for one night of the range is refused, naming the night",
             "The reservation is on the berth calendar the moment it is made"]),
    dict(a="booking.availability", t="Show which berths are free for a chosen week", parent="booking",
         who="priya", labels="bookings", pts=3, made="06-15 09:45", sprint="Sprint 1",
         moves=[("06-15 11:20", "Ready"), ("06-17 10:05", "In progress"),
                ("06-22 15:40", "In review"), ("06-23 10:20", "QA", "tomasz"),
                ("06-24 11:50", "Done", "mateo")],
         why="Before anybody reserves anything they ask the harbour office the same question: "
             "have you got room the week of the regatta. The answer has to come back as a list "
             "of berths that fit the boat, not as a grid the office has to read for them.",
         ok=["A week and a boat length come back as the berths that are free and long enough",
             "A berth held but not yet paid for is not offered to somebody else",
             "The answer is one request, not one request per berth"]),
    dict(a="booking.invoice", t="Send the guest an invoice when a booking is confirmed", parent="booking",
         who="tomasz", labels="invoicing", pts=5, made="06-15 09:50", sprint="Sprint 1",
         moves=[("06-16 11:00", "Ready"), ("06-22 09:50", "In progress"),
                ("06-24 16:10", "In review"), ("06-25 09:30", "In progress"),
                ("06-25 16:40", "In review"), ("06-26 10:30", "QA", "priya"),
                ("06-26 15:20", "Done", "mateo")],
         why="A marina's season is sold on invoices, and the sprint goal is only met when one "
             "comes out of a booking without anybody retyping it. The invoice carries the boat, "
             "the berth, the nights and the rate that applied on the day it was booked, because "
             "a rate that changes in August must not change what June already agreed.",
         ok=["Confirming a booking produces an invoice with the nights and the rate on it",
             "The rate on the invoice is the one that applied on the day of booking",
             "The invoice number is unique and never reused"],
         says=[("06-25 09:25", "priya",
                "Sending it back: the invoice takes today's rate rather than the rate on the day "
                "of booking, so every invoice we reissue after a price change is wrong by however "
                "much the price moved. The rest of it reads well.")]),
    dict(a="booking.hold", t="Hold a berth for twenty minutes while the guest pays", parent="booking",
         who="tomasz", labels="bookings,payments", pts=5, made="06-29 09:35", sprint="Sprint 2",
         moves=[("06-29 11:15", "Ready"), ("06-30 10:20", "In progress"),
                ("07-02 15:50", "In review"), ("07-03 10:40", "QA", "priya"),
                ("07-06 11:20", "Done", "mateo")],
         why="Between choosing a berth and the card clearing there is a minute or two in which "
             "the berth belongs to nobody, and on a Friday in July that is long enough for two "
             "people to buy it. A hold is a reservation with an expiry: the berth is off the "
             "market for twenty minutes, and comes back on its own if the payment never lands.",
         ok=["A held berth is not offered to anybody else while the hold lasts",
             "An unpaid hold expires on its own and the berth is free again",
             "A payment that lands after the hold expired is refunded, not silently kept"]),
    dict(a="booking.cancel", t="Cancel a booking and give the berth back", parent="booking",
         who="priya", labels="bookings", pts=3, made="06-29 09:40", sprint="Sprint 2",
         moves=[("06-30 11:30", "Ready"), ("07-06 09:50", "In progress"),
                ("07-08 16:00", "In review"), ("07-09 11:10", "QA", "tomasz"),
                ("07-09 16:30", "Done", "mateo")],
         why="Weather cancels more bookings than people do. The office needs one action that "
             "ends the booking, frees every night it held and leaves a record of who cancelled "
             "it and when — a berth quietly deleted is a berth nobody can explain in October.",
         ok=["Cancelling frees every night the booking held",
             "The cancelled booking is still readable, with who cancelled it and when",
             "The invoice for it is marked cancelled rather than deleted"]),
    dict(a="booking.season-rate", t="Price a season booking by the month, not by the night", parent="booking",
         who="tomasz", labels="bookings", tags=("customer/marina-vik",), pts=8,
         made="08-10 09:35", sprint="Sprint 5",
         moves=[("08-10 11:40", "Ready"), ("08-11 09:45", "In progress"),
                ("08-12 16:30", "In review")],
         why="A season berth is not two hundred nights at the nightly rate; it is five months at "
             "a monthly one, with the shoulder months cheaper than July. Vik Marina sells forty "
             "of them and has been doing the arithmetic in a spreadsheet since the vault opened.",
         ok=["A booking longer than a month is priced by the month",
             "The shoulder-month rate applies to April, May, September and October",
             "A season booking cut short is repriced rather than refunded night by night"],
         says=[("08-12 15:10", "tomasz",
                "Parked in review until we settle what happens when a season booking is cut "
                "short — repricing it monthly and refunding the difference is not the same "
                "number as refunding the unused nights, and Vik have asked for both.")]),
    dict(a="booking.group", t="Book a whole pontoon for a regatta", parent="booking",
         who="ingrid", labels="bookings", tags=("customer/marina-vik",),
         made="07-20 11:30", moves=[("07-21 10:15", "Ready")],
         why="Three marinas have now asked the same thing: a club takes a whole finger pier for "
             "a weekend, pays once, and hands us a boat list on the Thursday. Today that is "
             "fourteen separate bookings and one very patient harbour master.",
         ok=["A group booking holds a named set of berths for one range of dates",
             "The boat list can arrive after the berths are held",
             "One invoice covers the whole group"]),
    dict(a="booking.waitlist", t="Keep a waiting list for a week that is full", parent="booking",
         who="ingrid", labels="bookings", made="07-22 10:40",
         moves=[("08-04 11:20", "Cancelled")],
         why="When a week is full the office writes names on a pad and rings them if somebody "
             "cancels. The pad works; what it cannot do is tell the next person on it that the "
             "berth went half an hour ago.",
         ok=["A guest can be put on the list for a week that is full",
             "A cancellation offers the berth to the first name on the list"],
         says=[("08-04 11:10", "ingrid",
                "Cancelling this: it is the regatta story wearing a different hat. Both are "
                "'hold a berth for somebody who is not paying yet', and building two of those "
                "gives us two sets of expiry rules to argue about. The regatta story keeps the "
                "waiting list in its acceptance instead.")]),
    dict(a="booking.import-berths", t="Import the marina's berth list from a spreadsheet",
         type="task", parent="booking", who="ola", by="ola", labels="bookings", pts=3,
         made="06-15 10:10", sprint="Sprint 1",
         moves=[("06-16 09:30", "Ready"), ("06-17 13:40", "In progress"),
                ("06-18 11:20", "In review"), ("06-19 09:50", "QA", "tomasz"),
                ("06-19 15:10", "Done", "mateo")],
         why="Every marina we have spoken to keeps its berths in a spreadsheet with a column "
             "nobody can explain. Nothing else can be demonstrated until Harbor holds a real "
             "marina's forty-one berths with their real lengths, depths and power sockets.",
         ok=["A marina's spreadsheet becomes berths with length, depth and power",
             "A row that cannot be read stops the import and says which row"]),
    dict(a="booking.double-book", t="Two guests can hold the same berth if they click at the same second",
         type="bug", parent="booking", who="tomasz", priority="high", labels="bookings",
         tags=("regress",), pts=3, made="07-01 14:20", sprint="Sprint 2",
         moves=[("07-01 15:00", "Ready"), ("07-02 09:40", "In progress"),
                ("07-03 15:30", "In review"), ("07-06 10:15", "QA", "priya"),
                ("07-07 11:40", "Done", "mateo")],
         why="Two browsers, same berth, same week, confirm within the same second: both holds "
             "are created and both guests are told the berth is theirs. The availability check "
             "and the write are two separate reads of the same table with nothing between them.",
         ok=["Two simultaneous holds on one berth leave exactly one winner",
             "The loser is told the berth went, not shown an error page"],
         says=[("07-01 14:30", "mateo",
                "Reproduced eight times out of ten with two tabs and a stopwatch: berth A12, "
                "week of 10 August, both confirmations say 'held for you'. The second hold "
                "overwrites the first rather than being refused, so the first guest keeps a "
                "confirmation for a berth they do not have.")]),
]

# --- berth calendar --------------------------------------------------------------------

CALENDAR = [
    dict(a="calendar.month", t="A month of every berth on one screen", parent="calendar",
         who="priya", labels="bookings", made="06-29 09:50", sprint=["Sprint 2", "Sprint 3"],
         moves=[("06-30 09:40", "Ready"), ("07-01 10:30", "In progress"),
                ("07-14 16:20", "In review"), ("07-15 09:40", "In progress"),
                ("07-16 15:50", "In review"), ("07-17 10:20", "QA", "tomasz"),
                ("07-17 16:10", "Done", "mateo")],
         why="This is the wall planner. Berths down the side, days across the top, one cell per "
             "berth-night, and it has to be legible from the other side of the harbour office. "
             "It is also the screen the office will keep open all day, which makes how it "
             "scrolls a feature rather than a detail.",
         ok=["Every berth and every day of a month fit on one screen",
             "A booking reads as one bar across the nights it holds",
             "Scrolling a month of forty berths does not stutter"],
         says=[("07-15 09:30", "tomasz",
                "Back to you: it is lovely on forty berths and unusable on four hundred, and "
                "Sandholm have four hundred and six. The month query returns every cell rather "
                "than every booking, so the payload grows with the marina.")]),
    dict(a="calendar.month.1", t="Draw the month grid from the berth list", type="subtask",
         parent="calendar.month", who="priya", pts=5, made="06-30 10:10",
         moves=[("06-30 11:00", "Ready"), ("07-01 10:35", "In progress"),
                ("07-07 15:20", "In review"), ("07-08 10:10", "QA", "tomasz"),
                ("07-08 16:20", "Done", "mateo")],
         why="The grid itself: berths in the order the pontoons run, days across, and the "
             "weekend columns shaded so the eye finds Saturday without counting."),
    dict(a="calendar.month.2", t="Ask for the bookings, not for every cell", type="subtask",
         parent="calendar.month", who="priya", pts=3, made="07-06 11:20",
         moves=[("07-06 14:30", "Ready"), ("07-15 09:45", "In progress"),
                ("07-16 11:20", "In review"), ("07-16 14:40", "QA", "tomasz"),
                ("07-16 15:20", "Done", "mateo")],
         why="A month of four hundred berths is twelve thousand cells and about ninety "
             "bookings. Asking for the ninety and drawing the rest is the whole fix."),
    dict(a="calendar.drag", t="Drag a booking to another berth", parent="calendar",
         who="priya", labels="bookings", tags=("needs-design",), pts=5,
         made="07-13 09:35", sprint="Sprint 3",
         moves=[("07-13 11:20", "Ready"), ("07-20 09:45", "In progress"),
                ("07-22 16:10", "In review"), ("07-23 10:30", "QA", "tomasz"),
                ("07-23 16:40", "Done", "mateo")],
         why="Boats get moved. A yacht arrives with a bent fin, the berth beside the fuel dock "
             "is needed for a delivery, and the harbour master rearranges half a pontoon in the "
             "ten minutes before lunch. Retyping a booking to move it is why the wall planner "
             "is still on the wall.",
         ok=["A booking can be dragged to another berth and keeps its dates",
             "A drag onto an occupied berth is refused before it is dropped",
             "The move is in the booking's history with who moved it"]),
    dict(a="calendar.filters", t="Filter the calendar by boat length and shore power", parent="calendar",
         who="priya", labels="bookings", pts=3, made="08-24 09:50", sprint="Sprint 6",
         moves=[("08-24 11:30", "Ready"), ("08-26 10:10", "In progress"),
                ("09-02 16:20", "In review")],
         why="A harbour master looking for somewhere to put a fifteen-metre boat with a shore "
             "power lead does not want the whole marina, they want the eleven berths that could "
             "take it. The calendar already knows both facts about every berth.",
         ok=["The calendar can be narrowed to berths that fit a given length",
             "Berths without shore power can be hidden",
             "The filter survives a page reload, because it is how somebody works all morning"]),
    dict(a="calendar.print", t="Print the week for the harbour office wall", parent="calendar",
         who="priya", labels="bookings", made="08-05 15:30", moves=[("08-06 10:20", "Ready")],
         why="Two of the three marinas we sat with print the week on Monday morning and pin it "
             "up, because the pontoon has no screen and the dockhands do not carry laptops. The "
             "browser's own print of the calendar comes out as four illegible pages.",
         ok=["A week prints on one sheet of A4, landscape",
             "The printed sheet says which day it was printed"]),
    dict(a="calendar.colours", t="Colour a berth by what it is waiting for", parent="calendar",
         who="priya", labels="bookings", tags=("needs-design",), made="08-11 14:50",
         moves=[("08-12 10:10", "Ready")],
         why="The office wants to see, without clicking, which berths are held but unpaid, "
             "which are paid and unarrived, and which hold a boat that should have left "
             "yesterday. That is three states and one colour scale, and getting it wrong makes "
             "the calendar harder to read rather than easier.",
         ok=["Held-unpaid, paid-unarrived and overstayed are visible without clicking",
             "The scheme is legible to somebody who cannot tell red from green"]),
    dict(a="calendar.cache", t="Cache the month query so the calendar opens in under a second",
         type="task", parent="calendar", who="tomasz", by="tomasz", tags=("area/api",), pts=3,
         made="07-13 10:20", sprint="Sprint 3",
         moves=[("07-14 09:40", "Ready"), ("07-15 10:50", "In progress"),
                ("07-17 15:40", "In review"), ("07-20 10:20", "QA", "priya"),
                ("07-21 11:30", "Done", "mateo")],
         why="The month query is the one request the office makes forty times a day, and on a "
             "four-hundred-berth marina it takes two and a half seconds. Bookings change rarely "
             "enough that the answer can be kept until one does.",
         ok=["A month opens in under a second on a four-hundred-berth marina",
             "A new or moved booking invalidates the month it touches"]),
    dict(a="calendar.left-yesterday",
         t="Berth calendar shows a boat that left yesterday as still moored",
         type="bug", parent="calendar", who="tomasz", priority="high", labels="bookings",
         tags=("regress",), pts=2, made="07-16 11:40", sprint="Sprint 3",
         moves=[("07-16 14:20", "Ready"), ("07-21 09:50", "In progress"),
                ("07-22 15:20", "In review"), ("07-23 09:40", "QA", "priya"),
                ("07-24 10:50", "Done", "mateo")],
         why="A booking that ended yesterday is still drawn as occupying its berth today, so "
             "the office turns boats away from berths that are empty. The calendar compares the "
             "booking's last night with today rather than with the morning after it.",
         ok=["A booking that ended yesterday leaves its berth free today",
             "A booking that ends today still shows the boat as moored until the morning"],
         says=[("07-16 11:50", "mateo",
                "Sandholm rang about this one: pontoon C looked full on Tuesday and had four "
                "empty slips on it. Every booking whose last night was Monday was still drawn "
                "on Tuesday. It is an off-by-one on the last night, not a caching problem — it "
                "survives a hard reload."),
               ("07-22 15:10", "tomasz",
                "The check was `last_night >= today` where it wants `last_night >= today` on "
                "the checkout morning only. Fixed by asking the booking when the berth is free "
                "rather than when the guest leaves, which are a night apart on purpose.")]),
    dict(a="calendar.dst", t="A booking made the night the clocks change is a day short",
         type="bug", parent="calendar", who="tomasz", priority="normal", pts=2,
         made="08-25 11:30", sprint="Sprint 6",
         moves=[("08-25 14:10", "Ready"), ("08-27 10:20", "In progress"),
                ("09-01 16:00", "In review"), ("09-03 10:40", "QA", "priya")],
         why="Nights are counted by subtracting two timestamps and dividing by twenty-four "
             "hours, which is right for every night of the year except the two the clocks "
             "change on. A week over the October change is billed as six nights.",
         ok=["A range over a clock change counts the nights a calendar would count",
             "The invoice for such a range charges for every night the boat was there"],
         says=[("08-25 11:40", "mateo",
                "Found it on purpose rather than in the wild: booked 24 to 31 October at Vik "
                "and got six nights and six nights' money. It will be real in eight weeks, so "
                "it is worth doing now while nobody has been overcharged.")]),
]

# --- card payments ---------------------------------------------------------------------

PAYMENTS = [
    dict(a="payments.capture", t="Take the card payment when a booking is confirmed", parent="payments",
         who="tomasz", labels="payments", made="06-29 10:00", sprint="Sprint 2",
         moves=[("06-29 11:50", "Ready"), ("07-01 09:50", "In progress"),
                ("07-07 16:30", "In review"), ("07-08 11:20", "QA", "priya"),
                ("07-09 09:40", "In progress", "mateo"), ("07-10 15:40", "In review"),
                ("07-13 10:10", "QA", "priya"), ("07-13 16:20", "Done", "mateo")],
         why="The sprint goal in one story: a guest confirms a booking, a card is charged, and "
             "the booking is only confirmed if the charge was. Everything awkward about "
             "payments — the redirect, the retry, the reference the accountant needs — is a "
             "child of this one.",
         ok=["Confirming a booking charges the card once and only on success",
             "A failed charge leaves the berth free and tells the guest why",
             "The provider's payment reference is on the booking afterwards"],
         says=[("07-09 09:30", "mateo",
                "Failing it in QA. Card declined on a real sandbox card leaves the booking in "
                "'confirmed' with no payment on it — the failure path rolls back the charge and "
                "not the booking, so the berth is held for a guest who never paid. The happy "
                "path is fine and the redirect works on a phone.")]),
    dict(a="payments.capture.1", t="Set up the payment provider's sandbox account", type="subtask",
         parent="payments.capture", who="tomasz", pts=1, made="06-29 11:00",
         moves=[("06-30 09:50", "Ready"), ("06-30 14:20", "In progress"),
                ("07-01 16:10", "In review"), ("07-02 09:50", "QA", "priya"),
                ("07-02 15:30", "Done", "mateo")],
         why="Test cards, a webhook endpoint that reaches a laptop, and a second account so QA "
             "is not sharing a transaction list with whoever is developing."),
    dict(a="payments.capture.2", t="Carry the 3-D Secure redirect back to the booking", type="subtask",
         parent="payments.capture", who="tomasz", pts=5, made="06-29 11:05",
         moves=[("07-01 09:55", "Ready"), ("07-02 10:30", "In progress"),
                ("07-06 16:10", "In review"), ("07-07 10:20", "QA", "priya"),
                ("07-07 15:10", "Done", "mateo")],
         why="The bank sends the guest away to its own page and back again, and whatever we "
             "were holding in memory is gone by the time they return. The booking has to be "
             "findable from the redirect alone, on a phone that may have changed network."),
    dict(a="payments.capture.3", t="Store the provider's payment reference on the booking",
         type="subtask", parent="payments.capture", who="tomasz", pts=2, made="07-02 10:20",
         moves=[("07-02 14:10", "Ready"), ("07-08 09:50", "In progress"),
                ("07-09 15:50", "In review"), ("07-10 09:40", "QA", "priya"),
                ("07-10 11:40", "Done", "mateo")],
         why="Without the provider's own reference on the booking, matching a charge to a berth "
             "means reading two lists side by side, which is what the marina's bookkeeper does "
             "today and what Harbor is supposed to stop."),
    dict(a="payments.webhook", t="Reconcile the provider's webhook with the booking", parent="payments",
         who="tomasz", labels="payments", tags=("area/api",), pts=5,
         made="07-13 09:45", sprint="Sprint 3",
         moves=[("07-14 10:10", "Ready"), ("07-16 09:50", "In progress"),
                ("07-21 16:20", "In review"), ("07-22 10:20", "QA", "priya"),
                ("07-22 16:10", "Done", "mateo")],
         why="The provider tells us what happened twice: once as the answer to our request and "
             "once, minutes or hours later, as a webhook. When those two disagree the webhook "
             "is right, and today nothing is listening to it.",
         ok=["A webhook the provider sends twice is applied once",
             "A charge the webhook reports and the booking does not know about raises an alert",
             "A webhook for a booking that no longer exists is kept, not dropped"]),
    dict(a="payments.refunds", t="Refund a cancelled booking to the card it came from", parent="payments",
         who="tomasz", labels="payments", pts=8, made="08-24 10:00", sprint="Sprint 6",
         moves=[("08-24 11:50", "Ready"), ("08-27 09:50", "In progress")],
         ticks="09-02 15:30", ticked=1,
         why="Cancelling gives the berth back; it does not give the money back. Today the "
             "harbour office refunds by hand in the provider's own dashboard and writes the "
             "reference on a sticky note. A refund has to be a thing Harbor did, with a reason "
             "on it, and it has to become a credit note on the accounting side.",
         ok=["A cancelled booking can be refunded to the card that paid for it",
             "A refund carries a reason and who authorised it",
             "The refund appears on the accounting side as a credit note, not as a negative invoice"],
         says=[("08-25 11:00", "ingrid",
                "Holding the last acceptance box until credit notes land on the Ledgerline side "
                "— we agreed a refund is a credit note rather than an invoice with a minus in "
                "front of it, and doing half of that now would mean doing all of it twice.")]),
    dict(a="payments.receipt", t="Email a receipt the marina's accountant will accept", parent="payments",
         who="priya", labels="payments,invoicing", pts=3, made="08-24 10:05", sprint="Sprint 6",
         moves=[("08-25 09:40", "Ready"), ("08-26 09:50", "In progress"),
                ("08-31 16:20", "In review"), ("09-02 10:30", "QA", "tomasz")],
         why="The confirmation email is written for a guest and the accountant needs a "
             "document: the marina's registered name and number, the tax lines separated out, "
             "and the same invoice number the booking carries.",
         ok=["The receipt carries the marina's registered details and the invoice number",
             "Tax is shown as its own line rather than folded into the total",
             "The receipt can be re-sent without producing a second invoice number"]),
    dict(a="payments.deposit", t="Take a deposit now and the rest on arrival", parent="payments",
         who="tomasz", labels="payments", made="08-18 15:10", moves=[("08-19 10:20", "Ready")],
         why="Season berths are sold on a deposit in February and the balance in May, and "
             "Harbor can only charge all of it at once. Every marina we have shown it to has "
             "asked the same question within ten minutes.",
         ok=["A booking can be paid in two agreed instalments",
             "The balance is charged to the same card without asking for it again",
             "An unpaid balance is visible on the calendar before the boat arrives"]),
    dict(a="payments.provider-keys", t="Move the payment provider's keys out of the repository",
         type="task", parent="payments", who="ola", by="ola", priority="high",
         tags=("area/api",), pts=2, made="06-30 15:40", sprint="Sprint 2",
         moves=[("07-01 09:30", "Ready"), ("07-02 14:10", "In progress"),
                ("07-03 11:20", "In review"), ("07-06 09:40", "QA", "tomasz"),
                ("07-06 15:50", "Done", "mateo")],
         why="The sandbox keys went in with the first payment commit and the live ones would "
             "have followed. They belong in the deployment's own secret store, and the old ones "
             "have to be rotated because a key that has been in a repository is a key that is "
             "public.",
         ok=["No provider key is in the repository or its history going forward",
             "The sandbox keys that were committed are rotated"]),
    dict(a="payments.double-charge", t="A retried confirmation charges the card twice",
         type="bug", parent="payments", who="tomasz", priority="critical", labels="payments",
         tags=("area/api",), pts=3, made="07-08 11:20", sprint="Sprint 3",
         moves=[("07-08 11:50", "Ready"), ("07-08 13:40", "In progress"),
                ("07-09 15:20", "In review"), ("07-10 09:50", "QA", "priya"),
                ("07-10 16:20", "Done", "mateo")],
         why="A guest whose confirmation is slow presses the button again, and the second press "
             "makes a second charge for the same booking. Three marinas have refunded a guest "
             "this week. The confirmation is not idempotent: nothing on our side says these two "
             "requests are the same intention.",
         ok=["Confirming the same booking twice charges the card once",
             "A duplicate confirmation returns the first charge rather than a new one",
             "The three known double charges are refunded and listed here"],
         says=[("07-08 11:30", "mateo",
                "Three reports this morning, all within twenty minutes of each other: Vik, "
                "Sandholm and the small marina at Bergen. Same shape each time — slow "
                "confirmation, guest presses again, two charges and one booking. I can "
                "reproduce it by throttling the connection to 3G."),
               ("07-09 15:10", "tomasz",
                "Fixed by giving the confirmation an idempotency key derived from the booking "
                "and the guest's attempt, which the provider then honours on its side too. The "
                "three charges are refunded; references are on the incident.")]),
    dict(a="payments.refund-over", t="A refund larger than the invoice total is accepted",
         type="bug", parent="payments", who="tomasz", priority="high", labels="payments",
         pts=3, made="08-28 11:10", sprint="Sprint 6",
         moves=[("08-28 14:20", "Ready"), ("09-01 10:10", "In progress"),
                ("09-03 16:20", "In review")],
         why="The refund endpoint checks that the booking was paid and not how much it was paid. "
             "A refund of four hundred against an invoice of ninety is accepted and sent to the "
             "provider, which happily sends the money.",
         ok=["A refund larger than what is left on the invoice is refused",
             "Several partial refunds cannot add up to more than the invoice"],
         says=[("08-28 11:20", "mateo",
                "Found by the payments scenarios rather than by a marina, thankfully: "
                "HARBOR-PAY-004 refunds 400 against an invoice for 90 and passes. Nobody has "
                "done it in the wild because the number is typed by us and not by a guest, but "
                "it will be typed by a harbour master the moment refunds ship."),
               ("09-04 10:20", "tomasz",
                "Marking this as blocking the refunds story rather than the other way round: "
                "refunds can carry on being built, it must not ship while this is open. The "
                "refunds card deliberately does not say it is blocked — it is not waiting on "
                "anybody, it is being written.")]),
]

# --- mobile check-in ---------------------------------------------------------------------

CHECKIN = [
    dict(a="checkin.pontoon", t="Check a guest in from the pontoon with no signal", parent="checkin",
         who="aiko", labels="mobile", made="07-27 09:40", sprint=["Sprint 4", "Sprint 5"],
         moves=[("07-27 11:20", "Ready"), ("07-28 09:50", "In progress"),
                ("08-11 16:10", "In review"), ("08-12 10:20", "QA", "tomasz"),
                ("08-13 11:30", "Done", "mateo")],
         why="The dockhand meeting the boat has a phone, a wet hand and one bar of signal that "
             "comes and goes behind the fuel dock. Check-in has to complete on the pontoon and "
             "reconcile later — an app that needs a connection at the moment the boat arrives is "
             "an app the marina will stop opening.",
         ok=["A check-in completes with the phone in flight mode",
             "The office sees it within a minute of the phone reconnecting",
             "Two dockhands checking in the same boat produce one check-in, not two"]),
    dict(a="checkin.pontoon.1", t="Queue a check-in while the phone has no signal", type="subtask",
         parent="checkin.pontoon", who="aiko", pts=5, made="07-28 10:10",
         moves=[("07-28 11:40", "Ready"), ("07-29 09:50", "In progress"),
                ("08-05 16:20", "In review"), ("08-06 10:10", "QA", "tomasz"),
                ("08-06 15:20", "Done", "mateo")],
         why="The check-in is written to the phone first and sent second, so the dockhand's "
             "screen never waits on a network that is not there."),
    dict(a="checkin.pontoon.2", t="Flush the queue when the phone comes back", type="subtask",
         parent="checkin.pontoon", who="aiko", pts=3, made="07-28 10:15",
         moves=[("07-29 10:20", "Ready"), ("08-06 09:50", "In progress"),
                ("08-10 16:10", "In review"), ("08-11 10:20", "QA", "tomasz"),
                ("08-11 15:40", "Done", "mateo")],
         why="Sending what the phone kept, in the order it was written, and being able to send "
             "the same check-in twice without the office seeing two boats."),
    dict(a="checkin.qr", t="Scan the berth's QR code to open the right booking", parent="checkin",
         who="aiko", labels="mobile", pts=5, made="08-10 09:40", sprint="Sprint 5",
         moves=[("08-10 11:30", "Ready"), ("08-12 09:50", "In progress"),
                ("08-17 16:20", "In review"), ("08-18 10:30", "QA", "tomasz"),
                ("08-18 16:10", "Done", "mateo")],
         why="Finding the right booking on a phone in the rain means scrolling a list of "
             "forty-one berths. A weatherproof sticker on the pontoon cleat with the berth's "
             "code on it turns that into pointing a camera at it.",
         ok=["Scanning a berth's code opens today's booking for that berth",
             "Scanning a berth with no booking offers to check a walk-in in",
             "The scan works offline, from the berth list the phone already has"]),
    dict(a="checkin.photo", t="Photograph the boat's papers at check-in", parent="checkin",
         who="aiko", labels="mobile", tags=("customer/marina-vik",), pts=3,
         made="08-10 09:45", sprint="Sprint 5",
         moves=[("08-11 10:20", "Ready"), ("08-13 09:50", "In progress"),
                ("08-18 15:40", "In review"), ("08-19 10:20", "QA", "tomasz"),
                ("08-19 16:30", "Done", "mateo")],
         why="Insurance and registration are checked on arrival and written on a paper form "
             "that lives in a drawer. A photograph attached to the booking is the same evidence, "
             "findable in October when somebody asks whether the boat was insured in July.",
         ok=["A photograph taken at check-in is attached to the booking",
             "Photographs taken offline are uploaded when the phone reconnects",
             "The office can see the photograph without downloading anything"]),
    dict(a="checkin.kiosk", t="A kiosk in the harbour office for guests who arrive after hours",
         parent="checkin", who="ingrid", labels="mobile", made="07-30 11:10",
         moves=[("08-04 10:10", "Ready"), ("08-14 11:40", "Cancelled")],
         why="Boats arrive at eleven at night and the office is shut. Sandholm asked for a "
             "screen by the door that checks a guest in and prints the gate code.",
         ok=["A guest arriving out of hours can check themselves in",
             "The kiosk works when the office network is down"],
         says=[("08-14 11:30", "ingrid",
                "Cancelling. This is the same job as the QR sticker: Sandholm asked for a screen "
                "by the door and Vik asked for a sticker on the cleat, and both mean 'let the "
                "guest check themselves in against a berth'. The sticker shipped this week and "
                "costs nothing to weatherproof; a kiosk is a device we would have to own. "
                "Sandholm have seen the sticker and are happy.")]),
    dict(a="checkin.testflight", t="Get the check-in build onto the marina's own phones",
         type="task", parent="checkin", who="ola", by="ola", pts=2,
         made="08-10 10:10", sprint="Sprint 5",
         moves=[("08-11 09:40", "Ready"), ("08-14 10:20", "In progress"),
                ("08-17 11:10", "In review"), ("08-18 09:50", "QA", "aiko"),
                ("08-19 11:20", "Done", "mateo")],
         why="The launch is on a pontoon at Vik with two dockhands' own phones, one of which is "
             "four years old. Getting a build onto them is a week of provisioning and store "
             "review if it is left to the Friday.",
         ok=["Both dockhands' phones are running the check-in build before the launch weekend",
             "A new build reaches those phones the same day it is cut"]),
    dict(a="checkin.clock-skew", t="A check-in made offline arrives with the phone's wrong clock",
         type="bug", parent="checkin", who="aiko", priority="high", labels="mobile",
         tags=("regress",), pts=2, made="08-13 14:20", sprint="Sprint 5",
         moves=[("08-13 15:00", "Ready"), ("08-17 09:50", "In progress"),
                ("08-19 15:20", "In review"), ("08-20 10:10", "QA", "tomasz"),
                ("08-20 15:40", "Done", "mateo")],
         why="A queued check-in carries the time the phone thought it was, and the older test "
             "phone is eleven minutes fast. The office sees arrivals in the wrong order and, "
             "twice, in the future.",
         ok=["A check-in is stamped with a time the server can trust",
             "The phone's own idea of the time is kept too, for when they disagree"],
         says=[("08-13 14:30", "mateo",
                "Two check-ins on the old phone arrived stamped eleven minutes ahead of the "
                "clock on the wall, which put them above the ones made after them. It is the "
                "device clock, not the queue order — the queue is fine.")]),
]

# --- ops, and one thing that fell out of the plan ------------------------------------------

OPS = [
    dict(a="ops.season-runbook", t="Write the runbook for the season launch weekend",
         type="task", who="ola", by="ola", made="08-24 10:20", sprint="Sprint 6",
         moves=[("08-24 11:20", "Ready"), ("08-25 10:40", "In progress")],
         ticks="09-01 15:20", ticked=1,
         why="Two marinas go live over one weekend and the person who knows how any of it is "
             "deployed is on a boat with no signal. The runbook is who to ring, what to look "
             "at, and how to put it back — written down rather than remembered.",
         ok=["Somebody who has never deployed Harbor can follow it end to end",
             "It says how to restore the booking database and how long that takes",
             "It says who is on call and how the marina reaches them"]),
    dict(a="ops.season-runbook.1", t="Write down who is on call over the launch weekend",
         type="subtask", parent="ops.season-runbook", who="ola", made="08-24 11:00",
         moves=[("08-25 09:40", "Ready"), ("08-26 10:10", "In progress")],
         why="Two names per day, a phone number each, and what to do when neither answers."),
    dict(a="ops.season-runbook.2", t="Rehearse restoring the booking database from a backup",
         type="subtask", parent="ops.season-runbook", who="ola", made="08-24 11:05",
         moves=[("08-26 09:50", "Ready"), ("08-28 10:20", "In progress")],
         why="A backup nobody has restored is a file, not a backup. Doing it once with a "
             "stopwatch is the only way the runbook can say how long it takes."),
    dict(a="ops.season-runbook.3", t="Write down how the marina reaches us out of hours",
         type="subtask", parent="ops.season-runbook", who="ola", made="08-24 11:10",
         why="The harbour master has a mobile number for whoever was standing nearest in June. "
             "One number, one inbox, and a sentence about what counts as out of hours."),
    dict(a="loose.receipt-footer", t="Change the marina's address in the footer of the receipt email",
         type="task", by="ingrid", made="08-21 15:40",
         why="Vik moved office in the spring and the footer of the receipt email still has the "
             "old address on it. Nobody has complained; it is simply wrong.",
         ok=["The receipt footer carries the address the marina gives us",
             "The address is a marina setting rather than a line in a template"]),
]

WORK = EPICS + BOOKING + CALENDAR + PAYMENTS + CHECKIN + OPS

ALIASES: dict[str, str] = {PREFIX + spec["a"]: spec["t"] for spec in WORK}

# Relations, both sides written unless the story means them to disagree. `relate` events
# are dated after both tasks exist; the engine resolves aliases to keys when it runs.
RELATIONS = [
    ("07-16 11:00", "priya", "calendar.drag", dict(blocked_by=["calendar.month"])),
    ("07-16 11:01", "priya", "calendar.month", dict(blocks=["calendar.drag"])),
    ("07-28 11:30", "mateo", "calendar.left-yesterday", dict(relates=["checkin.pontoon"])),
    ("08-04 11:15", "ingrid", "booking.waitlist", dict(duplicates=["booking.group"])),
    ("08-04 11:16", "ingrid", "booking.group", dict(duplicated_by=["booking.waitlist"])),
    ("08-11 10:40", "aiko", "checkin.qr", dict(blocked_by=["checkin.pontoon"])),
    ("08-11 10:41", "aiko", "checkin.pontoon", dict(blocks=["checkin.qr"])),
    ("08-14 11:35", "ingrid", "checkin.kiosk", dict(duplicates=["checkin.qr"])),
    ("08-14 11:36", "ingrid", "checkin.qr", dict(duplicated_by=["checkin.kiosk"])),
    ("08-31 11:30", "priya", "payments.receipt", dict(relates=["booking.invoice"])),
    # The planted one-sided relation: the bug says it blocks the refunds story and the
    # refunds story does not say it is blocked. See the comment on the bug for why.
    ("09-04 10:15", "tomasz", "payments.refund-over", dict(blocks=["payments.refunds"])),
]

# Ledgerline's credit-notes story is created on 2026-07-14 10:00 by ledgerline.py, so both
# of these are dated well after it. SHOWCASE_NO_LEDGER=1 drops them, which is how Harbor is
# replayed on its own — `build.py --only people,labels,sprints,harbor` passes nothing and
# gets the default, because by then Ledgerline exists.
LEDGER_RELATIONS = [
    ("08-25 11:20", "tomasz", "payments.refunds", dict(blocked_by=["ledger.invoices.credit-notes"])),
    ("08-25 11:21", "tomasz", "ledger.invoices.credit-notes", dict(blocks=["payments.refunds"])),
]


def _relation_events(pairs):
    events = []
    for moment, who, alias, relations in pairs:
        named = {name: [_full(value) for value in values] for name, values in relations.items()}
        events.append(common.relate(moment, who, _full(alias), **named))
    return events


def _full(alias: str) -> str:
    """Harbor's own aliases are written here without their prefix; anybody else's whole."""
    return PREFIX + alias if PREFIX + alias in ALIASES else alias


def events(with_ledger: bool = True) -> list[story.Event]:
    if os.environ.get("SHOWCASE_NO_LEDGER"):
        with_ledger = False
    common.leaves_only(WORK, PREFIX)
    out = []
    for index, spec in enumerate(WORK):
        out += common.lifecycle(spec, PROJECT, PREFIX, index)
    out += _relation_events(RELATIONS)
    if with_ledger:
        out += _relation_events(LEDGER_RELATIONS)
    return out
