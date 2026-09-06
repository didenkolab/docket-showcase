"""What the quarter around the work must be true of before it is replayed.

The counts are here because a demo vault with two risks and one worklog demonstrates
nothing, and because they are the first thing to drift when the data is edited by hand.
Everything else in this file is a rule `docket check` or `docket anomalies` would find after
four hundred commits, asserted in a tenth of a second instead:

  * every alias crosscut names is a task some product actually creates,
  * a page only names work that existed on the day the page was written,
  * a worklog's parent carries no estimate (rule 12),
  * a request only becomes work that was written down after it was asked for,
  * every relation with an inverse is written from both ends,
  * and a decision has the four sections `docs/spec/documents.md` requires, in order.
"""
import collections
import datetime as dt
import pathlib
import re
import unittest

import crosscut
import story
from products import common, harbor, ledgerline, fieldnote

ALIASES = crosscut.ALIASES
PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_.-]*)\}")
SECTIONS = ("## Context", "## Decision", "## What this costs", "## Alternatives considered")
RELATIONS_WITH_INVERSE = crosscut._INVERSE


def news(events):
    return {e.args["alias"]: e for e in events if e.kind == "new"}


def kinds(events):
    return collections.Counter(e.args["type"] for e in events if e.kind == "new")


def referenced(event):
    """Every alias an event names: the task it is about, its parent, and every relation
    value on it. Statuses, hours and dates are not aliases and are left out."""
    args = event.args
    out = set()
    for name in ("task", "alias", "parent"):
        if args.get(name):
            out.add(args[name])
    for name, value in args.items():
        if name in RELATIONS_WITH_INVERSE or name in RELATIONS_WITH_INVERSE.values():
            out.update(value if isinstance(value, list) else [value])
    return out


class CountTests(unittest.TestCase):
    def setUp(self):
        self.events = crosscut.events()

    def test_the_quarter_is_the_size_it_says_it_is(self):
        c = kinds(self.events)
        self.assertEqual(c["objective"], 3)
        self.assertEqual(c["key_result"], 7)
        self.assertEqual(c["risk"], 6)
        self.assertEqual(c["incident"], 2)
        self.assertEqual(c["postmortem"], 2)
        self.assertEqual(c["request"], 8)
        self.assertEqual(c["worklog"], 30)
        self.assertEqual(sum(c.values()), 58)

    def test_the_data_and_the_events_agree(self):
        self.assertEqual(len(crosscut.OBJECTIVES), 3)
        self.assertEqual(len(crosscut.KEY_RESULTS), 7)
        self.assertEqual(len(crosscut.RISKS), 6)
        self.assertEqual(len(crosscut.INCIDENTS), 2)
        self.assertEqual(len(crosscut.POSTMORTEMS), 2)
        self.assertEqual(len(crosscut.REQUESTS), 8)
        self.assertEqual(len(crosscut.WORKLOGS), 30)
        self.assertEqual(len(crosscut.DECISIONS), 6)
        self.assertEqual(len(crosscut.DESIGN), 8)      # four pages, each rewritten once
        self.assertEqual(len(crosscut.INDEX), 2)

    def test_six_decisions_numbered_once_each(self):
        numbers = [d["n"] for d in crosscut.DECISIONS]
        self.assertEqual(numbers, ["0001", "0002", "0003", "0004", "0005", "0006"])
        pages = [e for e in self.events
                 if e.kind == "page" and e.args["kind"] == "decision"]
        self.assertEqual(len(pages), 6)
        for page in pages:
            self.assertRegex(pathlib.Path(page.args["path"]).name, r"^\d{4}-[a-z0-9-]+\.md$")
            self.assertEqual(page.args["extra"]["status"], "accepted")
            self.assertTrue(page.args["extra"]["date"].startswith("2026-"))


class ShapeTests(unittest.TestCase):
    def setUp(self):
        self.events = crosscut.events()
        self.made = news(self.events)

    def test_every_alias_named_is_one_somebody_creates(self):
        known = set(ALIASES) | set(self.made)
        for e in self.events:
            for alias in referenced(e):
                self.assertIn(alias, known, "%s names %s" % (e.message, alias))

    def test_the_epics_it_hangs_objectives_off_are_real(self):
        epics = {module.PREFIX + spec["a"]
                 for module in crosscut.PRODUCTS for spec in module.EPICS}
        for _, _, epic, kr in crosscut.CONTRIBUTIONS:
            self.assertIn(epic, epics, epic)
            self.assertIn(kr, self.made)

    def test_a_task_is_never_touched_before_it_exists(self):
        """Including the products' own tasks: a relation dated before the thing it names
        was written down is rule 10 after the replay, and a lie before it."""
        made = {alias: e.when for alias, e in self.made.items()}
        for e in _product_events():
            if e.kind == "new":
                made.setdefault(e.args["alias"], e.when)
        for e in sorted(self.events, key=lambda e: e.when):
            for alias in referenced(e):
                if alias in made:
                    self.assertLessEqual(made[alias], e.when, e.message + " names " + alias)

    def test_every_event_is_on_a_weekday_in_office_hours(self):
        for e in self.events:
            self.assertLess(e.when.weekday(), 5, e.message + " " + str(e.when))
            self.assertTrue(9 <= e.when.hour < 18, e.message + " " + str(e.when))
            self.assertTrue(story.at("2026-06-15", 9) <= e.when <= story.at("2026-09-04", 18))

    def test_both_sides_of_every_relation_are_written(self):
        """A relation with an inverse that only one side carries is what
        `docket anomalies --kind one-sided` reports, and Harbor plants the only one."""
        counterpart = dict(RELATIONS_WITH_INVERSE)
        counterpart.update({v: k for k, v in RELATIONS_WITH_INVERSE.items()})
        said = collections.defaultdict(set)
        for e in self.events:
            if e.kind != "set":
                continue
            for name, value in e.args.items():
                if name in counterpart:
                    said[(e.args["task"], name)].update(value)
        for (alias, name), targets in said.items():
            other = counterpart[name]
            for target in targets:
                self.assertIn(alias, said[(target, other)],
                              "%s %s %s and %s does not say so" % (alias, name, target, target))

    def test_the_bug_causes_the_incident_not_the_other_way_round(self):
        """The incident is what a customer saw; the bug is what did it. So the bug
        carries `causes` and the incident carries the inverse `caused_by`, not the
        other way round."""
        final = {}
        for e in self.events:
            if e.kind != "set":
                continue
            for name in ("causes", "caused_by"):
                if name in e.args:
                    final[(e.args["task"], name)] = list(e.args[name])
        for bug, incident in (("harbor.payments.double-charge", "inc.double-charge"),
                              ("field.offline.sync-loss", "inc.sync-loss")):
            self.assertEqual(final.get((bug, "causes")), [incident], bug)
            self.assertEqual(final.get((incident, "caused_by")), [bug], incident)


class RuleTests(unittest.TestCase):
    """The three rules that would otherwise be found by `docket check` after a replay."""

    def setUp(self):
        self.events = crosscut.events()
        self.made = news(self.events)
        self.specs = {module.PREFIX + spec["a"]: spec
                      for module in crosscut.PRODUCTS for spec in module.WORK}

    def test_no_worklog_hangs_off_a_task_that_has_a_number_on_it(self):
        """Rule 12: a container's size is what its children add up to, and a worklog is a
        child. Time is logged against work that was never sized, on purpose."""
        parents = {log["on"] for log in crosscut.WORKLOGS}
        self.assertGreaterEqual(len(parents), 5, "thirty worklogs on one task is not a quarter")
        for parent in parents:
            self.assertIn(parent, self.specs, parent)
            self.assertFalse(self.specs[parent].get("pts"),
                             "%s carries an estimate and worklogs" % parent)
        for log in crosscut.WORKLOGS:
            event = self.made[log["a"]]
            self.assertEqual(event.args["parent"], log["on"])
            self.assertEqual(event.args["status"], "Done")

    def test_hours_and_the_flag_say_what_they_should(self):
        for e in self.events:
            if e.kind != "set" or "spent" not in e.args:
                continue
            self.assertTrue(1 <= e.args["spent"] <= 6, e.message)
            billable = e.args["billable"] == "true"
            self.assertEqual(billable, e.args["logs"][0].startswith("harbor."), e.message)
        total = sum(log["spent"] for log in crosscut.WORKLOGS)
        self.assertTrue(80 <= total <= 130, "%d hours over two sprints" % total)

    def test_a_request_only_became_work_written_after_it_was_asked_for(self):
        became = 0
        for req in crosscut.REQUESTS:
            if not req.get("became"):
                continue
            became += 1
            asked = dt.date.fromisoformat(req["asked_on"])
            for alias in req["became"]:
                self.assertIn(alias, self.specs, alias)
                written = common.when(self.specs[alias]["made"]).date()
                self.assertGreater(written, asked,
                                   "%s became %s, which existed first" % (req["a"], alias))
        self.assertEqual(became, 3)
        refused = [r for r in crosscut.REQUESTS if r.get("cancelled")]
        self.assertEqual(len(refused), 2)
        for req in refused:
            self.assertIn("No", req["body"], "%s refuses without saying no" % req["a"])
        open_ones = [r for r in crosscut.REQUESTS
                     if not r.get("became") and not r.get("cancelled")]
        self.assertEqual(len(open_ones), 3)

    def test_definition_of_done_is_on_every_story_and_on_the_right_extras(self):
        held = {e.args["task"]: e.args["definition_of_done"] for e in self.events
                if e.kind == "set" and "definition_of_done" in e.args}
        for alias, spec in self.specs.items():
            if spec.get("dod"):
                self.assertNotIn(alias, held, "%s is held to two lists" % alias)
                continue
            if spec.get("type", "story") == "story":
                self.assertIn(alias, held, alias)
        self.assertEqual({a for a, v in held.items() if v == "release"},
                         set(crosscut.LAUNCH_STORIES))
        hotfix = {a for a, v in held.items() if v == "hotfix"}
        hotfix |= {a for a, s in self.specs.items() if s.get("dod") == "hotfix"}
        self.assertEqual(hotfix, set(crosscut.HOTFIX_BUGS))
        for alias in crosscut.LAUNCH_STORIES:
            self.assertEqual(self.specs[alias].get("type", "story"), "story")


class PageTests(unittest.TestCase):
    def setUp(self):
        self.events = crosscut.events()
        self.made = news(self.events)

    def pages(self, kind=None):
        return [e for e in self.events
                if e.kind == "page" and (kind is None or e.args["kind"] == kind)]

    def test_every_decision_has_the_four_sections_in_order(self):
        for page in self.pages("decision"):
            body = page.args["body"]
            at = [body.index(section) for section in SECTIONS]
            for section, where in zip(SECTIONS, at):
                self.assertGreater(where, 0, "%s has no %s" % (page.args["path"], section))
            self.assertEqual(at, sorted(at), "%s has them out of order" % page.args["path"])
            self.assertNotIn("## Status", body, "rule 14: status lives in the frontmatter")
            self.assertTrue(body.startswith("# ADR-"), page.args["path"])
            self.assertGreater(len(body.split()), 500, "%s is thin" % page.args["path"])

    def test_a_page_never_links_a_task(self):
        """`docs/spec/documents.md` §4.6: a decision names a task by key in backticks,
        because a page is not a place where work gathers. The same is true of the rest of
        these — the only wikilinks here are to other pages and to the drawing."""
        keys = {e.args["alias"] for e in self.events if e.kind == "new"} | set(ALIASES)
        for page in self.pages():
            for target in re.findall(r"\[\[([^\]]+)\]\]", page.args["body"]):
                name = target.split("|")[0].split("#")[0]
                self.assertNotIn(name, keys, "%s links a task" % page.args["path"])
                self.assertFalse(re.match(r"^[A-Z]+-\d+", name), page.args["path"])

    def test_a_page_only_names_work_that_existed_when_it_was_written(self):
        """An unassigned alias is written out as the alias rather than as a key, and
        nothing complains — so the check is here."""
        for page in self.pages():
            named = PLACEHOLDER.findall(page.args["body"])
            if named:
                self.assertTrue(page.args.get("keys"),
                                "%s names work and does not ask for keys" % page.args["path"])
            for alias in named:
                self.assertIn(alias, ALIASES, "%s names %s" % (page.args["path"], alias))
                made = min(e.when for e in _product_events() if
                           e.kind == "new" and e.args["alias"] == alias)
                self.assertLess(made, page.when,
                                "%s names %s before it exists" % (page.args["path"], alias))

    def test_the_design_pages_are_written_and_rewritten(self):
        design = self.pages("design")
        paths = collections.Counter(p.args["path"] for p in design)
        self.assertEqual(len(paths), 4)
        for path, times in paths.items():
            self.assertEqual(times, 2, "%s was never revisited" % path)
        first = [p for p in design if p.when.date() == dt.date(2026, 6, 16)]
        self.assertEqual(len(first), 4)
        for page in design:
            self.assertGreater(len(page.args["body"].split()), 300, page.args["path"])
            self.assertLess(len(page.args["body"].split()), 800, page.args["path"])

    def test_the_index_is_written_twice_and_lists_nothing(self):
        index = [p for p in self.pages() if p.args["path"] == "docs/index.md"]
        self.assertEqual(len(index), 2)
        self.assertEqual([p.when.date() for p in index],
                         [dt.date(2026, 6, 15), dt.date(2026, 9, 4)])
        for page in index:
            self.assertEqual(page.args["title"], "Northlight")

    def test_the_drawing_is_small_and_carries_no_font(self):
        svg = pathlib.Path(__file__).resolve().parent / "attachments" / "architecture.svg"
        text = svg.read_text(encoding="utf-8")
        self.assertLess(len(text.encode("utf-8")), 3072, "the drawing is over 3 KB")
        self.assertNotIn("@import", text)
        self.assertNotIn("http", text.replace("http://www.w3.org/2000/svg", ""))
        raw = [e for e in self.events if e.kind == "raw"]
        self.assertEqual(len(raw), 1)
        embed = [p for p in self.pages() if "![[architecture.svg]]" in p.args["body"]]
        self.assertTrue(embed)
        self.assertTrue(all(raw[0].when < p.when for p in embed))


class AttachTests(unittest.TestCase):
    """`common.attach` is the one event that carries bytes rather than Markdown."""

    def test_it_copies_the_file_into_the_vault(self):
        import tempfile

        class FakeEngine:
            def __init__(self, root):
                self.root = pathlib.Path(root)

        event = common.attach(common.when("06-16 11:00"), story.PEOPLE["ingrid"],
                              "architecture.svg", "the drawing")
        with tempfile.TemporaryDirectory() as tmp:
            event.args["fn"](FakeEngine(tmp), event)
            written = pathlib.Path(tmp, "attachments", "architecture.svg")
            self.assertTrue(written.exists())
            self.assertTrue(written.read_text(encoding="utf-8").startswith("<svg"))

    def test_it_refuses_a_file_that_is_not_there(self):
        with self.assertRaises(ValueError):
            common.attach(common.when("06-16 11:00"), story.PEOPLE["ingrid"],
                          "no-such-drawing.svg", "nothing")


_CACHE = []


def _product_events():
    if not _CACHE:
        for module in (harbor, ledgerline, fieldnote):
            _CACHE.extend(module.events())
    return _CACHE


if __name__ == "__main__":
    unittest.main()
