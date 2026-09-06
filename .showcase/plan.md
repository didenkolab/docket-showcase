# Northlight Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `docket-showcase` — an invented company's docket vault (three products, twelve weeks, six people, all twelve apps) — and `northlight`, the codebase beside it, both generated reproducibly and pushed private under `vadymdidenkolab`.

**Architecture:** A scaffold commit (vault from the template + three projects + twelve apps) is tagged `scaffold`. A generator in `.showcase/` holds the whole story as Python data and replays it on top of `scaffold`: every event runs an `docket` command or writes a page, patches the timestamps the CLI cannot take, and commits with the author and date the event has. The code repository `northlight` is built by the same generator on the same timeline, so test import, coverage-by-blame and executions read a real repository at real revisions.

**Tech Stack:** docket CLI (built from `docket/core`), Python 3.12 stdlib for the generator (`unittest` for its tests), `behave` in a venv inside `northlight`, git, gh.

## Global Constraints

- Spec: `docket-work/igl/docs/design/public-release-and-showcase.md` §2. Read it before starting.
- Company **Northlight**; products and keys exactly `HARBOR` (Harbor), `LEDGER` (Ledgerline), `FIELD` (Fieldnote). Domain `northlight.example`. Nothing may name a real customer, employer or product of the author, and no real person; the controller holds the private list of words that must not appear and greps for them before every push.
- Statuses `Backlog, Ready, In progress, In review, QA, Done, Cancelled`; priorities `low, normal, high, critical`; estimates `story points`, scale `[1, 2, 3, 5, 8, 13]`.
- Story history is authored by the six invented people at `<handle>@northlight.example`. Scaffold, generator, README and docs-about-the-showcase commits are `Vadym Didenko <vadym@didenkolab.com>`.
- Timeline: **2026-06-15 (Mon) to 2026-09-04 (Fri)**, six two-week sprints `Sprint 1`…`Sprint 6`; Sprint 5 is running on the "today" the vault ends at (2026-09-04), Sprint 6 is planned.
- Every generated vault state must pass `docket check` with no findings. `docket` here means the binary built from `docket/core` (`go build -o ~/bin/docket ./cmd/docket`, or set `DOCKET_BIN`).
- The generator is deterministic: two runs from `scaffold` produce identical trees (dates and content are data, never `now()`).
- Local paths: vault `/Volumes/Develop/develop/docket-showcase`, code `/Volumes/Develop/develop/northlight`, tool `/Volumes/Develop/develop/docket/core`, apps `/Volumes/Develop/develop/docket/apps`, template `/Volumes/Develop/develop/docket-template`.
- Commit often, as the owner identity, in `.showcase/` work; story commits are made only by the generator.

---

## File structure

```
docket-showcase/                      the vault (git)
  docket.yaml                         3 projects, vocabulary, transitions, 12 apps     (Task 1)
  README.md                          what this is, that it is invented, how to run   (Task 1, 10)
  HARBOR/ LEDGER/ FIELD/             tasks, written by the generator                 (Task 6-8)
  people/ docs/ attachments/ boards/ hooks/ templates/                               (Task 1, 7-8)
  .showcase/
    plan.md                          this file
    build.py                         entry point: reset to scaffold, replay, verify   (Task 5)
    engine.py                        Replay engine: run docket, stamp, commit          (Task 3)
    vault.py                         file helpers: frontmatter, comments, pages       (Task 2)
    story.py                         People, sprints, labels; the event list          (Task 4, 6)
    products/harbor.py               HARBOR epics, tasks, events                      (Task 6)
    products/ledgerline.py           LEDGER                                          (Task 6)
    products/fieldnote.py            FIELD                                           (Task 6)
    crosscut.py                      OKRs, risks, incidents, intake, decisions, docs (Task 7)
    code.py                          builds ../northlight on the same timeline       (Task 8)
    tests_flow.py                    imports features, coverage, executions         (Task 9)
    test_vault.py test_engine.py test_story.py test_code.py   unittest               (each task)
northlight/                          the code (git), written entirely by code.py     (Task 8)
  harbor/ ledgerline/ fieldnote/     packages
  features/<product>/*.feature       behave
  features/steps/*.py                step definitions
  run-tests                          behave "$1" --junit --junit-directory "$(dirname "$2")"
  README.md
```

**Timestamps.** Every event carries a `when: datetime` (UTC). The engine exports `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` and, after each command, rewrites `created:`/`updated:` on the files the command touched to `when` (the CLI writes `now()` and `docket set` refuses `created`). Pages carry `updated: YYYY-MM-DD` of the event.

---

### Task 1: Scaffold the vault and tag it

**Files:**
- Create: `/Volumes/Develop/develop/docket-showcase/` (git), `docket.yaml`, `README.md`, `.gitignore`
- Modify: `docket.yaml` (from the template) — statuses, priorities, estimates, transitions

**Interfaces:**
- Produces: git tag `scaffold` that every generator run starts from; `docket.yaml` vocabulary that `story.py` must match exactly.

- [ ] **Step 1: Build the CLI and create the repository**

```bash
cd /Volumes/Develop/develop/docket/core && go build -o "$HOME/bin/docket" ./cmd/docket && export PATH="$HOME/bin:$PATH" && docket version
mkdir -p /Volumes/Develop/develop/docket-showcase && cd /Volumes/Develop/develop/docket-showcase
git init -q -b main && git config user.name "Vadym Didenko" && git config user.email "vadym@didenkolab.com"
docket init --key HARBOR --name Harbor --template /Volumes/Develop/develop/docket-template --author "Vadym Didenko <vadym@didenkolab.com>" .
docket project add --key LEDGER --name Ledgerline .
docket project add --key FIELD  --name Fieldnote .
rm -f "docs/sprints/Sprint 1.md" docs/decisions/0001-a-session-is-a-signed-cookie.md
```
Expected: `docket init` prints the first-task hint; `git log --oneline` shows one commit.

- [ ] **Step 2: Set the vocabulary**

Replace the `name`, `statuses`, `priorities` sections and add `estimates` and `transitions` in `docket.yaml` so it reads:

```yaml
name: Northlight
projects:
  - key: HARBOR
    name: Harbor
  - key: LEDGER
    name: Ledgerline
  - key: FIELD
    name: Fieldnote
statuses:
  - name: Backlog
    category: todo
  - name: Ready
    category: todo
  - name: In progress
    category: doing
  - name: In review
    category: doing
  - name: QA
    category: doing
  - name: Done
    category: done
  - name: Cancelled
    category: done
types:
  - name: epic
    level: 1
  - story
  - task
  - bug
  - name: subtask
    level: -1
priorities:
  - low
  - normal
  - high
  - critical
estimates:
  unit: story points
  scale: [1, 2, 3, 5, 8, 13]
transitions:
  Backlog: [Ready, Cancelled]
  Ready: [In progress, Backlog, Cancelled]
  In progress: [In review, Ready, Cancelled]
  In review: [QA, In progress, Cancelled]
  QA: [Done, In progress]
  Done: [In progress]
  Cancelled: [Backlog]
```
Keep everything else the template wrote (comments, `fields:` if any). Run `docket check --fix .` — expected `No findings.` (boards regenerate).

- [ ] **Step 3: Install the twelve apps**

```bash
for a in tests time risks okr incidents intake time-in-status anomalies workload checklists estimation portfolio; do
  docket app add "/Volumes/Develop/develop/docket/apps#$a" . | tail -1
done
docket app list . && docket check . && rm -rf hooks/__pycache__
```
Expected: twelve lines "N files changed", `app list` shows twelve, `No findings.`

- [ ] **Step 4: README and .gitignore**

`README.md`:

```markdown
# Northlight

An [docket](https://github.com/vadymdidenkolab/docket) vault for an invented software company:
three products, six people, twelve weeks of work. **Everything here is made up** — the company,
the people, the customers and the incidents — and it was written by a generator,
`.showcase/build.py`, so that every command and every app docket has can be seen on a board that
looks like a team's rather than a form.

| Project | Product | What it is |
|---|---|---|
| `HARBOR` | Harbor | Berth booking and invoicing for marinas |
| `LEDGER` | Ledgerline | Bookkeeping for small businesses |
| `FIELD` | Fieldnote | Scheduling for field service crews, with an offline mobile app |

The code the tests come from is in [northlight](https://github.com/vadymdidenkolab/northlight).

## Open it

Clone, open the folder in Obsidian: a board, a backlog, a wiki and a graph. Or serve it:

    docket serve --programs

`--programs` lets the server run what the apps declared (test coverage, workload, OKRs…).

## Rebuild it

    .showcase/build.py            # resets to the `scaffold` tag and replays the story
    .showcase/build.py --verify   # also runs docket check, graph, anomalies, report

The story is data in `.showcase/story.py` and `.showcase/products/`. Change it and rebuild.
```

Append to `.gitignore`:
```
__pycache__/
*.pyc
.venv/
```

- [ ] **Step 5: Commit and tag**

```bash
git add -A && git commit -q -m "Northlight: three projects, twelve apps, and nothing on the board yet" && git tag scaffold && git log --oneline
```
Expected: two commits, tag `scaffold` on the second. `docket check .` → `No findings.`

---

### Task 2: `vault.py` — file helpers

**Files:**
- Create: `.showcase/vault.py`, `.showcase/test_vault.py`

**Interfaces:**
- Produces:
  - `read_frontmatter(path) -> (dict[str, str], str)` — raw frontmatter lines as `name -> raw value string`, and the body.
  - `patch_frontmatter(path, **values)` — rewrite existing keys in place (raw string values), append missing ones before the closing `---`.
  - `stamp(path, when: datetime, created: bool=False)` — sets `updated` (and `created` when asked) to `when.strftime('%Y-%m-%dT%H:%M:%SZ')`.
  - `append_comment(path, author: str, when: datetime, text: str)` — appends `**author · YYYY-MM-DD HH:mm** — text` under `## Comments` (creating the heading if absent).
  - `set_body(path, markdown: str)` — replaces everything after the frontmatter, keeping `## Comments` if present.
  - `write_page(path, title, kind, updated: date, body, **extra)` — a `docs/` page with `title/type/updated` frontmatter plus extras (`starts`, `ends`, `status`, `date`, `supersedes`).
  - `write_person(path, handle, name)` — `people/<handle>.md` as `type: person`, `name: <handle>` and a one-line body naming the person.
  - `task_path(root, key) -> Path` — the one file in `<PROJECT>/` starting with `<key> `.

- [ ] **Step 1: Write the failing tests**

```python
# .showcase/test_vault.py
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd /Volumes/Develop/develop/docket-showcase/.showcase && python3 -m unittest test_vault -v`
Expected: `ModuleNotFoundError: No module named 'vault'`

- [ ] **Step 3: Implement `vault.py`**

```python
"""Files in a docket vault, written the way the format says and nothing more."""
from __future__ import annotations
import datetime as dt
import pathlib
import re

STAMP = "%Y-%m-%dT%H:%M:%SZ"


def read_frontmatter(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    end = text.index("\n---\n", 4)
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 5:]


def _split(text):
    end = text.index("\n---\n", 4)
    return text[4:end].splitlines(), text[end + 5:]


def patch_frontmatter(path, **values):
    path = pathlib.Path(path)
    lines, body = _split(path.read_text(encoding="utf-8"))
    seen = set()
    out = []
    for line in lines:
        key = line.split(":", 1)[0].strip() if ":" in line and not line.startswith(" ") else None
        if key in values:
            out.append(f"{key}: {values[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key, value in values.items():
        if key not in seen:
            out.append(f"{key}: {value}")
    path.write_text("---\n" + "\n".join(out) + "\n---\n" + body, encoding="utf-8")


def stamp(path, when, created=False):
    values = {"updated": when.strftime(STAMP)}
    if created:
        values["created"] = when.strftime(STAMP)
    patch_frontmatter(path, **values)


def append_comment(path, author, when, text):
    path = pathlib.Path(path)
    content = path.read_text(encoding="utf-8")
    if "\n## Comments" not in content:
        content = content.rstrip("\n") + "\n\n## Comments\n"
    content = content.rstrip("\n") + "\n\n**%s · %s** — %s\n" % (author, when.strftime("%Y-%m-%d %H:%M"), text)
    path.write_text(content, encoding="utf-8")


def set_body(path, markdown):
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")
    end = text.index("\n---\n", 4) + 5
    head, old = text[:end], text[end:]
    comments = ""
    if "\n## Comments" in old:
        comments = old[old.index("\n## Comments"):]
    path.write_text(head + "\n" + markdown.rstrip("\n") + "\n" + comments, encoding="utf-8")


def write_page(path, title, kind, updated, body, **extra):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = [f"title: {title}", f"type: {kind}", f"updated: {updated.isoformat()}"]
    fm += [f"{k}: {v}" for k, v in extra.items()]
    path.write_text("---\n" + "\n".join(fm) + "\n---\n\n" + body.rstrip("\n") + "\n", encoding="utf-8")


def write_person(path, handle, name):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\ntype: person\nname: {handle}\n---\n\n{name}. Work on {handle} is everything that links here.\n",
                    encoding="utf-8")


def task_path(root, key):
    project = key.split("-")[0]
    matches = sorted(pathlib.Path(root, project).glob(f"{key} *.md"))
    assert len(matches) == 1, (key, matches)
    return matches[0]
```

- [ ] **Step 4: Run tests**

Run: `python3 -m unittest test_vault -v` — Expected: 6 tests OK.

- [ ] **Step 5: Commit**

```bash
cd /Volumes/Develop/develop/docket-showcase && git add .showcase/vault.py .showcase/test_vault.py .showcase/plan.md && git commit -q -m "showcase: the file helpers, and the plan"
```

---

### Task 3: `engine.py` — replay engine

**Files:**
- Create: `.showcase/engine.py`, `.showcase/test_engine.py`

**Interfaces:**
- Consumes: `vault.stamp`, `vault.task_path`, `vault.append_comment`.
- Produces:
  - `Person(handle, name, email, role)` dataclass; `Event` dataclass: `when: datetime`, `who: Person`, `kind: str`, `args: dict`, `message: str`.
  - `class Engine(root: Path, docket: str, dry: bool=False)` with:
    - `run(*args) -> str` — runs `docket` in `root`, raises on non-zero with stderr.
    - `commit(event)` — `git add -A` + commit with `--author "Name <email>"` and `GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=event.when` (ISO), message `event.message`; skips when nothing changed.
    - `apply(event)` — dispatches on `event.kind` to a handler `on_<kind>(event)`; after the handler, calls `stamp` on every task path listed in `event.args.get("touch", [])` plus what the handler returns; then `commit`.
    - handlers: `on_new` (args: `key_alias, title, type, project, assignee, priority, labels, parent, body`; runs `docket new`, records `keys[key_alias] = KEY`, stamps `created`), `on_set` (args: `task, **props` via `set`, e.g. `status`, `estimate`, `sprint`, relations), `on_comment` (args: `task, text`), `on_page` (args: `path, title, kind, body, extra`), `on_person`, `on_raw` (args: `fn` callable(engine) for anything else).
    - `keys: dict[str, str]` — alias → real key; `key(alias)`; `path(alias)`; aliases are strings like `"harbor.booking.week"` so story data never hard-codes numbers.
    - `replay(events)` — sorts by `when` (stable) and applies each.
- Env: handler `on_set` accepts relation values by alias: `blocked_by=["harbor.x"]` → resolved keys.

- [ ] **Step 1: Write the failing tests**

```python
# .showcase/test_engine.py
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
        self.assertIn("Ingrid Solberg <ingrid@northlight.example> 2026-06-15T09:00:00+00:00", log)
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
```

- [ ] **Step 2: Run to verify it fails** — `python3 -m unittest test_engine -v` → `No module named 'engine'`.

- [ ] **Step 3: Implement `engine.py`**

```python
"""Replays a story into a vault: one event, one docket command, one commit with its own date."""
from __future__ import annotations
import dataclasses as dc
import datetime as dt
import os
import pathlib
import subprocess
import vault


@dc.dataclass(frozen=True)
class Person:
    handle: str
    name: str
    email: str
    role: str


@dc.dataclass
class Event:
    when: dt.datetime
    who: Person
    kind: str
    args: dict
    message: str


class Engine:
    def __init__(self, root, docket="docket", dry=False):
        self.root = pathlib.Path(root)
        self.docket = docket
        self.dry = dry
        self.keys: dict[str, str] = {}
        self.order = 0

    # -- plumbing ---------------------------------------------------------
    def run(self, *args):
        out = subprocess.run([self.docket, *args, "."], cwd=self.root, capture_output=True, text=True)
        if out.returncode != 0:
            raise RuntimeError("docket %s failed:\n%s%s" % (" ".join(args), out.stdout, out.stderr))
        return out.stdout.strip()

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True,
                              env={**os.environ, **(env or {})}).stdout

    def key(self, alias):
        return self.keys[alias] if alias in self.keys else alias   # a real key passes through

    def path(self, alias):
        return vault.task_path(self.root, self.key(alias))

    def commit(self, event):
        self.git("add", "-A")
        if not self.git("status", "--porcelain").strip():
            return
        when = event.when.replace(tzinfo=dt.timezone.utc).isoformat()
        self.git("commit", "-q", "-m", event.message, "--author", f"{event.who.name} <{event.who.email}>",
                 env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when,
                      "GIT_COMMITTER_NAME": event.who.name, "GIT_COMMITTER_EMAIL": event.who.email})

    def apply(self, event):
        touched = getattr(self, "on_" + event.kind)(event) or []
        for alias in list(event.args.get("touch", [])) + list(touched):
            vault.stamp(self.path(alias), event.when)
        self.commit(event)

    def replay(self, events):
        for i, event in enumerate(sorted(events, key=lambda e: e.when)):
            self.apply(event)

    # -- handlers -----------------------------------------------------------
    def on_new(self, event):
        a = event.args
        cmd = ["new", a["title"], "--type", a.get("type", "task"), "--project", a["project"]]
        for flag in ("assignee", "priority", "labels", "status"):
            if a.get(flag):
                cmd += ["--" + flag, a[flag]]
        if a.get("parent"):
            cmd += ["--parent", self.key(a["parent"])]
        line = self.run(*cmd)
        key = line.split()[0]
        self.keys[a["alias"]] = key
        path = vault.task_path(self.root, key)
        if a.get("body"):
            vault.set_body(path, a["body"])
        vault.stamp(path, event.when, created=True)
        return []

    RELATIONS = {"blocks", "blocked_by", "duplicates", "duplicated_by", "causes", "caused_by", "relates",
                 "tests", "tested_by", "runs", "run_by", "found", "found_in", "includes", "included_in",
                 "logs", "logged_by", "threatens", "threatened_by", "mitigated_by", "mitigates",
                 "contributes_to", "contributed_by", "explains", "explained_by", "became", "came_from"}

    def on_set(self, event):
        a = dict(event.args)
        task = a.pop("task")
        a.pop("touch", None)
        pairs = []
        for name, value in a.items():
            if name in self.RELATIONS:
                value = ",".join(self.key(v) for v in (value if isinstance(value, list) else [value]))
            pairs.append(f"{name}={value}")
        self.run("set", self.key(task), *pairs, "--quiet")
        return [task]

    def on_comment(self, event):
        vault.append_comment(self.path(event.args["task"]), event.who.handle, event.when, event.args["text"])
        return [event.args["task"]]

    def on_page(self, event):
        a = event.args
        vault.write_page(self.root / a["path"], a["title"], a["kind"], event.when.date(), a["body"], **a.get("extra", {}))
        return []

    def on_person(self, event):
        a = event.args
        vault.write_person(self.root / "people" / f"{a['handle']}.md", a["handle"], a["name"])
        return []

    def on_raw(self, event):
        return event.args["fn"](self, event) or []
```

- [ ] **Step 4: Run tests** — `DOCKET_BIN=$HOME/bin/docket python3 -m unittest test_engine -v` → 4 OK. If `docket set` refuses a relation name, check the exact inverse names in `docket.yaml` of the scaffold and fix `RELATIONS`.

- [ ] **Step 5: Commit** — `git add .showcase/engine.py .showcase/test_engine.py && git commit -q -m "showcase: the replay engine"`

---

### Task 4: `story.py` — people, sprints, labels, the timeline helpers

**Files:**
- Create: `.showcase/story.py`, `.showcase/test_story.py`

**Interfaces:**
- Produces:
  - `PEOPLE: dict[str, Person]` — six: `ingrid` Ingrid Solberg (product), `tomasz` Tomasz Wierzbicki (backend), `aiko` Aiko Tanaka (mobile), `mateo` Mateo Ríos (QA), `priya` Priya Nair (frontend), `ola` Ola Nordmann (ops). Emails `<handle>@northlight.example`.
  - `SPRINTS: list[Sprint(name, starts: date, ends: date, goal: str)]` — Sprint 1 2026-06-15…06-26, 2: 06-29…07-10, 3: 07-13…07-24, 4: 07-27…08-07, 5: 08-10…08-21 → **correction: six sprints must reach 09-04**, so: 1: 06-15…06-26, 2: 06-29…07-10, 3: 07-13…07-24, 4: 07-27…08-07, 5: 08-10…08-21, 6: 08-24…09-04. Sprint 6 is the running one on 2026-09-04 (its last day); nothing is "planned next" — instead `docs/sprints/Sprint 7.md` is written as planned (09-07…09-18) with a goal and no retrospective.
  - `LABELS: dict[str, str]` — eight, name → one-paragraph meaning: `bookings`, `payments`, `invoicing`, `bank-import`, `tax`, `offline-sync`, `routing`, `mobile`.
  - `at(day: str, hour: int=10, minute: int=0) -> datetime` — `"2026-06-15"` → UTC datetime.
  - `T = TimelineBuilder(engine_person_lookup)` helpers that produce events: `new(when, who, alias, title, project, type, assignee, priority, labels, parent, body)`, `move(when, who, alias, status)`, `estimate(when, who, alias, points)`, `sprint(when, who, alias, name)`, `comment(when, who, alias, text)`, `relate(when, who, alias, **relations)`, `page(...)`, `person(...)`. Each returns an `Event` with a sensible commit message: `"<KEYALIAS>: <title>"` for new (engine resolves alias in message: `Engine.commit` replaces `{alias}` placeholders with keys — add this to `Engine.commit`: `message = event.message.format_map(KeyMap(self))` where `KeyMap.__missing__` returns the alias itself), `"<key>: Backlog → Ready"` for moves, etc.
  - `people_events() -> list[Event]` — six `person` events on 2026-06-15 09:00 by `ingrid`.
  - `label_events() -> list[Event]` — eight `page` events writing `docs/labels/<name>.md` (`type: page`, body = meaning + "Everything labelled is in this page's backlinks."), on 2026-06-15 09:10.
  - `sprint_events() -> list[Event]` — one `page` event per sprint at `starts` 09:00 with goal only; a second at `ends` 17:00 for sprints 1–5 rewriting the page with the retrospective (`body` composed from `Sprint.retro` text that Task 6 fills, default placeholder is **not allowed**: Task 6 supplies all five retros). Sprint 7 planned page at 2026-09-04 16:00.

- [ ] **Step 1: Write the failing tests**

```python
# .showcase/test_story.py
import datetime as dt, unittest
import story

class StoryTests(unittest.TestCase):
    def test_six_people_with_domain(self):
        self.assertEqual(len(story.PEOPLE), 6)
        self.assertTrue(all(p.email.endswith("@northlight.example") for p in story.PEOPLE.values()))

    def test_sprints_cover_the_twelve_weeks(self):
        self.assertEqual(story.SPRINTS[0].starts, dt.date(2026, 6, 15))
        self.assertEqual(story.SPRINTS[-1].ends, dt.date(2026, 9, 4))
        self.assertEqual(len(story.SPRINTS), 6)
        for a, b in zip(story.SPRINTS, story.SPRINTS[1:]):
            self.assertLess(a.ends, b.starts)

    def test_at(self):
        self.assertEqual(story.at("2026-06-15", 9, 30), dt.datetime(2026, 6, 15, 9, 30))

    def test_move_event_message(self):
        ev = story.move(story.at("2026-06-16"), story.PEOPLE["ingrid"], "x", "Ready")
        self.assertEqual(ev.kind, "set")
        self.assertEqual(ev.args, {"task": "x", "status": "Ready"})
        self.assertEqual(ev.message, "{x}: → Ready")

    def test_labels_are_eight_pages(self):
        evs = story.label_events()
        self.assertEqual(len(evs), 8)
        self.assertTrue(all(e.args["path"].startswith("docs/labels/") for e in evs))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails** — `python3 -m unittest test_story -v` → import error.

- [ ] **Step 3: Implement `story.py`** (people, sprints, labels, helpers exactly as in Interfaces; retros are `Sprint.retro: str = ""` and `sprint_events()` raises `ValueError("Sprint N has no retrospective")` for sprints 1–5 with empty retro, so Task 6 cannot forget them). Add to `Engine.commit`:

```python
class _KeyMap(dict):
    def __init__(self, engine): self.engine = engine
    def __missing__(self, alias): return self.engine.keys.get(alias, alias)
# in commit(): message = event.message.format_map(_KeyMap(self))
```

and a test in `test_engine.py`: message `"{a}: Book a berth"` becomes `"ACME-1: Book a berth"`.

- [ ] **Step 4: Run all tests** — `python3 -m unittest -v` (from `.showcase/`, with `DOCKET_BIN`) → all OK.

- [ ] **Step 5: Commit** — `git add .showcase && git commit -q -m "showcase: the people, the sprints, the labels"`

---

### Task 5: `build.py` — entry point that resets and replays

**Files:**
- Create: `.showcase/build.py` (executable)

**Interfaces:**
- Consumes: `engine.Engine`, `story.*`, `products.*.events()`, `crosscut.events()`, `code.build()`, `tests_flow.events()` (later tasks; import them lazily behind `--only` flags so the script runs at every stage).
- Produces: CLI `build.py [--verify] [--only people,labels,sprints,harbor,ledgerline,fieldnote,crosscut,code,tests]`.

- [ ] **Step 1: Write it**

```python
#!/usr/bin/env python3
"""Rebuild the Northlight vault from the `scaffold` tag by replaying the story."""
import argparse, os, pathlib, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine, story

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCKET = os.environ.get("DOCKET_BIN", "docket")
STAGES = ["people", "labels", "sprints", "harbor", "ledgerline", "fieldnote", "crosscut", "code", "tests"]


def events_for(stage, e):
    if stage == "people":   return story.people_events()
    if stage == "labels":   return story.label_events()
    if stage == "sprints":  return story.sprint_events()
    if stage == "harbor":   from products import harbor;      return harbor.events()
    if stage == "ledgerline": from products import ledgerline; return ledgerline.events()
    if stage == "fieldnote": from products import fieldnote;  return fieldnote.events()
    if stage == "crosscut": import crosscut;                  return crosscut.events()
    if stage == "code":     import code as northlight;        return northlight.events(ROOT.parent / "northlight")
    if stage == "tests":    import tests_flow;                return tests_flow.events(ROOT.parent / "northlight")
    raise SystemExit("unknown stage " + stage)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=",".join(STAGES))
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--keep", action="store_true", help="do not reset to scaffold first")
    a = ap.parse_args()
    if not a.keep:
        subprocess.run(["git", "reset", "-q", "--hard", "scaffold"], cwd=ROOT, check=True)
        subprocess.run(["git", "clean", "-qfd", "--exclude=.showcase", "--exclude=.venv"], cwd=ROOT, check=True)
    e = engine.Engine(ROOT, DOCKET)
    events = []
    for stage in a.only.split(","):
        events += events_for(stage, e)
    e.replay(events)
    print(f"{len(events)} events replayed; {len(e.keys)} tasks.")
    if a.verify:
        for cmd in (["check"], ["graph"], ["anomalies"], ["report", "time-in-status"]):
            print("$ docket", *cmd); print(e.run(*cmd))


if __name__ == "__main__":
    main()
```

Note: events across stages are sorted together by `replay`, so a Harbor comment on 07-02 lands between Ledgerline events of 07-01 and 07-03 — one interleaved history, like a real board's.

- [ ] **Step 2: Run the first three stages** — `chmod +x .showcase/build.py && DOCKET_BIN=$HOME/bin/docket .showcase/build.py --only people,labels,sprints` → expected: sprints stage raises `Sprint 1 has no retrospective`. Temporarily run `--only people,labels` → `14 events replayed; 0 tasks.`, `git log --oneline | head` shows commits by Ingrid on 2026-06-15, `docket check .` clean.

- [ ] **Step 3: Commit** — `git add .showcase/build.py && git commit -q -m "showcase: build.py replays the story from scaffold"` (commit as owner; note the story commits made in Step 2 sit above scaffold — that is fine, `build.py` resets them on the next run. Keep the owner's `.showcase` commits **below** `scaffold`? No: `.showcase/` is excluded from `git clean` but `git reset --hard scaffold` would drop later commits touching it. **Therefore:** after each `.showcase` change, move the tag: `git tag -f scaffold` on the owner commit that contains the latest `.showcase`, provided no story commits are between. Procedure for every owner commit from here on: `git reset -q --hard scaffold` (drops story commits) → make the `.showcase` change → commit → `git tag -f scaffold`.)

---

### Task 6: The three products — tasks, moves, comments, sprints, retros

**Files:**
- Create: `.showcase/products/__init__.py`, `.showcase/products/harbor.py`, `.showcase/products/ledgerline.py`, `.showcase/products/fieldnote.py`
- Modify: `.showcase/story.py` — fill `Sprint.goal` and `Sprint.retro` for sprints 1–5, goal for 6 and 7.
- Test: `.showcase/test_products.py`

**Interfaces:**
- Each product module exposes `events() -> list[Event]` and `ALIASES: dict[str, str]` (alias → title) for the tests. Aliases are `harbor.<epic>.<slug>`; a subtask `harbor.<epic>.<slug>.<n>`.
- Consumes `story.new/move/estimate/sprint/comment/relate/at/PEOPLE`.

**Content rules (the whole of "looks like real work"):**

| | HARBOR | LEDGER | FIELD |
|---|---|---|---|
| epics | 4: Season bookings, Berth calendar, Card payments, Mobile check-in | 3: Invoices, Bank import, Tax periods | 3: Job scheduling, Route planning, Offline mobile |
| stories/tasks/bugs | 34 (22 stories, 6 tasks, 6 bugs) | 26 (16/5/5) | 26 (15/5/6) |
| subtasks | 10 | 6 | 8 |
| assignees | ingrid writes stories; tomasz backend; priya web; aiko mobile; mateo bugs/QA; ola ops tasks | same | aiko carries most (the overload the workload app must show) |
| final states on 2026-09-04 | ~55% Done, 2 Cancelled, 3 In review, 2 QA, 4 In progress, rest Ready/Backlog | similar | Sprint 6: aiko has 6 open tasks, 5 sized (workload); one task in `In review` since 08-12 (time-in-status outlier) |
| estimates | every story that entered a sprint is sized on its scale; four Ready stories deliberately unsized (estimation app agenda); epics never carry one | | |
| relations | ≥2 each of `blocks/blocked_by`, `duplicates/duplicated_by`, `relates`; **cross-project:** `harbor.payments.refunds` blocked_by `ledger.invoices.credit-notes`; a FIELD sync bug `relates` a HARBOR check-in story | | |
| labels | one or two per story from `story.LABELS`; subtasks none | | |
| tags | free: `area/api`, `regress`, `needs-design`, `customer/marina-vik` (tag form, never a label) | | |
| comments | ≥1 on every bug, on every story that was returned from review (`In review → In progress`), and on every cancelled task saying why | | |
| moves | forward one stage at a time, dated on weekdays 09:00–18:00 UTC, per `transitions`; 2 returns from review, 1 from QA | | |
| sprints | stories set `sprint` when pulled (sprint start day) and keep it; carried-over stories set the next sprint on its start day | | |
| bodies | every story: one paragraph + `## Acceptance` with 2–4 `- [ ]` boxes; ticked `- [x]` as work finishes (checklists app reads them: Done stories all ticked, In progress partly) | | |
| anomalies planted | one `adrift` task nobody links (HARBOR); one `only-owner` (ola's ops task chain); one `one-sided` relation (a `blocks` without inverse) — exactly one so `docket check` does not fail (check rule about missing inverse? verify: if check reports it, plant `relates` one-sided instead, or drop) | | |

Sprint goals/retros (`story.py`): 1 "A marina can take a booking and send an invoice"; 2 "Card payments end to end on staging"; 3 "Bank import for Ledgerline, first three banks"; 4 "Fieldnote works a whole day offline" — retro names the sync loss (Task 7 incident); 5 "Harbor season launch: check-in on the pontoon"; 6 "Tax periods, and the sync fix under load"; 7 (planned) "Refunds and credit notes together". Each retro: 3 paragraphs, names tasks by key in backticks (never wikilinks — rule 13).

- [ ] **Step 1: Write the failing tests**

```python
# .showcase/test_products.py
import unittest, collections
from products import harbor, ledgerline, fieldnote
import story

class ProductTests(unittest.TestCase):
    def counts(self, mod):
        news = [e for e in mod.events() if e.kind == "new"]
        return collections.Counter(e.args["type"] for e in news)

    def test_harbor_shape(self):
        c = self.counts(harbor)
        self.assertEqual(c["epic"], 4); self.assertEqual(c["subtask"], 10)
        self.assertEqual(c["story"] + c["task"] + c["bug"], 34)

    def test_ledgerline_and_fieldnote_shape(self):
        self.assertEqual(self.counts(ledgerline)["epic"], 3)
        self.assertEqual(self.counts(fieldnote)["epic"], 3)

    def test_every_bug_has_a_comment(self):
        for mod in (harbor, ledgerline, fieldnote):
            evs = mod.events()
            bugs = {e.args["alias"] for e in evs if e.kind == "new" and e.args["type"] == "bug"}
            commented = {e.args["task"] for e in evs if e.kind == "comment"}
            self.assertTrue(bugs <= commented, bugs - commented)

    def test_events_inside_the_window(self):
        for mod in (harbor, ledgerline, fieldnote):
            for e in mod.events():
                self.assertTrue(story.at("2026-06-15") <= e.when <= story.at("2026-09-04", 18), e)

    def test_retros_present(self):
        for s in story.SPRINTS[:5]:
            self.assertTrue(len(s.retro) > 200, s.name)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails.**

- [ ] **Step 3: Write `harbor.py`** — data first (a list of dicts per epic), then a small function that turns the data into events: creation (by `ingrid` for stories, by the reporter for bugs), estimate, sprint pull, moves with dates, comments, relations, acceptance ticks (`on_raw` event that rewrites `- [ ]` → `- [x]` lines in the body via `vault.set_body`). Use one helper `lifecycle(alias, pulled: str, moves: list[tuple[str, str]])` so each task is ~6 lines of data. Write Ledgerline and Fieldnote the same way. Fill `story.SPRINTS` goals and retros.

- [ ] **Step 4: Replay and check** — `git reset -q --hard scaffold && .showcase/build.py --only people,labels,sprints,harbor,ledgerline,fieldnote --verify`. Expected: `docket check` → `No findings.`; `git log --format=%an | sort | uniq -c` shows six names; `docket export --format csv --fields key,type,status . | wc -l` ≈ 130. Fix any check finding by changing the data, never by hand-editing the vault.

- [ ] **Step 5: Commit** — `git reset -q --hard scaffold` then `git add .showcase && git commit -q -m "showcase: three products, twelve weeks" && git tag -f scaffold`.

---

### Task 7: `crosscut.py` — OKRs, risks, incidents, intake, time, decisions, design pages, index, attachments

**Files:**
- Create: `.showcase/crosscut.py`, `.showcase/attachments/architecture.svg` (hand-drawn SVG, three boxes and a shared "accounts" box, ≤ 3 KB), test `.showcase/test_crosscut.py`

**Interfaces:**
- `events() -> list[Event]` using aliases from the products (import their `ALIASES` to assert existence).

**Content:**
- **OKR** (`okr` app, types `objective` level 2, `key_result` level 1, fields `target,current,measure,quarter`): Q3 2026, three objectives in project HARBOR/LEDGER/FIELD respectively ("Marinas run the season on Harbor", "Ledgerline closes a quarter without a spreadsheet", "A crew's day survives a dead zone"), seven key results with `contributes_to` from epics (set on the epic: `contributes_to=<kr>`; verify direction in `apps/okr/docket-app.yaml` and flip if the relation is declared the other way). `current` updated twice on the timeline (07-31, 08-31).
- **Risks** (`risk` type; `likelihood, impact, owner, reviewed_on`; relations `threatens`, `mitigated_by`): six risks created 06-22 by `ola`/`ingrid`, each `threatens` an epic and three `mitigated_by` a task; `reviewed_on` bumped 08-03.
- **Incidents** (`incident`, `postmortem`; `severity, detected_at, resolved_at, customers_affected`; relation `explains` from postmortem to incident — verify direction): INC-1 Harbor double charge 07-08 (severity high, 3 marinas) → `causes` on bug `harbor.payments.double-charge`, postmortem 07-10 with the four sections from the template filled; INC-2 Fieldnote sync loss 07-29 (critical, 11 crews) → `causes` on `field.offline.sync-loss`, postmortem 08-03, "What we are changing" links tasks via `mitigated_by`.
- **Intake** (`request`; `asked_by, asked_on, wanted_by`; relation `became`): eight requests over the twelve weeks from "Vik Marina", "Sandholm Harbour", "Bergström Accounting", "Nordic Field Services" etc.; three `became` a story; two answered "no" in the body; three open.
- **Time** (`worklog` level −1; `spent, worked_on, billable`; relation `logs`): worklogs as children (`parent`) of tasks in Sprints 5–6 by tomasz, priya, aiko, mateo — 30 worklogs, 1–6 h, Harbor ones `billable: true`, others false; body one sentence each.
- **Checklists**: `definition_of_done` = `team` on stories, `release` on the two launch stories, `hotfix` on the incident bugs.
- **Decisions** (`docs/decisions/000N-*.md`, four required sections, `status: accepted`, `date`): 0001 "One vault for three products" (06-15), 0002 "Payments go through one provider" (06-24), 0003 "Bank imports are idempotent by statement hash" (07-15), 0004 "Offline first: the phone is the source of truth for a job" (07-31, after INC-2), 0005 "Tax periods close by decision, not by date" (08-18), 0006 "Refunds are credit notes" (08-27, `supersedes` nothing).
- **Design pages** (`docs/design/harbor.md`, `ledgerline.md`, `fieldnote.md`, `architecture.md` embedding `![[architecture.svg]]` from `attachments/`): what each product is, its main flows, its vocabulary, written 06-16 and updated once.
- **`docs/index.md`** rewritten 06-15 and 09-04: what is where, links to the design pages, decisions, sprints, labels, and the app pages the installs added (`docs/testing.md` etc.).

- [ ] **Step 1: Tests** — `test_crosscut.py`: counts (3 objectives, 7 KRs, 6 risks, 2 incidents, 2 postmortems, 8 requests, 30 worklogs, 6 decision pages), every alias referenced exists in the products' `ALIASES`, every decision body contains the four headings.
- [ ] **Step 2: Fail, implement, pass** — `python3 -m unittest test_crosscut -v`.
- [ ] **Step 3: Replay all vault stages with `--verify`** — `No findings.`; `docket anomalies .` lists the planted ones and nothing alarming; `docket report time-in-status .` shows the 08-12 review outlier.
- [ ] **Step 4: Commit** — reset to scaffold, `git add .showcase && git commit -q -m "showcase: the quarter around the work" && git tag -f scaffold`.

---

### Task 8: `code.py` — the `northlight` repository on the same timeline

**Files:**
- Create: `.showcase/code.py`, `.showcase/test_code.py`, and through it `/Volumes/Develop/develop/northlight/` (git)

**Interfaces:**
- `events(code_root) -> list[Event]` of kind `raw` whose `fn` writes files into `code_root` and commits there (the engine's `commit` is for the vault; `code.py` has its own `commit(code_root, event)` with the same author/date env). Events are dated on the vault timeline so `link-coverage` blame lines up with task keys.
- `CODE_COMMITS: list[dict(when, who, key_alias, subject, files: dict[path, content])]` — about 60 commits. Subjects are `"{harbor.booking.week}: reserve a berth for a date range"` (aliases resolved by the same `_KeyMap`).
- Layout produced:

```
northlight/
  README.md                        what it is, invented, `./run-tests`
  pyproject.toml                   name northlight, requires-python >=3.11
  harbor/__init__.py  harbor/booking.py  harbor/invoice.py  harbor/checkin.py
  ledgerline/__init__.py  ledgerline/invoices.py  ledgerline/bankimport.py  ledgerline/tax.py
  fieldnote/__init__.py  fieldnote/jobs.py  fieldnote/routes.py  fieldnote/sync.py
  features/harbor/booking.feature  features/harbor/payments.feature  features/harbor/checkin.feature
  features/ledgerline/invoices.feature  features/ledgerline/bankimport.feature  features/ledgerline/tax.feature
  features/fieldnote/jobs.feature  features/fieldnote/routes.feature  features/fieldnote/sync.feature
  features/steps/harbor_steps.py  features/steps/ledgerline_steps.py  features/steps/fieldnote_steps.py
  features/environment.py
  run-tests
  .gitignore                       .venv/ __pycache__/ reports/
```

- Modules are small and real (pure functions with a dict-shaped state): e.g. `harbor/booking.py`: `reserve(calendar, berth, start, end) -> Booking | Conflict`, `harbor/invoice.py`: `invoice_for(booking, rate) -> Invoice` with season pricing, `refund(invoice, amount) -> CreditNote`; `ledgerline/bankimport.py`: `import_statement(ledger, lines) -> Imported` idempotent by statement hash; `ledgerline/tax.py`: `close_period(ledger, period)`; `fieldnote/sync.py`: `merge(phone, server) -> Merged` with a conflict rule (phone wins for job status). Each with 3–8 scenarios; **60 scenarios total**, 44 tagged with case ids `@HARBOR-BKG-001`… (`AREA` ∈ BKG, PAY, CHK, INV, BNK, TAX, JOB, RTE, SYN), 16 untagged on purpose.
- Two scenarios must **fail at HEAD**: `HARBOR-PAY-004` (refund over the invoice total is accepted — the bug `harbor.payments.refund-over`), and an untagged Fieldnote sync scenario ("a job finished offline keeps its photos"). Earlier revisions (the executions of Sprints 2–4) have their own pass/fail pattern: INC-2's sync loss scenario fails at the 07-27 revision and passes after the 08-05 fix commit.
- `run-tests`:
  ```sh
  #!/bin/sh
  set -eu
  exec "$(dirname "$0")/.venv/bin/behave" "$1" --junit --junit-directory "$(dirname "$2")" --no-summary -q
  ```
- Commit messages: `"{alias}: subject"`; a handful of `chore:` commits without a key. `features/steps` commits reference the story they test.

- [ ] **Step 1: Tests** — `test_code.py`: building into a temp dir yields ≥ 55 commits, six authors, 60 `Scenario:` lines across features, exactly 44 case-id tags matching `^@[A-Z]+-[A-Z]{3}-\d{3}$`, `./run-tests` exists and is executable, `python3 -m py_compile` passes on every `.py`.
- [ ] **Step 2: Fail, implement, pass.**
- [ ] **Step 3: Venv and a real run** — `cd /Volumes/Develop/develop/northlight && python3 -m venv .venv && .venv/bin/pip -q install behave && mkdir -p reports && ./run-tests features/harbor/booking.feature reports/junit.xml && ls reports/` → JUnit files present; `.venv/bin/behave features -q --no-summary` → 58 passed, 2 failed.
- [ ] **Step 4: Create the GitHub repo and push** — `gh repo create vadymdidenkolab/northlight --private --source /Volumes/Develop/develop/northlight --remote origin --push --description "Northlight — an invented company's code, beside its docket vault. Everything here is made up."`
- [ ] **Step 5: Commit the generator** — reset to scaffold in the vault, `git add .showcase && git commit -q -m "showcase: the code the tests come from" && git tag -f scaffold`.

---

### Task 9: `tests_flow.py` — features in, coverage linked, eight executions

**Files:**
- Create: `.showcase/tests_flow.py`, `.showcase/test_tests_flow.py`

**Interfaces:**
- `events(code_root) -> list[Event]` of kind `raw`, dated:
  1. **06-23 by mateo** — three `test_plan`s (one per product, level 2), nine `test_set`s (one per feature file, `parent` = plan), then `hooks/import-features.sh <code_root>/features/harbor --project=HARBOR` (and LEDGER, FIELD) with `DOCKET_BIN`, `DOCKET_ROOT` set. Then for each test set, `docket set <set> includes=<tests of that feature>` (read the tests' `automation_id` from `docket export --format json` and match on the feature file named in the body).
  2. **06-24 by mateo** — `hooks/link-coverage.sh <code_root>/features --repo=<code_root> --project=HARBOR` per product, at the code revision of that date (`git -C code_root checkout <sha-at-date>` before, `checkout main` after).
  3. **Executions** at 07-03, 07-10, 07-24, 07-27, 08-05, 08-14, 08-28, 09-04 (Fridays and the incident days) by `mateo`: check out the code at the last commit before `when`, run `./run-tests features reports/junit.xml` (behave writes one XML per feature into `reports/`; concatenate their `<testcase>` elements into one file, or call `hooks/import-junit.sh` once per XML with `--execution <key>` after the first creates it), `--environment staging --revision <short sha>`; the last one `--environment production`. Then `python3 hooks/charts.py attachments/test-results.svg` so the chart is committed with the execution.
  4. After each execution with failures, `mateo` files nothing new (the bugs already exist) but sets `found=<bug alias>` on the failing run(s) — resolve run keys from the execution's children in `docket export`.
- Both hooks read `automation_id`; JUnit `classname.name` must equal the id the feature import stored. Verify with `hooks/import-features.sh … --dry-run` first and read one imported test.

- [ ] **Step 1: Tests** — `test_tests_flow.py`: `executions_schedule()` returns eight datetimes in order, all inside the window; `revision_at(code_root, when)` returns the newest commit ≤ when (test on the built temp repo from `test_code`).
- [ ] **Step 2: Implement; replay everything** — `.showcase/build.py --verify`. Expected: ~60 tests, 8 executions, ~480 runs, `docket check .` clean, `attachments/test-results.svg` exists, coverage page (`DOCKET_ROOT=. DOCKET_BIN=… hooks/coverage.sh`) prints a table with covered/uncovered counts, `hooks/workload.sh` shows aiko on top.
- [ ] **Step 3: Commit generator** — reset, add, commit "showcase: features, coverage and eight executions", `git tag -f scaffold`.

---

### Task 10: Final build, serve smoke test, docs in the other repositories, push

**Files:**
- Modify: `docket-showcase/README.md` (numbers as built), `docket-work/igl/README.md` (the third vault), `docket-work/igl/docs/design/the-testbed.md` (a paragraph on the showcase), `docket/core/README.md` (name the showcase beside the demo)

- [ ] **Step 1: Full build with verify** — `git reset -q --hard scaffold && DOCKET_BIN=$HOME/bin/docket .showcase/build.py --verify`. Record the numbers (tasks, commits, tests, executions) and put them into the README table.
- [ ] **Step 2: Serve smoke test** — `docket serve --programs --addr 127.0.0.1:8090 . &` then `curl -s localhost:8090/ | head`, and one page per app surface: `curl -s localhost:8090/app/tests/coverage` (find the exact URL shape in `docket/core/internal/server` — grep `"/app/"`), expect 200 and a table. Kill the server.
- [ ] **Step 3: people --from-git** — `cd /Volumes/Develop/develop/northlight && docket people --from-git /Volumes/Develop/develop/docket-showcase` is wrong (reads the vault's own git); instead run `docket people .` in the vault and confirm the six handles have pages; `git -C ../northlight log --format=%an | sort -u` prints the same six names.
- [ ] **Step 4: Owner commits on top** — after the final replay, commit `README.md` numbers as the owner (this is the one owner commit above the story; document in README that `build.py` recreates everything below it). Move the tag: no — leave `scaffold` where it is; README commit stays above.
- [ ] **Step 5: Push the vault** — `gh repo create vadymdidenkolab/docket-showcase --private --source . --remote origin --push --description "A docket vault for an invented company: three products, six people, twelve weeks, every app. Everything in it is made up."` then `git push origin scaffold`.
- [ ] **Step 6: The other repositories** — in `docket-work/igl`: README "The other vaults" gains `**docket-showcase** is the whole of it on a team's worth of work: three products, six people, twelve weeks and every app, all invented and built by a generator. Open it to see what a board looks like after a quarter.`; `the-testbed.md` gains the same paragraph after the demo one and bumps `updated`; commit as owner, `docket check`, push. In `docket/core/README.md` after the `docket-demo` paragraph: `To see the whole of it on a team's worth of work, clone [\`docket-showcase\`](https://github.com/vadymdidenkolab/docket-showcase): three products, six people, twelve weeks and every app, all invented.` — commit, `go test ./...` unaffected, push.
- [ ] **Step 7: Final grep** — the controller runs its private residue grep over `docket-showcase` and `northlight` (excluding `.git` and `.venv`) → nothing.

---

## Self-review

- **Spec coverage:** §2.1 products and keys → Task 1, 6; §2.2 vocabulary → Task 1; all twelve apps with data → Tasks 6 (checklists, estimation, workload, time-in-status, anomalies, portfolio via hierarchy), 7 (okr, risks, incidents, intake, time), 9 (tests); people, labels, index, design pages, decisions, sprints, attachments → Tasks 4, 7, 9; ~130 tasks, seven relations incl. cross-project → Task 6; §2.3 code layout, case ids, untagged scenarios, key-named commits, two failing at HEAD → Task 8; §2.4 generator, determinism, authorship split → Tasks 3–5, 10; §2.5 done criteria → Task 10 (check, graph, anomalies, serve, report, coverage, people, docs in board and core, both repos private); §2.6 exclusions respected (no import, no CI, no flipping).
- **Placeholders:** none; the one intentionally open point (whether `docket check` tolerates a one-sided relation) has a stated fallback in Task 6.
- **Type consistency:** `Event(when, who, kind, args, message)`, `Person(handle, name, email, role)`, `Engine.key/path/run/commit/apply/replay`, `story.at/new/move/estimate/sprint/comment/relate`, `vault.stamp/patch_frontmatter/append_comment/set_body/write_page/write_person/task_path` are used with the same names throughout.

---

### Task 11: READMEs across the family, by the canon

Every public-facing repository gets a README a stranger can act on in five minutes. Same skeleton everywhere, content per repository. Existing prose is kept where it is good and moved under the right heading; nothing is rewritten for the sake of it.

**The skeleton (in this order):**
1. `# name` + one-sentence tagline + one paragraph "what it is and who it is for".
2. **Quick start** — the shortest path to seeing it work, copy-pasteable, ≤ 10 lines, with what you should see after.
3. **Requirements** — exact: Go version (from `go.mod`), Python 3.11+ and `sh` for app hooks, git, optional Obsidian, Docker for compose.
4. **Install** — binary from Releases, `go install`, Docker; how to check (`docket version`).
5. **Usage** — the commands table (core), or "how to install this app / open this vault".
6. **Configuration** — env vars (`DOCKET_BIN`, `DOCKET_ROOT`, `DOCKET_PREFIX`, `DOCKET_JUNIT_SECRET`, serve flags `--auth`, `--author`, `--addr`, `--programs`), files (`docket.yaml`, `workspace.yaml`, `docket-app.yaml`).
7. **How it works** — the narrative that is there today (the "A board in the browser", "An agent, over a protocol", "A workspace" sections of core).
8. **Where things are** — the family: core, apps, board (spec + roadmap), template, demo, showcase, with one line each and links.
9. **Contributing** — how to run tests (`go test ./...`, `python3 -m unittest` in apps' hooks where present), the `docket check` pre-commit hook, where to file issues (the board in `docket-board`).
10. **License** — MIT (core; state the license of each repository; add `LICENSE` where missing — apps, board, template, demo, showcase, northlight — all MIT, same text as core).

**Files:**
- Modify: `docket/core/README.md` (restructure to the skeleton; keep the content), `docket/apps/README.md` (+ Requirements, Install per app with the `#name` URL form, the programs each app adds and what `--programs` means, Configuration env vars, a table of hooks that a person runs by hand — `import-features.sh`, `import-junit.sh`, `import-cucumber.sh`, `link-coverage.sh`, `import-docs.sh` — with one-line usage each), `docket-work/igl/README.md` (Quick start = clone + open; Where things are), `docket-template/README.md` (what `docket init` does with it, how to make your own template), `docket-demo/README.md` (Quick start: clone, open in Obsidian, `docket serve`; what to look at, in order), `docket-showcase/README.md` (Task 1 draft + Quick start with serve, a "What to look at" tour: the board, a project tab, the coverage page, an incident, a decision, the graph; Rebuild), `northlight/README.md` (what, how to run the features, how results reach the board).
- Create: `LICENSE` in every repository lacking one.

- [ ] **Step 1: Write core's README to the skeleton** — keep every existing section's text; add Quick start (init a vault, new, check, serve --auth none, open http://127.0.0.1:8080), Requirements, Configuration, Where things are, Contributing. Verify every command in it against `docket <cmd> --help`.
- [ ] **Step 2: apps README** as above; check each hook's usage line by running it with `--help` or reading its header.
- [ ] **Step 3: board, template, demo, showcase, northlight READMEs** — each ≤ 120 lines, each with Quick start first.
- [ ] **Step 4: LICENSE files** — copy `docket/core/LICENSE`, keep the copyright line as it is there.
- [ ] **Step 5: Read each README top to bottom as a stranger** — every command copy-pasteable, every link resolves (`gh api repos/vadymdidenkolab/<name>` for each repo link; relative links exist on disk). Commit per repository as owner; push.
