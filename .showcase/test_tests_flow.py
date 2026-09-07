"""What has to be true of the test flow before a replay is worth ten minutes.

None of this runs a hook or touches the vault. What it can check without either is the
part that would be expensive to get wrong: the schedule, the revision arithmetic, the
stamping, and every name this module says out loud — a bug alias, a case id, a feature
file — against the modules that actually define them.
"""
from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import codebase
import tests_flow
import vault
from products import fieldnote, harbor, ledgerline
from products.common import FIRST, LAST, when


def work_aliases() -> dict:
    """Every task the three products write down, by alias, with the minute it was made."""
    out = {}
    for module in (harbor, ledgerline, fieldnote):
        for spec in module.WORK:
            out[module.PREFIX + spec["a"]] = when(spec["made"])
    return out


class TheSchedule(unittest.TestCase):

    def setUp(self):
        self.runs = tests_flow.schedule()

    def test_seventeen_of_them(self):
        self.assertEqual(len(self.runs), 17)

    def test_in_order_and_inside_the_story(self):
        for before, after in zip(self.runs, self.runs[1:]):
            self.assertLess(before[1], after[1])
        for _, moment, _ in self.runs:
            self.assertLessEqual(FIRST, moment)
            self.assertLessEqual(moment, LAST)

    def test_the_last_event_of_the_story_is_still_the_story_s(self):
        """The vault's last event is a retrospective at 16:40 on 09-04. An execution after
        it would make the twelve weeks end on a machine writing a chart."""
        for _, moment, _ in self.runs:
            if moment.date() == dt.date(2026, 9, 4):
                self.assertLess(moment, dt.datetime(2026, 9, 4, 16, 0))

    def test_afternoons_only(self):
        for product, moment, _ in self.runs:
            self.assertLessEqual(dt.time(15, 0), moment.time(), product)
            self.assertLessEqual(moment.time(), dt.time(17, 30), product)

    def test_eight_dates_and_the_products_that_run_on_them(self):
        days = sorted({moment.date() for _, moment, _ in self.runs})
        self.assertEqual(len(days), 8)
        for day in days:
            self.assertLess(day.weekday(), 5, day)
        by_product = {}
        for product, moment, _ in self.runs:
            by_product.setdefault(product, []).append(moment.strftime("%m-%d"))
        self.assertEqual(by_product["harbor"],
                         ["07-03", "07-10", "07-24", "07-27", "08-05", "08-14", "08-28", "09-04"])
        self.assertEqual(by_product["ledgerline"], ["07-24", "08-14", "08-28", "09-04"])
        self.assertEqual(by_product["fieldnote"],
                         ["07-27", "08-05", "08-14", "08-28", "09-04"])

    def test_only_the_release_candidate_says_production(self):
        for product, moment, environment in self.runs:
            wanted = "production" if moment.date() == dt.date(2026, 9, 4) else "staging"
            self.assertEqual(environment, wanted, (product, moment))

    def test_a_product_is_never_run_twice_in_one_day(self):
        seen = [(product, moment.date()) for product, moment, _ in self.runs]
        self.assertEqual(len(seen), len(set(seen)))


class WhatAFailureFound(unittest.TestCase):

    def setUp(self):
        self.work = work_aliases()
        self.days = {(product, moment.strftime("%m-%d"))
                     for product, moment, _ in tests_flow.schedule()}

    def test_every_annotation_is_about_an_execution_that_happens(self):
        for product, day, _, _, _, _ in tests_flow.FOUND:
            self.assertIn((product, day), self.days)

    def test_every_bug_is_one_a_product_writes_down(self):
        for _, _, _, bug, _, _ in tests_flow.FOUND:
            if bug:
                self.assertIn(bug, self.work)

    def test_a_run_never_finds_a_bug_the_board_has_not_got(self):
        """Two of these are dated days after the execution they are about, and that is
        the whole reason they are separate events."""
        for product, day, ident, bug, moment, _ in tests_flow.FOUND:
            if not bug:
                continue
            self.assertLess(self.work[bug], when(moment),
                            "%s %s points at %s before it exists" % (product, ident, bug))

    def test_the_annotation_comes_after_the_run_it_annotates(self):
        by_day = {(product, moment.strftime("%m-%d")): moment
                  for product, moment, _ in tests_flow.schedule()}
        for product, day, _, _, moment, _ in tests_flow.FOUND:
            self.assertLess(by_day[(product, day)], when(moment))

    def test_inside_office_hours(self):
        for product, day, _, _, moment, _ in tests_flow.FOUND:
            said = when(moment)
            self.assertLess(said.weekday(), 5, (product, day))
            self.assertLessEqual(dt.time(9, 0), said.time())
            self.assertLess(said.time(), dt.time(18, 0))

    def test_each_failure_is_named_once_per_execution(self):
        named = [(product, day, ident) for product, day, ident, _, _, _ in tests_flow.FOUND]
        self.assertEqual(len(named), len(set(named)))


class NamesTheCodeAlsoUses(unittest.TestCase):
    """Every string this module shares with the repository it reads, checked against it."""

    def feature(self, path):
        return codebase._render(path, LAST)

    def test_the_nine_feature_files_are_the_nine_that_exist(self):
        written = sorted(path for path in codebase.BLOCKS if path.endswith(".feature"))
        said = sorted("features/%s/%s" % (product, name)
                      for product, files in tests_flow.FEATURES.items()
                      for name, _ in files)
        self.assertEqual(said, written)

    def test_each_set_is_named_after_its_feature_s_own_line(self):
        for product, files in tests_flow.FEATURES.items():
            for name, title in files:
                text = self.feature("features/%s/%s" % (product, name))
                self.assertEqual(text.splitlines()[0], "Feature: " + title)

    def test_every_case_id_a_failure_names_is_in_the_suite(self):
        whole = "\n".join(self.feature(path) for path in codebase.BLOCKS
                          if path.endswith(".feature"))
        for _, _, ident, bug, _, _ in tests_flow.FOUND:
            if bug:                              # a written tag, so the suite carries it
                self.assertIn("@" + ident, whole)

    def test_the_photo_failure_s_id_is_derived_from_the_scenario_that_fails(self):
        """It carries no tag, so its identity is the feature file and the scenario name —
        derived by the same function both importers use. Rename the scenario and this
        test fails before the replay does."""
        lines = self.feature("features/fieldnote/sync.feature").splitlines()
        titles = [n for n, line in enumerate(lines)
                  if line.strip() == "Scenario: A job finished offline keeps its photographs"]
        self.assertEqual(len(titles), 1)
        above = [line.strip() for line in lines[:titles[0]] if line.strip()][-1]
        self.assertFalse(above.startswith("@"), "it has a tag now: " + above)
        self.assertEqual(tests_flow.PHOTOS,
                         tests_flow.caseid.derived(
                             "sync.feature",
                             "A job finished offline keeps its photographs", "FIELD"))
        self.assertRegex(tests_flow.PHOTOS, tests_flow.caseid.DERIVED)

    def test_the_projects_are_the_vault_s(self):
        keys = {project for project, _ in tests_flow.PRODUCTS.values()}
        self.assertEqual(keys, {"HARBOR", "LEDGER", "FIELD"})
        self.assertEqual(set(tests_flow.PRODUCTS), set(tests_flow.FEATURES))


class RevisionAt(unittest.TestCase):
    """The newest commit at or before a moment, on a repository built for the purpose."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = pathlib.Path(cls._tmp.name) / "repo"
        cls.root.mkdir(parents=True)
        cls.shas = {}
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=cls.root, check=True)
        for day, clock in (("06-15", "10:00"), ("06-23", "09:00"), ("07-03", "11:30")):
            (cls.root / "file.txt").write_text(day + " " + clock)
            stamp = "2026-%s %s:00 +0000" % (day, clock)
            env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp,
                   "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@e",
                   "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@e"}
            subprocess.run(["git", "add", "-A"], cwd=cls.root, check=True)
            subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", day],
                           cwd=cls.root, check=True, env=env)
            cls.shas[day] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=cls.root,
                                           check=True, capture_output=True,
                                           text=True).stdout.strip()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_the_commit_of_the_day(self):
        self.assertEqual(tests_flow.revision_at(self.root, when("06-23 09:00")),
                         self.shas["06-23"])

    def test_the_newest_one_before(self):
        self.assertEqual(tests_flow.revision_at(self.root, when("06-30 16:00")),
                         self.shas["06-23"])

    def test_a_minute_before_a_commit_is_the_one_before_it(self):
        self.assertEqual(tests_flow.revision_at(self.root, when("06-23 08:59")),
                         self.shas["06-15"])

    def test_the_last_one(self):
        self.assertEqual(tests_flow.revision_at(self.root, when("09-04 15:00")),
                         self.shas["07-03"])

    def test_refuses_a_moment_before_the_repository(self):
        with self.assertRaises(ValueError):
            tests_flow.revision_at(self.root, when("06-01 10:00"))

    def test_utc_rather_than_the_machine_s_own_clock(self):
        """The commits are UTC. Read in a timezone thirteen hours away, a bare date would
        pick a different commit — which is how a replay in Auckland stops matching one in
        Lisbon."""
        was = os.environ.get("TZ")
        try:
            os.environ["TZ"] = "Pacific/Auckland"
            self.assertEqual(tests_flow.revision_at(self.root, when("06-23 09:30")),
                             self.shas["06-23"])
        finally:
            if was is None:
                os.environ.pop("TZ", None)
            else:
                os.environ["TZ"] = was


class TinyEngine:
    """Enough engine for `stamp_touched`: a root and git run inside it."""

    def __init__(self, root):
        self.root = pathlib.Path(root)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout


class StampsWhatTheHooksWrote(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        (self.root / "HARBOR").mkdir()
        (self.root / "attachments").mkdir()
        self.old = self.root / "HARBOR" / "HARBOR-1 An older task.md"
        self.old.write_text("---\nkey: HARBOR-1\ncreated: 2026-06-15T09:30:00Z\n"
                            "updated: 2026-06-15T09:30:00Z\n---\n\nBody.\n")
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "user.name=T",
                        "-c", "user.email=t@e", "commit", "-q", "-m", "base"],
                       cwd=self.root, check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_new_file_is_created_and_updated_and_an_old_one_only_updated(self):
        new = self.root / "HARBOR" / "HARBOR-2 A test the hook wrote.md"
        new.write_text("---\nkey: HARBOR-2\ncreated: 2026-09-07T18:00:00Z\n"
                       "updated: 2026-09-07T18:00:00Z\n---\n\nBody.\n")
        self.old.write_text(self.old.read_text() + "\nA hook appended this.\n")
        (self.root / "attachments" / "test-results.svg").write_text("<svg/>")

        moment = when("07-03 16:00")
        stamped = tests_flow.stamp_touched(TinyEngine(self.root), moment)
        self.assertEqual(stamped, ["HARBOR/HARBOR-1 An older task.md",
                                   "HARBOR/HARBOR-2 A test the hook wrote.md"])

        fresh, _ = vault.read_frontmatter(new)
        self.assertEqual(fresh["created"], "2026-07-03T16:00:00Z")
        self.assertEqual(fresh["updated"], "2026-07-03T16:00:00Z")

        older, _ = vault.read_frontmatter(self.old)
        self.assertEqual(older["created"], "2026-06-15T09:30:00Z")
        self.assertEqual(older["updated"], "2026-07-03T16:00:00Z")

    def test_it_leaves_everything_that_is_not_a_task_alone(self):
        (self.root / "attachments" / "test-results.svg").write_text("<svg/>")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "a-page.md").write_text("---\ntype: page\n---\n\nA page.\n")
        self.assertEqual(tests_flow.stamp_touched(TinyEngine(self.root), when("07-03 16:00")),
                         [])

    def test_a_clean_vault_stamps_nothing(self):
        self.assertEqual(tests_flow.stamp_touched(TinyEngine(self.root), when("07-03 16:00")),
                         [])


class TheEvents(unittest.TestCase):
    """The list itself, without replaying any of it."""

    def setUp(self):
        self.events = tests_flow.events(pathlib.Path("/nowhere/northlight"))

    def test_one_per_step(self):
        self.assertEqual(len(self.events), 3 + 17 + len(tests_flow.FOUND))

    def test_all_raw_and_all_mateo_s(self):
        for event in self.events:
            self.assertEqual(event.kind, "raw")
            self.assertEqual(event.who.handle, "mateo")
            self.assertTrue(callable(event.args["fn"]))

    def test_inside_the_twelve_weeks(self):
        for event in self.events:
            self.assertLessEqual(FIRST, event.when)
            self.assertLessEqual(event.when, LAST)

    def test_the_plan_comes_before_the_first_import_and_the_import_before_the_coverage(self):
        first = sorted(self.events, key=lambda e: e.when)[:3]
        self.assertEqual([e.when for e in first],
                         [when(tests_flow.PLANNED), when(tests_flow.IMPORTED),
                          when(tests_flow.COVERED)])

    def test_no_two_events_share_a_minute(self):
        moments = [event.when for event in self.events]
        self.assertEqual(len(moments), len(set(moments)))


class TheInversesItOwes(unittest.TestCase):
    """`_mirror` is for what this module sets itself, and nothing else.

    The app's importers write both sides of `runs`/`run_by` and `tests`/`tested_by` now.
    Mirroring those here again would be dead code that quietly hides the day an importer
    stops doing it, so the table has to be exactly the two verbs this module writes.
    """

    def test_only_what_the_flow_sets_with_its_own_docket_set(self):
        self.assertEqual(tests_flow.INVERSES,
                         {"includes": "included_in", "found": "found_in"})

    def test_those_two_verbs_are_the_ones_the_module_writes(self):
        source = pathlib.Path(tests_flow.__file__).read_text(encoding="utf-8")
        written = set(re.findall(r'"(\w+)=" *\+', source))
        self.assertEqual(written & {"includes", "found", "runs", "tests"},
                         set(tests_flow.INVERSES))

    def test_the_relations_are_the_vault_s_own(self):
        declared = (pathlib.Path(tests_flow.ROOT) / "docket.yaml").read_text(encoding="utf-8")
        for name, inverse in tests_flow.INVERSES.items():
            self.assertIn("- name: %s" % name, declared)
            self.assertIn("inverse: %s" % inverse, declared)


if __name__ == "__main__":
    unittest.main()
