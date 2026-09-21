import datetime as dt, os, pathlib, shutil, subprocess, tempfile, unittest
import engine, vault

DOCKET = os.environ.get("DOCKET_BIN", "docket")
# Where `docket init` clones an empty vault from. Point SHOWCASE_TEMPLATE at a
# local clone to run these tests without the network.
TEMPLATE = os.environ.get("SHOWCASE_TEMPLATE", "https://github.com/didenkolab/docket-template.git")
ING = engine.Person("ingrid", "Ingrid Solberg", "ingrid@northlight.example", "product")

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run([DOCKET, "init", "--key", "ACME", "--template", TEMPLATE, "--author", "T <t@example.com>", "."],
                       cwd=self.root, check=True, capture_output=True)
        self.e = engine.Engine(self.root, DOCKET)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_new_sets_created_and_commits_as_author(self):
        ev = engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                          {"alias": "a", "title": "Book a berth", "type": "story", "project": "ACME",
                           "assignee": "ingrid", "body": "Why.\n"}, "ACME-1: Book a berth")
        self.e.apply(ev)
        fm, body = vault.read_frontmatter(self.e.path("a"))
        self.assertEqual(fm["created"], "2026-06-15T09:00:00Z")
        self.assertEqual(fm["assignee"], "ingrid")
        self.assertIn("Why.", body)
        log = subprocess.run(["git", "log", "-1", "--format=%an <%ae> %ad %s", "--date=iso-strict"],
                             cwd=self.root, capture_output=True, text=True).stdout
        self.assertIn("Ingrid Solberg <ingrid@northlight.example> 2026-06-15T09:00:00Z", log)
        self.assertIn(self.e.key("a") + ": Book a berth", log)

    def test_set_moves_and_stamps_updated_only(self):
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                  {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m"))
        self.e.apply(engine.Event(dt.datetime(2026, 6, 16, 10, 0), ING, "set",
                                  {"task": "a", "status": "Ready"}, "moved"))
        fm, _ = vault.read_frontmatter(self.e.path("a"))
        self.assertEqual(fm["status"], "Ready")
        self.assertEqual(fm["created"], "2026-06-15T09:00:00Z")
        self.assertEqual(fm["updated"], "2026-06-16T10:00:00Z")

    def test_relation_by_alias(self):
        for alias in ("a", "b"):
            self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                      {"alias": alias, "title": alias.upper(), "type": "task", "project": "ACME"}, "m"))
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 5), ING, "set",
                                  {"task": "a", "blocked_by": ["b"]}, "blocked"))
        fm, _ = vault.read_frontmatter(self.e.path("a"))
        self.assertIn(self.e.key("b"), fm["blocked_by"])

    def test_declared_relations_read_from_vault(self):
        showcase = pathlib.Path(__file__).resolve().parent.parent
        rel = engine.declared_relations(showcase)
        for name in ("blocks", "relates", "logs", "logged", "contributes_to", "advanced_by", "tests", "found"):
            self.assertIn(name, rel, name)
        self.assertNotIn("logged_by", rel)
        self.assertNotIn("contributed_by", rel)
        self.assertEqual(engine.declared_relations(self.root) >= {"blocks", "blocked_by", "causes", "caused_by",
                                                                   "duplicates", "duplicated_by", "relates"}, True)

    def test_commit_message_substitutes_alias_for_key(self):
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                  {"alias": "a", "title": "Book a berth", "type": "story", "project": "ACME"},
                                  "{a}: Book a berth"))
        log = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.root,
                             capture_output=True, text=True).stdout.strip()
        self.assertEqual(log, "ACME-1: Book a berth")

    def test_commit_message_substitutes_a_dotted_alias(self):
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                  {"alias": "harbor.payments.refunds", "title": "Refund a booking",
                                   "type": "story", "project": "ACME"},
                                  "{harbor.payments.refunds}: Refund a booking"))
        log = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.root,
                             capture_output=True, text=True).stdout.strip()
        self.assertEqual(log, "ACME-1: Refund a booking")

    def test_an_unknown_dotted_alias_is_left_as_it_was_written(self):
        message = "{ledger.invoices.credit-notes}: waiting".format_map(engine._KeyMap(self.e))
        self.assertEqual(message, "ledger.invoices.credit-notes: waiting")

    def test_commit_does_not_stage_showcase(self):
        stray_dir = self.root / ".showcase"
        stray_dir.mkdir(parents=True, exist_ok=True)
        stray = stray_dir / "stray.py"
        stray.write_text("# not part of the story\n", encoding="utf-8")
        try:
            self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                      {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m"))
            out = subprocess.run(["git", "show", "--stat", "HEAD"], cwd=self.root,
                                 capture_output=True, text=True, check=True).stdout
            self.assertNotIn("stray.py", out)
        finally:
            shutil.rmtree(stray_dir, ignore_errors=True)

    def test_on_page_with_keys_writes_the_real_key(self):
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                  {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m"))
        real_key = self.e.key("a")
        ev = engine.Event(dt.datetime(2026, 6, 15, 9, 5), ING, "page",
                          {"path": "docs/notes/x.md", "title": "X", "kind": "page",
                           "body": "See {a} for details.", "keys": True}, "page")
        self.e.apply(ev)
        text = (self.root / "docs/notes/x.md").read_text(encoding="utf-8")
        self.assertIn("See %s for details." % real_key, text)

    def test_replay_sorts_by_time_and_check_is_clean(self):
        late = engine.Event(dt.datetime(2026, 6, 16, 9, 0), ING, "comment", {"task": "a", "text": "Later."}, "c")
        early = engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                             {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m")
        self.e.replay([late, early])
        self.assertIn("**ingrid · 2026-06-16 09:00** — Later.", self.e.path("a").read_text())
        out = subprocess.run([DOCKET, "check", "."], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def test_an_ignored_working_directory_does_not_stop_a_commit(self):
        """The vault ignores `.superpowers/`, where the showcase's own working
        notes live. A commit has to step over it rather than name it: git
        refuses an `add` whose pathspec mentions an ignored path, even to
        exclude it, and the whole replay stopped on the first event."""
        (self.root / ".gitignore").write_text(".superpowers/\n", encoding="utf-8")
        notes = self.root / ".superpowers" / "sdd"
        notes.mkdir(parents=True)
        (notes / "plan.md").write_text("# how this was built\n", encoding="utf-8")
        self.e.apply(engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                                  {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m"))
        files = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"],
                               cwd=self.root, capture_output=True, text=True).stdout
        self.assertIn(".md", files)
        self.assertNotIn(".superpowers", files)


if __name__ == "__main__":
    unittest.main()
