# Northlight

An [docket](https://github.com/vadymdidenkolab/docket) vault for a software company that does not exist.

Three products, six people, twelve weeks of work — and **everything here is invented**: the
company, the people, the customers, the incidents and the code. None of it was typed, either. A
generator, `.showcase/build.py`, replays those twelve weeks as commits, so that every command and
every app docket has can be seen on a board that looks like a team's rather than a form.

| Project | Product | What it is |
|---|---|---|
| `HARBOR` | Harbor | Berth booking and invoicing for marinas |
| `LEDGER` | Ledgerline | Bookkeeping for small businesses |
| `FIELD` | Fieldnote | Scheduling for field service crews, with an offline mobile app |

## Quick start

    git clone https://github.com/vadymdidenkolab/docket-showcase.git
    cd docket-showcase
    docket serve --programs --auth none --author "Your Name <you@example.com>"

Open <http://127.0.0.1:8080>. You should see a board called Northlight with seven columns —
Backlog, Ready, In progress, In review, QA, Done, Cancelled — with three products' work on it, a
backlog behind it and a wiki of 33 pages. The same folder opened in Obsidian is the same board,
the same pages, and a graph.

## Requirements

| | |
|---|---|
| `docket` | On the `PATH`, for the board in the browser. The vault is Markdown and readable without it |
| git | The vault is a git repository, and its history is the twelve weeks |
| Obsidian | Optional. The other way to read the same folder |
| Python 3.11 or newer | For the programs the apps bring — coverage, workload, the OKR roll-up. Without it those pages render and say they could not run |
| behave | Only if you rebuild the vault, which re-runs the test suite for real |

## Install

Download `docket` from [Releases](https://github.com/vadymdidenkolab/docket/releases) and put it on
your `PATH`. There is nothing else to install: the vault is the clone.

## Usage

What to look at, in order, with the server running on <http://127.0.0.1:8080>:

1. **The board**, at `/`. Seven columns in the order the workflow says, not alphabetically:
   Backlog, Ready, In progress, In review, QA, Done, Cancelled. Three products share it.
2. **A project tab**, at `/?project=HARBOR`. The same board with one product's sixty-one cards on
   it — and a tab draws only its own project's columns.
3. **The coverage page**, at `/app/coverage`. Sixty tests, fourteen open tasks that have one,
   fifty-three that do not, and the first twenty-five of those listed by key. Every number on it
   is a link the vault actually holds: a test says `tests:` and the work shows it in its
   backlinks, so a number can always be followed to the test behind it.
4. **An incident and its postmortem**, `HARBOR-63` and `HARBOR-65` — three marinas' guests charged
   twice for one booking on 8 July, and the write-up that came out of it a week later. They are
   two tasks, joined by `explains`/`explained_by`, because one is an hour of somebody's afternoon
   and the other is a document. `FIELD-51` and `FIELD-52` are the other pair, the afternoon eleven
   crews lost their offline work.
5. **A decision**, `docs/decisions/0006-refunds-are-credit-notes.md`. Six were taken this quarter;
   this is the one that explains why a refund in Harbor goes through Ledgerline at all.
6. **The graph** — Obsidian's, or `docket graph` at the command line, which says the same thing in
   words: 574 notes, 1275 links, one cluster of 570 around `tomasz`, and two notes nothing links
   to. One of the two is `HARBOR-181`, which is also the first anomaly.
7. **The anomalies page**, at `/app/anomalies`. Three findings, and all three were planted:
   - `HARBOR-181` is **adrift** — a task somebody typed and nobody linked to anything.
   - `HARBOR-190` is **one-sided** — it says it blocks `HARBOR-183`, and `HARBOR-183` does not say
     it is blocked by it.
   - `HARBOR-185` is **only-owner** — every open task under it is on `ola`.

   The point of the page is that those three are all it finds in 532 tasks and 1004 links.

`/app/executions` is worth a look after the coverage page: seventeen runs of the suite against
seventeen real revisions of the code, with the two that fail at HEAD still failing.

## Configuration

| | |
|---|---|
| `--programs` | Lets the server run what the apps declared — coverage, workload, OKRs. Without it those pages render, and say they were refused |
| `DOCKET_BIN`, `DOCKET_ROOT` | Where a hook in `hooks/` finds the binary and the vault root. They default to `docket` on the `PATH` and the current directory, so they matter when a hook is run from somewhere else |
| `SHOWCASE_TEMPLATE` | What the engine's own tests hand `docket init` as a template. Defaults to the public [docket-template](https://github.com/vadymdidenkolab/docket-template) URL, which the tests clone; point it at a local clone to run them without the network |
| `SHOWCASE_NO_LEDGER=1` | For a partial rebuild only. Drops the two relations Harbor has with Ledgerline, so `.showcase/build.py --only people,labels,sprints,harbor` can build Harbor on its own |

## How it works

    .showcase/build.py            # resets to the `scaffold` tag and replays the story
    .showcase/build.py --verify   # also runs docket check, graph, anomalies, report

A rebuild resets the whole repository to the `scaffold` tag — the last commit before the story —
and makes everything above it again. That includes this README and the LICENSE: they are part of
the scaffold, so a rebuild puts them back rather than throwing them away. Nothing survives a
rebuild that is not committed at or below `scaffold`.

From there `build.py` replays 1426 events into 1358 commits by the six invented people — checking
the code repository out at seventeen revisions and running `behave` for real along the way, which
is why it takes about half an hour rather than a minute. Nothing in the test data was typed: the
tests, the executions and the runs are all written by the vault's own hooks, run as a person would
run them.

The story is data: `.showcase/story.py` for the people and the sprints, `.showcase/products/` for
the three products' work, `.showcase/crosscut.py` for everything the apps brought,
`.showcase/codebase.py` for the code repository, `.showcase/tests_flow.py` for the test flow.

What comes out of it:

| | |
|---|---:|
| Work on the board | **120** |
| — epics, stories, tasks, bugs, sub-tasks | 10, 53, 16, 17, 24 |
| Records the apps brought | **412** |
| — test plans, sets, tests | 3, 9, 60 |
| — executions, runs | 17, 265 |
| — worklogs, risks, objectives, key results | 30, 6, 3, 7 |
| — incidents, postmortems, requests | 2, 2, 8 |
| Everything, as one file each | **532** |
| Relations between them | 1004 links in 27 verbs |
| Pages under `docs/` | **33** |
| — decisions, design, labels, sprints, app guides, spec, index | 6, 4, 8, 7, 6, 1, 1 |
| People with a page | 6 |
| Saved views in `boards/` | 10 |
| Apps installed | 12 — every one docket has |
| Commits | 1358 of the story, by the six; the rest are the owner's scaffolding |
| The whole graph | 574 notes, 1275 links |

Every relation is written on both sides except one, and that one is the second anomaly above.

## Where things are

- [docket](https://github.com/vadymdidenkolab/docket) — the tool: the binary, the vault format, the
  board in the browser.
- [docket-apps](https://github.com/vadymdidenkolab/docket-apps) — the twelve apps this vault
  installs. The scripts in `hooks/` came from them.
- [docket-board](https://github.com/vadymdidenkolab/docket-board) — docket's own board: its spec and
  its roadmap, kept in a vault like this one.
- [docket-template](https://github.com/vadymdidenkolab/docket-template) — what `docket init` clones
  to make an empty vault.
- [docket-demo](https://github.com/vadymdidenkolab/docket-demo) — a smaller vault to read first, if
  532 tasks is too many at once.
- [northlight](https://github.com/vadymdidenkolab/northlight) — the code the tests come from:
  sixty-eight commits by the same six people, 15 June to 4 September 2026, each message opening
  with the key of the task it belongs to. That is what `hooks/link-coverage.sh` blames a scenario
  against to say which work its test covers; nothing else joins the two repositories.

All of those are private today except the template; each link starts resolving as it is opened up.

## Contributing

The story has its own tests, and a replay is a long way to find a typo:

    cd .showcase && DOCKET_BIN=$(command -v docket) python3 -m unittest

Some of those tests build an empty vault with `docket init` and clone the template to do it. Set
`SHOWCASE_TEMPLATE` to a local clone of [docket-template](https://github.com/vadymdidenkolab/docket-template)
to run them offline.

To change the story, change the data — a task in `.showcase/products/harbor.py`, a person in
`.showcase/story.py`, a page in `.showcase/crosscut.py` — then run those tests, commit `.showcase`,
move the `scaffold` tag onto that commit, and only then rebuild. `build.py` resets the working
tree to `scaffold` before it replays, so an uncommitted change to the generator is a change the
rebuild would throw away: it refuses to start while `.showcase`, `hooks/`, `docket.yaml` or this
README have uncommitted changes, and names them. `--keep` skips the reset and the check both.
Issues about docket itself belong on its own board, in
[docket-board](https://github.com/vadymdidenkolab/docket-board).

## License

MIT. See [LICENSE](LICENSE).
