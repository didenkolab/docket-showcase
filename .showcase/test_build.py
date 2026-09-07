"""The guard that stands between an uncommitted generator and `git reset --hard`."""
import pathlib, shutil, subprocess, tempfile, unittest
import build


def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


class UncommittedGeneratorFilesTests(unittest.TestCase):
    """A rebuild resets to `scaffold`. Anything uncommitted under the generator
    or the scaffold is gone when it does, so it has to be named beforehand."""

    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "config", "user.email", "t@example.com")
        git(self.root, "config", "user.name", "T")
        (self.root / ".showcase").mkdir()
        (self.root / "hooks").mkdir()
        (self.root / ".showcase" / "story.py").write_text("PEOPLE = []\n")
        (self.root / "hooks" / "workload.sh").write_text("#!/bin/sh\n")
        (self.root / "docket.yaml").write_text("name: Test\n")
        (self.root / "README.md").write_text("# Test\n")
        (self.root / "HARBOR").mkdir()
        (self.root / "HARBOR" / "HARBOR-1.md").write_text("a task\n")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "scaffold")

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_a_clean_tree_has_nothing_to_lose(self):
        self.assertEqual(build.uncommitted_generator_files(self.root), [])

    def test_an_edited_story_file_is_named(self):
        (self.root / ".showcase" / "story.py").write_text("PEOPLE = ['ingrid']\n")
        self.assertEqual(build.uncommitted_generator_files(self.root), [".showcase/story.py"])

    def test_a_hook_a_config_and_the_readme_are_all_watched(self):
        (self.root / "hooks" / "workload.sh").write_text("#!/bin/sh\necho hi\n")
        (self.root / "docket.yaml").write_text("name: Other\n")
        (self.root / "README.md").write_text("# Other\n")
        self.assertEqual(build.uncommitted_generator_files(self.root),
                         ["README.md", "hooks/workload.sh", "docket.yaml"])

    def test_an_untracked_generator_file_counts_too(self):
        """A new story file nobody has `git add`ed is lost as surely as an edit."""
        (self.root / ".showcase" / "products").mkdir()
        (self.root / ".showcase" / "products" / "harbor.py").write_text("def events(): return []\n")
        self.assertEqual(build.uncommitted_generator_files(self.root),
                         [".showcase/products/harbor.py"])

    def test_the_vault_itself_is_not_watched(self):
        """The replay rewrites the tasks. Editing one by hand is not a warning —
        it is the ordinary case the reset exists for."""
        (self.root / "HARBOR" / "HARBOR-1.md").write_text("edited by hand\n")
        (self.root / "HARBOR" / "HARBOR-2.md").write_text("new by hand\n")
        self.assertEqual(build.uncommitted_generator_files(self.root), [])

    def test_a_committed_change_is_not_a_warning(self):
        (self.root / ".showcase" / "story.py").write_text("PEOPLE = ['ola']\n")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "the story moved on")
        self.assertEqual(build.uncommitted_generator_files(self.root), [])


if __name__ == "__main__":
    unittest.main()
