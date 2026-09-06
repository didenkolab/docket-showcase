import tempfile, unittest, pathlib, datetime as dt
import vault

TASK = """---
key: HARBOR-1
title: Book a berth
type: story
status: Backlog
status_category: todo
priority: normal
assignee: ingrid
labels: []
created: 2026-09-06T10:00:00Z
updated: 2026-09-06T10:00:00Z
aliases: []
---

Body text.

## Comments
"""

class VaultTests(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        (self.dir / "HARBOR").mkdir()
        self.task = self.dir / "HARBOR" / "HARBOR-1 Book a berth.md"
        self.task.write_text(TASK)

    def test_stamp_rewrites_updated_and_created(self):
        vault.stamp(self.task, dt.datetime(2026, 6, 15, 9, 30), created=True)
        fm, _ = vault.read_frontmatter(self.task)
        self.assertEqual(fm["created"], "2026-06-15T09:30:00Z")
        self.assertEqual(fm["updated"], "2026-06-15T09:30:00Z")

    def test_patch_appends_missing_key_before_closing(self):
        vault.patch_frontmatter(self.task, estimate="3")
        text = self.task.read_text()
        self.assertIn("estimate: 3\n---\n\nBody", text)

    def test_append_comment_format(self):
        vault.append_comment(self.task, "ingrid", dt.datetime(2026, 6, 16, 14, 3), "Reproduced.")
        self.assertTrue(self.task.read_text().endswith(
            "## Comments\n\n**ingrid · 2026-06-16 14:03** — Reproduced.\n"))

    def test_set_body_keeps_comments(self):
        vault.append_comment(self.task, "ingrid", dt.datetime(2026, 6, 16, 14, 3), "Kept.")
        vault.set_body(self.task, "New body.\n")
        text = self.task.read_text()
        self.assertIn("New body.", text)
        self.assertIn("**ingrid · 2026-06-16 14:03** — Kept.", text)
        self.assertNotIn("Body text.", text)

    def test_write_page_and_person(self):
        p = self.dir / "docs" / "sprints" / "Sprint 1.md"
        vault.write_page(p, "Sprint 1", "sprint", dt.date(2026, 6, 26), "# Sprint 1\n\nGoal.\n",
                         starts="2026-06-15", ends="2026-06-26")
        self.assertTrue(p.read_text().startswith("---\ntitle: Sprint 1\ntype: sprint\nupdated: 2026-06-26\nstarts: 2026-06-15\nends: 2026-06-26\n---\n"))
        q = self.dir / "people" / "ingrid.md"
        vault.write_person(q, "ingrid", "Ingrid Solberg")
        self.assertIn("type: person\nname: ingrid\n", q.read_text())

    def test_a_page_title_with_a_colon_stays_valid_yaml(self):
        """`title: Offline first: the phone wins` is a mapping inside a mapping and every
        reader of the vault refuses the file. Decision 0004 has exactly that title."""
        p = self.dir / "docs" / "decisions" / "0004-offline-first.md"
        vault.write_page(p, "Offline first: the phone is the source of truth", "decision",
                         dt.date(2026, 7, 31), "# ADR-0004\n", status="accepted",
                         date="2026-07-31")
        text = p.read_text()
        self.assertIn("title: 'Offline first: the phone is the source of truth'\n", text)
        self.assertIn("status: accepted\n", text)      # nothing else gains quotes
        self.assertIn("date: 2026-07-31\n", text)

    def test_scalar_quotes_only_what_would_change(self):
        for plain in ("Northlight", "Sprint 1", "2026-06-15", "accepted", "Refunds are 3x"):
            self.assertEqual(vault.scalar(plain), plain)
        self.assertEqual(vault.scalar("A: B"), "'A: B'")
        self.assertEqual(vault.scalar("- listy"), "'- listy'")
        self.assertEqual(vault.scalar("it's fine mid-word"), "it's fine mid-word")
        quote = chr(39)
        self.assertEqual(vault.scalar(quote + 'quoted' + quote),
                         quote * 3 + 'quoted' + quote * 3)
        self.assertEqual(vault.scalar(""), "''")

    def test_task_path(self):
        self.assertEqual(vault.task_path(self.dir, "HARBOR-1"), self.task)

if __name__ == "__main__":
    unittest.main()
