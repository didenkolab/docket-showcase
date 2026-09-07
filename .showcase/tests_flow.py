"""The automation arriving in the vault: features as tests, coverage from the blame, and
seventeen executions that are real `behave` runs against the code repository's own history.

Nothing here writes a test, a run or a result by hand. Every task this module produces is
produced by the vault's own hooks — `import-features.sh`, `link-coverage.sh`,
`import-cucumber.sh`, `charts.py` — run as a person would run them, from the vault root,
with `DOCKET_BIN` and `DOCKET_ROOT` in the environment. That is the point: a showcase whose
test data was typed into Markdown would prove nothing about the tool that is supposed to
collect it.

The shape of it:

  **06-23** three `test_plan`s, nine `test_set`s named after the nine feature files, and
  the first import. Only three feature files exist that day — the plan names the nine
  areas it intends to cover, and the sets fill up as the suite is written.

  **06-24** `link-coverage.sh` per product, at that day's revision: a scenario's lines are
  blamed, and the ticket in the commit that wrote them becomes the work the test covers.

  **the seventeen executions**, per product per date (an execution belongs to one project,
  so eight dates across three products is seventeen, not eight). Each one checks the code
  out at the newest commit at or before its own minute, imports whatever scenarios the
  suite has grown since the last time, runs `behave` for real, and brings the Cucumber
  JSON back in. The counts are therefore not written down anywhere — they are whatever
  the suite did at that revision.

  **the annotations**, after an execution that failed: the failing run is pointed at the
  bug it found. Two of them are pointed later than the execution, because the bug was not
  written down until days afterwards — the 07-03 double charge was filed on 07-08 and the
  07-27 sync loss on 07-29. A run cannot find a bug the board does not have yet.

Two things are done here that the hooks do not do for themselves, both deliberate:

  * **dates.** `docket new` stamps `created`/`updated` with the clock of the machine
    replaying. After each event every task file the hooks touched — found by reading
    `git status` in the vault — is stamped to the event's own minute, so a replay in
    2027 produces the same vault as a replay today.

  * **the other side of what this module itself sets.** The importers write both sides
    of everything they write. Two relations are set here rather than by a hook —
    `includes:` on a set, when the sets are rewritten after an import, and `found:` on a
    failing run — so their inverses, `included_in:` and `found_in:`, are written here
    too. Nothing this module does leaves a pair of tasks disagreeing about their own
    relationship.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

import engine
import vault
from products.common import office_hours, when
from story import PEOPLE

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks"

sys.path.insert(0, str(HOOKS))
import caseid                                                   # noqa: E402  the hooks' own

MATEO = PEOPLE["mateo"]

# Which project each product's work lives in, and what the plan for it is called.
PRODUCTS = {
    "harbor": ("HARBOR", "The Harbor suite"),
    "ledgerline": ("LEDGER", "The Ledgerline suite"),
    "fieldnote": ("FIELD", "The Fieldnote suite"),
}

# The nine feature files, and the `Feature:` line each one opens with. A file's name and
# its scenarios' names never change once written (codebase.py has a test for it), because
# a derived case id is the pair of them — so these are safe to name up front.
FEATURES = {
    "harbor": [
        ("booking.feature", "Berth booking"),
        ("payments.feature", "What a stay costs and who pays for it"),
        ("checkin.feature", "Checking a guest in from the pontoon"),
    ],
    "ledgerline": [
        ("invoices.feature", "Invoice numbers and the lines under them"),
        ("bankimport.feature", "Importing a bank statement"),
        ("tax.feature", "Tax rates, quarters, and closing one"),
    ],
    "fieldnote": [
        ("jobs.feature", "A crew's day"),
        ("routes.feature", "Ordering a crew's day"),
        ("sync.feature", "Putting a phone back together with the board"),
    ],
}

PLANNED = "06-23 09:40"        # the plan and its sets
IMPORTED = "06-23 11:20"       # the first import of the features
COVERED = "06-24 10:10"        # the blame, read into `tests:` links

# Every execution: which product, when, and where it says it ran. Harbor is run on all
# eight dates because Harbor is where the money is; Ledgerline and Fieldnote join as
# their suites become worth running. The last three are the release candidate, which is
# why they say production and why they are early enough in the afternoon to leave the
# story's last event where it was.
SCHEDULE = [
    ("harbor", "07-03 16:00", "staging"),
    ("harbor", "07-10 16:00", "staging"),
    ("harbor", "07-24 16:00", "staging"),
    ("ledgerline", "07-24 16:30", "staging"),
    ("harbor", "07-27 16:00", "staging"),
    ("fieldnote", "07-27 17:00", "staging"),
    ("harbor", "08-05 16:00", "staging"),
    ("fieldnote", "08-05 17:00", "staging"),
    ("harbor", "08-14 16:00", "staging"),
    ("ledgerline", "08-14 16:30", "staging"),
    ("fieldnote", "08-14 17:00", "staging"),
    ("harbor", "08-28 16:00", "staging"),
    ("ledgerline", "08-28 16:30", "staging"),
    ("fieldnote", "08-28 17:00", "staging"),
    ("harbor", "09-04 15:00", "production"),
    ("ledgerline", "09-04 15:20", "production"),
    ("fieldnote", "09-04 15:40", "production"),
]

# The scenario that fails when a job's photographs come back one short. Nobody tagged it,
# so its identity is derived — by the same function both importers use, which is the whole
# reason a derived id is worth anything.
PHOTOS = caseid.derived("sync.feature", "A job finished offline keeps its photographs", "FIELD")

# What a failing run found, and when somebody could say so. A run cannot point at a bug
# the board has not got: the double charge was written down on 07-08 and the sync loss on
# 07-29, both after the execution that failed. The photo failure has no bug at all — it is
# the one mateo writes about in the story rather than files — so it gets a comment.
FOUND = [
    ("harbor", "07-03", "HARBOR-PAY-005", "harbor.payments.double-charge", "07-08 11:40",
     "The Friday run had already caught this. Linking the failing run to the bug so the "
     "history says when we first saw it rather than when we noticed we had seen it."),
    ("fieldnote", "07-27", "FIELD-SYN-001", "field.offline.sync-loss", "07-29 14:30",
     "This is the run from the Monday afternoon, before we knew what it was. It is the "
     "same failure as the bug I have just written down."),
    ("harbor", "08-28", "HARBOR-PAY-004", "harbor.payments.refund-over", "08-28 16:20",
     "Written as a scenario this morning and failing this afternoon, which is the right "
     "order for once."),
    ("harbor", "09-04", "HARBOR-PAY-004", "harbor.payments.refund-over", "09-04 15:10",
     "Still red on the release candidate. The fix is in review, not in the build."),
    ("fieldnote", "08-28", PHOTOS, None, "08-28 17:20",
     "Off by one photo, see the story: the newest picture on the phone is held back on "
     "the theory that it may still be uploading, so a job with six comes back with five. "
     "No bug filed yet — it is a five-minute fix and a very bad demo."),
    ("fieldnote", "09-04", PHOTOS, None, "09-04 15:50",
     "Off by one photo again, on the release candidate. Nobody has picked it up because "
     "it is not written down; that is the lesson rather than the bug."),
]

# The relations this module sets with its own `docket set`, and the side each one owes.
INVERSES = {"includes": "included_in", "found": "found_in"}

TASK_FILE = re.compile(r"^(?:HARBOR|LEDGER|FIELD)/[^/]+\.md$")
IN_FEATURE = re.compile(r"in `([^`]+\.feature)`")


# -- the code repository ---------------------------------------------------------------

def revision_at(code_root, moment: dt.datetime) -> str:
    """The newest commit on `main` at or before a moment, as a full sha.

    The story's commits are written with UTC dates, so the moment is handed to git as
    UTC — `--before` reads a bare date in the machine's own timezone otherwise, and a
    replay in Auckland would check out a different revision from a replay in Lisbon.
    """
    said = moment.strftime("%Y-%m-%d %H:%M:%S +0000")
    sha = _git(code_root, "rev-list", "-1", "--before=" + said, "main").strip()
    if not sha:
        raise ValueError("no commit in %s at or before %s" % (code_root, said))
    return sha


def _git(code_root, *args) -> str:
    done = subprocess.run(["git", "-C", str(code_root), *args],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise RuntimeError("git %s in %s failed:\n%s%s"
                           % (" ".join(args), code_root, done.stdout, done.stderr))
    return done.stdout


def _checkout(code_root, what: str) -> None:
    """The repository at one revision, refusing to move if anything is uncommitted.

    A dirty checkout would either lose somebody's work or carry it into the run, and
    either one makes the results a lie about the revision they claim.
    """
    if _git(code_root, "status", "--porcelain").strip():
        raise RuntimeError("%s has uncommitted changes; the run would not be about %s"
                           % (code_root, what))
    _git(code_root, "checkout", "-q", what)


def _behave(code_root, product: str) -> pathlib.Path:
    """One product's suite, run for real, reported as Cucumber JSON.

    Run from the repository root with a relative path, because behave writes the feature
    it ran as `location: "features/harbor/booking.feature:1"` and the file name in that
    is what an untagged scenario's identity is derived from. An absolute path there and
    every derived id still agrees — only the name counts — but the report stops being
    about a repository and starts being about this machine.
    """
    # Bytecode from a later revision, next to source from an earlier one. Python decides
    # by mtime and a checkout rewrites those, so this is belt and braces — but the belt is
    # cheap and a stale `sync.pyc` would make a run about software that never existed.
    # The virtualenv is not ours to clean and holds thousands of these.
    for entry in sorted(code_root.iterdir()):
        if not entry.is_dir() or entry.name in (".venv", ".git"):
            continue
        for cache in sorted(entry.rglob("__pycache__")):
            shutil.rmtree(cache, ignore_errors=True)
    reports = code_root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    out = reports / (product + ".json")
    done = subprocess.run([str(code_root / ".venv" / "bin" / "behave"),
                           "features/" + product, "-q", "--no-summary",
                           "-f", "json", "-o", str(out)],
                          cwd=code_root, capture_output=True, text=True)
    # 1 is what behave exits with when a scenario failed, and three of these runs are
    # supposed to fail. Anything else — 2 for a bad option, 130 for an interrupt — is not
    # a result and must not be imported as one.
    if done.returncode not in (0, 1):
        raise RuntimeError("behave features/%s exited %d:\n%s%s"
                           % (product, done.returncode, done.stdout, done.stderr))
    if not out.exists():
        raise RuntimeError("behave wrote no report for %s" % product)
    return out


# -- the hooks -------------------------------------------------------------------------

def _hook(eng, script: str, *args) -> str:
    """One of the vault's hooks, run the way a person runs it: from the vault root, with
    DOCKET_BIN and DOCKET_ROOT said out loud."""
    env = {**os.environ, "DOCKET_BIN": str(eng.docket), "DOCKET_ROOT": str(eng.root)}
    done = subprocess.run(["sh", str(HOOKS / script), *[str(a) for a in args]],
                          cwd=eng.root, env=env, capture_output=True, text=True)
    if done.returncode != 0:
        raise RuntimeError("hooks/%s %s exited %d:\n%s%s"
                           % (script, " ".join(str(a) for a in args), done.returncode,
                              done.stdout, done.stderr))
    return done.stdout


def _charts(eng) -> str:
    env = {**os.environ, "DOCKET_BIN": str(eng.docket), "DOCKET_ROOT": str(eng.root)}
    done = subprocess.run(["python3", str(HOOKS / "charts.py"),
                           "attachments/test-results.svg"],
                          cwd=eng.root, env=env, capture_output=True, text=True)
    if done.returncode != 0:
        raise RuntimeError("hooks/charts.py exited %d:\n%s%s"
                           % (done.returncode, done.stdout, done.stderr))
    return done.stdout


# -- the vault -------------------------------------------------------------------------

def _export(eng) -> list:
    return json.loads(eng.run("export", "--format", "json") or "[]")


def _number(key: str) -> tuple:
    project, _, digits = key.partition("-")
    return (project, int(digits) if digits.isdigit() else 0)


def stamp_touched(eng, moment: dt.datetime) -> list:
    """Every task file the hooks just wrote or changed, dated to the story's own minute.

    Read from `git status` rather than from a list this module keeps, because the whole
    point of running the real hooks is that they decide what to write. A file git has
    never seen is new, so it gets `created` as well.
    """
    stamped = []
    for entry in eng.git("status", "--porcelain", "-z").split("\0"):
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if not TASK_FILE.match(path):
            continue
        vault.stamp(eng.root / path, moment, created=code == "??")
        stamped.append(path)
    return sorted(stamped)


def _mirror(eng) -> int:
    """The other side of the two relations this module sets for itself.

    `docket set a includes=b` does not write `included_in` on b, and `docket anomalies`
    reports the pair as disagreeing about their own relationship. The story plants
    exactly one of those on purpose, and it is not one of these. The importers look
    after their own inverses, so this is only `includes` and `found`.
    """
    tasks = _export(eng)
    known = {t["key"]: t for t in tasks}
    held = {key: {name: list((t.get("relations") or {}).get(name) or [])
                  for name in INVERSES.values()}
            for key, t in known.items()}

    changed: dict[str, set] = {}
    for t in tasks:
        relations = t.get("relations") or {}
        for name, inverse in INVERSES.items():
            for other in relations.get(name) or []:
                if other not in known or t["key"] in held[other][inverse]:
                    continue
                held[other][inverse].append(t["key"])
                changed.setdefault(other, set()).add(inverse)

    for key in sorted(changed, key=_number):
        eng.run("set", key,
                *["%s=%s" % (name, ",".join(held[key][name])) for name in sorted(changed[key])],
                "--quiet")
    return len(changed)


def _tests_by_feature(eng) -> dict:
    """Which tests came from which feature file, read from what the importer wrote.

    `import-features.py` ends every test's body with ``From `Berth booking` in
    `booking.feature`.`` — one line per scenario that settles the case, so a test settled
    from two files is in both sets, which is correct and is why this collects rather than
    picks.
    """
    out: dict[str, list] = {}
    for t in _export(eng):
        if t.get("type") != "test":
            continue
        text = (eng.root / t["path"]).read_text(encoding="utf-8")
        for name in dict.fromkeys(IN_FEATURE.findall(text)):
            out.setdefault(name, []).append(t["key"])
    return {name: sorted(keys, key=_number) for name, keys in out.items()}


def _fill_sets(eng, product: str) -> int:
    """A product's three sets: what its feature files hold today, said two ways.

    `includes:` because that is the tests app's own relation, and `parent:` because a
    test with neither a parent nor a label nor a sprint is reported adrift however many
    relations its frontmatter carries — `anomaly.adrift` reads the body for links and
    nothing else, so sixty tests linked to their sets, their runs and the work they cover
    are still sixty tasks "nothing links to". The parent is not a workaround for that: a
    test belongs to a set, the levels say so (set 1, test 0), and the tree is the shape
    somebody opening the vault expects. It is the thing that makes the defect invisible
    here, which is why the report says it out loud.

    Rewritten after every import rather than added to, so a set is a statement about the
    suite as it now stands and not a log of everything that was ever in it.
    """
    by_feature = _tests_by_feature(eng)
    tasks = _export(eng)
    held = {t["key"]: list((t.get("relations") or {}).get("includes") or [])
            for t in tasks if t.get("type") == "test_set"}
    under = {t["key"]: t.get("parent", "") for t in tasks if t.get("type") == "test"}
    filled = 0
    for name, _ in FEATURES[product]:
        key = eng.keys["tests.set.%s.%s" % (product, name.split(".")[0])]
        wanted = by_feature.get(name, [])
        if not wanted:
            continue
        if held.get(key) != wanted:
            eng.run("set", key, "includes=" + ",".join(wanted), "--quiet")
            filled += 1
        for test in wanted:
            if under.get(test) != key:
                eng.run("set", test, "parent=" + key, "--quiet")
                filled += 1
    return filled


# -- the events ------------------------------------------------------------------------

def schedule() -> list:
    """The seventeen executions: product, minute, environment — in the order they run."""
    out = [(product, office_hours(when(moment), "%s execution" % product), environment)
           for product, moment, environment in SCHEDULE]
    for before, after in zip(out, out[1:]):
        if after[1] <= before[1]:
            raise ValueError("%s at %s is not after %s" % (after[0], after[1], before[1]))
    return out


def _plans(eng, event):
    """Three plans and nine sets, before there is anything to put in them.

    A test plan written after the suite exists is a list of what happened. This one is
    written first, names the nine areas the automation is going to have, and is why the
    sets are here on the day only three of the nine feature files are.
    """
    for product, (project, title) in PRODUCTS.items():
        plan = eng.run("new", title, "--type", "test_plan", "--project", project).split()[0]
        eng.keys["tests.plan." + product] = plan
        vault.set_body(vault.task_path(eng.root, plan), _plan_body(product, project))
        for name, feature in FEATURES[product]:
            key = eng.run("new", feature, "--type", "test_set", "--project", project,
                          "--parent", plan).split()[0]
            eng.keys["tests.set.%s.%s" % (product, name.split(".")[0])] = key
            vault.set_body(vault.task_path(eng.root, key), _set_body(product, name))
    stamp_touched(eng, event.when)
    return []


def _plan_body(product: str, project: str) -> str:
    return (
        "Every scenario in `features/%s` in the automation repository, as tests one per "
        "case. The sets under this are the feature files; the tests under those arrive "
        "from `hooks/import-features.sh` and are identified by their case id rather than "
        "by their title, because a title gets improved and an id does not.\n\n"
        "Three of the nine files exist today. The rest are named here because we know "
        "what we are going to cover, and a plan that only lists what is already written "
        "is a report.\n\n"
        "```\nDOCKET_ROOT=. DOCKET_BIN=docket \\\n"
        "  hooks/import-features.sh ../northlight/features/%s --project=%s\n```\n"
        % (product, product, project))


def _set_body(product: str, name: str) -> str:
    return (
        "The cases settled by the scenarios in `features/%s/%s`.\n\n"
        "`includes:` is rewritten after each import, so this set is what the file holds "
        "today — not a list of everything that was ever in it.\n" % (product, name))


def _import(root):
    """The first import: the features as they stood on the day the plan was written."""
    def fn(eng, event):
        sha = revision_at(root, event.when)
        _checkout(root, sha)
        try:
            for product, (project, _) in PRODUCTS.items():
                where = root / "features" / product
                if not where.is_dir():
                    continue                       # written later in the summer
                _hook(eng, "import-features.sh", where, "--project=" + project)
                _fill_sets(eng, product)
        finally:
            _checkout(root, "main")
        _mirror(eng)
        stamp_touched(eng, event.when)
        return []
    return fn


def _coverage(root):
    """What each test was written for, read out of the blame of its own lines."""
    def fn(eng, event):
        sha = revision_at(root, event.when)
        _checkout(root, sha)
        try:
            for product, (project, _) in PRODUCTS.items():
                where = root / "features" / product
                if not where.is_dir():
                    continue
                _hook(eng, "link-coverage.sh", where,
                      "--repo=" + str(root), "--project=" + project)
        finally:
            _checkout(root, "main")
        _mirror(eng)
        stamp_touched(eng, event.when)
        return []
    return fn


def _execution(root, product: str, environment: str, alias: str):
    """One product's suite, actually run, at the revision of that afternoon.

    The import of the features comes first, because a suite grows between executions and
    a result whose test is not in the vault lands nowhere — `import-cucumber.py` says so
    itself, in as many words, at the end of every run. Coverage is relinked for the same
    reason: a scenario written last week was written for a ticket, and the blame knows
    which one.
    """
    def fn(eng, event):
        project = PRODUCTS[product][0]
        sha = revision_at(root, event.when)
        _checkout(root, sha)
        try:
            where = root / "features" / product
            if not where.is_dir():
                raise RuntimeError("no features/%s at %s" % (product, sha[:7]))
            _hook(eng, "import-features.sh", where, "--project=" + project)
            _fill_sets(eng, product)
            _hook(eng, "link-coverage.sh", where,
                  "--repo=" + str(root), "--project=" + project)
            report = _behave(root, product)
            _hook(eng, "import-cucumber.sh", report,
                  "--environment", environment, "--revision", sha[:7],
                  "--project", project)
        finally:
            _checkout(root, "main")

        made = [t for t in _export(eng)
                if t.get("type") == "test_execution" and t["key"] not in eng.keys.values()]
        if len(made) != 1:
            raise RuntimeError("%s: expected one new execution, found %d"
                               % (alias, len(made)))
        eng.keys[alias] = made[0]["key"]
        _mirror(eng)
        stamp_touched(eng, event.when)
        _charts(eng)
        return []
    return fn


def _annotation(exec_alias: str, ident: str, bug: str, note: str):
    """What a failing run means, said once somebody could say it.

    Either the bug it found — a relation, so the bug's page shows the run that caught it —
    or, when there is no bug, mateo's own sentence about why there is not.
    """
    def fn(eng, event):
        execution = eng.keys[exec_alias]
        runs = [t for t in _export(eng)
                if t.get("type") == "test_run" and t.get("parent") == execution
                and (t.get("fields") or {}).get("result") == "failed"
                and (t.get("fields") or {}).get("automation_id") == ident]
        if len(runs) != 1:
            raise RuntimeError("%s: %d failing runs for %s, expected one"
                               % (exec_alias, len(runs), ident))
        run = runs[0]
        if bug:
            eng.run("set", run["key"], "found=" + eng.key(bug), "--quiet")
        vault.append_comment(eng.root / run["path"], MATEO.handle, event.when, note)
        _mirror(eng)
        stamp_touched(eng, event.when)
        return []
    return fn


def events(code_root) -> list:
    """Everything the automation did to this vault, on the story's own timeline."""
    root = pathlib.Path(code_root)
    runs = schedule()
    aliases = {(product, moment.strftime("%m-%d")):
               "tests.execution.%s.%s" % (product, moment.strftime("%m-%d"))
               for product, moment, _ in runs}

    out = [
        engine.Event(office_hours(when(PLANNED), "the test plans"), MATEO, "raw",
                     {"fn": _plans},
                     "{tests.plan.harbor}, {tests.plan.ledgerline}, "
                     "{tests.plan.fieldnote}: a plan per product and a set per feature"),
        engine.Event(office_hours(when(IMPORTED), "the first import"), MATEO, "raw",
                     {"fn": _import(root)},
                     "{tests.plan.harbor}: the scenarios we have so far, as tests"),
        engine.Event(office_hours(when(COVERED), "the coverage links"), MATEO, "raw",
                     {"fn": _coverage(root)},
                     "{tests.plan.harbor}: what each test covers, from the blame"),
    ]

    for product, moment, environment in runs:
        alias = aliases[(product, moment.strftime("%m-%d"))]
        out.append(engine.Event(
            moment, MATEO, "raw",
            {"fn": _execution(root, product, environment, alias)},
            "{%s}: %s on %s" % (alias, PRODUCTS[product][1].lower(), environment)))

    for product, day, ident, bug, moment, note in FOUND:
        alias = aliases[(product, day)]
        out.append(engine.Event(
            office_hours(when(moment), "the %s failure of %s" % (product, day)),
            MATEO, "raw", {"fn": _annotation(alias, ident, bug, note)},
            ("{%s}: %s found {%s}" % (alias, ident, bug)) if bug
            else ("{%s}: %s failed and nobody has written it down" % (alias, ident))))

    return out
