#!/usr/bin/env python3
"""Rebuild the Northlight vault from the `scaffold` tag by replaying the story."""
import argparse, os, pathlib, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine, story

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCKET = os.environ.get("DOCKET_BIN", "docket")
STAGES = ["people", "labels", "sprints", "harbor", "ledgerline", "fieldnote", "crosscut", "code", "tests"]

# What a rebuild replays *from*, rather than what it writes. A change to any of
# these is a change to the generator or to the scaffold, and the reset below
# would throw it away without saying so.
GENERATOR_PATHS = (".showcase/", "hooks/", "docket.yaml", "README.md")


def uncommitted_generator_files(root):
    """Paths under the generator or the scaffold that git says are not committed.

    `build.py` starts by resetting the tree to `scaffold`. An edit to a story
    file, a hook or the README that has not been committed and tagged is gone
    the moment it does — silently, and after half an hour of replay somebody is
    left wondering why nothing changed. Naming them first is cheaper.
    """
    # -uall: an untracked directory is collapsed to its name by default, and
    # "`.showcase/products/` would be lost" says less than naming the file.
    out = subprocess.run(["git", "status", "--porcelain", "-uall", "--"] + [p.rstrip("/") for p in GENERATOR_PATHS],
                         cwd=root, check=True, capture_output=True, text=True).stdout
    hits = []
    for line in out.splitlines():
        if not line.strip():
            continue
        path = line[3:]
        if " -> " in path:                      # a rename: the destination is what is at risk
            path = path.split(" -> ", 1)[1]
        path = path.strip('"')
        if any(path == p.rstrip("/") or path.startswith(p) for p in GENERATOR_PATHS):
            hits.append(path)
    return sorted(set(hits))


def events_for(stage, e):
    if stage == "people":   return story.people_events()
    if stage == "labels":   return story.label_events()
    if stage == "sprints":  return story.sprint_events()
    if stage == "harbor":   from products import harbor;      return harbor.events()
    if stage == "ledgerline": from products import ledgerline; return ledgerline.events()
    if stage == "fieldnote": from products import fieldnote;  return fieldnote.events()
    if stage == "crosscut": import crosscut;                  return crosscut.events()
    if stage == "code":     import codebase;                  return codebase.events(ROOT.parent / "northlight")
    if stage == "tests":    import tests_flow;                return tests_flow.events(ROOT.parent / "northlight")
    raise SystemExit("unknown stage " + stage)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=",".join(STAGES))
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--keep", action="store_true", help="do not reset to scaffold first")
    a = ap.parse_args()
    if not a.keep:
        loose = uncommitted_generator_files(ROOT)
        if loose:
            print("Uncommitted changes the reset to `scaffold` would throw away:", file=sys.stderr)
            for path in loose:
                print("  " + path, file=sys.stderr)
            raise SystemExit("Commit them, move the tag (git tag -f scaffold), then rebuild — or pass --keep.")
        subprocess.run(["git", "reset", "-q", "--hard", "scaffold"], cwd=ROOT, check=True)
        # `git clean` looks at ignored files only with -x, which is not passed;
        # the excludes are for .showcase, which is tracked, and for a .venv or
        # a .superpowers somebody has that this vault's .gitignore may not.
        subprocess.run(["git", "clean", "-qfd", "--exclude=.showcase", "--exclude=.venv", "--exclude=.superpowers"], cwd=ROOT, check=True)
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
