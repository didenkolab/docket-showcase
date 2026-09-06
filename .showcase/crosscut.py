"""The quarter around the work: what it was for, what could go wrong with it, what did,
who asked for it, where the hours went, and the pages that argue for all of it.

Harbor, Ledgerline and Fieldnote say what the team built. This module says everything
else a real quarter leaves behind and a demo vault usually has none of:

  * **objectives and key results** — three objectives, one per product, and the seven
    numbers that would have told the team by the end of September whether the quarter
    worked. The work points at them from below (`contributes_to` on an epic), because a
    key result is not a container of tasks and counting finished cards is the failure
    OKRs were invented to prevent.
  * **a risk register** — six things that could have gone wrong, written on 22 June by
    the two people who would have had to deal with them, reviewed again on 3 August after
    one of them nearly did.
  * **two incidents and their postmortems** — the double charge on 8 July and the
    afternoon eleven crews lost on 29 July, each with the bug it produced and a
    postmortem whose actions are cards rather than prose.
  * **eight requests** — what four customers actually asked for, in their words. Three
    became stories, two were answered no, and three are still waiting, which is roughly
    the ratio any team that answers its post has.
  * **thirty worklogs** — where four people's hours went in the last two sprints.
  * **six decisions and four design pages** — the arguments the code cannot hold, and
    the front page that tells a newcomer which of them to read first.

Three rules shape the data more than taste does:

  * Rule 12 refuses an estimate on a task that has children, and a worklog is a child.
    So time is logged only against work that was never sized — the container stories
    whose subtasks carry the numbers, and the spikes that were investigated rather than
    estimated. `WORKLOGS` names its parents and `test_crosscut` asserts none of them has
    a number on it.
  * The anomalies Harbor plants on purpose have to stay the only three. Every request
    carries a label so that none of them reads as adrift; every relation with an inverse
    is written from both ends; and a worklog is created finished, so a task with five of
    them under it does not become a body of work one person is the whole of.
  * `docket set` replaces a relation rather than appending to it, so the inverse on a task
    that several things point at — a parent with six worklogs, an epic two risks threaten
    — is written once, naming all of them, after the last of them exists.
"""
from __future__ import annotations
import datetime as dt

import engine
import story
from story import PEOPLE

from products import common, harbor, ledgerline, fieldnote

PRODUCTS = (harbor, ledgerline, fieldnote)
ALIASES: dict[str, str] = {}
for _module in PRODUCTS:
    ALIASES.update(_module.ALIASES)

QUARTER = "2026-Q3"

# Where a crosscutting task lives: the product it measures, threatens, interrupted or was
# asked of. There is no fourth project for "the team", and there should not be — a risk
# that threatens Harbor's payments is Harbor's risk, and a board that filters by project
# is the board somebody actually opens.
HARBOR, LEDGER, FIELD = "HARBOR", "LEDGER", "FIELD"


def _at(moment: str) -> dt.datetime:
    """"07-31 16:20", checked against the story's weeks and the team's office hours."""
    return common.office_hours(common.when(moment), moment)


def _new(moment, who, alias, title, project, kind, status="", assignee="", labels="",
         parent="", body="") -> engine.Event:
    return story.new(_at(moment), PEOPLE[who], alias, title, project, type=kind,
                     status=status, assignee="[[%s]]" % assignee if assignee else "",
                     labels=labels, parent=parent, body=body)


# --- objectives and key results -------------------------------------------------------
#
# Written on 16 June, the second morning, when the sprint board already existed and the
# question "what is all this for" had been asked twice in a planning session. One
# objective per product, because the three products serve three different customers and a
# single company objective would have been a sentence nobody could disagree with.
#
# The objectives stay in progress for the whole quarter — a quarter closes in October and
# this vault stops on 4 September — and each is on ingrid, so that no board shows a thing
# in flight with nobody's name against it.

OBJECTIVES = [
    dict(a="okr.harbor", t="Marinas run the season on Harbor", project=HARBOR,
         who="ingrid", made="06-16 09:20",
         why="The season is June to September and it happens once. A marina that tries "
             "Harbor in July and goes back to the wall planner in August has told us "
             "something no survey will: that the software was harder than the paper it "
             "replaced, on the week it mattered. So the objective is not adoption in the "
             "abstract. It is four marinas taking the whole of their season through "
             "Harbor and not keeping a second copy of the truth beside it."),
    dict(a="okr.ledger", t="Ledgerline closes a quarter without a spreadsheet", project=LEDGER,
         who="ingrid", made="06-16 09:22",
         why="Every accountant we have spoken to keeps one spreadsheet beside whatever "
             "software they are given, and the spreadsheet is where the quarter is "
             "actually assembled. That is the thing to replace. Not the invoicing, which "
             "they will tolerate anywhere, but the fortnight at the end of the quarter "
             "when the numbers are gathered by hand from four places and typed into a "
             "return. If Q3 closes out of Ledgerline and the spreadsheet stays shut, the "
             "product is worth paying for."),
    dict(a="okr.field", t="A crew's day survives a dead zone", project=FIELD,
         who="ingrid", made="06-16 09:24",
         why="Nordic Field's crews work in valleys where there is no signal for hours at "
             "a time, and every scheduling tool they have tried assumed a connection and "
             "quietly lost the afternoon. The whole product rests on one claim: take the "
             "phone into the mountains, do a day's work, come back, and everything you "
             "did is there. Nothing else we build for them matters if that is not true."),
]

# target/current/measure, and the two mornings the numbers were read again. `current` at
# creation is where the quarter started, not zero for its own sake: two of these had
# months of history behind them before the objective was written.
KEY_RESULTS = [
    dict(a="okr.harbor.marinas", t="Four marinas take the whole season through Harbor",
         parent="okr.harbor", project=HARBOR, who="ingrid", made="06-16 09:30",
         target=4, current=1, july=3, august=4,
         source="Counted by hand at the end of each month against the berth import and the "
                "bookings for July and August. There is no query for it and it does not need "
                "one at four marinas; it needs two people to get the same answer",
         measure="Marinas whose berth list is in Harbor and whose July and August "
                 "bookings were made in it",
         why="Not signups and not trials. A marina counts when its berths are in Harbor "
             "and its season is being sold out of Harbor, which is the only version of "
             "adoption that survives August."),
    dict(a="okr.harbor.pontoon", t="Nine in ten arrivals are checked in from the pontoon",
         parent="okr.harbor", project=HARBOR, who="aiko", made="06-16 09:32",
         target=90, current=0, july=0, august=71,
         source="The check-in log, which carries where each check-in came from. Over the last "
                "fourteen days rather than the season, because the season includes the weeks "
                "before there was anything to check in with",
         measure="Share of check-ins that arrived from the mobile queue rather than "
                 "being typed in the office, over the last fourteen days",
         why="The office keyboard is the fallback, and a fallback that is used for half "
             "the arrivals is the real product. This is the number that says whether "
             "check-in works standing on a finger pier in the rain."),
    dict(a="okr.harbor.calendar", t="The biggest marina's month opens in under a second",
         parent="okr.harbor", project=HARBOR, who="priya", made="06-16 09:34",
         target=90, current=12, july=94, august=96,
         source="The staging timings, month view only, on Sandholm's data. Measured on "
                "staging on purpose: a marina's own wifi is not something this number should "
                "be reporting on",
         measure="Share of month-view loads under one second on Sandholm's four hundred "
                 "and six berths",
         why="The calendar is the screen the harbour office leaves open all day. On forty "
             "berths everything is fast; the number is measured on the largest marina we "
             "have, because that is where a month view stops being usable."),
    dict(a="okr.ledger.close", t="Three businesses close Q3 out of Ledgerline",
         parent="okr.ledger", project=LEDGER, who="tomasz", made="06-16 09:36",
         target=3, current=0, july=0, august=1,
         source="Asked of each accountant at the close, in those words, and written down. "
                "There is no query for this and there should not be — a report that was "
                "generated and then ignored counts as a no",
         measure="Businesses whose quarterly return was produced from the tax report and "
                 "not retyped",
         why="Asked rather than measured, on purpose. The number we can compute is how "
             "many reports were generated, and a report that was generated and then "
             "ignored is worse than none."),
    dict(a="okr.ledger.matched", t="Nine in ten bank lines are matched without a person",
         parent="okr.ledger", project=LEDGER, who="tomasz", made="06-16 09:38",
         target=90, current=0, july=61, august=78,
         source="The import log over the previous thirty days, counting lines rather than "
                "statements. A line a person confirmed without changing counts as settled; a "
                "line a person corrected does not",
         measure="Share of imported statement lines the matcher settled on its own over "
                 "the last thirty days",
         why="Matching by hand is the work the spreadsheet was doing. Every line the "
             "importer settles is a line nobody reads, and the ones it cannot settle are "
             "the ones worth a person's attention."),
    dict(a="okr.field.nothing-lost", t="No crew loses work to a sync",
         parent="okr.field", project=FIELD, who="aiko", made="06-16 09:40",
         target=0, current=0, july=11, august=0,
         source="The sync log over the previous thirty days. It sees only what we can see: a "
                "crew who noticed and retyped the job without ringing anybody is invisible "
                "to it, so the dispatcher is asked as well",
         measure="Jobs whose offline edits were dropped by a merge, counted over the "
                 "previous thirty days",
         why="A target of zero is the only honest one: a crew that loses a day's work "
             "once does not lose it twice, because they stop using the phone. The number "
             "was zero when it was written because nobody had looked."),
    dict(a="okr.field.from-the-van", t="Nine in ten jobs are written up before the crew gets back",
         parent="okr.field", project=FIELD, who="aiko", made="06-16 09:42",
         target=90, current=35, july=58, august=74,
         source="The job log: the time of a note's first version against the time of that "
                "crew's last stop. A note written the next morning counts as late, which is "
                "the point of measuring it",
         measure="Share of job notes whose first version reached us before the crew's "
                 "last stop of the day",
         why="A job written up in the van is written from memory of ten minutes ago; one "
             "written at the depot at six is written from memory of eight hours ago, and "
             "it is the second kind that produces the callbacks."),
]


# --- the risk register ----------------------------------------------------------------
#
# Written in one sitting on the Monday of Sprint 1's second week, by the two people who
# would have had to deal with any of them, and read again on 3 August — the Monday after
# the sync incident, when somebody asked whether we had seen it coming. We had not, which
# is why the sixth one is on the register now.
#
# Three carry `mitigated_by`, and only three: a register where every line has work
# against it is a register somebody filled in. The other three are watched, and two of
# them are things no card can prevent.

RISKS = [
    dict(a="risk.provider", t="The payment provider suspends a marina's account mid-season",
         project=HARBOR, threatens="harbor.payments", by="ola", owner="ola",
         likelihood="unlikely", impact="severe", labels="payments",
         why="Marinas take a season's money in eight weeks, which to a payment provider's "
             "fraud model looks like a dormant account that suddenly turns over forty "
             "thousand kroner in a fortnight. A provider that decides to hold funds while "
             "it asks questions stops a marina taking bookings on the weekend it earns "
             "its year, and there is no second provider to fail over to — that is the "
             "price the payments decision names and accepts.",
         plan="Every marina is onboarded with its expected season volume declared up "
              "front rather than discovered, and we hold the provider's escalation "
              "contact rather than the support form. If it happens, bookings continue and "
              "payment is taken on arrival, which is what the marina did before us."),
    dict(a="risk.oncall", t="The launch weekend arrives and nobody who can restore the database is reachable",
         project=HARBOR, threatens="harbor.checkin", by="ola", owner="ola",
         likelihood="likely", impact="major", labels="bookings",
         mitigated_by=["harbor.ops.season-runbook"], mitigated_on="08-24 14:20",
         why="Six people, no rota, and a launch on a Saturday in August when four of them "
             "have already said they are away. The restore has been done once, by one "
             "person, from memory, on a laptop. Nothing about that is unusual for a team "
             "this size and all of it is fine until the weekend it is not.",
         plan="A runbook that says who is on call, how the marina reaches us out of hours, "
              "and a restore that somebody other than its author has rehearsed."),
    dict(a="risk.statement-format", t="A bank changes its statement format and the import stops without saying so",
         project=LEDGER, threatens="ledger.bank", by="ola", owner="ola",
         likelihood="likely", impact="moderate", labels="bank-import",
         why="Two of the three banks we read give us a file rather than an API, and a "
             "file format is a promise nobody made. The failure we should expect is not a "
             "crash: it is a column that moves, an import that succeeds, and a quarter of "
             "lines that are quietly wrong until an accountant notices in October.",
         plan="The importer refuses a statement it cannot fully account for rather than "
              "importing the part it understands, and the manual matching screen is the "
              "fallback for a bank that has moved under us."),
    dict(a="risk.keys", t="The sandbox keys that were in the repository are still in somebody's clone",
         project=HARBOR, threatens="harbor.payments", by="ola", owner="ola",
         likelihood="possible", impact="major", labels="payments",
         mitigated_by=["harbor.payments.provider-keys"], mitigated_on="07-01 14:30",
         why="The provider's sandbox keys were committed in the first sprint and taken "
             "out in the second, which removes them from the working tree and from "
             "nothing else. They are in the history, in every clone, and in whatever "
             "search index has been over this repository since June. Sandbox keys are not "
             "money, but the habit that put them there is the habit that will put live "
             "ones somewhere.",
         plan="Rotate what was committed, keep secrets in the deployment's own store, and "
              "make the person who needs a key ask for it rather than find it."),
    dict(a="risk.winter", t="Three marinas decide over the winter not to come back",
         project=HARBOR, threatens="harbor.booking", by="ingrid", owner="ingrid",
         likelihood="likely", impact="major", labels="bookings",
         why="The season ends in September and every marina then has six months in which "
             "nothing we built is in front of them. The decision to renew is taken in "
             "February, from whatever they remember of August, and what people remember "
             "of August is the thing that went wrong on the busy weekend.",
         plan="Close the season with each marina rather than letting it end: what they "
              "took, what it cost them in office time, and the two things they would "
              "change. A conversation in September is worth more than a discount in "
              "February."),
    dict(a="risk.crews-stop", t="A crew loses a day's work again and Nordic Field stop using the phone",
         project=FIELD, threatens="field.offline", by="ingrid", owner="aiko",
         likelihood="possible", impact="severe", labels="offline-sync",
         mitigated_by=["field.offline.sync-fix-load"], mitigated_on="08-25 14:20",
         why="Eleven crews lost an afternoon on 29 July and rang the office about it. The "
             "fix went in within a week, and the thing that has not been tested is the "
             "case that produced it: a whole depot coming back into signal at once, at "
             "half past four, with a day of queued edits each. Dispatchers do not give "
             "software a third chance with their crews' time.",
         plan="Hold the sync under a depot's worth of reconnections before the next "
              "season, and give the crew the conflict rather than resolving it for them."),
]


# --- the two incidents, and what was written down afterwards ---------------------------
#
# Two tasks each, because the incident is over when the system is well and the postmortem
# is done when the changes are decided, and those are different days. Kept as one, the
# second half closes early: the pressure is off and nobody reopens a card marked Done.
#
# Both go through the workflow like everything else, QA included. That is not ceremony:
# what mateo checks on a postmortem is that every line under "What we are changing" is a
# card somebody can be asked about, which is the failure the template warns of.

INCIDENTS = [
    dict(a="inc.double-charge", t="Guests at three marinas were charged twice for one booking",
         project=HARBOR, who="tomasz", labels="payments", made="07-08 09:50",
         severity="sev2", detected_at="2026-07-08T09:40:00Z", resolved_at="2026-07-08T13:15:00Z",
         customers_affected="3 marinas, 7 guests, 11 duplicate charges",
         from_bugs=["harbor.payments.double-charge"], caused_on="07-08 15:40",
         moves=[("07-08 13:20", "In review", "tomasz"), ("07-08 14:40", "QA", "mateo"),
                ("07-08 16:30", "Done", "mateo")],
         why="Between 09:40 and 10:05 on Wednesday 8 July, eleven card charges were taken "
             "for seven bookings across three marinas. Every one of them has the same "
             "shape: the confirmation call to the provider took longer than the guest was "
             "willing to wait, the guest pressed the button again, and the second press "
             "was a second charge against a booking that already had one.\n\n"
             "Vik rang at 09:52 to say a guest had been charged twice. Sandholm rang at "
             "10:04. The charges were stopped by taking confirmation off the booking "
             "screen at 10:20; the eleven duplicates were refunded by hand from the "
             "provider's console by 13:15, and every affected guest was rung by the "
             "marina rather than emailed by us.\n\n"
             "Found by three customers rather than by us, which is the part of this that "
             "should be uncomfortable. The fix, the reconciliation that would have caught "
             "it, and what we are doing about the general case are in the postmortem."),
    dict(a="inc.sync-loss", t="Eleven crews' offline work was overwritten when their phones reconnected",
         project=FIELD, who="aiko", labels="offline-sync", made="07-29 14:20",
         severity="sev1", detected_at="2026-07-29T14:05:00Z", resolved_at="2026-07-29T18:30:00Z",
         customers_affected="11 crews, 34 jobs, one afternoon",
         from_bugs=["field.offline.sync-loss"], caused_on="07-30 10:20",
         moves=[("07-30 09:30", "In review", "aiko"), ("07-30 11:20", "QA", "mateo"),
                ("07-30 15:40", "Done", "mateo")],
         why="On Wednesday 29 July the Storelva crew rang the dispatcher at 14:05 to ask "
             "why their morning was empty. It was empty because their phones had come "
             "back into signal at the depot and the sync had taken the server's version "
             "of every job they had touched. By 14:40 the same was true of eleven crews "
             "and thirty-four jobs: no notes, no parts used, no photographs, and two jobs "
             "back to unfinished after the customer had signed for them.\n\n"
             "Sync was turned off for every phone at 14:50, which stopped it spreading "
             "and left every crew's work sitting on their own handset. Twenty-nine of the "
             "thirty-four jobs were rebuilt from the request logs by 18:30; the remaining "
             "five were rung round and retyped by the dispatcher the next morning.\n\n"
             "Nobody enjoyed ringing eleven crews to ask what they had done that day. The "
             "merge rule that did this was never written down anywhere, so nobody had the "
             "chance to disagree with it before it ran; that is the subject of the "
             "postmortem and of the decision it produced."),
]

POSTMORTEMS = [
    dict(a="pm.double-charge", t="Postmortem: the double charge of 8 July",
         project=HARBOR, who="tomasz", labels="payments", made="07-10 10:20",
         explains="inc.double-charge", explained_on="07-10 10:40",
         mitigated_by=["harbor.payments.double-charge", "harbor.payments.webhook"],
         mitigated_on="07-13 11:00",
         moves=[("07-13 10:40", "In review", "tomasz"), ("07-14 09:50", "QA", "mateo"),
                ("07-14 15:20", "Done", "mateo")],
         says=[("07-14 10:20", "mateo",
                "Checked what this says it is changing against the board: the fix and the "
                "reconciliation are both cards with numbers on them, and the acceptance "
                "line about idempotence is on the two payment stories in Sprint 3. The "
                "provider-side idempotency key is the only one that is prose here and it "
                "is inside the fix, so I am happy. Passing it.")],
         body="## What happened\n\n"
              "09:40 — the first duplicate charge, at Vik. The provider's confirmation "
              "call was taking between eight and twenty seconds all morning; the booking "
              "screen showed a spinner and no other feedback.\n\n"
              "09:52 — Vik ring the office: a guest has two charges on one card for one "
              "berth.\n\n"
              "10:04 — Sandholm ring with the same thing. By now there are nine "
              "duplicates across two marinas.\n\n"
              "10:20 — confirmation is taken off the booking screen for every marina. "
              "Eleven duplicates in total; no further ones after this.\n\n"
              "11:20 — the cause is understood and written up as a bug.\n\n"
              "13:15 — all eleven duplicate charges refunded by hand from the provider's "
              "console. Each marina rings its own guests.\n\n"
              "## Why it was possible\n\n"
              "Confirming a booking sent a charge and had no way of saying that this "
              "charge was the same intention as the last one. The provider supports an "
              "idempotency key on exactly this call and we were not sending one, because "
              "the happy path does not need it and the happy path is what we tested.\n\n"
              "The second half is that a slow confirmation looked, to a guest, exactly "
              "like one that had not been sent. A spinner with no words on it invites a "
              "second press, and we had built the button that way in the first sprint "
              "without anybody deciding to.\n\n"
              "The third half — and this is the one that matters — is that nothing on our "
              "side compared what the provider thought had happened with what the booking "
              "thought had happened. Eleven charges existed for seven bookings for three "
              "and a half hours, and every one of the systems involved was content.\n\n"
              "## What we are changing\n\n"
              "The confirmation call carries an idempotency key derived from the booking "
              "and the attempt, so a retry is the same charge rather than a second one. "
              "That is the fix, and it is a card.\n\n"
              "The provider's webhook is reconciled against the booking nightly and "
              "anything that disagrees is raised rather than logged, so a charge without "
              "a booking is found by us within a day. That is a card too, in Sprint 3.\n\n"
              "Anything that spends money now has idempotence in its acceptance, in "
              "writing, rather than in whoever reviewed it.\n\n"
              "## What we are not changing, and why\n\n"
              "We are not building an automatic refund for a duplicate charge. Eleven "
              "refunds by hand took forty minutes; an automatic refunder that is wrong "
              "sends money to the wrong card, and the case is rare enough that a person "
              "should look at it.\n\n"
              "We are not disabling the confirmation button while the call is in flight "
              "and calling that the fix. It is worth doing and it is on the payments "
              "story, but it makes the same mistake we made in June: a browser cannot be "
              "the thing that guarantees a charge happens once."),
    dict(a="pm.sync-loss", t="Postmortem: the afternoon eleven crews lost",
         project=FIELD, who="aiko", labels="offline-sync", made="08-03 10:30",
         explains="inc.sync-loss", explained_on="08-03 10:50",
         mitigated_by=["field.offline.conflict", "field.offline.sync-fix-load"],
         mitigated_on="08-24 14:30",
         moves=[("08-05 11:20", "In review", "aiko"), ("08-06 10:40", "QA", "mateo"),
                ("08-06 15:10", "Done", "mateo")],
         says=[("08-06 11:10", "mateo",
                "The two changes are cards and the decision is written. What is not a "
                "card is the sentence about load, and that is the one I would bet on "
                "happening again — a depot coming back at once is not the same as one "
                "phone coming back eleven times. Passing it, but I would like that on a "
                "board before the next season."),
               ("08-24 14:35", "aiko",
                "Both changes are on the Sprint 6 board now, linked from here, and the "
                "load case mateo asked for is one of them.")],
         body="## What happened\n\n"
              "07:00 — the planner rebuilds every crew's day, as it does every morning. "
              "This touches every job row, including rows for jobs whose crews are "
              "already out of signal.\n\n"
              "08:10 to 13:50 — eleven crews work in the eastern valley with no signal. "
              "Notes, parts, photographs and two customer signatures are written on the "
              "phones and queued.\n\n"
              "13:55 — the first crew reaches the depot and their phone reconnects. The "
              "merge sees that the server has touched every job since the phone last saw "
              "it, and keeps the server's version of each field.\n\n"
              "14:05 — the Storelva crew ring the dispatcher to ask why their morning is "
              "empty.\n\n"
              "14:40 — eleven crews, thirty-four jobs. Two jobs the customer had signed "
              "for are back to unfinished.\n\n"
              "14:50 — sync is turned off for every phone, which stops the loss "
              "spreading.\n\n"
              "18:30 — twenty-nine jobs rebuilt from the request logs. The remaining five "
              "are rung round the following morning and retyped by the dispatcher.\n\n"
              "## Why it was possible\n\n"
              "The merge was last-writer-wins over the whole job, and the server counted "
              "as the writer whenever it had touched the row since the phone last saw it. "
              "The planner touches every row at seven in the morning. So the phone always "
              "lost, and it lost hardest for the crews who had been offline longest — "
              "which is to say, for exactly the people the product exists for.\n\n"
              "That rule was never written down. It was a line in the sync code and it "
              "read as reasonable there; nobody outside the two people who wrote it ever "
              "had the chance to say that a day in a dead zone is the case where the "
              "phone is right and the server is a stale copy from seven o'clock.\n\n"
              "The tests reached the same conclusion by the same route. There was one "
              "sync scenario, it was the happy path, and it was written by the person who "
              "wrote the merge.\n\n"
              "## What we are changing\n\n"
              "The rule is now a decision with a document behind it: for a job, the phone "
              "is the source of truth, and anything the server cannot reconcile is kept "
              "rather than dropped.\n\n"
              "Where the two genuinely disagree, both versions are held and the crew is "
              "shown what disagreed and asked to choose. That is a card in Sprint 6, and "
              "it is the piece of work this incident bought.\n\n"
              "The sync gets a scenario per conflict shape instead of one happy path, and "
              "it is held under a whole depot reconnecting at once rather than one phone "
              "at a time. That is a second card.\n\n"
              "## What we are not changing, and why\n\n"
              "We are not stopping the planner touching every row at seven. It is how the "
              "day is built and it is not the fault; a merge that cannot cope with the "
              "server having a normal morning is the fault.\n\n"
              "We are not resolving conflicts automatically by field, however tempting it "
              "looks in the code. Two fields of one job merged from two versions produce "
              "a job that nobody wrote and that the crew cannot recognise, and the first "
              "time that reaches a customer we will have spent the trust this cost us "
              "twice over."),
]


# --- what customers asked for ---------------------------------------------------------
#
# A request is not a task. It is somebody outside the team saying what they want, kept in
# their words until we decide what, if anything, to do — so `asked_by` is a person at a
# customer rather than a company, because a request with no name behind it cannot be asked
# a question.
#
# Three became stories, two were answered no, and three are still waiting. Each carries a
# label so that a request nobody has answered yet is still findable from the work it is
# about; without one it would read to `docket anomalies` as something that fell out of the
# plan, which is the opposite of what an unanswered request is.

REQUESTS = [
    dict(a="req.print-week", t="Can the office print the week for the wall?",
         project=HARBOR, labels="bookings", made="06-18 10:20",
         asked_by="Jonas Vik, harbourmaster at Vik Marina",
         asked_on="2026-06-18", wanted_by="2026-07-10",
         became=["harbor.calendar.print"], became_on="08-05 16:20", ready="08-06 11:00",
         body="## What was asked\n\n"
              "\"The screen is fine but the girl on the desk at the weekend is seventeen "
              "and she is not going to have a laptop open on the pontoon. We printed the "
              "week off the old planner every Friday and it went on the wall by the "
              "kettle. Can it print?\"\n\n"
              "## What they are trying to do\n\n"
              "Hand the weekend over to somebody who is not going to be trained on "
              "anything. The paper is not nostalgia — it is the one artefact in the "
              "harbour office that works when the wifi does not and that four people can "
              "stand in front of at once.\n\n"
              "## What we did about it\n\n"
              "Yes, and it took until August to write down because we kept treating it as "
              "a print stylesheet. It is a view: a week, every berth, who is arriving and "
              "leaving, on one sheet of A3. It is on the board and it is not scheduled."),
    dict(a="req.regatta", t="Can we book the whole east pontoon for the regatta weekend?",
         project=HARBOR, labels="bookings", made="06-26 11:10",
         asked_by="Marit Sandholm, Sandholm Harbour",
         asked_on="2026-06-26", wanted_by="2026-08-14",
         body="## What was asked\n\n"
              "\"We have the regatta in the second week of August and forty boats arrive "
              "together for two nights. At the moment I would have to make forty "
              "bookings, and half of them do not know which boat is on which berth until "
              "they are tied up. Can I just take the east pontoon out of the calendar and "
              "sort it out on the day?\"\n\n"
              "## What they are trying to do\n\n"
              "Sell a block of berths to one organiser and settle the details on the "
              "pontoon. The money is one invoice to the sailing club, not forty; the "
              "allocation is a conversation with a clipboard.\n\n"
              "## What we did about it\n\n"
              "Not yet. There is a story for booking a whole pontoon and it has not been "
              "sized, because the interesting part is not the block booking — it is what "
              "happens to a block when one boat does not turn up and the berth should go "
              "back on sale for the night. Marit ran August's regatta on the old "
              "spreadsheet and has asked again for next year."),
    dict(a="req.lock-quarter", t="Can a quarter be locked so nothing new lands in it?",
         project=LEDGER, labels="tax", made="07-06 09:50",
         asked_by="Elin Bergström, Bergström Accounting",
         asked_on="2026-07-06", wanted_by="2026-10-15",
         became=["ledger.tax.close"], became_on="08-24 12:00", ready="08-24 12:10",
         body="## What was asked\n\n"
              "\"The thing that ruins my October is an invoice appearing in September "
              "after I have filed September. Not a mistake, usually — somebody enters it "
              "late with the right date on it, and now the return I sent and the books "
              "disagree. Whatever you build, I need to be able to shut a period and have "
              "it stay shut.\"\n\n"
              "## What they are trying to do\n\n"
              "Make the return she filed and the books she keeps say the same thing "
              "afterwards, for ever. What she is describing is not a feature — it is the "
              "difference between bookkeeping software and a spreadsheet.\n\n"
              "## What we did about it\n\n"
              "Yes, and it turned into the decision about how a period closes as well as "
              "into the story. She got the version she asked for: a period is open until "
              "somebody closes it, closing has a name and a date on it, and afterwards a "
              "correction is a document in the open period rather than an edit to the "
              "closed one."),
    dict(a="req.kiosk", t="Can we have a kiosk in the office for guests who arrive without the app?",
         project=HARBOR, labels="mobile", made="07-14 10:40",
         asked_by="Marit Sandholm, Sandholm Harbour",
         asked_on="2026-07-14", wanted_by="2026-08-01",
         cancelled="08-14 12:10",
         says=[("08-14 12:20", "ingrid",
                "Rang Marit to say no rather than letting it sit on the board. It was one "
                "conversation and she was fine about it: what she actually wants is for a "
                "guest who turns up at eleven at night to be able to check in without "
                "waking anybody, and the sticker on the cleat does that from the guest's "
                "own phone, in the dark, without a screen in the office to maintain. We "
                "should have said this in July.")],
         body="## What was asked\n\n"
              "\"Half the people who come in have not downloaded anything. Could there be "
              "a screen on the counter they can use — like the ones at the airport — so "
              "the desk is not doing it for them?\"\n\n"
              "## What they are trying to do\n\n"
              "Take the queue off the desk on a Friday evening, when four boats arrive "
              "within twenty minutes and the person on the counter is also answering the "
              "phone.\n\n"
              "## What we did about it\n\n"
              "No. It is the same job as the QR sticker on the cleat, done with hardware "
              "we would have to own and a screen in a building the guest has to walk into "
              "first. The sticker gets a guest into their own booking on their own phone "
              "at the berth, which is where they already are. The kiosk story was "
              "cancelled in Sprint 5 for the same reason, and Marit was told rather than "
              "left to notice."),
    dict(a="req.twenty-minutes", t="Text the customer when the crew is twenty minutes away",
         project=FIELD, labels="routing", made="07-22 11:20",
         asked_by="Halvard Rue, dispatcher at Nordic Field Services",
         asked_on="2026-07-22", wanted_by="2026-09-30",
         body="## What was asked\n\n"
              "\"The single biggest thing you could do for me is stop people ringing to "
              "ask where the van is. If they got a text twenty minutes out I would lose "
              "half my phone calls.\"\n\n"
              "## What they are trying to do\n\n"
              "Get the dispatcher's afternoon back. Every call is two minutes and a lost "
              "thread, and he takes thirty of them a day in the season.\n\n"
              "## What we did about it\n\n"
              "Not yet, and the reason is worth writing down: we send an arrival time "
              "already and it is the one from the morning plan rather than the one from "
              "where the van actually is, which is a bug we found in August. Texting a "
              "customer a number we know to be wrong makes the phone ring more, not less. "
              "The arrival-window story and the estimate bug both have to land before "
              "this is worth building."),
    dict(a="req.van-map", t="A live map of where every van is",
         project=FIELD, labels="routing", made="08-06 10:50",
         asked_by="Halvard Rue, dispatcher at Nordic Field Services",
         asked_on="2026-08-06",
         cancelled="08-25 12:10",
         says=[("08-25 12:20", "ingrid",
                "Answered this properly rather than building it. Halvard asked for a map "
                "and what he needs is for the day to stay driveable when a job overruns — "
                "he watches the map to work out by hand what to move, which is the work we "
                "should be doing for him. The reflow story is in Sprint 6 and he is "
                "getting that instead. The map spike is cancelled.")],
         body="## What was asked\n\n"
              "\"Could I have a map with the vans on it? I have a screen on the wall doing "
              "nothing.\"\n\n"
              "## What they are trying to do\n\n"
              "Work out, at a glance, which crew can take the job that has just come in "
              "and what to move when one of them runs an hour long. The map is the tool he "
              "has for a question the software should be answering.\n\n"
              "## What we did about it\n\n"
              "No, not as a map. A wall of moving dots tells a dispatcher where everybody "
              "is and not what to do about it, and it costs a live position feed off every "
              "phone for the whole day, which is the battery the crew needs for the job. "
              "What he is getting instead is the day rearranging itself when a job "
              "overruns, with what changed shown to him before it is applied."),
    dict(a="req.signature", t="The customer signs for the work on the phone",
         project=FIELD, labels="offline-sync", made="08-13 11:30",
         asked_by="Halvard Rue, dispatcher at Nordic Field Services",
         asked_on="2026-08-13", wanted_by="2026-10-01",
         became=["field.offline.signature"], became_on="08-24 12:20", ready="08-26 12:10",
         body="## What was asked\n\n"
              "\"The paper docket is the last bit of paper we have and it is the one that "
              "loses us money — no signature, no invoice, and the crew has already driven "
              "away. If they could sign on the phone I would bill everything in the same "
              "week it was done.\"\n\n"
              "## What they are trying to do\n\n"
              "Close the gap between the work being finished and the work being billable. "
              "A docket that comes back in a van on Friday is invoiced the following "
              "Thursday, and about one in twenty never comes back at all.\n\n"
              "## What we did about it\n\n"
              "Yes. It is a story in Sprint 6 and the hard half is not the signature — it "
              "is that a signature taken in a valley with no signal has to be as good as "
              "one taken outside the depot, which means it has to survive the same merge "
              "that lost eleven crews their afternoon in July."),
    dict(a="req.deposit", t="Can a guest pay half at booking and the rest on arrival?",
         project=HARBOR, labels="payments", made="08-31 10:30",
         asked_by="Jonas Vik, harbourmaster at Vik Marina",
         asked_on="2026-08-31", wanted_by="2027-04-01",
         body="## What was asked\n\n"
              "\"For a season berth nobody wants to put eighteen thousand on a card in "
              "March. We have always taken a third up front and the rest at Easter. If "
              "Harbor cannot do that I will be taking season money on the phone again next "
              "year.\"\n\n"
              "## What they are trying to do\n\n"
              "Keep the arrangement that gets a season berth sold in March, when the boat "
              "is under a tarpaulin and the owner is not feeling wealthy.\n\n"
              "## What we did about it\n\n"
              "Not yet, and it is the request most likely to be the next thing we build. "
              "There is a story for taking a deposit now and the rest on arrival, and it "
              "is unsized because the question underneath it is not technical: what "
              "happens to the second payment when the season is cut short, which is the "
              "same question that has held the season-rate story in review since the "
              "middle of August."),
]


# --- where the hours went -------------------------------------------------------------
#
# Thirty entries across the last two sprints, written in the evening of the day they
# describe. Each is a child of the work it is about and also points at it with `logs:`,
# which is what the app's own page asks for: the child is the hierarchy a board reads, the
# relation is the annotation a person's page and the worklog board read.
#
# The six parents are all unsized, and that is rule 12 rather than an accident: a task
# that has children may not carry an estimate, because a container's size is what its
# children add up to. So time is logged against the container stories whose sub-tasks hold
# the numbers, and against the two spikes that were investigated rather than estimated —
# one of which was cancelled the week after, which is the whole reason a spike's hours are
# worth recording at all.
#
# Harbor's hours are billable and the other two products' are not. That is not a judgement
# about the work: Harbor is on a contract that bills for time and the other two are not,
# and the flag records the contract rather than the effort.

WORKLOGS = [
    # Sprint 5 — the check-in launch. The container story; its two sub-tasks carry the
    # points, so the hours can hang here without giving rule 12 a second answer.
    dict(a="log.pontoon.1", on="harbor.checkin.pontoon", who="aiko", day="08-10",
         made="08-10 17:20", spent=6, t="Queue flush against a phone with no signal",
         why="Ran the flush against a handset in aeroplane mode all morning and then let "
             "it back on the network: eleven queued check-ins, in order, no duplicates."),
    dict(a="log.pontoon.2", on="harbor.checkin.pontoon", who="priya", day="08-10",
         made="08-10 17:30", spent=3, t="Showing the queued state on the check-in screen",
         why="A check-in that is waiting for signal now says so on the phone, because the "
             "dockhand who cannot tell has no reason to trust the thing twice."),
    dict(a="log.pontoon.3", on="harbor.checkin.pontoon", who="aiko", day="08-11",
         made="08-11 17:10", spent=5, t="Pontoon flow written up for review",
         why="Tidied the flow, wrote the acceptance out properly and put it into review; "
             "most of the day went on the case where the phone dies mid-queue."),
    dict(a="log.pontoon.4", on="harbor.checkin.pontoon", who="priya", day="08-11",
         made="08-11 17:25", spent=2, t="Wet-hands pass over the check-in screen",
         why="Buttons and hit areas gone over for somebody standing on a finger pier in "
             "the rain holding a rope in the other hand."),
    dict(a="log.pontoon.5", on="harbor.checkin.pontoon", who="mateo", day="08-12",
         made="08-12 17:15", spent=4, t="Check-in tested on the pontoon at Vik",
         why="Four hours at Vik with both phones on the real pontoon, which found the "
             "clock skew that the office was never going to show us."),
    dict(a="log.pontoon.6", on="harbor.checkin.pontoon", who="aiko", day="08-12",
         made="08-12 17:40", spent=2, t="Fixing what came back from the pontoon",
         why="Two of the three things mateo found on the pontoon; the third is the clock "
             "and it became a bug of its own."),
    dict(a="log.pontoon.7", on="harbor.checkin.pontoon", who="mateo", day="08-13",
         made="08-13 17:10", spent=3, t="Second pass, and the papers photograph",
         why="Ran the whole check-in again including the boat papers, on both phones, "
             "with the office watching arrivals come in on the calendar."),
    dict(a="log.pontoon.8", on="harbor.checkin.pontoon", who="aiko", day="08-13",
         made="08-13 17:30", spent=2, t="Closing the pontoon story",
         why="Last fixes, notes for the launch weekend, and the story moved to done."),
    dict(a="log.pontoon.9", on="harbor.checkin.pontoon", who="mateo", day="08-14",
         made="08-14 16:50", spent=1, t="Check the launch build on both marina phones",
         why="Half an hour each on the marina's own handsets after the build went out, so "
             "nobody discovers the install on Saturday morning."),

    # A spike, not a story: what a deposit would mean before anybody sizes it.
    dict(a="log.deposit.1", on="harbor.payments.deposit", who="tomasz", day="08-18",
         made="08-18 17:20", spent=3, t="What a deposit means to the provider",
         why="Read what the provider supports for a part payment now and the rest later, "
             "which is three different things depending on how long later is."),
    dict(a="log.deposit.2", on="harbor.payments.deposit", who="tomasz", day="08-19",
         made="08-19 17:10", spent=2, t="Deposit written up as a question, not a plan",
         why="Wrote the story up as far as it goes and stopped: what happens to the second "
             "payment when a season is cut short is a product question, not a technical one."),

    # The map spike, and the week after it was cancelled — the hours are the reason the
    # decision to stop was cheap to make.
    dict(a="log.map.1", on="field.routes.map", who="priya", day="08-18",
         made="08-18 17:00", spent=4, t="A day's route drawn on a map",
         why="Got a day's stops onto a map with the road between them; it looks good and "
             "it does not answer the question the dispatcher is asking it."),
    dict(a="log.map.2", on="field.routes.map", who="priya", day="08-19",
         made="08-19 17:30", spent=3, t="What a live position would cost the phone",
         why="Measured what a position every thirty seconds does to a phone that also has "
             "to last a crew's day: about a fifth of the battery."),
    dict(a="log.map.3", on="field.routes.map", who="priya", day="08-20",
         made="08-20 17:00", spent=2, t="Watched the dispatcher use his own map",
         why="Sat with Halvard for two hours while he used the map he already has, and "
             "wrote down what he was actually working out from it."),

    # Sprint 6 — the conflict work the postmortem bought.
    dict(a="log.conflict.1", on="field.offline.conflict", who="aiko", day="08-26",
         made="08-26 17:20", spent=5, t="Keeping both versions of a job",
         why="Both versions of a job are now held rather than one being chosen; nothing "
             "shows them yet, which is the next thing."),
    dict(a="log.conflict.2", on="field.offline.conflict", who="tomasz", day="08-26",
         made="08-26 17:40", spent=3, t="What the server should do with a version it cannot place",
         why="Went through the merge with aiko so that the rule in the decision and the "
             "rule in the code are the same sentence."),
    dict(a="log.conflict.3", on="field.offline.conflict", who="aiko", day="08-27",
         made="08-27 17:10", spent=6, t="The screen that shows a crew what disagreed",
         why="Most of the day on the screen itself: two versions side by side, in the "
             "crew's own words, with the difference marked."),
    dict(a="log.conflict.4", on="field.offline.conflict", who="tomasz", day="08-28",
         made="08-28 17:00", spent=4, t="Conflicts through the sync queue end to end",
         why="Pushed a conflicting pair through the whole queue from two phones and "
             "watched both survive to the screen."),
    dict(a="log.conflict.5", on="field.offline.conflict", who="aiko", day="08-31",
         made="08-31 17:20", spent=4, t="Choosing a version, and what happens to the other",
         why="A crew can now choose, and the version they did not choose is kept rather "
             "than deleted — which is the half of this the incident was about."),
    dict(a="log.conflict.6", on="field.offline.conflict", who="mateo", day="09-01",
         made="09-01 17:00", spent=3, t="Two phones, one job, no signal",
         why="Made the conflict happen on purpose with two handsets in aeroplane mode and "
             "wrote down each shape it comes out in."),
    dict(a="log.conflict.7", on="field.offline.conflict", who="aiko", day="09-02",
         made="09-02 17:30", spent=5, t="Photographs and signatures through a conflict",
         why="An attachment attached to the version nobody chose was being dropped; it is "
             "kept now and shown with the version it came from."),
    dict(a="log.conflict.8", on="field.offline.conflict", who="tomasz", day="09-02",
         made="09-02 17:45", spent=2, t="A depot's worth of reconnections, first go",
         why="Twenty phones coming back at once against staging: nothing lost, and the "
             "last one waits about ninety seconds, which is not good enough yet."),
    dict(a="log.conflict.9", on="field.offline.conflict", who="mateo", day="09-03",
         made="09-03 17:10", spent=3, t="Conflict scenarios written down",
         why="One scenario per conflict shape rather than the single happy path we had in "
             "July, and two of them fail on purpose."),
    dict(a="log.conflict.10", on="field.offline.conflict", who="aiko", day="09-04",
         made="09-04 16:40", spent=4, t="Conflict screen on a real crew phone",
         why="Ran the whole thing on a crew's own handset before the weekend; it is not "
             "finished and it is the first version a dispatcher could be shown."),

    # Groundwork for Sprint 7, done in Sprint 6 because the decision was taken.
    dict(a="log.credit.1", on="ledger.invoices.credit-notes", who="tomasz", day="08-27",
         made="08-27 17:20", spent=2, t="Reading what a credit note has to be",
         why="Two hours with Elin's own credit notes from last year, which is where the "
             "rule about never exceeding the invoice came from."),
    dict(a="log.credit.2", on="ledger.invoices.credit-notes", who="tomasz", day="08-28",
         made="08-28 17:20", spent=3, t="Credit note against an invoice, on paper",
         why="Worked the numbering and the tax lines through by hand for a partial refund "
             "before writing any of it."),
    dict(a="log.credit.3", on="ledger.invoices.credit-notes", who="priya", day="09-01",
         made="09-01 17:25", spent=2, t="What a credit note looks like in the PDF",
         why="Laid a credit note out against the invoice it credits, so the pair reads as "
             "one thing on an accountant's desk."),
    dict(a="log.credit.4", on="ledger.invoices.credit-notes", who="tomasz", day="09-03",
         made="09-03 17:30", spent=4, t="Harbor's refund against a Ledgerline credit note",
         why="Walked a Harbor refund all the way through to a credit note on staging to "
             "find out what Sprint 7 is actually going to cost."),

    dict(a="log.rounding.1", on="ledger.tax.rounding", who="tomasz", day="08-24",
         made="08-24 17:10", spent=3, t="Which rounding the rules actually want",
         why="Read the Norwegian and Swedish rules on rounding per line against per "
             "invoice, and they do not agree with each other."),
    dict(a="log.rounding.2", on="ledger.tax.rounding", who="tomasz", day="08-25",
         made="08-25 17:20", spent=2, t="Rounding written up for the tax stories",
         why="Wrote down what the two rules mean for an invoice of forty lines, which is "
             "eleven øre and an argument with an auditor."),
]


# --- the six decisions ----------------------------------------------------------------
#
# `docs/spec/documents.md` is normative and this is what it asks for: four sections in
# order, a status and a date in the frontmatter, a number that is never reused, and a
# heading that makes the number sayable. What it cannot check is whether the Context
# states a problem, whether the alternatives were live options, and whether the cost named
# is the real one — so each of these was written to be readable a year later by somebody
# who finds the choice inconvenient.
#
# Tasks are named by key in backticks and never linked. A decision is not a place where
# work gathers, and `{alias}` here is spelled out into a key by the engine when the page
# is written — which is why a decision may only name work that existed on the day it was
# taken.

DECISIONS = [
    dict(n="0001", slug="one-vault-for-three-products", t="One vault for three products",
         when="06-15 16:20", who="ingrid",
         body="# ADR-0001 — One vault for three products\n\n"
              "## Context\n\n"
              "Northlight is six people building three products for the same stretch of "
              "coast: Harbor for marinas, Ledgerline for the accountants who bill for "
              "them, and Fieldnote for the crews who service the boats. The three are "
              "separate products with separate customers, and everybody on the team works "
              "on at least two of them in any given fortnight.\n\n"
              "We had to decide, before anything was written down, whether that is three "
              "projects or one. It is not a question we can defer: the first week produces "
              "keys, and a key is the thing people say out loud for the rest of the "
              "product's life. Two dependencies were already visible on the whiteboard on "
              "day one. A refund in Harbor has to become a credit note in Ledgerline or "
              "the marina's accountant cannot explain it. And the hardest problem in "
              "Fieldnote — a phone that works for a day with no signal — is the same "
              "problem as checking a boat in from a pontoon, which is Harbor's.\n\n"
              "## Decision\n\n"
              "**All three products live in one vault, on one board, in one key space, "
              "separated by a project prefix: HARBOR, LEDGER and FIELD.**\n\n"
              "A relation crosses projects like any other link, so the refund story can "
              "say it is blocked by the credit-note story and both cards show it. A sprint "
              "is the team's fortnight rather than a product's, because the team is one "
              "team and pretending otherwise would mean three planning sessions for six "
              "people. The prefix carries which product something belongs to, and it "
              "carries it in the one place everybody reads: the key.\n\n"
              "This also settles where cross-cutting things go. A risk that threatens "
              "Harbor's payments is a HARBOR task; an objective about closing a quarter is "
              "a LEDGER one. There is no fourth project for the team itself, and there "
              "should not be — work that belongs to everybody belongs to nobody, and the "
              "board that filters by product is the one people actually open.\n\n"
              "## What this costs\n\n"
              "One backlog is longer than any one person wants to read. Somebody who only "
              "cares about Fieldnote scrolls past two products' worth of tax and berths to "
              "find their own work, and the default view of this vault is not useful to "
              "anybody — filtering stops being a convenience and becomes the only way in. "
              "Every board here is a saved filter for that reason.\n\n"
              "The sprint goal is the sharper cost. A fortnight that serves three products "
              "either gets one sentence that is true of all of them, which is usually "
              "vague, or three sentences wearing one coat. Sprint 3 was \"bank import for "
              "Ledgerline\" and Harbor did a sprint's work underneath it that the goal did "
              "not mention.\n\n"
              "And a customer conversation is now harder to have from the board. Nothing "
              "here says which marina is waiting for what; that lives in requests and in "
              "people's heads, which is fine at four customers and will not be at forty.\n\n"
              "## Alternatives considered\n\n"
              "**Three vaults, one per product.** Rejected because the two dependencies "
              "that hurt most cross the boundary. A link between repositories is a URL in "
              "a comment: it does not appear in a backlink, a graph or a board, and it "
              "rots the first time something is renamed. We would have discovered the "
              "refund and credit-note pair by having the argument twice.\n\n"
              "**One vault, one project, and a label per product.** Rejected because the "
              "key is what people say. \"HARBOR-41\" tells you which product you are "
              "talking about with no lookup, in a commit message, in a corridor and in a "
              "phone call to a marina; a label does not appear in a key and a numbering "
              "shared across three products makes the number meaningless.\n\n"
              "**One vault now, split when it hurts.** This is the one to revisit, and it "
              "is worth saying why we did not simply plan for it: splitting later means "
              "renumbering, and a key that moves is not a name. If this becomes wrong it "
              "will be because the team has grown into three teams, and at that point the "
              "split is worth its price rather than free."),
    dict(n="0002", slug="payments-go-through-one-provider",
         t="Payments go through one provider", when="06-24 15:40", who="tomasz",
         keys=True,
         body="# ADR-0002 — Payments go through one provider\n\n"
              "## Context\n\n"
              "`{harbor.payments}` needs to take a card at the moment a berth is booked "
              "and hand money back when the weather cancels a weekend, and it needs to do "
              "it in eight weeks. `{ledger.invoices}` will need to take payment for an "
              "invoice within the year, against the same businesses.\n\n"
              "So the choice is not really which provider. It is whether we build against "
              "one of them directly, or build the abstraction that would let us hold two. "
              "Marinas take a year's revenue in eight weeks, which means the day a "
              "provider stops working for us is a day a marina loses its season — and "
              "there is no way to make that day painless. There is only a choice about "
              "what we pay in advance to make it less likely.\n\n"
              "## Decision\n\n"
              "**Both products take money through one provider, called from one internal "
              "payments module that Harbor and Ledgerline both use.**\n\n"
              "The module exists because two products calling a payment API two different "
              "ways is how a refund comes to mean two things. It is not a provider "
              "abstraction: it speaks this provider's vocabulary, holds this provider's "
              "idempotency rules, and would have to be rewritten rather than reconfigured "
              "to speak to another one. That is deliberate.\n\n"
              "One provider means one sandbox, one webhook shape, one set of keys to keep "
              "out of the repository, one refund model to explain to an accountant, and "
              "one set of failure modes for the whole team to learn rather than two sets "
              "for half the team each.\n\n"
              "What the three products do and do not share, and why this is the one "
              "dependency between two of them that was chosen rather than grown, is "
              "[[architecture|the architecture page]].\n\n"
              "## What this costs\n\n"
              "The day this provider suspends a marina's account, holds funds while it "
              "asks about a suspicious eight-week revenue curve, or changes an endpoint "
              "with a month's notice, both products stop taking money and there is nothing "
              "to fail over to. That is on the risk register with a name against it, and "
              "the honest mitigation is a phone number for an escalation contact and a "
              "marina taking cards on arrival for a day. It is not a technical answer, "
              "because there is not one.\n\n"
              "We also lose the ability to negotiate. A provider that knows it is the only "
              "one integrated prices accordingly at renewal, and the cost of moving is a "
              "rewrite rather than a configuration change.\n\n"
              "And the module will read as an abstraction to whoever opens it next. It is "
              "not one, and the first person who tries to add a second provider behind it "
              "will find that out expensively — which is why it is written here.\n\n"
              "## Alternatives considered\n\n"
              "**Two providers behind a routing layer from the start.** Rejected because "
              "it doubles the integration work in the sprint that has to ship a season, "
              "and because the layer would have been designed against two providers we had "
              "not yet operated. The failure we are guarding against is rare; the cost of "
              "guarding against it lands every fortnight.\n\n"
              "**One provider now, behind a real abstraction, so a second is cheap "
              "later.** Rejected because an abstraction written against one implementation "
              "is that implementation with different words on it. Every seam we would have "
              "guessed at — refunds, disputes, the shape of a webhook, when a charge is "
              "final — is exactly where two providers actually differ, and we would have "
              "guessed them all from one example.\n\n"
              "**Take payment through the marina's own provider, whichever it is.** This "
              "is the one worth revisiting when we are talking to forty marinas rather "
              "than four, because several of them already have a card terminal and a "
              "contract. Rejected now because it makes every marina's onboarding a bespoke "
              "integration, and we have six people."),
    dict(n="0003", slug="bank-imports-are-idempotent-by-statement-hash",
         t="Bank imports are idempotent by statement hash", when="07-15 11:20",
         who="tomasz", keys=True,
         body="# ADR-0003 — Bank imports are idempotent by statement hash\n\n"
              "## Context\n\n"
              "The bank import went in this sprint and the first thing it did on real data "
              "was produce two of everything, because an accountant who is not sure "
              "whether an import worked imports it again. That is `{ledger.bank.dedupe}`, "
              "and it is not a bug in the sense of somebody having made a mistake: nothing "
              "in the design said what the same statement twice was supposed to mean.\n\n"
              "A week earlier `{harbor.payments.double-charge}` had the same shape from "
              "the other end — a guest who was not sure whether a payment had worked "
              "pressed the button again, and a system with no way to say \"this is the "
              "same intention as the last one\" charged the card twice. Two products, two "
              "weeks, one missing idea.\n\n"
              "The three banks our first accountants use make it worse rather than better. "
              "One has an API with a transaction id; two send a file. Neither of the two "
              "guarantees that a statement fetched twice is byte-identical, and one of them "
              "reissues a corrected statement for the same period under the same name.\n\n"
              "## Decision\n\n"
              "**A statement is identified by the hash of its normalised content, and every "
              "line by the hash of that statement plus the line's position in it. "
              "Importing a statement whose hash we already hold is a no-op that reports "
              "what it skipped.**\n\n"
              "Normalisation is the part with the rules in it: line endings, the "
              "thousands separator, trailing whitespace and the header rows that carry the "
              "fetch time rather than the data. Everything that survives normalisation is "
              "content, and content decides identity.\n\n"
              "The line's position matters because a business that pays the same supplier "
              "the same amount on the same day twice is not making a mistake, and two "
              "lines that are identical in every field are two payments.\n\n"
              "What the import does with a line once it has one is "
              "[[ledgerline|Ledgerline's design page]].\n\n"
              "## What this costs\n\n"
              "The normalisation rules are where every future bug lives. A bank that adds "
              "a column, changes a date format or pads an amount produces a different "
              "hash for the same statement, and the import silently duplicates rather than "
              "silently skipping — which is the worse of the two failures and the one "
              "nobody notices until a quarter is being closed. Every new bank adds a rule "
              "to a function that is already the most delicate thing in the importer.\n\n"
              "A restated statement cannot be corrected in place. When the bank reissues a "
              "period, we import it as a new statement and somebody has to reconcile the "
              "two by hand, because we have deliberately made ourselves unable to tell a "
              "correction from a fresh document.\n\n"
              "And the hash is not readable. When an import does nothing, the message a "
              "person gets is that this statement was already imported on a date, which is "
              "the best we can do and is not the same as showing them why.\n\n"
              "## Alternatives considered\n\n"
              "**Match on the bank's own transaction id.** Rejected because two of our "
              "three banks do not send one, and the third's is unique per fetch rather "
              "than per transaction — the same payment fetched on Tuesday and Wednesday "
              "arrives with two different ids. A rule that works for one bank and has to "
              "be special-cased for two is not a rule.\n\n"
              "**De-duplicate on date, amount and reference together.** Rejected because "
              "it makes a genuine second payment invisible. A business that pays two "
              "identical invoices to the same supplier on the same day is ordinary, and an "
              "importer that swallows the second one is worse than one that duplicates: a "
              "duplicate is seen and deleted, a missing line is found in October.\n\n"
              "**Ask the person: \"you have imported this before, continue?\"** Rejected "
              "because it is the same question the accountant could not answer in the "
              "first place. They import twice precisely because they do not know whether "
              "the first one worked, and a dialogue that asks them to know is a dialogue "
              "they will click through."),
    dict(n="0004", slug="the-phone-is-the-source-of-truth-for-a-job",
         t="Offline first: the phone is the source of truth for a job",
         when="07-31 11:30", who="aiko", keys=True,
         body="# ADR-0004 — Offline first: the phone is the source of truth for a job\n\n"
              "## Context\n\n"
              "On Wednesday 29 July eleven crews lost an afternoon's work. Their phones "
              "came back into signal at the depot, the merge saw that the server had "
              "touched every job since the phone last saw it, and it kept the server's "
              "version of every field. Thirty-four jobs went back to how they had looked "
              "at seven that morning: no notes, no parts, no photographs, and two jobs the "
              "customer had signed for marked unfinished. That is "
              "`{field.offline.sync-loss}`; the incident is written up in this vault and "
              "the postmortem is being drafted this week.\n\n"
              "The rule that did it — last writer wins, and the server counts as the "
              "writer whenever it has touched the row — was a line in the sync code. It "
              "read as reasonable there. It was never written anywhere a dispatcher, a "
              "product person or the other four engineers could see it, so nobody ever had "
              "the chance to say the obvious thing: a day in a dead zone is precisely the "
              "case where the phone is right and the server is a stale copy from seven in "
              "the morning.\n\n"
              "The same question is now live in a second product. "
              "`{harbor.checkin.pontoon}` queues check-ins on a phone with no signal and "
              "flushes them later, and it will need an answer to the same conflict within "
              "the month. Deciding this once, in writing, is the point.\n\n"
              "## Decision\n\n"
              "**For a job, the phone is the source of truth. The server never overwrites "
              "a field that a phone changed while it was offline, and anything the server "
              "cannot reconcile is kept rather than dropped.**\n\n"
              "Where the two genuinely disagree — the phone changed a field and a "
              "dispatcher changed the same field while the crew was out — both versions "
              "are held and the crew is shown what disagreed and asked to choose. Nothing "
              "is resolved silently in either direction.\n\n"
              "\"Kept rather than dropped\" is the load-bearing half. A merge that cannot "
              "decide must never delete: the version nobody chose stays, attached to the "
              "job, until somebody says otherwise. Storage is cheap and a crew's afternoon "
              "is not.\n\n"
              "This is a rule about jobs. It is not a rule about the schedule: which crew "
              "is on which job tomorrow is the dispatcher's to decide and the server holds "
              "it.\n\n"
              "How the rest of the day fits around that is "
              "[[fieldnote|Fieldnote's design page]].\n\n"
              "## What this costs\n\n"
              "A dispatcher's correction no longer takes effect while a crew is out. If he "
              "fixes an address at eleven and the crew has already edited the job, the "
              "crew's version wins and he has to say it again — and he will find that "
              "annoying, correctly, because he was right and the software preferred "
              "somebody else.\n\n"
              "Two versions of a job can now exist for hours, so every screen that shows a "
              "job has to be able to show that. The conflict screen is real work nobody "
              "had planned for and it is the largest thing on the next fortnight.\n\n"
              "And a job carries its history rather than its state, so the data grows with "
              "every conflict and never shrinks on its own. We have not decided when a "
              "kept version may be thrown away, which means for now it never is.\n\n"
              "## Alternatives considered\n\n"
              "**Last write wins by timestamp.** Rejected because the phone's clock is the "
              "thing we trust least in the whole system. A handset that has been off the "
              "network since seven in the morning has no better idea what time it is "
              "than we do, and two of the test phones already disagree with each other "
              "by minutes. Deciding whose work survives with a number the device made "
              "up is not a rule, it is a coin.\n\n"
              "**Server wins, which is what we had.** Rejected for the reason the incident "
              "showed: the server is authoritative about everything except the one thing "
              "the crew was actually doing, and the longer a crew is offline — which is to "
              "say, the more work they have done — the more of it this throws away.\n\n"
              "**Merge per field with no winner.** Rejected because two fields of one job "
              "taken from two versions produce a job that nobody wrote. A crew reading it "
              "back cannot recognise their own work, and the first time that reaches a "
              "customer it costs more than the incident did.\n\n"
              "**Lock a job to a crew while they hold it offline.** The closest call. "
              "Rejected because a lock has to be released by something, and the thing that "
              "would release it is the network the crew does not have."),
    dict(n="0005", slug="tax-periods-close-by-decision",
         t="Tax periods close by decision, not by date", when="08-18 15:10",
         who="tomasz", keys=True,
         body="# ADR-0005 — Tax periods close by decision, not by date\n\n"
              "## Context\n\n"
              "`{ledger.tax}` has to decide when a quarter stops accepting entries, and "
              "the obvious answer is wrong in a way that only shows up in October.\n\n"
              "A quarter ends on 30 September. The books for that quarter do not: an "
              "accountant is still entering September's invoices in the second week of "
              "October, with September dates on them, and that is not sloppiness — it is "
              "how the work arrives. The return is filed some time after that, and from "
              "the moment it is filed the period must not change, because the number in "
              "the return and the number in the books have to agree for ever afterwards.\n\n"
              "So there are two dates that matter and neither is the end of the quarter: "
              "the day the books for it are finished, and the day the return goes. Every "
              "accountant we have asked has a different gap between them, and one of them "
              "described the invoice that appears in a filed period as the thing that "
              "ruins her October.\n\n"
              "## Decision\n\n"
              "**A tax period is open until somebody closes it. Closing is an act, with "
              "the person and the moment recorded on it, and after it nothing can be "
              "booked into that period at all.**\n\n"
              "A correction to a closed period is a document in the open period that "
              "refers to the closed one — never an edit to what is closed. That is what an "
              "accountant does on paper and it is what an auditor expects to find.\n\n"
              "A period that is closed can be reopened, by a person, and the reopening is "
              "recorded the same way the closing was. Refusing to allow it would be "
              "pretending nobody ever closes a quarter by mistake at half past four on a "
              "Friday.\n\n"
              "What a period is made of, and what else this product does with it, is "
              "[[ledgerline|Ledgerline's design page]].\n\n"
              "## What this costs\n\n"
              "A quarter can stay open indefinitely, and a business that never closes one "
              "gets a report that changes underneath it every time somebody enters "
              "something old. The software cannot save them from that; the most it can do "
              "is say how long a period has been open and how many entries have landed in "
              "it since the quarter ended, and then keep saying it.\n\n"
              "Two periods being open at once is now a normal state rather than an error, "
              "so every query, every report and every screen has to say which period it "
              "means. That is a running cost on everything we build in this product from "
              "here.\n\n"
              "And an entry can be refused for a reason that is nowhere in the entry: the "
              "date is fine, the amounts are fine, and the period is shut. That error "
              "message has to say who closed it and when, or it reads as a bug.\n\n"
              "## Alternatives considered\n\n"
              "**Close on the calendar date.** Rejected because it puts the honest work — "
              "entering September's invoices in October — outside the period it belongs "
              "to, and it would land in the wrong quarter. The software would be forcing "
              "an accountant to file a return she knows to be incomplete.\n\n"
              "**A grace period of N days after the quarter ends.** Rejected because N is "
              "a number nobody can defend. Every accountant we asked gave a different one, "
              "the good answer depends on the business's own customers, and a default here "
              "silently becomes a policy for everybody who does not change it.\n\n"
              "**Allow back-dated entries into a closed period, with an audit trail.** "
              "Rejected because a return that has already been filed cannot be un-filed by "
              "an audit trail. The trail records that the books and the return stopped "
              "agreeing; it does not stop it happening, and the whole value of closing is "
              "that it cannot happen."),
    dict(n="0006", slug="refunds-are-credit-notes", t="Refunds are credit notes",
         when="08-27 15:30", who="tomasz", keys=True,
         body="# ADR-0006 — Refunds are credit notes\n\n"
              "## Context\n\n"
              "`{harbor.payments.refunds}` gives a guest their money back when the weather "
              "cancels a weekend, and `{ledger.invoices.credit-notes}` has to make that "
              "explicable to the marina's accountant. The two have been circling each "
              "other since June: the refund story is blocked by the credit-note story and "
              "has been sitting in Sprint 6 waiting for this.\n\n"
              "What forced it now is a question nobody could answer on Tuesday: what "
              "stops a refund being larger than the invoice it refunds. Harbor knows "
              "what it charged. Nothing on the accounting side knows what may be given "
              "back, because there is nothing on the accounting side yet.\n\n"
              "There are two coherent ways to record money going back out. It is a "
              "negative payment against the invoice, or it is a document of its own that "
              "credits the invoice. They look similar until a quarter is closed, and then "
              "they are nothing alike.\n\n"
              "## Decision\n\n"
              "**Every refund is a credit note against the invoice it refunds. The card "
              "refund is what the credit note causes, not the other way round.**\n\n"
              "So the sequence is one way only: a credit note is issued against an "
              "invoice, and issuing it is what tells Harbor to return money to the card "
              "the payment came from. A refund cannot exist without one, which is what "
              "makes a refund larger than the invoice impossible rather than merely "
              "checked for — a credit note cannot credit more than the invoice it is "
              "written against, and there is no other path to the card.\n\n"
              "A credit note carries its own number in the same unbroken sequence as "
              "invoices, its own tax lines, and a reference to what it credits. It is a "
              "document the business sends, not a state on another document.\n\n"
              "What that sequence has to survive is "
              "[[ledgerline|Ledgerline's design page]].\n\n"
              "## What this costs\n\n"
              "Harbor's refund flow now depends on Ledgerline being up. A marina that "
              "wants to refund a guest standing in front of them cannot do it while the "
              "accounting side is down, and \"refund later\" is a poor answer on a pontoon. "
              "That is a real coupling between two products we deliberately keep "
              "separable, and it is the price of the invoice and the refund telling the "
              "same story.\n\n"
              "Refunding a booking that was never invoiced — a deposit taken and returned "
              "the same week, which happens — now needs an invoice first, or a special "
              "case. We have chosen the invoice, so a guest may get paperwork for "
              "something they thought was a phone call.\n\n"
              "And a partial refund needs line items to credit, which means Harbor has to "
              "send an invoice that has them. \"One booking, one line\" was doing fine "
              "until this.\n\n"
              "## Alternatives considered\n\n"
              "**A negative payment against the invoice.** Rejected because it leaves the "
              "invoice saying a total that was never true. An accountant cannot hand in a "
              "document whose total has changed since it was sent, and a customer who "
              "compares the invoice in their inbox with the one in the system finds two "
              "different numbers.\n\n"
              "**A refund with no ledger record at all, reconciled from the bank "
              "statement.** Rejected because that is the spreadsheet we are replacing. It "
              "works right up until the quarter is closed and somebody has to explain a "
              "line of money leaving that no document accounts for.\n\n"
              "**A credit note only when the invoice has been sent, a plain reversal "
              "before that.** Genuinely tempting, and rejected because \"sent\" is a state "
              "that changes: an invoice that was reversed quietly on Tuesday and sent on "
              "Wednesday leaves two conflicting histories, and the rule that decides which "
              "happened is the kind of rule that produces the next postmortem."),
]


# --- design pages and the front page --------------------------------------------------
#
# A design page explains how something works and why it is that way, for somebody who has
# to change it. `docs/spec/documents.md` gives it no required sections on purpose — an
# argument has the shape its argument has — and asks three things of it instead: say what
# the page is about before any detail, say honestly what the approach costs, and say what
# is unbuilt as unbuilt rather than in the present tense.
#
# Each of the four was written on the second morning and rewritten once, when something
# happened that made the first version wrong. The rewrites are what a design page is for;
# a decision may not be edited and this may.
#
# Tasks are named by key in backticks here too. The vocabulary sections are the part that
# earns the page: three products, three sets of nouns, and a team that moves between them
# every fortnight.

DESIGN = [
    dict(path="docs/design/harbor.md", title="Harbor", when="06-16 11:20", who="ingrid",
         body="# Harbor\n\n"
              "Harbor is booking software for a small marina, and the claim it makes is "
              "that one sentence holds the whole product: **this boat has that berth from "
              "this day to that day.** Everything else — the invoice, the card payment, "
              "the calendar on the office wall, the check-in on the pontoon — hangs off "
              "that sentence being true and being in one place.\n\n"
              "What it replaces is a wall planner: one sheet of paper, a season's berths "
              "down the side, the weeks across the top, and pencil. The planner is not "
              "primitive. It is readable from across the room by four people at once, it "
              "works when the wifi does not, and everybody in the harbour office already "
              "knows how to use it. Anything we build is measured against it.\n\n"
              "## The flows\n\n"
              "**Booking.** Someone asks for a berth for a range of dates. Harbor answers "
              "which berths are free for that range — by length, draught and shore power, "
              "because a nine-metre boat does not fit a seven-metre berth — holds one for "
              "twenty minutes while the guest pays, and confirms it. The hold is what "
              "stops two people buying the same berth while one of them is typing a card "
              "number, and it is the reason availability and the write cannot be two "
              "separate reads.\n\n"
              "**Money.** Confirmation takes a card payment, and cancellation gives it "
              "back. An invoice goes to the guest priced at the rate that applied on the "
              "day the booking was made, not today's rate, so that a marina which raises "
              "its prices in August does not reissue June's invoices at August's money.\n\n"
              "**The calendar.** A month of every berth on one screen, readable across the "
              "office. Arrivals, departures, and the slip that has been empty for a "
              "fortnight, without clicking anything.\n\n"
              "**Check-in.** A guest arrives at a pontoon with one bar of signal and a wet "
              "phone. Harbor finds the booking, confirms the boat, photographs the papers, "
              "and shows the office all of it whenever the phone next has a network.\n\n"
              "## The vocabulary\n\n"
              "A **berth** is a physical place a boat is tied to; it has a length, a "
              "depth, and shore power or not. A **booking** is one boat in one berth for a "
              "range of nights. A **hold** is a booking that has not been paid for yet and "
              "expires. **Check-in** is the arrival, which is a different event from the "
              "booking and can happen weeks later. A **season** booking is priced by the "
              "month rather than the night, and is the thing most likely to be cut short.\n\n"
              "The word we avoid is \"reservation\", because half the marinas use it for a "
              "hold and half for a confirmed booking, and the ambiguity is exactly where "
              "double-bookings live.\n\n"
              "## What this costs, and what is not built\n\n"
              "Holding availability and the booking write together is what makes the hold "
              "correct and it is also the slowest thing in the product; the month view "
              "needs a cache to stay usable on a four-hundred-berth marina. Group "
              "bookings, a waiting list for a full week, and printing the week for the "
              "office wall are all unbuilt. So is anything to do with the winter: Harbor "
              "currently assumes boats are in the water."),
    dict(path="docs/design/harbor.md", title="Harbor", when="08-21 16:20", who="ingrid",
         keys=True, update=True,
         body="# Harbor\n\n"
              "Harbor is booking software for a small marina, and the claim it makes is "
              "that one sentence holds the whole product: **this boat has that berth from "
              "this day to that day.** Everything else — the invoice, the card payment, "
              "the calendar on the office wall, the check-in on the pontoon — hangs off "
              "that sentence being true and being in one place.\n\n"
              "What it replaces is a wall planner: one sheet of paper, a season's berths "
              "down the side, the weeks across the top, and pencil. The planner is not "
              "primitive. It is readable from across the room by four people at once, it "
              "works when the wifi does not, and everybody in the harbour office already "
              "knows how to use it. Anything we build is measured against it, and the one "
              "thing it still does better is print.\n\n"
              "## The flows\n\n"
              "**Booking.** Someone asks for a berth for a range of dates. Harbor answers "
              "which berths are free for that range — by length, draught and shore power — "
              "holds one for twenty minutes while the guest pays, and confirms it. The "
              "hold is what stops two people buying the same berth while one of them is "
              "typing a card number: `{harbor.booking.double-book}` was two separate reads "
              "with nothing between them, and fixing it properly meant changing how a hold "
              "is created rather than adding a lock.\n\n"
              "**Money.** Confirmation takes a card payment, and cancellation gives it "
              "back. An invoice is priced at the rate that applied on the day of the "
              "booking, not today's. Anything that spends money is idempotent by "
              "construction and says so in its acceptance — that rule was bought with "
              "eleven duplicate charges in July, and the reasoning is in "
              "[[0003-bank-imports-are-idempotent-by-statement-hash|ADR-0003]]. Which "
              "provider takes the money, and why there is only one, is "
              "[[0002-payments-go-through-one-provider|ADR-0002]].\n\n"
              "**The calendar.** A month of every berth on one screen, readable across the "
              "office. The month query is cached because the honest version took two and a "
              "half seconds on Sandholm's four hundred and six berths, which is a screen "
              "nobody leaves open.\n\n"
              "**Check-in.** This is the part that changed. A guest arrives at a pontoon "
              "with one bar of signal and a wet phone; the dockhand scans the sticker on "
              "the cleat, which opens that berth's booking, confirms the boat, photographs "
              "the papers, and queues the lot. The office sees it when the phone next has "
              "a network. Two dockhands ran a whole weekend on their own phones in the "
              "rain in August, which is the only test of this that counts.\n\n"
              "## The vocabulary\n\n"
              "A **berth** is a physical place a boat is tied to; it has a length, a "
              "depth, and shore power or not. A **booking** is one boat in one berth for a "
              "range of nights. A **hold** is a booking that has not been paid for yet and "
              "expires. **Check-in** is the arrival, which is a different event from the "
              "booking and can happen weeks later — a queued check-in carries the time the "
              "phone thought it was, which is why `{harbor.checkin.clock-skew}` put "
              "arrivals in the future. A **season** booking is priced by the month rather "
              "than the night.\n\n"
              "The word we avoid is \"reservation\", because half the marinas use it for a "
              "hold and half for a confirmed booking, and the ambiguity is exactly where "
              "double-bookings live.\n\n"
              "## What this costs, and what is not built\n\n"
              "The queue on the phone is the price of the pontoon working at all: every "
              "screen that shows an arrival now has to be able to show one that has not "
              "reached us yet. Group bookings, a waiting list, and printing the week for "
              "the office wall are all unbuilt, and the last of those is a customer "
              "request that has been waiting since June. What happens to a season booking "
              "that is cut short is not decided, which is why the season-rate story has "
              "sat in review since the middle of August. Harbor still assumes boats are in "
              "the water: there is nothing here about winter storage.\n\n"
              "What Harbor shares with the other two products, and what it deliberately "
              "does not, is [[architecture|the architecture page]]."),
]

DESIGN += [
    dict(path="docs/design/ledgerline.md", title="Ledgerline", when="06-16 11:40",
         who="ingrid",
         body="# Ledgerline\n\n"
              "Ledgerline is bookkeeping for a business too small to have a finance "
              "department and too real to be run out of a spreadsheet. The claim is "
              "narrower than \"accounting software\": **the quarter closes out of "
              "Ledgerline and the spreadsheet stays shut.**\n\n"
              "That is a deliberate target. Every accountant we have spoken to already has "
              "software, and every one of them also has a spreadsheet beside it where the "
              "quarter is actually assembled — numbers gathered by hand from four places "
              "and typed into a return. The invoicing they will tolerate anywhere. The "
              "fortnight at the end of the quarter is the thing worth paying to be rid "
              "of.\n\n"
              "## The flows\n\n"
              "**Invoicing.** An invoice is written line by line with the tax shown per "
              "line, numbered in one unbroken sequence per business year, rendered as a "
              "PDF the customer's accountant will accept, and emailed with some idea of "
              "whether it arrived. The numbering is not a detail: a gap in the sequence is "
              "a question an auditor asks, so the number is allocated once and never "
              "reused, even when an invoice is abandoned.\n\n"
              "**Bank import.** A statement comes in from the bank — through an API where "
              "there is one, as a file where there is not — and each line is matched "
              "against the invoice it pays, on amount, date and whatever reference the "
              "payer typed. What the importer cannot guess goes to a screen where a person "
              "matches it by hand, and that screen is the product's honest half: the "
              "matching that cannot be automated is the work the spreadsheet was doing.\n\n"
              "**Tax.** Rates that apply on the day rather than today, the rounding rules, "
              "and the quarterly return an accountant can hand to the authority without "
              "retyping it.\n\n"
              "## The vocabulary\n\n"
              "An **invoice** is a document that has been sent; before that it is a draft "
              "and it has no number. A **credit note** is a document that credits an "
              "invoice — it is not a negative invoice and not a state on one. A "
              "**statement** is one bank's record of a period; a **line** is one movement "
              "on it. **Matching** joins a line to the invoice it pays, and a line may "
              "match nothing, which is a normal outcome and not an error. A **period** is "
              "a tax quarter, and it is either open or closed.\n\n"
              "We say **business** rather than \"company\" throughout, because half our "
              "first customers are sole traders and the word matters to them.\n\n"
              "## What this costs, and what is not built\n\n"
              "Matching on amount, date and reference is a heuristic, and a heuristic that "
              "is right nine times in ten is wrong once a week for a business with fifty "
              "invoices a month. Every wrong match is worse than a missing one, so the "
              "importer is deliberately conservative and the manual screen is busier than "
              "it would need to be if we were braver.\n\n"
              "Recurring invoices, chasing a late one, and rounding tax per line versus per "
              "invoice are all unbuilt. So is anything an accountant would call double "
              "entry: Ledgerline records what happened to a business's money and does not "
              "yet keep the books in the form an auditor would want to see them."),
    dict(path="docs/design/ledgerline.md", title="Ledgerline", when="09-02 16:10",
         who="ingrid", keys=True, update=True,
         body="# Ledgerline\n\n"
              "Ledgerline is bookkeeping for a business too small to have a finance "
              "department and too real to be run out of a spreadsheet. The claim is "
              "narrower than \"accounting software\": **the quarter closes out of "
              "Ledgerline and the spreadsheet stays shut.**\n\n"
              "That is a deliberate target. Every accountant we have spoken to already has "
              "software, and every one of them also has a spreadsheet beside it where the "
              "quarter is actually assembled. The invoicing they will tolerate anywhere. "
              "The fortnight at the end of the quarter is the thing worth paying to be rid "
              "of, and as of this week it is the part of the product that exists.\n\n"
              "## The flows\n\n"
              "**Invoicing.** An invoice is written line by line with the tax shown per "
              "line, numbered in one unbroken sequence per business year, rendered as a "
              "PDF, and emailed with some idea of whether it arrived. The number is "
              "allocated once and never reused, even when an invoice is abandoned, because "
              "a gap in the sequence is a question an auditor asks — and "
              "`{ledger.invoices.same-number}` showed how easily two invoices issued in "
              "the same minute can claim one.\n\n"
              "**Bank import.** A statement comes in from the bank — through an API where "
              "there is one, as a file where there is not — and each line is matched "
              "against the invoice it pays. Importing the same statement twice does "
              "nothing, and the rule that makes that true is "
              "[[0003-bank-imports-are-idempotent-by-statement-hash|ADR-0003]] rather than a "
              "trick in the importer. What the importer cannot guess goes to "
              "`{ledger.bank.match-by-hand}`, which is the product's honest half: the "
              "matching that cannot be automated is the work the spreadsheet was doing.\n\n"
              "**Tax.** Rates that applied on the day rather than today, and a quarter "
              "that closes when somebody closes it rather than when the calendar does — "
              "[[0005-tax-periods-close-by-decision|ADR-0005]]. A closed period cannot be "
              "booked into "
              "at all; a correction is a document in the open period that refers to the "
              "closed one. That rule came from an accountant describing the invoice that "
              "appears in a filed quarter as the thing that ruins her October.\n\n"
              "## The vocabulary\n\n"
              "An **invoice** is a document that has been sent; before that it is a draft "
              "and it has no number. A **credit note** is a document that credits an "
              "invoice — it is not a negative invoice and not a state on one, and since "
              "[[0006-refunds-are-credit-notes|ADR-0006]] it is also the only way a refund "
              "reaches a card. A **statement** is "
              "one bank's record of a period; a **line** is one movement on it. "
              "**Matching** joins a line to the invoice it pays, and a line may match "
              "nothing, which is a normal outcome and not an error. A **period** is a tax "
              "quarter, and it is open until somebody closes it.\n\n"
              "We say **business** rather than \"company\" throughout, because half our "
              "first customers are sole traders and the word matters to them.\n\n"
              "## What this costs, and what is not built\n\n"
              "Matching is a heuristic, and a heuristic that is right nine times in ten is "
              "wrong once a week for a business with fifty invoices a month. Every wrong "
              "match is worse than a missing one, so the importer is deliberately "
              "conservative and the manual screen is busier than it would be if we were "
              "braver — the number we watch is the share of lines it settles on its own, "
              "and it is short of where it needs to be.\n\n"
              "Closing a period cost us the assumption that one period is open at a time; "
              "every query in this product now has to say which one it means, for ever.\n\n"
              "Recurring invoices and chasing a late one are unbuilt, and the second was "
              "cancelled rather than deferred. Rounding per line versus per invoice is "
              "still an open question with two national rules disagreeing about it. So is "
              "anything an accountant would call double entry."),
    dict(path="docs/design/fieldnote.md", title="Fieldnote", when="06-16 12:00",
         who="ingrid",
         body="# Fieldnote\n\n"
              "Fieldnote is job scheduling for crews who work where there is no signal. "
              "The claim is one sentence and the whole product rests on it: **take the "
              "phone into the valley, do a day's work, come back, and everything you did "
              "is there.**\n\n"
              "Every scheduling tool our first customer has tried assumed a connection. "
              "Each one worked in the depot car park and quietly lost the afternoon "
              "somewhere past the second stop, and each time the crews went back to paper "
              "dockets and the dispatcher went back to the telephone. Offline is not a "
              "feature here. It is the premise, and everything else is negotiable.\n\n"
              "## The flows\n\n"
              "**The day.** A dispatcher puts jobs on crews from a board. Before a crew "
              "leaves, the phone takes the whole day — jobs, addresses, what happened last "
              "time somebody went to that address, and the route between them — and holds "
              "it locally. Nothing after that point needs a network.\n\n"
              "**The job.** A crew arrives, does the work, and writes it up from the van "
              "while it is fresh: what was wrong, what was used, photographs, and the "
              "customer's signature. All of it is queued on the handset.\n\n"
              "**The route.** The stops are ordered so the day is driveable, using the "
              "road's travel time rather than the distance between two dots, with the "
              "depot and the last stop as fixed ends. When a job overruns, the rest of the "
              "day should move rather than the crew improvising.\n\n"
              "**Coming back.** The phone finds a signal, sends its queue oldest first, "
              "and the office sees the day. This is the part with the hard problem in it, "
              "and this page will be wrong about it before the quarter is out.\n\n"
              "## The vocabulary\n\n"
              "A **job** is one visit to one address for one customer; it is the unit "
              "everything else is about. A **crew** is the people in one van, and it is "
              "the thing work is assigned to rather than a person. A **stop** is a job "
              "seen from the route's point of view. A **day** is a crew's list, in order, "
              "and it is what the phone holds. A **conflict** is one job with two versions "
              "that disagree.\n\n"
              "We say **crew** and not \"technician\" because the van holds two people and "
              "the work belongs to the van.\n\n"
              "## What this costs, and what is not built\n\n"
              "Everything is harder because of the premise. Data has to be complete on the "
              "phone before it leaves, which means downloading things the crew will "
              "probably not need. Every edit is a queued intention rather than a write, so "
              "the phone holds a history rather than a state. And the moment the phone "
              "reconnects is the moment everything can go wrong at once.\n\n"
              "What happens when the phone and the server disagree about the same job is "
              "not decided. That is the largest unanswered question in the product and it "
              "is currently answered by whatever the sync code happens to do."),
    dict(path="docs/design/fieldnote.md", title="Fieldnote", when="08-04 15:40",
         who="ingrid", keys=True, update=True,
         body="# Fieldnote\n\n"
              "Fieldnote is job scheduling for crews who work where there is no signal. "
              "The claim is one sentence and the whole product rests on it: **take the "
              "phone into the valley, do a day's work, come back, and everything you did "
              "is there.**\n\n"
              "On 29 July that claim was false for eleven crews, and this page was wrong "
              "in the way it said it would be. The section on coming back has been "
              "rewritten around the answer the incident forced.\n\n"
              "## The flows\n\n"
              "**The day.** A dispatcher puts jobs on crews from a board. Before a crew "
              "leaves, the phone takes the whole day — jobs, addresses, what happened last "
              "time somebody went to that address, and the route between them — and holds "
              "it locally. Nothing after that point needs a network.\n\n"
              "**The job.** A crew arrives, does the work, and writes it up from the van "
              "while it is fresh: what was wrong, what was used, photographs, and the "
              "customer's signature. All of it is queued on the handset.\n\n"
              "**The route.** The stops are ordered so the day is driveable, using the "
              "road's travel time rather than the distance between two dots, with the "
              "depot and the last stop as fixed ends.\n\n"
              "**Coming back.** The phone finds a signal and sends its queue oldest first. "
              "For a job, the phone wins: the server never overwrites a field a phone "
              "changed while it was offline, and anything the server cannot reconcile is "
              "kept rather than dropped. Where the two genuinely disagree, both versions "
              "are held and the crew is shown what disagreed and asked to choose. That is "
              "[[0004-the-phone-is-the-source-of-truth-for-a-job|ADR-0004]] now rather than "
              "a line in the sync code, "
              "which is what `{field.offline.sync-loss}` cost us.\n\n"
              "The rule is about jobs. It is not about the schedule: which crew is on "
              "which job tomorrow belongs to the dispatcher and the server holds it.\n\n"
              "## The vocabulary\n\n"
              "A **job** is one visit to one address for one customer; it is the unit "
              "everything else is about. A **crew** is the people in one van, and it is "
              "the thing work is assigned to rather than a person. A **stop** is a job "
              "seen from the route's point of view. A **day** is a crew's list, in order, "
              "and it is what the phone holds. A **conflict** is one job with two versions "
              "that disagree, and it is now a thing a crew sees rather than a thing the "
              "code resolves.\n\n"
              "We say **crew** and not \"technician\" because the van holds two people and "
              "the work belongs to the van.\n\n"
              "## What this costs, and what is not built\n\n"
              "Everything is harder because of the premise. Data has to be complete on the "
              "phone before it leaves, which means downloading things the crew will "
              "probably not need. Every edit is a queued intention rather than a write. "
              "And a job now carries its history rather than its state, so it grows with "
              "every conflict and nothing has been decided about when a kept version may "
              "be thrown away.\n\n"
              "A dispatcher's correction no longer takes effect while a crew is out, and "
              "he will find that annoying, correctly.\n\n"
              "The conflict screen is unbuilt. So is holding the sync while a whole depot "
              "comes back into signal at once, which is the case that produced the "
              "incident and the case we have still not tested."),
]

DESIGN += [
    dict(path="docs/design/architecture.md", title="Architecture", when="06-16 12:20",
         who="ingrid",
         body="# Architecture\n\n"
              "Three products, one shared thing underneath them, and a deliberate refusal "
              "to share anything else. This page says what that shared thing is, why it is "
              "the only one, and what it costs to keep it that way.\n\n"
              "![[architecture.svg]]\n\n"
              "## Why anything is shared at all\n\n"
              "A marina, an accountant and a maintenance company are three customers. They "
              "are also, often, the same customer: the marina that takes bookings in "
              "Harbor is invoiced by an accountant using Ledgerline, and the crew that "
              "services its pontoons works out of Fieldnote. Somebody at that marina "
              "should sign in once and see the two of those they pay for.\n\n"
              "So one thing is shared, and it is the smallest thing that makes that "
              "possible: **a business, the people in it, and what each of them may see.** "
              "Everything else — berths, invoices, jobs — belongs to exactly one product "
              "and is not visible from the others except through a link somebody made on "
              "purpose.\n\n"
              "## What is not shared, on purpose\n\n"
              "There is no shared customer record. A marina in Harbor and a business in "
              "Ledgerline are different rows even when they are the same organisation, "
              "because what Harbor knows about a marina — berth count, pontoon layout, "
              "shore power — is nothing an accounting product should carry, and merging "
              "them would mean the union of two products' opinions about what a customer "
              "is.\n\n"
              "There is no shared scheduling. Harbor's bookings and Fieldnote's jobs are "
              "both \"somebody has a slot\" and it is a false friend: a berth is booked "
              "for nights and a job is booked for hours, one is sold and the other is "
              "assigned, and the day we merge them is the day both get worse.\n\n"
              "The one place we have deliberately allowed a dependency is money. Harbor "
              "and Ledgerline take payment through the same provider and the same internal "
              "module, and the reason is written down as a decision rather than left in "
              "the code.\n\n"
              "## What this costs\n\n"
              "Signing in once is the easy half; deciding what somebody may see is not. "
              "Permissions live in the shared service and the meaning of a permission "
              "lives in each product, so every new role is a change in two places and a "
              "conversation about which of them owns the word.\n\n"
              "Three products in one repository and one vault means one deployment "
              "cadence. Fieldnote cannot ship on Tuesday because Harbor is mid-launch. We "
              "have accepted that at six people and it is the first thing that will have "
              "to change.\n\n"
              "## What is not built\n\n"
              "The accounts service is one database table and a session cookie. There is "
              "no organisation hierarchy, no invitation flow, and no way for a marina to "
              "give its accountant read access to its own bookings — which is the most "
              "requested thing that does not exist."),
    dict(path="docs/design/architecture.md", title="Architecture", when="08-27 11:40",
         who="ingrid", keys=True, update=True,
         body="# Architecture\n\n"
              "Three products, one shared thing underneath them, and a deliberate refusal "
              "to share anything else. This page says what that shared thing is, why it is "
              "the only one, and what it costs to keep it that way.\n\n"
              "![[architecture.svg]]\n\n"
              "## Why anything is shared at all\n\n"
              "A marina, an accountant and a maintenance company are three customers. They "
              "are also, often, the same customer: the marina that takes bookings in "
              "Harbor is invoiced by an accountant using Ledgerline, and the crew that "
              "services its pontoons works out of Fieldnote. Somebody at that marina "
              "should sign in once and see the two of those they pay for.\n\n"
              "So one thing is shared, and it is the smallest thing that makes that "
              "possible: **a business, the people in it, and what each of them may see.** "
              "Everything else — berths, invoices, jobs — belongs to exactly one product "
              "and is not visible from the others except through a link somebody made on "
              "purpose.\n\n"
              "## What is not shared, on purpose\n\n"
              "There is no shared customer record. A marina in Harbor and a business in "
              "Ledgerline are different rows even when they are the same organisation, "
              "because what Harbor knows about a marina is nothing an accounting product "
              "should carry.\n\n"
              "There is no shared scheduling. Harbor's bookings and Fieldnote's jobs are "
              "both \"somebody has a slot\" and it is a false friend: a berth is booked "
              "for nights and a job is booked for hours, one is sold and the other is "
              "assigned, and the day we merge them is the day both get worse.\n\n"
              "## The two seams that turned out to be real\n\n"
              "Two dependencies have grown between the products this quarter, and both "
              "were predicted on the first day.\n\n"
              "**Money crosses from Harbor to Ledgerline.** A refund in Harbor is a credit "
              "note in [[ledgerline|Ledgerline]], and since "
              "[[0006-refunds-are-credit-notes|ADR-0006]] it is only ever a credit note: "
              "`{harbor.payments.refunds}` is blocked by "
              "`{ledger.invoices.credit-notes}` and will stay that way, because the "
              "direction is now a rule. The cost is that Harbor's refund flow depends on "
              "Ledgerline being up, which is a coupling we would not have chosen and did "
              "choose.\n\n"
              "**Offline crosses from Fieldnote to Harbor.** Queueing work on a phone with "
              "no signal and reconciling it later is one problem, and it appeared in "
              "[[fieldnote|Fieldnote]]'s jobs and [[harbor|Harbor]]'s pontoon check-in "
              "within a fortnight of each other. The two share "
              "[[0004-the-phone-is-the-source-of-truth-for-a-job|ADR-0004]] rather than a "
              "library — the conflict rule "
              "is the same and the code is not, because a job and a check-in disagree in "
              "different shapes.\n\n"
              "## What this costs\n\n"
              "Signing in once is the easy half; deciding what somebody may see is not. "
              "Permissions live in the shared service and the meaning of a permission "
              "lives in each product, so every new role is a change in two places and a "
              "conversation about which of them owns the word.\n\n"
              "Three products in one repository and one vault means one deployment "
              "cadence. Fieldnote cannot ship on Tuesday because Harbor is mid-launch. We "
              "have accepted that at six people and it is the first thing that will have "
              "to change.\n\n"
              "## What is not built\n\n"
              "The accounts service is one database table and a session cookie. There is "
              "no organisation hierarchy, no invitation flow, and no way for a marina to "
              "give its accountant read access to its own bookings — which is the most "
              "requested thing that does not exist."),
]

# The front page. `docs/spec/documents.md` §8 refuses a page whose purpose is to list
# other pages, and §10 exempts `docs/index.md` from being named after its title, because
# everything that clones a vault has to find the front page without knowing the project.
# Both apply here at once, so this is written as the shortest useful piece of prose that
# gets a newcomer to the right document, and not as an index of everything in `docs/`.
INDEX = [
    dict(when="06-15 09:20", who="ingrid",
         body="# Northlight\n\n"
              "Three products for the same stretch of coast, built by six people: Harbor "
              "for marinas, Ledgerline for the businesses that invoice for them, and "
              "Fieldnote for the crews who service the boats. They live in one vault with "
              "one key space — HARBOR, LEDGER and FIELD — for reasons that are written "
              "down rather than assumed.\n\n"
              "This is the first day of that vault, so there is not much here yet. What "
              "there is:\n\n"
              "Read [[documents]] before writing anything under `docs/`. It says what the "
              "five kinds of page are, which folder each lives in, and what a decision has "
              "to contain. It is normative and `docket check` enforces the checkable half "
              "of it.\n\n"
              "The board is the work. A task is a file, a sprint is a page, and the links "
              "between them are the whole of the integration between the two. Nothing here "
              "should list the tasks it is about: a page names work by key, in backticks, "
              "and the backlinks do the rest.\n\n"
              "The labels — [[bookings]], [[payments]], [[offline-sync]] and the rest — "
              "each have a page saying what they mean, and everything labelled is in that "
              "page's backlinks. That is the pattern to copy: a page is found through what "
              "links to it, not through a list somebody remembered to update."),
    dict(when="09-04 16:30", who="ingrid", keys=True,
         body="# Northlight\n\n"
              "Three products for the same stretch of coast, built by six people between "
              "15 June and today: Harbor for marinas, Ledgerline for the businesses that "
              "invoice for them, and Fieldnote for the crews who service the boats. One "
              "vault, one board, one key space — HARBOR, LEDGER and FIELD — and the reason "
              "for that is [[0001-one-vault-for-three-products|ADR-0001]], which is also "
              "the first thing to read if you are wondering why the backlog is this "
              "long.\n\n"
              "## If you are new\n\n"
              "Start with the product you are going to touch: [[harbor|Harbor]], "
              "[[ledgerline|Ledgerline]] or [[fieldnote|Fieldnote]]. Each says what the "
              "product is, the flows it has, the words it uses for things, and what it "
              "costs — and each was rewritten once this quarter when something happened "
              "that made the first version wrong. [[architecture|The architecture page]] "
              "says what the three share, which is less than people expect.\n\n"
              "Then read [[documents]], which is normative: the five kinds of page, where "
              "each lives, and what a decision must contain. `docket check` enforces the "
              "half of it that a program can.\n\n"
              "## The arguments\n\n"
              "Six decisions were taken this quarter and they are in `docs/decisions/`, "
              "numbered in the order they were made. Two of them explain most of what is "
              "surprising in the code: "
              "[[0004-the-phone-is-the-source-of-truth-for-a-job|ADR-0004]], which is why "
              "Fieldnote keeps two versions of a job rather than merging them, and "
              "[[0006-refunds-are-credit-notes|ADR-0006]], which is why a refund in Harbor "
              "goes through Ledgerline at all. Both were bought expensively.\n\n"
              "## The work\n\n"
              "Sprints are pages in `docs/sprints/`, one per fortnight, each with the goal "
              "it started with and the retrospective it ended with; the tasks that were in "
              "one are its backlinks rather than a list. Sprint 6 finished today and "
              "Sprint 7 is planned.\n\n"
              "The labels — [[bookings]], [[payments]], [[offline-sync]] and the rest — "
              "each have a page saying what they mean, and everything carrying one is in "
              "that page's backlinks.\n\n"
              "## The apps, and the pages they brought\n\n"
              "This vault runs eleven packs on top of the board, and five of them brought "
              "a document explaining how the thing they add is meant to be kept: "
              "[[okrs]] on why progress is not a percentage of finished tasks, [[risks]] "
              "on why a risk has two words rather than a score, [[incidents]] on why an "
              "incident and its postmortem are two tasks, [[intake]] on why a request is "
              "not a backlog item, and [[logging-time]] on why an hour is a note rather "
              "than a number on a card. [[testing]] is the largest of them and says how a "
              "test plan, a test and a run relate.\n\n"
              "Everything those five describe is in this vault with real data in it: three "
              "objectives and seven key results for the quarter, six risks reviewed twice, "
              "two incidents with their postmortems, eight customer requests, and thirty "
              "worklogs from the last two sprints.\n\n"
              "## Where the quarter got to\n\n"
              "Harbor launched check-in on the pontoon in August and the whole check-in "
              "epic is finished. Ledgerline is closing its first quarter this week. "
              "Fieldnote lost eleven crews an afternoon in July, and the work that came "
              "out of that is most of what is on the board now. The one thing nobody has "
              "settled is what happens to a season berth that is cut short, which is why "
              "`{harbor.booking.season-rate}` has been in review since the middle of "
              "August."),
]


# --- turning the data above into events ------------------------------------------------

MINUTE = common.MINUTE

# Which list a piece of work is held to. Every story is held to the team's list; the two
# launch stories are held to the release list, because a season launch and a filed tax
# return are not things a team's usual list covers; and the two bugs that came out of an
# incident are held to the hotfix list. `field.offline.sync-loss` already says so itself
# in `fieldnote.py`, and is left alone rather than said twice.
LAUNCH_STORIES = ("harbor.checkin.pontoon", "ledger.tax.close")
HOTFIX_BUGS = ("harbor.payments.double-charge", "field.offline.sync-loss")

# Which key result each epic advances. Seven epics of the ten point at one; the other
# three — invoices, routes and payments — advance nothing on this list, which is the
# ordinary case and not a fault.
CONTRIBUTIONS = [
    ("06-16 14:20", "ingrid", "harbor.booking", "okr.harbor.marinas"),
    ("06-16 14:24", "ingrid", "harbor.checkin", "okr.harbor.pontoon"),
    ("06-16 14:28", "ingrid", "harbor.calendar", "okr.harbor.calendar"),
    ("06-16 14:32", "ingrid", "ledger.tax", "okr.ledger.close"),
    ("06-16 14:36", "ingrid", "ledger.bank", "okr.ledger.matched"),
    ("06-16 14:40", "ingrid", "field.offline", "okr.field.nothing-lost"),
    ("06-16 14:44", "ingrid", "field.jobs", "okr.field.from-the-van"),
]

_INVERSE = {"contributes_to": "advanced_by", "threatens": "threatened_by",
            "mitigated_by": "mitigates", "causes": "caused_by",
            "explains": "explained_by", "became": "came_from", "logs": "logged"}

REVIEWED_AT_FIRST = "2026-06-22"
REVIEWED_AGAIN = "2026-08-03"


def _set_at(when, who, alias, **values) -> engine.Event:
    said = ", ".join(sorted(values))
    return engine.Event(when, PEOPLE[who], "set", {"task": alias, **values},
                        "{%s}: %s" % (alias, said))


def _after(moment, minutes, what) -> dt.datetime:
    return common.office_hours(common.when(moment) + minutes * MINUTE, what)


def _project_of(alias) -> str:
    return {"harbor": HARBOR, "ledger": LEDGER, "field": FIELD}[alias.split(".", 1)[0]]


def _relation_events(declared, forward=True) -> list[engine.Event]:
    """Both sides of every relation, and only ever one `docket set` per side.

    `docket set` replaces a relation rather than appending to it, so an epic that two risks
    threaten and a story that six worklogs point at have to be written with everything
    they hold each time. What is accumulated here is exactly what the file should say at
    that moment, which is also what makes replaying twice produce the same vault.

    `forward=False` writes only the inverse: a worklog's own `logs` is set in the same
    command as its hours, so writing it again here would be a second commit saying
    nothing new."""
    held_forward: dict[tuple, list] = {}
    held_inverse: dict[tuple, list] = {}
    out = []
    for moment, who, source, name, targets in sorted(declared, key=lambda d: common.when(d[0])):
        when = common.office_hours(common.when(moment), source)
        if forward:
            held = held_forward.setdefault((source, name), [])
            held += [t for t in targets if t not in held]
            out.append(_set_at(when, who, source, **{name: list(held)}))
        for step, target in enumerate(targets, start=1):
            inverse = _INVERSE[name]
            held = held_inverse.setdefault((target, inverse), [])
            if source not in held:
                held.append(source)
            out.append(_set_at(_after(moment, step, target), who, target,
                               **{inverse: list(held)}))
    return out


def _dod_events() -> list[engine.Event]:
    out = []
    for module in PRODUCTS:
        for spec in module.WORK:
            alias = module.PREFIX + spec["a"]
            if spec.get("dod"):
                continue
            if alias in LAUNCH_STORIES:
                held = "release"
            elif alias in HOTFIX_BUGS:
                held = "hotfix"
            elif spec.get("type", "story") == "story":
                held = "team"
            else:
                continue
            out.append(engine.Event(_after(spec["made"], 7, alias), PEOPLE["ingrid"], "set",
                                    {"task": alias, "definition_of_done": held},
                                    "{%s}: held to the %s list" % (alias, held)))
    return out


def _okr_events(declared) -> list[engine.Event]:
    out = []
    for o in OBJECTIVES:
        out.append(_new(o["made"], o["who"], o["a"], o["t"], o["project"], "objective",
                        status="In progress", assignee=o["who"], body=common.body(o["why"])))
        out.append(_set_at(_after(o["made"], 2, o["a"]), o["who"], o["a"], quarter=QUARTER))
    for index, kr in enumerate(KEY_RESULTS):
        out.append(_new(kr["made"], "ingrid", kr["a"], kr["t"], kr["project"], "key_result",
                        status="In progress", assignee=kr["who"], parent=kr["parent"],
                        body=common.body(kr["why"] + "\n\n## Where the number comes from\n\n"
                                         + kr["source"] + ".")))
        out.append(_set_at(_after(kr["made"], 2, kr["a"]), "ingrid", kr["a"],
                           target=kr["target"], current=kr["current"],
                           measure=kr["measure"], quarter=QUARTER))
        out.append(_set_at(_after("07-31 11:00", index * 3, kr["a"]), "ingrid", kr["a"],
                           current=kr["july"]))
        out.append(_set_at(_after("08-31 11:00", index * 3, kr["a"]), "ingrid", kr["a"],
                           current=kr["august"]))
    declared += [(m, who, epic, "contributes_to", [kr]) for m, who, epic, kr in CONTRIBUTIONS]
    return out


def _risk_events(declared) -> list[engine.Event]:
    out = []
    for index, r in enumerate(RISKS):
        made = "06-22 %02d:%02d" % (10 + index // 4, 20 + 10 * (index % 4))
        body = ("## What could happen\n\n%s.\n\n## Why we think so\n\n%s\n\n"
                "## What we would do\n\n%s" % (r["t"], r["why"], r["plan"]))
        out.append(_new(made, r["by"], r["a"], r["t"], r["project"], "risk",
                        assignee=r["owner"], labels=r["labels"], body=common.body(body)))
        out.append(_set_at(_after(made, 2, r["a"]), r["by"], r["a"],
                           likelihood=r["likelihood"], impact=r["impact"],
                           owner=r["owner"], reviewed_on=REVIEWED_AT_FIRST))
        declared.append((_after(made, 4, r["a"]).strftime("%m-%d %H:%M"), r["by"], r["a"],
                         "threatens", [r["threatens"]]))
        if r.get("mitigated_by"):
            declared.append((r["mitigated_on"], r["by"], r["a"], "mitigated_by",
                             r["mitigated_by"]))
            out.append(_set_at(_after(r["mitigated_on"], 3, r["a"]), r["by"], r["a"],
                               status="Ready"))
        out.append(_set_at(_after("08-03 %02d:%02d" % (14, 10 + 5 * index), 0, r["a"]),
                           "ola", r["a"], reviewed_on=REVIEWED_AGAIN))
    return out


def _incident_events(declared) -> list[engine.Event]:
    out = []
    for inc in INCIDENTS:
        out.append(_new(inc["made"], inc["who"], inc["a"], inc["t"], inc["project"],
                        "incident", status="In progress", assignee=inc["who"],
                        labels=inc["labels"], body=common.body(inc["why"])))
        out.append(_set_at(_after(inc["made"], 2, inc["a"]), inc["who"], inc["a"],
                           severity=inc["severity"], detected_at=inc["detected_at"],
                           resolved_at=inc["resolved_at"],
                           customers_affected=inc["customers_affected"]))
        for moment, status, who in inc["moves"]:
            out.append(story.move(_at(moment), PEOPLE[who], inc["a"], status))
        for bug in inc["from_bugs"]:
            declared.append((inc["caused_on"], inc["who"], bug, "causes", [inc["a"]]))

    for pm in POSTMORTEMS:
        out.append(_new(pm["made"], pm["who"], pm["a"], pm["t"], pm["project"],
                        "postmortem", status="In progress", assignee=pm["who"],
                        labels=pm["labels"], body=pm["body"]))
        for moment, status, who in pm["moves"]:
            out.append(story.move(_at(moment), PEOPLE[who], pm["a"], status))
        for moment, who, text in pm.get("says", ()):
            out.append(story.comment(_at(moment), PEOPLE[who], pm["a"], text))
        declared.append((pm["explained_on"], pm["who"], pm["a"], "explains", [pm["explains"]]))
        declared.append((pm["mitigated_on"], pm["who"], pm["a"], "mitigated_by",
                         pm["mitigated_by"]))
    return out


def _request_events(declared) -> list[engine.Event]:
    out = []
    for req in REQUESTS:
        out.append(_new(req["made"], "ingrid", req["a"], req["t"], req["project"], "request",
                        assignee="ingrid", labels=req["labels"], body=req["body"]))
        fields = dict(asked_by=req["asked_by"], asked_on=req["asked_on"])
        if req.get("wanted_by"):
            fields["wanted_by"] = req["wanted_by"]
        out.append(_set_at(_after(req["made"], 2, req["a"]), "ingrid", req["a"], **fields))
        if req.get("became"):
            declared.append((req["became_on"], "ingrid", req["a"], "became", req["became"]))
            out.append(_set_at(_at(req["ready"]), "ingrid", req["a"], status="Ready"))
        if req.get("cancelled"):
            out.append(_set_at(_at(req["cancelled"]), "ingrid", req["a"], status="Cancelled"))
        for moment, who, text in req.get("says", ()):
            out.append(story.comment(_at(moment), PEOPLE[who], req["a"], text))
    return out


def _worklog_events(declared) -> list[engine.Event]:
    out = []
    for log in WORKLOGS:
        project = _project_of(log["on"])
        billable = "true" if project == HARBOR else "false"
        out.append(_new(log["made"], log["who"], log["a"], log["t"], project, "worklog",
                        status="Done", assignee=log["who"], parent=log["on"],
                        body=log["why"] + "\n"))
        out.append(_set_at(_after(log["made"], 2, log["a"]), log["who"], log["a"],
                           spent=log["spent"], worked_on="2026-" + log["day"],
                           billable=billable, logs=[log["on"]]))
        declared.append((_after(log["made"], 2, log["a"]).strftime("%m-%d %H:%M"),
                         log["who"], log["a"], "logs", [log["on"]]))
    return out


def _page_events() -> list[engine.Event]:
    """Pages, in the order the vault gained them, and the one file that is not Markdown.

    A page body goes through the alias map when it names work, so a page may only name a
    task that existed on the day it was written — an alias the engine has not assigned yet
    would be written out as the alias, silently. `test_crosscut` holds that line."""
    out = [story.page(_at(INDEX[0]["when"]), PEOPLE[INDEX[0]["who"]], "docs/index.md",
                      "Northlight", "page", INDEX[0]["body"])]

    # The drawing has to be in the vault before a page embeds it: a wikilink to an
    # attachment that is not there is rule 8, the same as any other dead link. It is
    # embedded by its path rather than by its name — `docket check` resolves a bare name
    # only without its extension, and `[[architecture]]` in `docs/design/architecture.md`
    # would be the page embedding itself.
    out.append(common.attach(common.when("06-16 11:00"), PEOPLE["ingrid"],
                             "architecture.svg", "the three products, on one page"))

    for page in DESIGN:
        out.append(story.page(_at(page["when"]), PEOPLE[page["who"]], page["path"],
                              page["title"], "design", page["body"],
                              keys=page.get("keys", False)))

    for d in DECISIONS:
        when = _at(d["when"])
        path = "docs/decisions/%s-%s.md" % (d["n"], d["slug"])
        out.append(story.page(when, PEOPLE[d["who"]], path, d["t"], "decision", d["body"],
                              keys=d.get("keys", False),
                              status="accepted", date=when.date().isoformat()))

    out.append(story.page(_at(INDEX[1]["when"]), PEOPLE[INDEX[1]["who"]], "docs/index.md",
                          "Northlight", "page", INDEX[1]["body"], keys=True))
    return out


def events() -> list[engine.Event]:
    declared: list[tuple] = []
    out = _dod_events()
    out += _okr_events(declared)
    out += _risk_events(declared)
    out += _incident_events(declared)
    out += _request_events(declared)
    logs = _worklog_events(declared)
    out += logs

    # A worklog's own `logs` is written in the same command as its hours, so only the
    # other side of it is generated here; everything else gets both sides.
    forward = [d for d in declared if d[3] != "logs"]
    backward = [d for d in declared if d[3] == "logs"]
    out += _relation_events(forward)
    out += _relation_events(backward, forward=False)

    out += _page_events()
    return sorted(out, key=lambda e: e.when)
