import datetime as dt, os, pathlib, shutil, subprocess, tempfile, unittest
import engine, vault

DOCKET = os.environ.get("DOCKET_BIN", "docket")
TEMPLATE = "/Volumes/Develop/develop/docket-template"
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

    def test_replay_sorts_by_time_and_check_is_clean(self):
        late = engine.Event(dt.datetime(2026, 6, 16, 9, 0), ING, "comment", {"task": "a", "text": "Later."}, "c")
        early = engine.Event(dt.datetime(2026, 6, 15, 9, 0), ING, "new",
                             {"alias": "a", "title": "T", "type": "task", "project": "ACME"}, "m")
        self.e.replay([late, early])
        self.assertIn("**ingrid · 2026-06-16 09:00** — Later.", self.e.path("a").read_text())
        out = subprocess.run([DOCKET, "check", "."], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

if __name__ == "__main__":
    unittest.main()
