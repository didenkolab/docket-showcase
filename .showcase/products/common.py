"""What every product module needs: one task's whole life, from about six lines of data.

Harbor, Ledgerline and Fieldnote all describe the same thing — a task somebody wrote
down, sized in a planning session, pulled into a sprint, moved across a board a few
times, argued about in a comment and finally ticked off — so the description lives here
and each product module is left saying only what is true of it.

A spec is a plain dict, and the keys are short because they are typed forty times a file:

    dict(a="booking.week", t="Reserve a berth for a date range", who="tomasz",
         labels="bookings", pts=5, made="06-15 09:30", sprint="Sprint 1",
         moves=[("06-16 09:40", "Ready"), ("06-17 10:10", "In progress"),
                ("06-19 15:20", "In review"), ("06-22 11:05", "QA", "mateo"),
                ("06-23 14:30", "Done", "mateo")],
         why="...", ok=["...", "..."])

    a       alias, without the product's prefix          t       title
    type    epic|story|task|bug|subtask (story)          parent  another spec's `a`
    who     assignee's handle                            by      who wrote it down
    labels  "bookings" or "bookings,payments"            tags    ("area/api", "regress")
    pts     estimate, on the vault's scale               priority
    made    when it was written down                     sprint  a name, or several
    moves   (when, status[, who]) in order               says    (when, who, text)
    why     the paragraph the body opens with            ok      the acceptance boxes
    ticks   when the boxes were ticked                   ticked  how many of them were

Everything here refuses rather than guesses: a date on a Saturday, a tick before the work
started, an estimate on a task that has children — each raises, because a story replayed
into a vault that `docket check` then rejects is a bug found in the wrong place.
"""
from __future__ import annotations
import datetime as dt

import engine
import story
from story import PEOPLE

YEAR = 2026
OPENS, CLOSES = 9, 18                       # office hours, UTC, as the brief fixes them
FIRST = story.at("2026-06-15", 9, 0)        # the window every event lives in
LAST = story.at("2026-09-04", 18, 0)

SPRINTS = {s.name: s for s in story.SPRINTS}
MINUTE = dt.timedelta(minutes=1)

# Who writes a task down when the spec does not say. A story or an epic is product work
# and comes from ingrid; a bug is written by whoever found it, which is nearly always
# mateo; a chore is written by the person who is going to do it.
WRITER = {"story": "ingrid", "epic": "ingrid", "bug": "mateo"}

DOING = ("In review", "QA", "Done")


def when(text: str, year: int = YEAR) -> dt.datetime:
    """"06-17 10:15" — the year is the story's own, and every date in it is data.

    Full dates ("2026-06-17 10:15") are accepted too, for the few events that want to
    say the year out loud."""
    day, clock = text.split()
    if day.count("-") == 1:
        day = "%d-%s" % (year, day)
    hour, minute = (int(part) for part in clock.split(":"))
    return story.at(day, hour, minute)


def office_hours(moment: dt.datetime, what: str) -> dt.datetime:
    """A moment a working team could have produced, or a refusal saying which one is not."""
    if moment.weekday() >= 5:
        raise ValueError("%s falls on a %s" % (what, moment.strftime("%A")))
    if not (OPENS <= moment.hour < CLOSES):
        raise ValueError("%s is at %s, outside office hours" % (what, moment.strftime("%H:%M")))
    if not FIRST <= moment <= LAST:
        raise ValueError("%s is outside the story's twelve weeks" % what)
    return moment


def body(paragraph: str, acceptance=()) -> str:
    """A task's whole body: why it exists, then what would make it true.

    The template ships one `- [ ]` of its own, so the body is written whole rather than
    appended to — the checklist apps count the boxes in the file and would count that
    one as work nobody did."""
    text = paragraph.strip()
    if acceptance:
        text += "\n\n## Acceptance\n\n" + "\n".join("- [ ] " + line for line in acceptance)
    return text + "\n"


def tick(moment, who, alias, index) -> engine.Event:
    """Ticks the index-th acceptance box, counting the ones already ticked.

    Counting all the boxes rather than the empty ones is what makes replaying twice
    produce the same file: box three is box three whatever happened to boxes one and two."""
    def fn(eng, event):
        path = eng.path(alias)
        lines = path.read_text(encoding="utf-8").split("\n")
        seen = 0
        for i, line in enumerate(lines):
            if line.startswith("- [ ] ") or line.startswith("- [x] "):
                seen += 1
                if seen == index:
                    lines[i] = "- [x] " + line[6:]
                    path.write_text("\n".join(lines), encoding="utf-8")
                    return []
        raise ValueError("%s has no acceptance box %d" % (alias, index))

    return engine.Event(moment, who, "raw", {"fn": fn, "touch": [alias]},
                        "{%s}: ticked an acceptance box" % alias)


def tag(moment, who, alias, names) -> engine.Event:
    """`docket new` has no --tags, so a tag is written the moment after the task is."""
    return engine.Event(moment, who, "set", {"task": alias, "tags": ",".join(names)},
                        "{%s}: tagged %s" % (alias, ", ".join(names)))


def relate(moment, who, alias, **relations) -> engine.Event:
    """One side of a relationship. Both sides are written unless the story means them to
    disagree — see the one-sided anomaly the products plant on purpose."""
    return story.relate(office_hours(when(moment), alias), PEOPLE[who], alias, **relations)


def lifecycle(spec: dict, project: str, prefix: str = "", index: int = 0) -> list[engine.Event]:
    """Every event one task ever produced, in the order it produced them."""
    kind = spec.get("type", "story")
    alias = prefix + spec["a"]
    owner = spec.get("who", "")
    writer = PEOPLE[spec.get("by") or WRITER.get(kind) or owner or "ingrid"]
    hand = PEOPLE[owner] if owner else writer

    made = office_hours(when(spec["made"]), alias)
    events = [story.new(made, writer, alias, spec["t"], project, type=kind,
                        assignee="[[%s]]" % owner if owner else "",
                        priority=spec.get("priority", ""),
                        labels=spec.get("labels", ""),
                        parent=prefix + spec["parent"] if spec.get("parent") else "",
                        body=body(spec["why"], spec.get("ok", ())))]

    if spec.get("tags"):
        events.append(tag(office_hours(made + 4 * MINUTE, alias), writer, alias, spec["tags"]))

    # Pulled into a sprint on the sprint's first morning, in planning, unless the task
    # did not exist yet — work written mid-sprint joins the one that is running.
    pulled = None
    names = spec.get("sprint") or ()
    for name in (names,) if isinstance(names, str) else names:
        sp = SPRINTS[name]
        moment = dt.datetime.combine(sp.starts, dt.time(9, 15 + index % 40))
        if moment <= made:
            moment = made + 20 * MINUTE
        events.append(story.sprint(office_hours(moment, alias), PEOPLE["ingrid"], alias, name))
        pulled = pulled or moment

    if spec.get("pts"):
        sizer = PEOPLE["ingrid"] if kind in ("story", "epic") else hand
        events.append(story.estimate(office_hours((pulled or made) + MINUTE, alias),
                                     sizer, alias, spec["pts"]))

    moves = [(office_hours(when(m[0]), alias), m[1], PEOPLE[m[2] if len(m) > 2 else owner])
             for m in spec.get("moves", ())]
    for moment, status, who in moves:
        events.append(story.move(moment, who, alias, status))

    events += _ticks(spec, alias, hand, moves)

    for moment, who, text in spec.get("says", ()):
        events.append(story.comment(office_hours(when(moment), alias), PEOPLE[who], alias, text))

    return sorted(events, key=lambda e: e.when)


def _ticks(spec, alias, hand, moves) -> list[engine.Event]:
    """Acceptance boxes get ticked as the work becomes true, which is just before the
    card is moved on: everything for work that finished, all but the last argument for
    work waiting in review, and whatever the spec says for work still in hand."""
    boxes = len(spec.get("ok", ()))
    if not boxes:
        return []
    final = moves[-1][1] if moves else "Backlog"
    count = spec.get("ticked")
    if count is None:
        count = boxes if final == "Done" else boxes - 1 if final in ("In review", "QA") else 0
    if not count:
        return []
    if count > boxes:
        raise ValueError("%s has %d acceptance boxes and ticks %d" % (alias, boxes, count))

    if spec.get("ticks"):
        base = when(spec["ticks"])
    else:
        if not moves:
            raise ValueError("%s has ticked set but no moves to base the tick on" % alias)
        base = next((m for m, status, _ in moves if status in DOING), moves[-1][0])
    started = next((m for m, status, _ in moves if status == "In progress"), None)
    first = base - 5 * count * MINUTE
    if started and first <= started:
        raise ValueError("%s ticks a box at %s, before the work started" % (alias, first))
    return [tick(office_hours(base - 5 * (count - k) * MINUTE, alias), hand, alias, k + 1)
            for k in range(count)]


def leaves_only(specs, prefix="") -> None:
    """Rule 12: a container's size is what its children add up to, so an estimate on a
    task that has children is a second answer to the same question. Refused here rather
    than found by `docket check` after four hundred commits."""
    parents = {prefix + s["parent"] for s in specs if s.get("parent")}
    for spec in specs:
        if spec.get("pts") and prefix + spec["a"] in parents:
            raise ValueError("%s has children and an estimate" % spec["a"])
