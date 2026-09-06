"""The Northlight story: the people, the sprints, the labels, and the timeline helpers
that turn them into engine.Event objects. No dates are computed from "now" — every date
here is data, fixed to the story being replayed."""
from __future__ import annotations
import dataclasses as dc
import datetime as dt
import subprocess
import engine

Person = engine.Person
Event = engine.Event


def at(day: str, hour: int = 10, minute: int = 0) -> dt.datetime:
    """A naive UTC datetime for the given ISO date and time of day."""
    y, m, d = (int(p) for p in day.split("-"))
    return dt.datetime(y, m, d, hour, minute)


def _plain(text):
    """Escapes a free-text fragment so it survives Engine.commit's format_map() unchanged,
    even when it contains literal `{` or `}` (e.g. a title like "Render {berth} as a card")."""
    return text.replace("{", "{{").replace("}", "}}")


PEOPLE: dict[str, Person] = {
    p.handle: p
    for p in (
        Person("ingrid", "Ingrid Solberg", "ingrid@northlight.example", "product"),
        Person("tomasz", "Tomasz Wierzbicki", "tomasz@northlight.example", "backend"),
        Person("aiko", "Aiko Tanaka", "aiko@northlight.example", "mobile"),
        Person("mateo", "Mateo Ríos", "mateo@northlight.example", "QA"),
        Person("priya", "Priya Nair", "priya@northlight.example", "frontend"),
        Person("ola", "Ola Nordmann", "ola@northlight.example", "ops"),
    )
}


@dc.dataclass
class Sprint:
    name: str
    starts: dt.date
    ends: dt.date
    goal: str = ""
    retro: str = ""


SPRINTS: list[Sprint] = [
    Sprint(
        "Sprint 1", dt.date(2026, 6, 15), dt.date(2026, 6, 26),
        goal="A marina can take a booking and send an invoice",
        retro=(
            "We got the sentence the whole product hangs off \u2014 this boat has that berth from "
            "this day to that one \u2014 and an invoice out of the end of it, which is what we said "
            "the sprint was for. Reserving a berth for a date range, the free-berths answer the "
            "harbour office actually asks for, and importing a real marina's forty-one berths "
            "all finished inside the two weeks. Ledgerline's invoice numbering landed beside "
            "them, so the demo we gave on the Friday was one flow across two products rather "
            "than two demos.\n\n"
            "The one that hurt was the invoice story coming back from review on the Thursday: "
            "it priced the booking at today's rate rather than the rate on the day it was "
            "booked, and a marina that changes its prices in August would have reissued June's "
            "invoices at August's money. Priya caught it reading the code rather than running "
            "it, which is luck we should not plan for. It cost us most of a day and it was the "
            "right day to spend.\n\n"
            "Two things change. Rates are now written down as a decision rather than argued "
            "about in each story, because three of us had three answers when it came up. And "
            "the spreadsheet import gets a real marina's file before the story is written, not "
            "after: half of the import estimate went on a column called 'note2' that turned out "
            "to hold shore power."
        ),
    ),
    Sprint(
        "Sprint 2", dt.date(2026, 6, 29), dt.date(2026, 7, 10),
        goal="Card payments end to end on staging",
        retro=(
            "A guest can pay for a berth on staging: the card is charged when the booking is "
            "confirmed, the bank's own page hands the guest back to the right booking, and the "
            "provider's reference ends up on the booking so the marina's bookkeeper can match "
            "the two. The twenty-minute hold went in beside it, which is what stops two people "
            "buying the same berth while one of them is typing a card number.\n\n"
            "It was not a clean two weeks. The card-payment story failed in QA on the Thursday: "
            "a declined card rolled back the charge and not the booking, so the berth stayed "
            "held for a guest who had not paid \u2014 the failure path had been tested by reasoning "
            "about it rather than by declining a real sandbox card. On top of that, the "
            "double-booking bug found on the first day of the sprint took a day and a half "
            "because the availability check and the write were two separate reads with nothing "
            "between them, and fixing it properly meant changing how a hold is created rather "
            "than adding a lock. Ola also found the sandbox keys sitting in the repository, "
            "which is a sprint's worth of unpleasantness we bought ourselves in Sprint 1.\n\n"
            "From now on a payment story is not in review until its unhappy half has been run "
            "against the provider's sandbox, and QA gets the sandbox account rather than "
            "sharing ours. The keys are in the deployment's secret store and the committed ones "
            "are rotated."
        ),
    ),
    Sprint(
        "Sprint 3", dt.date(2026, 7, 13), dt.date(2026, 7, 24),
        goal="Bank import for Ledgerline, first three banks",
        retro=(
            "Ledgerline can pull a statement from the three banks our first accountants "
            "actually use, and importing the same statement twice no longer produces two of "
            "everything \u2014 which is the difference between a feature and a liability. Harbor "
            "carried on underneath: the webhook reconciliation, the month-query cache that took "
            "the calendar from two and a half seconds to under one, and the calendar bug that "
            "drew boats which had left the day before as still moored.\n\n"
            "The double charge on the Wednesday of the first week was the sprint's real event. "
            "Three marinas, twenty minutes apart, all with the same shape: a slow confirmation, "
            "a guest pressing the button again, two charges and one booking. It is written up "
            "as an incident with the refunds against it. What made it possible was that our "
            "confirmation had no way of saying 'this is the same intention as the last one', "
            "and it was found by three customers rather than by us. The calendar month story "
            "also came back from review \u2014 beautiful on forty berths and unusable on four "
            "hundred and six, which is what Sandholm have.\n\n"
            "Two changes. Anything that spends money is idempotent by construction and says so "
            "in its acceptance. And a screen goes into review with the largest marina's data "
            "loaded, not with the demo marina's \u2014 the size of the customer is not a detail we "
            "get to discover in review."
        ),
    ),
    Sprint(
        "Sprint 4", dt.date(2026, 7, 27), dt.date(2026, 8, 7),
        goal="Fieldnote works a whole day offline",
        retro=(
            "A crew phone now holds its jobs, its route and its photographs for a whole day "
            "without a signal and reconciles when it gets one, and Harbor's check-in learned "
            "the same trick from it: the queued check-in and the flush that empties the queue "
            "were both written this sprint. Two products sharing one hard problem turned out to "
            "be cheaper than two products each having half of it.\n\n"
            "On the Wednesday of the second week we lost work that eleven crews had done "
            "offline. The merge took the server's version of a job whenever the two disagreed, "
            "and a day in a dead zone is exactly the case where the phone is right and the "
            "server is stale. It is written up as an incident with a postmortem; the short "
            "version is that the rule was never stated anywhere, so nobody could disagree with "
            "it before it ran. Nobody enjoyed ringing eleven crews to ask what they had done "
            "that day.\n\n"
            "The rule is now a decision with a document: for a job, the phone is the source of "
            "truth, and anything the server cannot reconcile is kept rather than dropped. "
            "Sync now has a scenario per conflict shape instead of one happy-path scenario, and "
            "the sync work is on the sprint board rather than being 'nearly done' for a fortnight."
        ),
    ),
    Sprint(
        "Sprint 5", dt.date(2026, 8, 10), dt.date(2026, 8, 21),
        goal="Harbor season launch: check-in on the pontoon",
        retro=(
            "Two dockhands at Vik checked boats in from the pontoon all weekend on their own "
            "phones, in the rain, with one bar of signal. Check-in, the QR sticker on the cleat "
            "that opens the right berth's booking, and the photograph of the boat's papers all "
            "shipped, and the whole check-in epic is finished. Ola had both phones on the build "
            "a week before the launch instead of on the Friday, which is the only reason the "
            "weekend was boring.\n\n"
            "Two things we would rather had gone differently. The old test phone's clock is "
            "eleven minutes fast and queued check-ins carried it, so the office saw arrivals "
            "out of order and twice in the future \u2014 found on the Thursday, fixed by the "
            "Tuesday, but it is the kind of thing a launch weekend should not be discovering. "
            "And season pricing has been sitting in review since the middle of the sprint "
            "waiting for us to decide what happens when a season berth is cut short, which is a "
            "product question that a card in review cannot answer on its own.\n\n"
            "The kiosk was cancelled during the sprint rather than carried: it is the same job "
            "as the sticker, and saying so cost one conversation with Sandholm. We should do "
            "that earlier and more often. Next sprint starts by taking a decision on the "
            "shortened-season refund rather than by pulling more work in beside it."
        ),
    ),
    Sprint("Sprint 6", dt.date(2026, 8, 24), dt.date(2026, 9, 4),
           goal="Tax periods, and the sync fix under load"),
]

SPRINT_7 = Sprint("Sprint 7", dt.date(2026, 9, 7), dt.date(2026, 9, 18),
                  goal="Refunds and credit notes together")


LABELS: dict[str, str] = {
    "bookings": (
        "Anything to do with reserving a berth: the search and hold flow in Harbor, "
        "availability windows, cancellations, and the edge cases around double-booking "
        "a slip that two boats tried to claim at once."
    ),
    "payments": (
        "Taking money from a customer at the point of booking or invoicing: card capture, "
        "holds and refunds, payment provider webhooks, and the reconciliation work when a "
        "charge and a booking or invoice disagree about what happened."
    ),
    "invoicing": (
        "Ledgerline's core: turning billable work into an invoice a small business can send, "
        "covering line items, tax lines, numbering, PDF rendering, and the states an invoice "
        "moves through from draft to paid."
    ),
    "bank-import": (
        "Pulling a business's bank transactions into Ledgerline so they can be matched against "
        "invoices and expenses, including the feed connectors, de-duplication of re-imported "
        "statements, and the manual matching screen for anything the importer can't guess."
    ),
    "tax": (
        "The tax rules layered onto Ledgerline's invoicing and bookkeeping: rate tables, "
        "rounding, and the reports a small business hands to its accountant, kept separate "
        "from plain invoicing because the rules change on their own schedule."
    ),
    "offline-sync": (
        "Fieldnote's offline-first app: what a crew phone does with schedule and job data when "
        "it has no signal, and how those local changes reconcile with the server once it's back, "
        "including the conflicts that come from two people editing the same job offline."
    ),
    "routing": (
        "Getting a Fieldnote crew from one job to the next: stop ordering, travel-time estimates, "
        "and the schedule adjustments that ripple through the rest of the day when one job runs "
        "long or a crew is reassigned."
    ),
    "mobile": (
        "Work specific to the phone apps themselves rather than the backend behind them: platform "
        "quirks, app-store releases, device compatibility, and anything that only reproduces on a "
        "device and not in a browser."
    ),
}


class TimelineBuilder:
    """Produces engine.Event objects. `{alias}` placeholders in messages are resolved by
    Engine.commit against the real keys it has assigned, via _KeyMap."""

    def new(self, when, who, alias, title, project, type="story", assignee="", priority="",
            labels="", parent="", body="", status=""):
        args = {"alias": alias, "title": title, "project": project, "type": type}
        if assignee:
            args["assignee"] = assignee
        if priority:
            args["priority"] = priority
        if labels:
            args["labels"] = labels
        if parent:
            args["parent"] = parent
        if body:
            args["body"] = body
        if status:
            args["status"] = status
        return Event(when, who, "new", args, "{%s}: %s" % (alias, _plain(title)))

    def move(self, when, who, alias, status):
        return Event(when, who, "set", {"task": alias, "status": status}, "{%s}: → %s" % (alias, status))

    def estimate(self, when, who, alias, points):
        return Event(when, who, "set", {"task": alias, "estimate": points},
                     "{%s}: sized at %s" % (alias, points))

    def sprint(self, when, who, alias, name):
        return Event(when, who, "set", {"task": alias, "sprint": name}, "{%s}: into %s" % (alias, name))

    def comment(self, when, who, alias, text):
        return Event(when, who, "comment", {"task": alias, "text": text},
                     "{%s}: comment from %s" % (alias, who.handle))

    def relate(self, when, who, alias, **relations):
        args = {"task": alias, **relations}
        return Event(when, who, "set", args, "{%s}: %s" % (alias, ", ".join(relations)))

    def page(self, when, who, path, title, kind, body, **extra):
        args = {"path": path, "title": title, "kind": kind, "body": body}
        if extra:
            args["extra"] = extra
        return Event(when, who, "page", args, _plain(title))

    def person(self, when, who, handle, name):
        return Event(when, who, "person", {"handle": handle, "name": name}, "%s joins" % name)


T = TimelineBuilder()

new = T.new
move = T.move
estimate = T.estimate
sprint = T.sprint
comment = T.comment
relate = T.relate
page = T.page
person = T.person


def people_events() -> list[Event]:
    when = at("2026-06-15", 9, 0)
    ingrid = PEOPLE["ingrid"]
    return [person(when, ingrid, p.handle, p.name) for p in PEOPLE.values()]


def label_events() -> list[Event]:
    when = at("2026-06-15", 9, 10)
    ingrid = PEOPLE["ingrid"]
    events = []
    for name, meaning in LABELS.items():
        body = "# %s\n\n%s\n\nEverything labelled is in this page's backlinks.\n" % (name, meaning)
        events.append(page(when, ingrid, "docs/labels/%s.md" % name, name, "page", body))
    return events


SPRINT_PAGE = "sprint"   # not "page": vault.ParseSprint only reads a page that says so, and
                         # rule 13 calls a task's sprint "not a sprint page" when it does not


def _regenerate_boards(engine_, event):
    """`docket check --fix` regenerates a board that has drifted from docket.yaml.

    The scaffold's sprint board still groups by a status called Dropped, from before the
    workflow gained QA and Cancelled \u2014 harmless until the vault has sprint pages, and a
    rule 9 finding from the moment it does. Ola regenerates it on the first morning. The
    exit status is ignored on purpose: at this point in the story the vault is half
    written, and everything else `check` has to say is said again at the end of the build."""
    subprocess.run([engine_.docket, "check", "--fix", "."], cwd=engine_.root,
                   capture_output=True, text=True)
    return []


def sprint_events() -> list[Event]:
    """A start page for every sprint (goal only), plus a retrospective rewrite of that same
    page at the end of sprints 1-5. Sprint 6 is still running as of the story's present
    (2026-09-04) and gets no end event yet; Sprint 7 is only planned so far, and gets the
    one-off planning page below instead of its own start event."""
    ingrid = PEOPLE["ingrid"]
    events = [Event(at("2026-06-15", 9, 20), PEOPLE["ola"], "raw", {"fn": _regenerate_boards},
                    "boards: the sprint board catches up with the workflow")]
    for sp in SPRINTS:
        start_when = dt.datetime.combine(sp.starts, dt.time(9, 0))
        extra = {"starts": sp.starts.isoformat(), "ends": sp.ends.isoformat()}
        start_body = "# %s\n\n%s\n" % (sp.name, sp.goal)
        events.append(page(start_when, ingrid, "docs/sprints/%s.md" % sp.name, sp.name,
                           SPRINT_PAGE, start_body, **extra))

    for sp in SPRINTS[:5]:
        if not sp.retro:
            raise ValueError("%s has no retrospective" % sp.name)
        end_when = dt.datetime.combine(sp.ends, dt.time(17, 0))
        extra = {"starts": sp.starts.isoformat(), "ends": sp.ends.isoformat()}
        end_body = "# %s\n\n%s\n\n## Retrospective\n\n%s\n" % (sp.name, sp.goal, sp.retro)
        events.append(page(end_when, ingrid, "docs/sprints/%s.md" % sp.name, sp.name,
                           SPRINT_PAGE, end_body, **extra))

    sp7 = SPRINT_7
    extra7 = {"starts": sp7.starts.isoformat(), "ends": sp7.ends.isoformat()}
    body7 = "# %s\n\n%s\n" % (sp7.name, sp7.goal)
    events.append(page(at("2026-09-04", 16, 0), ingrid, "docs/sprints/%s.md" % sp7.name, sp7.name,
                       SPRINT_PAGE, body7, **extra7))
    return events
