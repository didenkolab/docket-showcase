# Working in this vault

This repository is a docket vault: a task tracker and a knowledge base made of Markdown files.
You change it with ordinary file tools. There is no API to call and no server to ask.

If `docket mcp` is connected, prefer its tools for anything that changes a task: they allocate
the key, keep `status` and `status_category` together, check the move against the workflow,
rename the file when the title changes and commit — each of which is a way to corrupt the vault
by hand. Read with file tools freely; this file tells you how.

The [vault format](https://github.com/didenkolab/docket-board/blob/main/docs/spec/vault-format.md)
is normative. This file is the short version — the rules you need in order to not corrupt the
vault.

## Keys and where files live

A key is `HARBOR-12`. The file is named after the task — the key, a space, and the title:

```
HARBOR/HARBOR-12 Fix login redirect loop.md
```

The name carries the title because that is what Obsidian shows in the graph, in the file
explorer and in search. A file called `12.md` tells nobody anything.

The projects this vault holds are listed in `docket.yaml`, each a folder at the root. Numbers
start at 1 per project and are never reused.

**Link to a task by its whole note name**, not by its key:
`[[HARBOR-12 Fix login redirect loop]]`. Obsidian resolves the name of a note and does not
consult aliases, so `[[HARBOR-12]]` on its own points at nothing. `docket check` says so and
prints the form to use.

To pick a key, list the project's folder, take the highest number, add one — or run
`docket new`, which does exactly that. If two agents pick the same number in parallel branches,
git reports an add/add conflict on merge: rename one task and fix inbound links. Do not
renumber existing tasks to close gaps; a key is permanent.

## Creating a task

Copy `templates/task.md` to `HARBOR/HARBOR-<n> <title>.md` and fill the frontmatter. Every
field in the template is required except `parent`, `labels` and `aliases`.

```markdown
---
key: HARBOR-12
title: Fix login redirect loop
type: bug
status: In progress
status_category: doing
priority: high
assignee: agent/claude
parent: "[[HARBOR-4 Session model]]"
labels: ["[[auth]]"]
created: 2026-01-01T09:00:00Z
updated: 2026-01-01T09:00:00Z
aliases: []
---
```

## The three rules that matter most

**A relationship is a link.** `parent` and every entry in `labels` are wikilinks — not bare
words:

```yaml
parent: "[[HARBOR-4 Session model]]"
labels: ["[[auth]]", "[[regression]]"]
```

A wikilink is the only pointer Obsidian resolves, draws in the graph and counts as a backlink.
The same word written plainly connects nothing, so an epic written that way has no edge to its
tasks and a label groups nothing. Link by note name — `[[HARBOR-4 Its title]]`, never
`[[HARBOR-4]]`, because Obsidian does not consult aliases. Quote them: unquoted,
`[[auth]]` is a nested list in YAML. A label link need not resolve; an unresolved link is still
an edge, and writing the page later is what gives the label somewhere to explain itself.

A relation says **how** two tasks are connected, and the property name is the verb:
`blocks`, `blocked_by`, `duplicates`, `duplicated_by`, `causes`, `caused_by`, `relates`. Same
form — a list of links. Write each side yourself; nothing writes the inverse for you.

`parent` is hierarchy and decides what the board does. A relation is an annotation. Do not use
one for the other.

A type has a level, and **a parent sits above its child**: an epic holds a task, a task holds a
sub-task, and a bug cannot hold an epic. `docket.yaml` says which level each type is at. A
sub-task never appears in a backlog on its own, because it is work inside a task rather than a
thing to schedule.

`tags` is the other one, and a different thing: a label says what a task is about, a tag says
which slice of the work it is in, and tags nest — `area/auth` is inside `area`. Written without
the `#` and unquoted: `tags: [area/auth, needs-review]`. No spaces, and not all digits.

**Frontmatter is flat.** No nested objects, ever. Obsidian's property editor only handles flat
values and Bases only filters on top-level properties — a nested field makes the task
uneditable by hand and invisible to the board. Vault-specific fields go at the same level as
core ones. Fields carried in from another system are prefixed `x_`.

**`status` and `status_category` move together.** `status` is the human name from `docket.yaml`;
`status_category` is its category in that same file. Changing one without the other puts the
task in a column the board cannot render. Both change in the same edit.

## Editing a task

- Set `updated` to the current UTC time on every change.
- Leave `order` alone. It is where somebody dragged the card in its column; a task without
  one sorts after the ones that have one, which is where a new task belongs.
- Never edit `key` or `created`. Changing `title` renames the file too; `docket check`
  reports a name that no longer matches.
- Append comments under `## Comments`, newest last, in the form
  `**<author> · <YYYY-MM-DD HH:mm>** — text`.
- Link to other tasks and pages by note name: `[[HARBOR-4 Its title]]`, `[[docs/some-page]]`.

## Estimates and sprints

Both are optional, and each is one line of frontmatter.

**An estimate** is a plain unquoted number written after `priority`: `estimate: 3`. The unit and
the values allowed are in `docket.yaml` under `estimates` — points on a Fibonacci scale in a fresh
vault. Two ways to get it wrong, and `docket check` reports both: a number that is not on the
declared scale, which is a finding rather than something to round, and an estimate on a task that
has children, because a container's estimate is the sum of its children's and is added up when it
is shown. Writing that sum down is a second record of one fact, and it is the one that will
disagree. Absent is not `0`: `0` says there is no work in the task, absent says nobody has
estimated it — so leave the field out rather than filling it with a guess.

**A sprint** is a page under `docs/sprints/`, named after its title, carrying `starts`, `ends` and
a body that is the goal, what was cut and why, and the retrospective. It has no state field:
whether a sprint is running is a question about its dates and today. A task is in one by linking
to it, after `assignee` — `sprint: "[[Sprint 1]]"`, quoted like every other link, by note name.
One sprint at a time: carrying a task over means pointing the field at the new sprint, and the old
sprint's retrospective is where it is recorded that the task did not finish. Do not add a list of
tasks to a sprint page; its contents are its backlinks.

## Writing documentation

Every page under `docs/` carries `title`, `type` and `updated`, and `type` says where it lives:

| `type` | What it is | Where |
|---|---|---|
| `decision` | A choice that was hard to make and is expensive to revisit | `docs/decisions/NNNN-kebab-title.md` |
| `design` | How something works and why it is that way | `docs/design/` |
| `spec` | What must be true; the thing `docket check` enforces | `docs/spec/`, with `status: normative` |
| `sprint` | A fortnight: the goal, what was cut, the retrospective | `docs/sprints/`, with `starts` and `ends` |
| `page` | Everything else | anywhere under `docs/` |

`updated` is a plain `YYYY-MM-DD` and you set it on every change.

**A decision is the only kind with a required shape**, and it is `## Context`, `## Decision`,
`## What this costs`, `## Alternatives considered`, spelled that way and in that order. It also
carries `status: proposed | accepted | superseded` and `date`. Numbers run from `0001` in the
order the decisions were taken and are never reused or renumbered, because the number is what
gets cited. The other four kinds have no required sections: they are arguments, and a required
shape flattens an argument.

Write a decision only when there was a real fork — alternatives somebody would have argued for,
and a cost that was accepted. Explaining how a mechanism works is a design page, even when it
argues hard for itself. Getting this wrong in the other direction is worse: a fork recorded as a
design page never writes its alternatives down, and the argument gets had again.

Everything else — what each section must contain, how a page is named, superseding, and what
`docket check` can and cannot tell you — is in [[documents]], and
[[0001-a-session-is-a-signed-cookie]] is a worked decision to read before writing one.

**Do not write a page whose purpose is to list other pages.** No index of labels, no "see all",
no front page linking every epic. A link is a relationship, not a route: a list connects
everything on it, so it lands in the middle of the graph and collapses the distance between
clusters that have nothing to do with each other. On a vault of forty notes, two such pages were
the two most connected notes in it and accounted for eighteen per cent of every edge.

Finding a page is what the file explorer, the tag pane, the quick switcher and backlinks are
for. None of them draws an edge. A front page may link the three or four pages somebody must
read first — that is a relationship. It may not link everything. A page nothing links to is a
page nobody finds, and `docket graph` reports it.

## Labels and tags: which to use

- **A label is a theme work gathers around**, and it is a link, so it costs the graph an edge.
  One or two per task. A task with five has labels that each mean too little.
- **A label page never links another label page.** Its value is its backlinks; linking siblings
  turns the labels themselves into a blob.
- **A tag is a slice to search by**, and it is not a node, so it costs the graph nothing. Use
  tags liberally: `area/...` for where the work is, plus whatever a search would want.
- **Never say the same thing twice.** A task with both `labels: ["[[payments]]"]` and
  `tags: [payments]` records one fact in two places, and the copy is the one that goes stale.
- **A sub-task usually needs no labels.** It is inside a task that has them.

## Committing

One commit per logical change, describing what changed for the reader, not which files moved.
Moving a task to `In review` is a commit. Writing a page is a commit. The commit history *is*
the change history of the tracker: there is no separate audit log, and
`git log --follow -p "HARBOR/HARBOR-12 Fix login redirect loop.md"` is how anyone sees
who moved what and when — with `--follow`, because retitling renames the file.
