"""What has to be true of the `northlight` repository before it is worth pushing anywhere.

The vault is not needed for any of this: a stub engine hands out a made-up key for every
alias the commit subjects use, so the whole history can be built into a temporary
directory and read back.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import codebase

CASE_ID = re.compile(r"^@(HARBOR|LEDGER|FIELD)-[A-Z]{3}-\d{3}$")


class StubEngine:
    """Enough engine for a code event: a key for every alias, and nothing else."""

    def __init__(self, aliases):
        self.keys = {alias: "%s-%d" % (alias.split(".")[0].upper()[:6], number)
                     for number, alias in enumerate(sorted(aliases), start=1)}


def used_aliases():
    return {alias for _, _, subject in codebase.COMMITS
            for alias in codebase._aliases(subject)}


def build(root, keys=None):
    """Replay the whole code history into `root` and give back the HEAD sha."""
    events = codebase.events(root)
    engine = StubEngine(used_aliases() if keys is None else keys)
    for event in events:
        event.args["fn"](engine, event)
    return codebase._git(pathlib.Path(root), "rev-parse", "HEAD").strip()


class BuildsOnce(unittest.TestCase):
    """One build, read many ways."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = pathlib.Path(cls._tmp.name) / "northlight"
        cls.head = build(cls.root)
        cls.log = codebase._git(cls.root, "log", "--format=%H%x09%ae%x09%s").splitlines()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_enough_commits(self):
        self.assertGreaterEqual(len(self.log), 55, "the history is too short to be a repository")

    def test_six_authors(self):
        emails = {line.split("\t")[1] for line in self.log}
        self.assertEqual(len(emails), 6, emails)
        for email in emails:
            self.assertTrue(email.endswith("@northlight.example"), email)

    def test_no_alias_left_in_a_subject(self):
        for line in self.log:
            self.assertNotIn("{", line.split("\t")[2], line)

    def test_sixty_scenarios(self):
        found = sum(1 for path in sorted((self.root / "features").rglob("*.feature"))
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if line.strip().startswith("Scenario:"))
        self.assertEqual(found, 60)

    def test_forty_four_case_ids_and_no_other_tags(self):
        tags = [line.strip() for path in sorted((self.root / "features").rglob("*.feature"))
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip().startswith("@")]
        self.assertEqual(len(tags), 44, tags)
        for tag in tags:
            self.assertRegex(tag, CASE_ID)
        self.assertEqual(len(set(tags)), 44, "a case id is used twice")

    def test_run_tests_is_executable(self):
        script = self.root / "run-tests"
        self.assertTrue(script.exists())
        self.assertTrue(os.access(script, os.X_OK), "run-tests is not executable")

    def test_every_python_file_compiles(self):
        files = sorted(str(p) for p in self.root.rglob("*.py"))
        self.assertTrue(files)
        done = subprocess.run([sys.executable, "-m", "py_compile", *files],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_the_layout_the_plan_asked_for(self):
        for path in ("README.md", "pyproject.toml", ".gitignore", "run-tests",
                     "harbor/booking.py", "harbor/invoice.py", "harbor/checkin.py",
                     "ledgerline/invoices.py", "ledgerline/bankimport.py", "ledgerline/tax.py",
                     "fieldnote/jobs.py", "fieldnote/routes.py", "fieldnote/sync.py",
                     "features/environment.py", "features/steps/harbor_steps.py",
                     "features/steps/ledgerline_steps.py", "features/steps/fieldnote_steps.py"):
            self.assertTrue((self.root / path).exists(), path)

    def test_gitignore_keeps_the_venv_out(self):
        text = (self.root / ".gitignore").read_text(encoding="utf-8")
        for line in (".venv/", "__pycache__/", "reports/"):
            self.assertIn(line, text)


class BuildsTheSameTwice(unittest.TestCase):
    def test_same_head_from_the_same_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "northlight"
            first = build(root)
            second = build(root)
            self.assertEqual(first, second, "a second replay produced a different history")

    def test_same_head_from_a_different_directory(self):
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            self.assertEqual(build(pathlib.Path(one) / "northlight"),
                             build(pathlib.Path(two) / "northlight"))


class RefusesRatherThanGuesses(unittest.TestCase):
    def test_an_alias_the_engine_does_not_know_raises(self):
        aliases = used_aliases()
        missing = sorted(a for a in aliases if a.startswith("harbor."))[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "northlight"
            with self.assertRaises(ValueError) as caught:
                build(root, keys=aliases - {missing})
            self.assertIn(missing, str(caught.exception))

    def test_every_alias_is_written_down_before_it_is_named(self):
        made = codebase._made_dates()
        for text, _, subject in codebase.COMMITS:
            for alias in codebase._aliases(subject):
                self.assertIn(alias, made, subject)
                self.assertLess(made[alias], codebase.when(text), subject)


class NamesStaySteady(unittest.TestCase):
    """A derived case id is the feature file's name and the scenario's, so neither may
    move once the results importer has seen it."""

    def test_a_scenario_keeps_its_name_when_it_is_rewritten(self):
        for path, blocks in codebase.BLOCKS.items():
            if not path.endswith(".feature"):
                continue
            titles = {}
            for name, since, text in blocks:
                lines = [line.strip() for line in text.splitlines()
                         if line.strip().startswith(("Scenario:", "Feature:"))]
                self.assertTrue(lines, (path, name))
                titles.setdefault(name, lines)
                self.assertEqual(titles[name], lines,
                                 "%s: %s was renamed at %s" % (path, name, since))

    def test_the_two_scenarios_that_are_meant_to_fail_are_there(self):
        rendered = "\n".join(
            codebase._render(path, codebase.when(codebase.COMMITS[-1][0]))
            for path in codebase.BLOCKS if path.endswith(".feature"))
        self.assertIn("Scenario: A refund larger than the invoice it credits is refused", rendered)
        self.assertIn("Scenario: A job finished offline keeps its photographs", rendered)
        self.assertIn("@HARBOR-PAY-004", rendered)


class TheStoryItself(unittest.TestCase):
    def test_the_timeline_validates(self):
        self.assertEqual(len(codebase._timeline()), len(codebase.COMMITS))

    def test_no_date_is_computed_from_now(self):
        source = pathlib.Path(codebase.__file__).read_text(encoding="utf-8")
        for banned in ("datetime.now", "date.today", "time.time"):
            self.assertNotIn(banned, source)


if __name__ == "__main__":
    unittest.main()
