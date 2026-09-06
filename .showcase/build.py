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
        subprocess.run(["git", "reset", "-q", "--hard", "scaffold"], cwd=ROOT, check=True)
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
