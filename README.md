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
