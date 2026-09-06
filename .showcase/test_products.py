"""What the products must be true of before anything is replayed into a vault.

Ledgerline and Fieldnote are written after Harbor, so they are imported lazily and their
own assertions skip while they are missing. Everything that is about Harbor, about the
sprint retrospectives, or about the rules `docket check` will apply to all three runs now.
"""
import collections
import importlib
import unittest

import story
from products import harbor

LATER = ("ledgerline", "fieldnote")

# The workflow, as docket.yaml declares it. Written out rather than parsed because the
# vault's YAML needs a parser the standard library does not have, and a second copy that
# `docket check` disagrees with would show up on the first replay.
TRANSITIONS = {
    "Backlog": {"Ready", "Cancelled"},
    "Ready": {"In progress", "Backlog", "Cancelled"},
    "In progress": {"In review", "Ready", "Cancelled"},
    "In review": {"QA", "In progress", "Cancelled"},
    "QA": {"Done", "In progress"},
    "Done": {"In progress"},
    "Cancelled": {"Backlog"},
}
SCALE = {1, 2, 3, 5, 8, 13}
DONE = ("Done", "Cancelled")


def later(name):
    """A product module that may not have been written yet."""
    try:
        return importlib.import_module("products." + name)
    except ModuleNotFoundError:
        return None


def products():
    return [harbor] + [module for module in (later(name) for name in LATER) if module]


def news(module):
    return [e for e in module.events() if e.kind == "new"]


class ProductTests(unittest.TestCase):
    def counts(self, module):
        return collections.Counter(e.args["type"] for e in news(module))

    def test_harbor_shape(self):
        c = self.counts(harbor)
        self.assertEqual(c["epic"], 4)
        self.assertEqual(c["subtask"], 10)
        self.assertEqual(c["story"] + c["task"] + c["bug"], 34)
        self.assertEqual((c["story"], c["task"], c["bug"]), (22, 6, 6))

    def shape(self, name, epics, subtasks, kinds):
        """One product's counts, or a skip while that product is still to be written.

        A test per product rather than one loop over both: a loop that skips on the
        product nobody has written yet reports the one that exists as skipped too, and a
        product whose shape is never asserted out loud is a product nobody is holding to
        it."""
        module = later(name)
        if module is None:
            self.skipTest("%s not written yet" % name)
        c = self.counts(module)
        self.assertEqual(c["epic"], epics)
        self.assertEqual(c["subtask"], subtasks)
        self.assertEqual(c["story"] + c["task"] + c["bug"], sum(kinds))
        self.assertEqual((c["story"], c["task"], c["bug"]), kinds)

    def test_ledgerline_shape(self):
        self.shape("ledgerline", epics=3, subtasks=6, kinds=(16, 5, 5))

    def test_fieldnote_shape(self):
        self.shape("fieldnote", epics=3, subtasks=8, kinds=(15, 5, 6))

    def test_every_alias_is_declared_and_unique(self):
        for module in products():
            with self.subTest(product=module.__name__):
                created = [e.args["alias"] for e in news(module)]
                self.assertEqual(len(created), len(set(created)))
                self.assertEqual(set(created), set(module.ALIASES))
                for alias, title in module.ALIASES.items():
                    self.assertTrue(alias.startswith(module.PREFIX), alias)
                    self.assertGreater(len(title), 10, alias)

    def test_every_bug_has_a_comment(self):
        for module in products():
            evs = module.events()
            bugs = {e.args["alias"] for e in evs if e.kind == "new" and e.args["type"] == "bug"}
            commented = {e.args["task"] for e in evs if e.kind == "comment"}
            self.assertTrue(bugs <= commented, bugs - commented)

    def test_every_cancelled_and_every_returned_task_says_why(self):
        for module in products():
            evs = module.events()
            commented = {e.args["task"] for e in evs if e.kind == "comment"}
            for alias, moves in _moves(evs).items():
                statuses = [status for _, status in moves]
                if "Cancelled" in statuses:
                    self.assertIn(alias, commented, "cancelled with no reason: " + alias)
                came_back = any(before in ("In review", "QA") and after == "In progress"
                                for (_, before), (_, after) in zip(moves, moves[1:]))
                if came_back:
                    self.assertIn(alias, commented, "returned with no reason: " + alias)

    def test_moves_follow_the_workflow(self):
        for module in products():
            for alias, moves in _moves(module.events()).items():
                status = "Backlog"
                for when, wanted in moves:
                    self.assertIn(wanted, TRANSITIONS[status],
                                  "%s: %s -> %s on %s" % (alias, status, wanted, when))
                    status = wanted

    def test_estimates_are_on_the_scale_and_only_on_leaves(self):
        for module in products():
            evs = module.events()
            parents = {e.args["parent"] for e in evs if e.kind == "new" and e.args.get("parent")}
            for e in evs:
                if e.kind == "set" and "estimate" in e.args:
                    self.assertIn(e.args["estimate"], SCALE, e.args["task"])
                    self.assertNotIn(e.args["task"], parents, "sized a container: " + e.args["task"])
            sized = {e.args["task"] for e in evs if e.kind == "set" and "estimate" in e.args}
            for e in news(module):
                if e.args["type"] == "epic":
                    self.assertNotIn(e.args["alias"], sized, "an epic is never sized")

    def test_labels_are_one_or_two_per_story_and_none_on_a_subtask(self):
        for module in products():
            for e in news(module):
                labels = [label for label in e.args.get("labels", "").split(",") if label]
                self.assertLessEqual(len(labels), 2, e.args["alias"])
                if e.args["type"] == "subtask":
                    self.assertEqual(labels, [], e.args["alias"])
                for label in labels:
                    self.assertIn(label, story.LABELS, e.args["alias"])

    def test_every_tag_is_on_at_least_two_tasks(self):
        carried = collections.defaultdict(set)
        for module in products():
            for e in module.events():
                if e.kind == "set" and "tags" in e.args:
                    for tag in e.args["tags"].split(","):
                        carried[tag].add(e.args["task"])
        self.assertTrue(carried, "no tags at all")
        for tag, tasks in carried.items():
            self.assertGreaterEqual(len(tasks), 2, "%r is a set of one" % tag)
            self.assertNotIn(tag.split("/")[-1], story.LABELS, "%r is a tag and a label" % tag)

    def test_a_body_says_why_and_what_would_make_it_true(self):
        for module in products():
            for e in news(module):
                body = e.args.get("body", "")
                self.assertGreater(len(body.split("\n")[0]), 60, e.args["alias"])
                self.assertNotIn("[[", body, "a body linking a task is rule 8's problem")
                if e.args["type"] != "subtask":
                    self.assertIn("## Acceptance", body, e.args["alias"])
                    boxes = body.count("- [ ] ")
                    self.assertTrue(2 <= boxes <= 4, "%s has %d boxes" % (e.args["alias"], boxes))

    def test_finished_work_is_fully_ticked_and_work_in_hand_is_not(self):
        for module in products():
            evs = module.events()
            boxes = {e.args["alias"]: e.args.get("body", "").count("- [ ] ") for e in news(module)}
            ticked = collections.Counter(e.args["touch"][0] for e in evs
                                         if e.kind == "raw" and "touch" in e.args)
            for alias, moves in _moves(evs).items():
                if not boxes.get(alias):
                    continue
                final = moves[-1][1] if moves else "Backlog"
                if final == "Done":
                    self.assertEqual(ticked[alias], boxes[alias], "not fully ticked: " + alias)
                elif final in ("Backlog", "Ready", "Cancelled"):
                    self.assertEqual(ticked[alias], 0, "ticked without being started: " + alias)
                else:
                    self.assertLess(ticked[alias], boxes[alias], "ticked and not finished: " + alias)

    def test_events_inside_the_window(self):
        # Nine in the morning rather than `at("2026-06-15")`'s default ten: sprint planning
        # is the first thing on a Monday, so the first sprint's pulls are at 09:15 on the
        # first day of the story. The rule the vault is held to is office hours, below.
        for module in products():
            for e in module.events():
                self.assertTrue(story.at("2026-06-15", 9) <= e.when <= story.at("2026-09-04", 18), e)

    def test_every_event_is_on_a_weekday_in_office_hours(self):
        for module in products():
            for e in module.events():
                self.assertLess(e.when.weekday(), 5, e.message + " " + str(e.when))
                self.assertTrue(9 <= e.when.hour < 18, e.message + " " + str(e.when))

    def test_a_task_is_never_touched_before_it_exists(self):
        for module in products():
            made = {e.args["alias"]: e.when for e in news(module)}
            for e in module.events():
                for alias in _about(e):
                    if alias in made:
                        self.assertLessEqual(made[alias], e.when, e.message)

    def test_retros_present(self):
        for s in story.SPRINTS[:5]:
            self.assertTrue(len(s.retro) > 200, s.name)
            self.assertEqual(len(s.retro.split("\n\n")), 3, s.name)
            self.assertNotIn("[[", s.retro, "rule 13: a sprint page does not link tasks")


class HarborAnomalyTests(unittest.TestCase):
    """The three anomalies Harbor plants, asserted from the events rather than hoped for."""

    def setUp(self):
        self.events = harbor.events(with_ledger=False)

    def test_the_adrift_task_is_adrift(self):
        alias = "harbor.loose.receipt-footer"
        made = next(e for e in self.events if e.kind == "new" and e.args["alias"] == alias)
        self.assertNotIn("parent", made.args)
        self.assertNotIn("labels", made.args)
        for e in self.events:
            if e is made:
                continue
            self.assertNotIn(alias, _about(e), "something links the adrift task: " + e.message)
            self.assertNotIn(alias, str(e.args.get("parent", "")))

    def test_the_ops_chain_is_only_ola(self):
        chain = [spec for spec in harbor.WORK
                 if spec.get("parent") == "ops.season-runbook"]
        self.assertGreaterEqual(len(chain), 3)
        for spec in chain:
            self.assertEqual(spec["who"], "ola")
            self.assertNotIn(spec.get("moves", [(0, "Backlog")])[-1][1], DONE)

    def test_exactly_one_relation_has_no_other_side(self):
        pairs = set()
        for _, _, alias, relations in harbor.RELATIONS:
            for name, others in relations.items():
                for other in others:
                    pairs.add((name, alias, other))
        inverse = {"blocks": "blocked_by", "blocked_by": "blocks",
                   "duplicates": "duplicated_by", "duplicated_by": "duplicates"}
        lonely = [p for p in pairs
                  if p[0] in inverse and (inverse[p[0]], p[2], p[1]) not in pairs]
        self.assertEqual(lonely, [("blocks", "payments.refund-over", "payments.refunds")])

    def test_something_has_been_in_review_since_the_middle_of_august(self):
        stuck = [spec for spec in harbor.WORK
                 if spec.get("moves") and spec["moves"][-1][1] == "In review"
                 and spec["moves"][-1][0] < "08-20"]
        self.assertTrue(stuck, "nothing for the time-in-status report to notice")
        for spec in stuck:
            last = max(when for when, *_ in spec["moves"])
            for when, _, _ in spec.get("says", ()):
                self.assertLess(when, last, "%s was touched after it stalled" % spec["a"])

    def test_ledgerline_is_only_reached_when_it_is_there(self):
        without = harbor.events(with_ledger=False)
        with_it = harbor.events(with_ledger=True)
        self.assertEqual(len(with_it) - len(without), 2)
        self.assertFalse([e for e in without if "ledger." in str(e.args)])
        self.assertTrue([e for e in with_it if "ledger.invoices.credit-notes" in str(e.args)])


def _moves(events):
    """alias -> [(when, status)], in order."""
    out = collections.defaultdict(list)
    for e in sorted(events, key=lambda e: e.when):
        if e.kind == "set" and "status" in e.args:
            out[e.args["task"]].append((e.when, e.args["status"]))
    return out


def _about(event):
    """Every alias an event names, whatever kind it is."""
    args = event.args
    named = set()
    for key, value in args.items():
        if key in ("task", "parent"):
            named.add(value)
        elif key == "touch":
            named.update(value)
        elif isinstance(value, list) and key != "touch":
            named.update(v for v in value if isinstance(v, str))
    return named


if __name__ == "__main__":
    unittest.main()
