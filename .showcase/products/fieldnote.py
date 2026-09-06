"""Fieldnote: twelve weeks of scheduling for people who work out of a van.

Three epics between 15 June and 4 September 2026 — job scheduling, route planning and
the offline mobile app — and the thirty-four pieces of work under them. The customer is
Nordic Field Services, a heating contractor in Tromsø with four crews, an office that
still rings them to find out where they are, and a service area that includes two
tunnels, a fjord crossing and a mountain road where nobody has had a signal since the
road was built.

The shape of the twelve weeks, read off the sprint goals:

  * Sprint 1 is Harbor's, and Fieldnote is three epic pages and nothing else.
  * Sprint 2 is the first real fortnight: a crew can see its day, the dispatcher can put
    a job on a crew, and the job list arrives from the customer's old scheduler.
  * Sprint 3 is route planning — the stop order, the travel time between two stops, and
    the four zones Nordic Field actually work in.
  * Sprint 4 is Fieldnote's own goal, "Fieldnote works a whole day offline", and it is
    the fortnight this file is really about. On Wednesday 29 July the merge took the
    server's version of a job whenever the two disagreed, and eleven crews lost the work
    they had done in a dead zone. `field.offline.sync-loss` is that afternoon.
  * Sprint 5 is Harbor's season launch; Fieldnote carries on quietly underneath it.
  * Sprint 6 is "tax periods, and the sync fix under load", and the sync half of that
    goal is `field.offline.sync-fix-load`, still in progress on the day the vault is read.

Nothing here plants an anomaly — Harbor owns all three of those, and a second `only-owner`
or a second one-sided relation arriving by accident would make the demonstration a lie.
So every parent with three or more open children has them on more than one person, every
`blocks` written here is written from both ends, and every card has a parent.

What this file does carry is the overload: aiko is the whole of the crew app, and on
4 September she is holding seven open cards with five of them sized while everybody else
in Fieldnote is holding three or fewer. That is not a mistake in the data — it is what
the workload page exists to show.

One relation reaches out of the project: `field.offline.sync-loss` relates Harbor's
`harbor.checkin.pontoon`, because the queued check-in on the pontoon is the same
merge with a different noun in front of it. `relates` has no inverse, so it is written
once, from this side, the day after the incident.
"""
from __future__ import annotations

import story

from . import common

PROJECT = "FIELD"
PREFIX = "field."

# --- the epics ------------------------------------------------------------------------

EPICS = [
    dict(a="jobs", t="Job scheduling", type="epic", who="ingrid", made="06-15 09:37",
         moves=[("06-15 12:00", "Ready"), ("06-29 09:20", "In progress")],
         ticks="07-24 15:30", ticked=2,
         why="A heating contractor's day is a whiteboard in the office and four phone calls to "
             "find out whether it is still true. Everything under this epic replaces the "
             "whiteboard: a job has a customer, an address, a crew and a time, the crew sees "
             "the same day the office sees, and moving a job is one action rather than four "
             "conversations.",
         ok=["A crew opens the app and sees the day it is actually going to have",
             "The office can put a job on a crew and the crew knows within the minute",
             "A job carries what happened last time somebody went to that address"]),
    dict(a="routes", t="Route planning", type="epic", who="priya", made="06-15 09:38",
         moves=[("06-15 12:05", "Ready"), ("07-13 09:25", "In progress")],
         ticks="07-24 15:40", ticked=1,
         why="Nordic Field's four crews drive about nine hundred kilometres a week between them, "
             "and the order of the stops is decided at seven in the morning by whoever is holding "
             "the whiteboard pen. This epic is that decision made with the travel times in front "
             "of it, and remade when the day goes wrong — which it does, because a boiler that "
             "was going to take an hour takes three.",
         ok=["A crew's stops are ordered so the day is driveable, not just possible",
             "The travel time between two stops is the road's, not a line on a map",
             "A job that overruns moves the rest of the day rather than breaking it"]),
    dict(a="offline", t="Offline mobile", type="epic", who="aiko", made="06-15 09:39",
         moves=[("06-15 12:10", "Ready"), ("07-27 09:25", "In progress")],
         ticks="08-07 15:40", ticked=2,
         why="Half of Nordic Field's service area has no signal: two tunnels, the mountain road "
             "to the eastern valley, and most cellars. An app that needs a connection to show a "
             "crew what it is doing is an app the crews will stop opening by the second week. "
             "Everything under this epic is the phone being right on its own for a whole day and "
             "reconciling honestly when it comes back.",
         ok=["A crew phone holds the whole day — jobs, notes and photographs — with no signal",
             "What the crew did offline reaches the office when the phone finds a signal",
             "When the phone and the server disagree, nobody's work is quietly thrown away"]),
]

# --- job scheduling -------------------------------------------------------------------

JOBS = [
    dict(a="jobs.day", t="Show a crew the day's jobs in the order they are meant to happen",
         parent="jobs", who="aiko", labels="mobile", made="06-29 09:40", sprint="Sprint 2",
         moves=[("06-29 11:20", "Ready"), ("06-30 09:50", "In progress"),
                ("07-07 16:10", "In review"), ("07-08 10:20", "QA", "mateo"),
                ("07-08 15:40", "Done", "mateo")],
         why="This is the screen the crews will open thirty times a day and judge the whole "
             "product by. It is today, in order, with the address, the customer's name, what "
             "the job is and how long it is meant to take — and it opens on a cold phone in a "
             "van at half past six in the morning without asking anybody to log in again.",
         ok=["A crew sees today's jobs in the planned order, without choosing a date",
             "The screen opens from a cold start in under two seconds",
             "A job the office moves off the crew disappears from it"]),
    dict(a="jobs.day.1", t="Hold the day's jobs on the phone before the crew leaves the depot",
         type="subtask", parent="jobs.day", who="aiko", pts=3, made="06-30 10:10",
         moves=[("06-30 11:40", "Ready"), ("07-01 09:50", "In progress"),
                ("07-03 16:20", "In review"), ("07-06 10:10", "QA", "mateo"),
                ("07-06 15:20", "Done", "mateo")],
         why="The day is written to the phone the moment it is planned, so the screen is reading "
             "the phone rather than the network every time somebody opens it."),
    dict(a="jobs.day.2", t="Show what happened the last time somebody went to this address",
         type="subtask", parent="jobs.day", who="aiko", pts=2, made="06-30 10:15",
         moves=[("07-01 10:20", "Ready"), ("07-06 09:50", "In progress"),
                ("07-07 11:10", "In review"), ("07-07 14:20", "QA", "mateo"),
                ("07-08 09:40", "Done", "mateo")],
         why="Two lines from the last visit under the job: what was wrong, what was done, and "
             "which part was fitted, so nobody arrives asking a question the firm already knows "
             "the answer to."),
    dict(a="jobs.assign", t="Put a job on a crew from the dispatcher's board",
         parent="jobs", who="priya", labels="routing", pts=5, made="06-29 09:45", sprint="Sprint 2",
         moves=[("06-29 11:25", "Ready"), ("07-01 09:40", "In progress"),
                ("07-07 15:30", "In review"), ("07-08 10:40", "QA", "mateo"),
                ("07-09 11:20", "Done", "mateo")],
         why="The office side of the same sentence: four columns, one per crew, and an unplanned "
             "pile down the left that the dispatcher empties by dragging. It has to survive being "
             "used by one person while another is looking at it, because on a Monday morning both "
             "of Nordic Field's office staff are on the same board.",
         ok=["A job dragged onto a crew is on that crew's phone within the minute",
             "Two dispatchers moving different jobs do not overwrite each other",
             "A job put on a crew that is already full says so rather than accepting it"]),
    dict(a="jobs.import", t="Load Nordic Field's customers and jobs out of their old scheduler",
         type="task", parent="jobs", who="ola", by="ola", tags=("customer/nordic-field",),
         pts=3, made="06-29 10:10", sprint="Sprint 2",
         moves=[("06-30 09:35", "Ready"), ("07-02 10:20", "In progress"),
                ("07-03 11:40", "In review"), ("07-06 09:50", "QA", "mateo"),
                ("07-07 10:30", "Done", "mateo")],
         why="Eleven hundred customers and about four thousand past jobs, exported from a "
             "scheduler the firm has used since 2014, in a file where the address is one column "
             "and the flat number is sometimes in it and sometimes in the note. Nothing about "
             "the pilot works until this has been done once against the real file.",
         ok=["Every customer in the export exists in Fieldnote with an address that finds them",
             "Past jobs keep their dates, so the last-visit line has something to say",
             "Rows the importer could not read are listed rather than dropped"]),
    dict(a="jobs.slots-api", t="Publish the job and slot endpoints the dispatcher board reads",
         type="task", parent="jobs", who="tomasz", by="tomasz", tags=("area/api",), pts=3,
         made="06-29 10:15", sprint="Sprint 2",
         moves=[("06-30 09:45", "Ready"), ("07-01 10:10", "In progress"),
                ("07-06 16:20", "In review"), ("07-07 10:20", "QA", "priya"),
                ("07-07 15:50", "Done", "mateo")],
         why="The board, the phone and eventually the customer's own booking page all want the "
             "same three questions answered — what is on this crew today, what is unplanned, and "
             "is this slot free — and answering them three different ways is how the three "
             "screens come to disagree about the same day.",
         ok=["One endpoint answers a crew's day and one answers a day's unplanned work",
             "A slot that is taken is refused with the job that took it, not a bare error"]),
    dict(a="jobs.notes", t="A crew writes up the job from the van, before it drives off",
         parent="jobs", who="aiko", labels="mobile", pts=5, made="07-13 09:50", sprint="Sprint 3",
         moves=[("07-13 11:30", "Ready"), ("07-14 09:50", "In progress"),
                ("07-20 16:10", "In review"), ("07-21 10:20", "QA", "mateo"),
                ("07-22 09:40", "In progress", "mateo"), ("07-23 15:20", "In review"),
                ("07-24 10:10", "QA", "mateo"), ("07-24 15:30", "Done", "mateo")],
         why="A job that is written up in the evening is written up from memory, and a job that "
             "is written up next week is invented. The write-up happens in the van with the "
             "customer still in the doorway: what was wrong, what was done, what was fitted, and "
             "whether somebody has to come back.",
         ok=["A crew can finish a job with a note and a photograph in under a minute",
             "A job cannot be finished without saying whether a return visit is needed",
             "The write-up is kept if the app is closed halfway through it"],
         says=[("07-22 09:50", "mateo",
                "Sending this back. Finishing a job with the return-visit switch on produces a "
                "job that is closed and a return visit that exists nowhere — I did it four times "
                "and got four dead ends. The acceptance says the crew cannot finish without "
                "answering the question, and it is right; what it does not say is that answering "
                "it yes has to put something on somebody's board.")]),
    dict(a="jobs.overlap", t="Two jobs can be booked into the same crew's two o'clock",
         type="bug", parent="jobs", who="tomasz", priority="high", labels="routing", pts=3,
         made="07-15 14:20", sprint="Sprint 3",
         moves=[("07-15 15:10", "Ready"), ("07-16 09:50", "In progress"),
                ("07-17 16:20", "In review"), ("07-20 10:20", "QA", "mateo"),
                ("07-20 15:40", "Done", "mateo")],
         why="The board asks whether the slot is free and then writes the job, and between the "
             "two questions there is nothing stopping the other dispatcher doing the same. Two "
             "jobs at two o'clock is one crew, one van, and a customer who was promised an "
             "afternoon.",
         ok=["A slot that has been taken between the check and the write is refused",
             "The refusal names the job that took the slot so the dispatcher can move one"],
         says=[("07-15 14:30", "mateo",
                "Reproduced it in ten seconds with two browser windows, which means the office "
                "will find it on the first Monday. Both windows accept the drop and the board "
                "shows both jobs; refresh and they are still both there. The check and the write "
                "are two separate questions with a gap in the middle.")]),
    dict(a="jobs.recurring", t="A yearly service visit that plans itself twelve months ahead",
         parent="jobs", who="aiko", labels="routing", pts=8, made="08-24 09:50", sprint="Sprint 6",
         moves=[("08-25 11:20", "Ready")],
         why="Two thirds of Nordic Field's work is the annual service on a boiler they fitted, "
             "and today it is remembered by a spreadsheet that one person in the office keeps. "
             "A service that plans itself a year out is the difference between a contractor with "
             "a full calendar in February and one ringing people to ask for work.",
         ok=["Finishing a service visit plans the next one a year out, on the same crew if it can",
             "The office can see next year's planned services and move them in bulk",
             "A customer who cancels the contract stops generating them"]),
    dict(a="jobs.tomorrow", t="A job moved to tomorrow stays on today's list until the app restarts",
         type="bug", parent="jobs", who="aiko", priority="normal", labels="mobile",
         tags=("device/older-fleet",), pts=2, made="08-28 11:10", sprint="Sprint 6",
         moves=[("08-28 14:20", "Ready")],
         why="The phone is told the job has moved and removes it from the server's answer, but "
             "the list on the screen was built when the day was opened and nothing tells it to "
             "build itself again. The crew sees a job it is no longer going to, which on the "
             "older half of the fleet lasts until somebody closes the app properly.",
         ok=["A job moved off the crew leaves the day's list without a restart",
             "The same is true of a job moved onto the crew mid-morning"],
         says=[("08-28 11:20", "mateo",
                "Only on the older phones, and only when the day is left open — which is exactly "
                "what a crew does, because the phone sits in the cradle all day. The newer ones "
                "rebuild the list when the screen comes back on and hide it.")]),
    dict(a="jobs.window", t="Promise the customer a two-hour arrival window and keep it",
         parent="jobs", who="ingrid", labels="routing", made="08-26 11:20",
         why="Every customer asks the same question when the job is booked — when will they "
             "come — and today the office answers with a morning or an afternoon, because that "
             "is all it can honestly promise. A two-hour window is the thing the crews would be "
             "measured against, so it cannot be sized until the replanning story says what "
             "happens to it when the day goes wrong.",
         ok=["A booked job carries a two-hour window the customer is told",
             "A window that can no longer be kept tells the office before it tells the customer",
             "The firm can see how often the window was met, by crew and by month"]),
]

# --- route planning -------------------------------------------------------------------

ROUTES = [
    dict(a="routes.order", t="Order a crew's stops so the day is driveable",
         parent="routes", who="tomasz", labels="routing", made="07-13 09:55", sprint="Sprint 3",
         moves=[("07-13 11:35", "Ready"), ("07-15 09:50", "In progress"),
                ("07-22 16:10", "In review"), ("07-23 10:30", "QA", "mateo"),
                ("07-24 11:20", "Done", "mateo")],
         why="Nine jobs handed to a crew in the order the office took the calls is a day with "
             "two crossings of the same island in it. Ordering them is not the interesting "
             "problem — keeping the order somebody deliberately chose is, because the crew "
             "knows things about the customer that the planner never will.",
         ok=["A day's stops come back in an order that does not cross itself",
             "A stop the crew or the office pinned stays where it was put",
             "Reordering nine stops answers fast enough to do it while somebody watches"]),
    dict(a="routes.order.1", t="Treat the depot and the last stop as fixed ends of the day",
         type="subtask", parent="routes.order", who="tomasz", pts=3, made="07-15 10:10",
         moves=[("07-15 11:40", "Ready"), ("07-16 09:50", "In progress"),
                ("07-20 16:20", "In review"), ("07-21 10:10", "QA", "mateo"),
                ("07-21 15:20", "Done", "mateo")],
         why="A crew starts at the depot with a loaded van and finishes wherever the last job "
             "is, and an order that ignores both ends produces a beautiful route nobody drives."),
    dict(a="routes.order.2", t="Keep the crew's own reordering when the day is replanned",
         type="subtask", parent="routes.order", who="tomasz", pts=3, made="07-15 10:15",
         moves=[("07-16 10:20", "Ready"), ("07-21 09:50", "In progress"),
                ("07-22 11:10", "In review"), ("07-22 14:20", "QA", "mateo"),
                ("07-23 09:40", "Done", "mateo")],
         why="A crew that drags a job up its own list has a reason, usually a customer who is "
             "only in before ten. The replan has to work around that rather than undo it."),
    dict(a="routes.travel", t="Put the road's travel time between two stops, not a straight line",
         parent="routes", who="tomasz", labels="routing", pts=5, made="07-13 10:00", sprint="Sprint 3",
         moves=[("07-14 11:30", "Ready"), ("07-16 09:40", "In progress"),
                ("07-21 16:20", "In review"), ("07-22 10:20", "QA", "mateo"),
                ("07-22 15:50", "Done", "mateo")],
         why="Two addresses eight kilometres apart are twelve minutes or fifty depending on "
             "which side of the water they are on, and a planner that measures in straight lines "
             "will confidently build a day nobody can drive. The times are asked for once per "
             "pair and kept, because the roads do not move.",
         ok=["A pair of addresses gets a driving time that accounts for the water between them",
             "Times already asked for are reused rather than asked again",
             "A pair we cannot get a time for is planned pessimistically, not optimistically"]),
    dict(a="routes.zones", t="Draw the four service zones Nordic Field actually work in",
         type="task", parent="routes", who="ola", by="ola", tags=("customer/nordic-field",),
         pts=2, made="07-13 10:20", sprint="Sprint 3",
         moves=[("07-14 09:35", "Ready"), ("07-15 10:20", "In progress"),
                ("07-16 11:10", "In review"), ("07-17 09:50", "QA", "priya"),
                ("07-20 10:30", "Done", "mateo")],
         why="The firm thinks in four areas — the island, the town, the eastern valley and the "
             "coast road — and every crew knows which one they are in this week. The planner has "
             "to know it too, or it will build a day that is efficient on paper and crosses a "
             "bridge four times.",
         ok=["The four zones exist with the boundaries the firm drew on a paper map",
             "A job's zone is decided from its address without anybody choosing it"]),
    dict(a="routes.reflow", t="When a job overruns, move the rest of the day rather than break it",
         parent="routes", who="priya", labels="routing", pts=8, made="08-24 09:55", sprint="Sprint 6",
         moves=[("08-24 11:40", "Ready"), ("08-26 09:50", "In progress"),
                ("09-02 16:10", "In review")],
         why="An hour's job that takes three is the normal case, not the exception, and today "
             "the whole afternoon quietly becomes wrong while the office finds out by being "
             "rung. Replanning is what turns an overrun into three moved appointments and one "
             "phone call the office chooses to make.",
         ok=["An overrunning job pushes the crew's remaining stops and says which ones moved",
             "A stop that can no longer be reached today is offered to another crew or tomorrow",
             "The office sees the replan before the customer does"]),
    dict(a="routes.map", t="Draw the day's route on a map the dispatcher can read at a glance",
         parent="routes", who="priya", labels="routing", tags=("needs-design",), made="08-11 11:30",
         moves=[("08-12 10:30", "Ready"), ("08-25 11:40", "Cancelled")],
         why="The dispatcher's board is a list, and a list of nine addresses does not tell "
             "anybody that two of them are on the wrong side of the water. A map of the day, "
             "one crew at a time, was meant to make the shape of it obvious.",
         ok=["A crew's day is drawn as a route with the stops numbered in order",
             "The map is readable on the office's own screen without zooming"],
         says=[("08-25 11:30", "ingrid",
                "Cancelling this one. We asked the two dispatchers at Nordic Field to point at "
                "what they actually look at, and it was the travel time in the list — the "
                "number between two rows — not a picture. The replanning story puts that number "
                "where they are already looking. A map is a week of work and a provider to "
                "choose to tell them something the list can say in a column, and we would still "
                "have to decide what it does when a crew is in a tunnel.")]),
    dict(a="routes.ferry", t="The planner sends a crew across the fjord after the last ferry",
         type="bug", parent="routes", who="tomasz", priority="high", labels="routing", pts=5,
         made="08-26 14:10", sprint="Sprint 6",
         moves=[("08-27 09:40", "Ready")],
         why="The coast-road zone is reached by a crossing that stops at six, and the travel "
             "times know how long it takes but not when it runs. A five o'clock job on the far "
             "side is planned happily and the crew spends the night on the wrong side of the "
             "water or drives two hours round.",
         ok=["A crossing has a timetable and the planner refuses to plan across it after the last one",
             "A day that has to cross late is flagged to the office rather than silently reordered"],
         says=[("08-26 14:20", "mateo",
                "The Kvaløya crew found this one for us, politely. Job at seventeen ten on the "
                "far side, last crossing at eighteen, and the planner had them leaving the "
                "previous job at seventeen forty. They drove round. It has been planning like "
                "this since the travel times went in, so it is not new — it is just that nobody "
                "had a late job over there until this week.")]),
    dict(a="routes.eta", t="The arrival time texted to the customer is the one from before the replan",
         type="bug", parent="routes", who="priya", priority="high", labels="routing", pts=3,
         made="08-24 14:20", sprint="Sprint 6",
         moves=[("08-24 15:10", "Ready"), ("08-25 09:50", "In progress"),
                ("08-26 16:20", "In review"), ("08-27 10:20", "QA", "mateo")],
         why="The message to the customer is composed from the day as it was planned in the "
             "morning, and the day is replanned every time a job overruns. The customer is told "
             "half past one, the crew arrives at four, and the firm is the one that looks "
             "disorganised for a number nobody at Nordic Field ever typed.",
         ok=["The message is composed when it is sent, from the day as it stands then",
             "A replan that moves a stop more than an hour offers to tell the customer",
             "The office can see what was sent and when"],
         says=[("08-24 14:30", "mateo",
                "Found it against the replanning branch, so it is not in front of a customer "
                "yet. The estimate is read once when the day is planned and carried in the "
                "message queue for hours."),
               ("09-01 11:10", "mateo",
                "Still sitting with me, and it is my fault rather than the fix's. I do not want "
                "to pass it on the demo data — the whole point is a day that gets replanned "
                "twice, and I want to watch it against the crews' real week before I sign it "
                "off. Ola is loading last week's jobs for me.")]),
]

# --- offline mobile, and the Wednesday afternoon it went wrong --------------------------

OFFLINE = [
    dict(a="offline.day", t="A crew phone holds a whole day's work with no signal",
         parent="offline", who="aiko", labels="offline-sync,mobile", made="07-27 09:40",
         sprint="Sprint 4",
         moves=[("07-27 11:20", "Ready"), ("07-28 09:50", "In progress"),
                ("08-05 16:10", "In review"), ("08-06 10:20", "QA", "mateo"),
                ("08-06 15:40", "Done", "mateo")],
         why="The sprint goal, as one card. A crew leaves the depot at seven, spends the day "
             "between a tunnel, a cellar and the mountain road, and comes back at four having "
             "done nine jobs — and every one of them has to be on the phone, editable, and "
             "still there when the van finally passes a mast.",
         ok=["A day planned before the crew leaves is fully readable with the phone in flight mode",
             "Jobs finished offline are finished, not queued drafts the crew has to redo",
             "Nothing the crew typed is lost when the app is closed or the phone is restarted"]),
    dict(a="offline.day.1", t="Keep the day's jobs, notes and photographs on the phone itself",
         type="subtask", parent="offline.day", who="aiko", pts=5, made="07-28 10:10",
         moves=[("07-28 11:40", "Ready"), ("07-29 09:50", "In progress"),
                ("08-03 16:20", "In review"), ("08-04 10:10", "QA", "tomasz"),
                ("08-04 15:20", "Done", "mateo")],
         why="Everything the crew will need for the day is written to the phone while it still "
             "has a signal, photographs included, so that the app never asks the network a "
             "question it cannot answer."),
    dict(a="offline.day.2", t="Queue every edit the crew makes while the phone is dark",
         type="subtask", parent="offline.day", who="aiko", pts=5, made="07-28 10:15",
         moves=[("07-29 10:20", "Ready"), ("08-04 09:50", "In progress"),
                ("08-05 11:10", "In review"), ("08-05 14:20", "QA", "tomasz"),
                ("08-06 09:40", "Done", "mateo")],
         why="Every change the crew makes is written down as the change it was — this note, on "
             "this job, at this time — rather than as a new version of the job, so the two sides "
             "have something to reconcile rather than something to choose between."),
    dict(a="offline.day.3", t="Send the queue when the phone finds a signal, oldest first",
         type="subtask", parent="offline.day", who="tomasz", pts=3, made="07-28 10:20",
         moves=[("07-29 10:25", "Ready"), ("07-30 09:50", "In progress"),
                ("08-04 16:10", "In review"), ("08-05 10:20", "QA", "aiko"),
                ("08-05 15:30", "Done", "mateo")],
         why="Four crews coming into signal at the top of the hill at the same time, each with a "
             "day's changes in order, and the server taking them one at a time without minding "
             "being sent the same one twice."),
    dict(a="offline.photos-kept", t="A job finished offline keeps its photographs",
         parent="offline", who="aiko", labels="offline-sync", pts=5, made="07-27 09:45",
         sprint="Sprint 4",
         moves=[("07-28 11:30", "Ready"), ("07-30 09:40", "In progress"),
                ("08-05 15:40", "In review"), ("08-06 10:40", "QA", "mateo"),
                ("08-07 11:20", "Done", "mateo")],
         why="A photograph of the old part, the meter reading and the finished pipework is what "
             "the office invoices from and what the firm produces when a customer says the work "
             "was never done. Six photographs at three megabytes each, taken in a cellar, have "
             "to survive a day in a pocket and a sync that runs while the van is moving.",
         ok=["Photographs taken offline are attached to the job before it is sent",
             "Every photograph the crew took reaches the office, in the order they were taken",
             "A photograph that fails to upload is retried rather than dropped"],
         says=[("09-02 11:40", "mateo",
                "Late note against a finished story, because I would rather it lived here than "
                "in my head. Running the offline day again this week on the older phone, the "
                "job arrives with five photographs and the crew took six. The sixth is on the "
                "phone and never leaves it. One device, one photograph, every time I run it — "
                "which is the sort of off-by-one that is a five-minute fix and a very bad demo.")]),
    dict(a="offline.sync-loss", t="Offline edits are lost when the server's version wins the merge",
         type="bug", parent="offline", who="tomasz", by="mateo", priority="critical",
         labels="offline-sync", tags=("regress",), dod="hotfix", pts=8,
         made="07-29 14:10", sprint="Sprint 4",
         moves=[("07-29 14:40", "Ready"), ("07-29 15:20", "In progress"),
                ("08-04 16:20", "In review"), ("08-05 10:10", "QA", "mateo"),
                ("08-05 15:20", "Done", "mateo")],
         why="When a job comes back from a phone and the server's copy has also changed, the "
             "merge keeps the server's fields and drops the phone's. A day in a dead zone is "
             "exactly the case where the phone is right and the server is a stale copy from "
             "seven in the morning, so the rule throws away the only version of the work that "
             "anybody actually did.",
         ok=["A field the phone changed while offline is never overwritten by an older server value",
             "Anything the server cannot reconcile is kept somewhere a person can read it",
             "The eleven crews' lost notes are recovered from the request logs where they exist",
             "The merge rule is written down as a decision rather than living in the code"],
         says=[("07-29 14:20", "mateo",
                "Eleven crews, one afternoon. The Storelva crew rang the office to ask why their "
                "morning was empty and it went from there. Every job they finished in the "
                "eastern valley is back to the state it was in when they left the depot: no "
                "notes, no parts, no photographs, and two of them marked unfinished. This is "
                "everything four people did today."),
               ("07-29 15:10", "tomasz",
                "Found it. The merge is last-writer-wins on the whole job and the server counts "
                "as the writer whenever it has touched the row since the phone last saw it — and "
                "the planner touches every row at seven when it builds the day. So the phone "
                "always loses, and it loses hardest for the crews that were offline longest. "
                "I am taking it now; nothing else I have is worth a crew's day."),
               ("07-29 16:30", "ingrid",
                "What we are telling Nordic Field: we lost this afternoon's write-ups for eleven "
                "crews, we know exactly which jobs, and we are asking those crews to write them "
                "again tomorrow morning rather than pretending we can recover them all. Tomasz "
                "thinks the notes are in the request logs and is looking. Nobody rings a crew to "
                "ask what they did today twice — so the second half of this card is the decision "
                "about who wins a merge, written down where somebody can disagree with it."),
               ("08-05 15:30", "tomasz",
                "Done. The phone wins for anything it changed while it was offline, the server "
                "keeps what only it changed, and anything that is genuinely two edits of the "
                "same field is kept as both and handed to the crew to choose — that last part "
                "is its own story, and until it ships the pair is written to a table nobody "
                "throws away. Nine of the eleven crews' notes came back out of the logs.")]),
    dict(a="offline.duplicate-job", t="A job sent twice from a phone appears twice on the board",
         type="bug", parent="offline", who="tomasz", priority="high", labels="offline-sync",
         pts=3, made="08-28 11:20", sprint="Sprint 6",
         moves=[("08-28 14:30", "Ready")],
         why="A phone that sends its queue, loses the signal before it hears the answer and "
             "sends again produces two of the same finished job, and the office invoices one of "
             "them and wonders about the other. The queue is ordered and retried; what it is not "
             "is idempotent, which is the same lesson the payments work learned in July.",
         ok=["The same queued change sent twice is applied once",
             "A duplicate that already reached the board can be merged into the original"],
         says=[("08-28 11:30", "mateo",
                "Two of the crews' phones did this on the trial week and I have been able to "
                "make it happen on demand: send the queue standing in the tunnel entrance, walk "
                "in, walk out. Same job, two rows, both finished, both invoiceable. It is the "
                "sync loss's cousin — the phone is being careful about not losing work and "
                "nothing at the other end is being careful about not counting it twice.")]),
    dict(a="offline.conflict", t="Show the crew what disagreed and let them choose",
         parent="offline", who="aiko", labels="offline-sync,mobile", tags=("needs-design",),
         made="08-24 10:00", sprint="Sprint 6",
         moves=[("08-24 11:45", "Ready"), ("08-26 09:40", "In progress")],
         ticks="09-02 15:20", ticked=1,
         why="The half of the merge decision that the incident could not fix in an afternoon: "
             "when the phone and the office have both changed the same thing, somebody has to "
             "choose, and the only person who knows which is right is the one who was standing "
             "in the cellar. Today those pairs go to a table nobody reads.",
         ok=["A job with a genuine conflict is shown to the crew as two versions side by side",
             "Choosing one keeps the other where the office can still see it",
             "A crew that ignores the question is asked again rather than quietly resolved"]),
    dict(a="offline.conflict.1", t="Keep both versions of a job until somebody chooses",
         type="subtask", parent="offline.conflict", who="aiko", pts=5, made="08-26 10:10",
         moves=[("08-26 11:40", "Ready"), ("08-27 09:50", "In progress")],
         why="The storage half: a conflicting pair is a first-class thing with both versions, "
             "who wrote each and when, rather than a row in a table that exists to be swept."),
    dict(a="offline.sync-fix-load", t="The sync holds when a whole depot comes back into signal at once",
         parent="offline", who="tomasz", labels="offline-sync", tags=("area/api",), pts=8,
         made="08-24 10:05", sprint="Sprint 6",
         moves=[("08-24 11:50", "Ready"), ("08-25 09:40", "In progress")],
         ticks="09-03 11:20", ticked=1,
         why="Half of the sprint goal. The merge rule from the incident is right and slow: it "
             "reads every change a phone made before it decides anything, and four crews driving "
             "into the depot yard at the same time is forty days of changes arriving in one "
             "minute. It has to hold up under that with the phones on the yard's own weak signal, "
             "which is the shape the next customer will have four times over.",
         ok=["Four crews' full days sync together without a phone timing out",
             "A phone that loses the signal mid-sync resumes rather than starting again",
             "The reconciliation is measured, so we find out from a graph rather than a crew"]),
    dict(a="offline.attachments", t="Upload a job's photographs over a connection that keeps dropping",
         parent="offline", who="aiko", labels="offline-sync,mobile", tags=("device/older-fleet",),
         pts=5, made="08-24 10:10", sprint="Sprint 6",
         moves=[("08-25 11:30", "Ready"), ("08-27 09:40", "In progress"),
                ("09-03 16:10", "In review")],
         why="Six photographs from a cellar are eighteen megabytes going up a connection that "
             "exists for forty seconds at a time on the mountain road. Sending them whole means "
             "sending them again, and again, until the crew gets back to town — which is why the "
             "phones come home with a day of photographs still on them.",
         ok=["A photograph is uploaded in pieces and resumes where it stopped",
             "Photographs go up after the job's text, so the office is not waiting on them",
             "The crew can see which photographs have reached the office"]),
    dict(a="offline.signature", t="The customer signs for the work on the phone and it survives the sync",
         parent="offline", who="aiko", labels="mobile", pts=5, made="08-24 10:15", sprint="Sprint 6",
         moves=[("08-26 11:30", "Ready")],
         why="Nordic Field's crews carry a pad of job sheets the customer signs, and the office "
             "types them up again a week later from the copy that came back in the van. A "
             "signature on the phone is the same evidence without the second typing — as long "
             "as it is attached to the job the same way a photograph is, and comes back from a "
             "day offline just as reliably.",
         ok=["A customer signs on the phone with no signal and the job carries the signature",
             "The signature reaches the office with the job, not separately",
             "A job that was signed cannot be quietly edited afterwards without saying so"]),
    dict(a="offline.devices", t="Get the offline build onto both crews' own phones before the trial day",
         type="task", parent="offline", who="ola", by="ola",
         tags=("device/older-fleet", "customer/nordic-field"), pts=2, made="07-27 10:10",
         sprint="Sprint 4",
         moves=[("07-28 09:35", "Ready"), ("07-29 10:30", "In progress"),
                ("07-30 11:10", "In review"), ("07-31 09:50", "QA", "aiko"),
                ("08-03 10:20", "Done", "mateo")],
         why="The trial day is two crews driving the eastern valley with their own phones, one "
             "of which is five years old and full. Getting a build onto them is a week of "
             "provisioning and a store review if it is left until the Friday, and the whole "
             "sprint goal is unmeasurable without it.",
         ok=["Both crews' phones are running the offline build a week before the trial day",
             "A new build reaches those phones the same day it is cut"]),
    dict(a="offline.dead-zone", t="Book a day on the mountain road where there is no signal to test in",
         type="task", parent="offline", who="ola", by="ola", pts=1, made="07-27 10:15",
         sprint="Sprint 4",
         moves=[("07-28 09:40", "Ready"), ("08-06 11:40", "Cancelled")],
         why="Flight mode is not a dead zone. A phone that has been out of signal for six hours "
             "and comes back on a weak connection behaves differently from one somebody switched "
             "off, and the plan was to spend a day up the eastern valley finding out how.",
         ok=["A day is booked with a crew who will let us sit in the van",
             "What the phones did that day is captured well enough to replay"],
         says=[("08-06 11:30", "ola",
                "Cancelling, and not happily. The twenty-ninth gave us the day for free and at "
                "the worst possible price: eleven crews' phones, six hours out of signal, and "
                "every request they made on the way back is in the logs. Aiko has built the "
                "fixtures from it, so what a dead zone does to us is now a test rather than a "
                "field trip. If the load work turns up something the logs cannot answer I will "
                "book the van day again and say so here.")]),
]

WORK = EPICS + JOBS + ROUTES + OFFLINE

ALIASES: dict[str, str] = {PREFIX + spec["a"]: spec["t"] for spec in WORK}

# Both sides of everything with an inverse, so Harbor's planted one-sided relation stays
# the only one in the vault. `relates` has no inverse and is written once, from the side
# that noticed — including the one that reaches into Harbor.
RELATIONS = [
    ("07-15 11:10", "tomasz", "routes.order", dict(blocked_by=["routes.travel"])),
    ("07-15 11:11", "tomasz", "routes.travel", dict(blocks=["routes.order"])),
    # The day after the incident: Harbor's queued check-in is the same merge with a
    # different noun in front of it, and both teams should read one decision.
    ("07-30 11:15", "mateo", "offline.sync-loss", dict(relates=["harbor.checkin.pontoon"])),
    ("08-27 11:50", "priya", "routes.eta", dict(relates=["routes.reflow"])),
    ("08-28 11:45", "mateo", "offline.duplicate-job", dict(relates=["offline.sync-loss"])),
    ("09-01 11:40", "aiko", "offline.signature", dict(blocked_by=["offline.attachments"])),
    ("09-01 11:41", "aiko", "offline.attachments", dict(blocks=["offline.signature"])),
]


def events() -> list[story.Event]:
    common.leaves_only(WORK, PREFIX)
    out = []
    for index, spec in enumerate(WORK):
        out += common.lifecycle(spec, PROJECT, PREFIX, index)
    out += common.relation_events(RELATIONS, ALIASES, PREFIX)
    return out
