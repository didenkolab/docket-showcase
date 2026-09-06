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

    def test_task_path(self):
        self.assertEqual(vault.task_path(self.dir, "HARBOR-1"), self.task)

if __name__ == "__main__":
    unittest.main()
