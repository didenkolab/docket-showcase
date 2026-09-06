"""The Northlight story: the people, the sprints, the labels, and the timeline helpers
that turn them into engine.Event objects. No dates are computed from "now" — every date
here is data, fixed to the story being replayed."""
from __future__ import annotations
import dataclasses as dc
import datetime as dt
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
    Sprint("Sprint 1", dt.date(2026, 6, 15), dt.date(2026, 6, 26)),
    Sprint("Sprint 2", dt.date(2026, 6, 29), dt.date(2026, 7, 10)),
    Sprint("Sprint 3", dt.date(2026, 7, 13), dt.date(2026, 7, 24)),
    Sprint("Sprint 4", dt.date(2026, 7, 27), dt.date(2026, 8, 7)),
    Sprint("Sprint 5", dt.date(2026, 8, 10), dt.date(2026, 8, 21)),
    Sprint("Sprint 6", dt.date(2026, 8, 24), dt.date(2026, 9, 4)),
]

SPRINT_7 = Sprint("Sprint 7", dt.date(2026, 9, 7), dt.date(2026, 9, 18))


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


def sprint_events() -> list[Event]:
    """A start page for every sprint (goal only), plus a retrospective rewrite of that same
    page at the end of sprints 1-5. Sprint 6 is still running as of the story's present
    (2026-09-04) and gets no end event yet; Sprint 7 is only planned so far, and gets the
    one-off planning page below instead of its own start event."""
    ingrid = PEOPLE["ingrid"]
    events = []
    for sp in SPRINTS:
        start_when = dt.datetime.combine(sp.starts, dt.time(9, 0))
        extra = {"starts": sp.starts.isoformat(), "ends": sp.ends.isoformat()}
        start_body = "# %s\n\n%s\n" % (sp.name, sp.goal)
        events.append(page(start_when, ingrid, "docs/sprints/%s.md" % sp.name, sp.name, "page",
                           start_body, **extra))

    for sp in SPRINTS[:5]:
        if not sp.retro:
            raise ValueError("%s has no retrospective" % sp.name)
        end_when = dt.datetime.combine(sp.ends, dt.time(17, 0))
        extra = {"starts": sp.starts.isoformat(), "ends": sp.ends.isoformat()}
        end_body = "# %s\n\n%s\n\n## Retrospective\n\n%s\n" % (sp.name, sp.goal, sp.retro)
        events.append(page(end_when, ingrid, "docs/sprints/%s.md" % sp.name, sp.name, "page",
                           end_body, **extra))

    sp7 = SPRINT_7
    extra7 = {"starts": sp7.starts.isoformat(), "ends": sp7.ends.isoformat()}
    body7 = "# %s\n\n%s\n" % (sp7.name, sp7.goal)
    events.append(page(at("2026-09-04", 16, 0), ingrid, "docs/sprints/%s.md" % sp7.name, sp7.name,
                       "page", body7, **extra7))
    return events
