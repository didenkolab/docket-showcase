---
title: Documents
type: spec
status: normative
updated: 2026-08-31
---

# Documents

Normative specification of this vault's knowledge base. The
[vault format](https://github.com/didenkolab/docket-board/blob/main/docs/spec/vault-format.md)
says what a task is; this says what a page is — the five kinds a document under `docs/` can be,
what each is for, where it lives, what frontmatter it carries and what it must contain.

It arrives with a new vault because a knowledge base with no shape drifts within a fortnight, and
it is yours to change: the amendment rule is §13.

## 1. Why there is a shape at all

docket's own instructions used to say that pages go anywhere under `docs/` in whatever tree makes
sense, and that there is no schema because it is a wiki. What that produced is on the record in
the project that wrote the format. Five decisions, written over two days by the same hands, came
out in three different shapes: one ended with a `## Status` heading, one grew `## How it is
distributed` and `## Consequences`, and three settled on `## What this costs`. Nobody chose that.
It drifted, because nothing said what the shape was, and each author copied whichever file they
happened to open.

The cost lands on the next reader, and increasingly the next reader is an agent that cloned the
repository ten seconds ago. Asked to write down a decision, it has three examples and no way to
tell which is the pattern. It picks one, and the drift continues.

So the shape is written down. It is deliberately thin — one kind of document has required
sections and four do not — because a required heading buys consistency where a reader needs to
find the same thing in the same place, and costs an argument its shape everywhere else.

## 2. Every page carries frontmatter

```yaml
---
title: How sessions work
type: design
updated: 2026-01-08
---
```

`title` is the page's title, and it matches the file name (§10). It exists in the frontmatter as
well as in the name because Bases sorts and displays on a property and cannot read a file name
into a column.

`type` is one of `decision`, `design`, `spec`, `sprint`, `page`, and it tells a reader, a board
and `docket check` which of §4 to §8 applies. Those five are the kinds that have rules. A vault
writing some other word gets no complaint from rule 14 and no help from it either, because the
format does not own anybody's knowledge base — but a sixth kind in *this* list is a change to
argue for, and §13 says how.

`updated` is a plain unquoted `YYYY-MM-DD`, which is the form Obsidian reads as a date and can
sort on — the same form `starts` and `ends` take on a sprint. It is the day the page was last
changed, and it is set in the commit that changes it. A task's `updated` is an RFC 3339 timestamp
because a task moves several times a day and the order of the moves is what the board reads; a
page is written in sittings, and the day is the resolution anybody needs.

These three are required of every page. Each kind adds one or two of its own, listed below. A
page may carry other properties freely — `aliases`, `tags`, whatever this vault finds it wants —
and nothing objects: the requirement is a floor, not a list of what is permitted.

## 3. The five kinds

| `type` | What it is | Where | Required sections | Extra frontmatter |
|---|---|---|---|---|
| `decision` | A choice that was hard to make and is expensive to revisit | `docs/decisions/NNNN-kebab-title.md` | `## Context`, `## Decision`, `## What this costs`, `## Alternatives considered` | `status`, `date`, and `supersedes` when it replaces one |
| `design` | How something works and why it is that way | `docs/design/` | none | none |
| `spec` | What must be true; the thing `docket check` enforces | `docs/spec/` | none | `status: normative` |
| `sprint` | A fortnight: the goal, what was cut, the retrospective | `docs/sprints/` | none | `starts`, `ends` |
| `page` | Everything else in the knowledge base | anywhere under `docs/` | none | none |

The first four kinds each have one folder and are found nowhere else, because each is looked up
by kind: somebody reads the decisions in order, or reads every spec before changing something
load-bearing. A `page` is everything the other four are not, and it goes wherever the tree makes
sense — which is most of a knowledge base and is the default answer.

## 4. Decision

### 4.1 What a decision is for

A decision records a choice that was hard to make and is expensive to revisit. It is written for
the person who, a year from now, finds the choice inconvenient and wants to know whether the
reasons still hold — and that person is usually the one who made it.

The value of the page is not the choice. The choice is generally visible in the code; anybody can
see *what* was done. What nothing else records is the two things either side of it: the options
that were live at the time, and the price that was accepted for taking this one. Those are what
let a later reader tell a decision that has expired from a decision that is merely annoying.

A decision is not a status report and not a plan. It says what was chosen and why, in the present
tense, as a rule somebody can apply.

### 4.2 Where it goes, and what it is called

```
docs/decisions/0001-a-session-is-a-signed-cookie.md
```

Four digits, from `0001`, in the order the decisions were taken. **Numbers are never reused and
never renumbered.** A number is the handle: `ADR-0003` gets said in commit messages, in other
decisions, in the code and out loud, and renumbering makes every one of those point at something
else. A gap left by a decision that was deleted stays a gap, for the reason a task key does.

The rest of the name is the title in lower case with hyphens for spaces. It may drop an article
or shorten a clause to stay readable in a file explorer, because the full title is in the
frontmatter and in the heading, and the name only has to identify.

The first line of the body is the heading, in the form `# ADR-0001 — A session is a signed
cookie`: the number, an em dash, the title. That is what a reader sees at the top of the page and
what makes the number sayable.

Retitling a decision renames the file and rewrites the links to it, as retitling anything does —
but there is rarely a reason. A decision is a record of what was thought at a moment. If the
title turns out to be wrong, the thinking probably is too, and that is a new decision rather than
an edit.

### 4.3 Frontmatter

```yaml
---
title: A session is a signed cookie
type: decision
status: accepted
date: 2026-01-08
updated: 2026-08-31
---
```

`status` is one of three:

| Value | Meaning |
|---|---|
| `proposed` | Written and argued, not yet agreed. It does not govern anything. |
| `accepted` | It governs. Code and other documents may rely on it. |
| `superseded` | Another decision replaced it. |

Three, because a fourth is a question nobody remembers the answer to. There is no `rejected`: a
proposal that lost is either deleted before it is committed or, if the argument is worth keeping,
becomes the `## Alternatives considered` entry of the decision that beat it. A rejected page
sitting in the folder with a number is a decision that half the readers will act on.

**Nothing is deleted when it is superseded.** The page keeps its number and its text, because
links to it and commit messages naming it must keep resolving, and because the superseded
reasoning is the most useful thing in the folder — it is the record of an argument that has
already been had once.

`date` is the day the decision was taken and never changes. `updated` is the day the file was
last touched. The gap between them is informative: a decision dated eight months ago whose
`updated` is today has been annotated since, which is what §4.5 asks for.

`supersedes` goes after `date`, and only when there is one to name. Its value is a quoted
wikilink to the decision this one replaces, written like every other link in the vault, because
a relationship is a link — the earlier decision gets the edge in its backlinks without anybody
editing it, so the pair reads from either end.

A decision whose `status` is `superseded` must carry it. That is the one state where a missing
property is worse than no property at all: the page tells a reader not to follow it and does not
say where to look instead. Rule 14 reports it.

When a decision is replaced in full, its own `status` becomes `superseded` in the same commit.
When it is replaced only in part, it stays `accepted` and a note above `## Context` says which
part went and to which decision. Flipping it to `superseded` would tell a reader to ignore a
holding that is still in force.

### 4.4 The four sections

`## Context`, `## Decision`, `## What this costs`, `## Alternatives considered`, spelled exactly
that way and in that order, so that a reader who opens any decision in any repository finds the
cost in the same place. Sub-headings inside a section are free. Prose above the first heading is
allowed and is where a supersession note goes.

**`## Context`.** The situation that forced a choice. What was true, what went wrong, what
constraint applies, and what would have happened if nobody decided anything. It states a problem,
not a subject: "the fix worked in the web front end and failed behind the job runner, because the
two had grown different answers to the same question" is a context, and "this page is about
authentication" is a heading with nothing under it.

The test is that a reader who has never seen the project can finish the sentence *and so we had
to choose between…*. If the Context can be read without learning that anything was at stake,
there was no decision to record — see §9.

**`## Decision`.** What was chosen, in the present tense, as a rule the reader can apply. The
first line is the choice in one sentence and in bold; everything after it is the reasoning, in
the order the reasons carry weight rather than the order they were thought of. Consequences that
follow immediately from the choice belong here, and so does anything the choice settles as a
by-product.

Write it so it can be quoted. Other documents will cite this section as the authority for a rule,
and a decision whose central sentence has to be assembled from three paragraphs gets cited
inaccurately.

**`## What this costs`.** What was given up, named by the people who accepted it. This is the
section that gets skipped and the one a reader a year later opens first, because it is the only
place that says what going the other way would have bought.

A decision with no cost is not a decision. It is a preference, or the cost has not been found
yet, and the second is far more common than the first. Look for it in three places: what got
slower, what got harder to explain, and what the rejected alternative was actually good at. If
the cost is genuinely small, write what it is and write that it is small — "none" is almost
always a failure to look, and it reads as one.

**`## Alternatives considered`.** The options that were genuinely available, each with the reason
it was not taken. One per paragraph, the alternative in bold, then the reason — which must be a
reason and not a verdict. "Rejected because every request then costs a read, and because the job
runner would need the same database connection as the front end" is a reason. "Rejected: not a
good fit" is a verdict, and it is exactly what somebody will re-propose against in a year.

Two or three is the usual number. An alternative nobody would have chosen is filler and makes the
section look worked when it is not; the entries worth writing are the ones somebody will suggest
again. None at all means either that the choice was forced, in which case the Context should say
so and the page is probably a design page, or that the alternatives were not looked for.

### 4.5 A decision is amended, not rewritten

The page records the reasoning as it stood on its `date`. When a later decision overturns it, the
old page keeps its text and gains a note above `## Context` saying which decision replaced it and
why, in the terms the replacement uses.

A decision edited afterwards to agree with what actually happened records nothing. It reads as
though the authors were right the whole time, which removes the only evidence a later reader has
about how good this team's judgement is.

Corrections of fact — a broken link, a renamed file, a mistyped command — are ordinary edits and
just bump `updated`.

### 4.6 A worked example

`docs/decisions/0001-a-session-is-a-signed-cookie.md` is the one this template ships with. It is invented and it
is meant to be deleted, but read it before writing your first real one, because four things in it
are what the shape is for:

- Its Context says what went wrong and why the wrongness forced a choice, in two paragraphs and
  with a task key in them. It could not be mistaken for a page about sessions in general.
- Its Decision is one bold sentence that another document could quote, followed by the reasoning
  and by what the choice settles as a by-product.
- Its cost is a real loss — sessions cannot be ended early — written plainly, with the sentence
  that the day somebody needs to eject one person immediately, the answer will be that we cannot.
  That is the sentence a decision exists to make findable in advance.
- Its alternatives are three things a colleague would have argued for, each with the reason it
  lost, and one of them is named as the first to revisit if the cost bites.

Note also what it does not do. It does not link the tasks it mentions: `HARBOR-12` is written as a
key in backticks, because a decision is not a place where work should gather.

## 5. Design

A design page explains how something works and why it is that way. It is written for somebody who
has to change the thing and needs the reasons before they touch it, and its job is to be
convincing rather than to be complete.

It has **no required sections**, and that is a decision rather than an omission. A design page is
an argument, and an argument has the shape its argument has. Forcing `## Context` on to a page
whose first job is to describe a mechanism produces a heading with a sentence under it that the
writer resented — and the discipline the sections were supposed to buy is spent on filling them.

What a design page owes its reader instead:

- The first paragraph says what the page is about and what claim it is making, before any detail.
- Somewhere in it, honestly, what the approach costs. That paragraph is what makes the rest
  credible.
- What is unbuilt, if anything is, said as such rather than in the present tense.

`docs/design/`, and the three properties from §2 with nothing added.

## 6. Spec

A spec says what must be true. It is the document a checker is written against, and a reader may
act on every sentence in it without checking anywhere else — which is what `status: normative`
declares.

`docs/spec/`, and `status: normative` in the frontmatter. No required sections: a spec is
organised by its subject.

**Rules are numbered, and a number is never reused or renumbered.** A finding prints a rule
number, a source comment cites a section, other pages cite `§3.10`, and a commit message says
which rule it satisfies. Renumbering silently repoints every one of those at something else, and
nothing anywhere will report it. So a rule that is withdrawn keeps its number and says it is
withdrawn, and a new rule takes the next number even when it belongs, logically, in the middle of
the list.

A spec and a design page usually come in pairs, and they say different things about the same
subject: the design page argues and the spec states. When the two disagree, the spec is what
holds — and the design page is wrong and gets edited, because a design page that argues for
something the spec forbids will be believed by somebody.

## 7. Sprint

A sprint is a fortnight, and it is fully specified in
[vault format §5.3](https://github.com/didenkolab/docket-board/blob/main/docs/spec/vault-format.md).
In summary, so that this table is complete: `docs/sprints/`, named after its title, `starts` and
`ends` as plain `YYYY-MM-DD`, no state field because whether a sprint is running is a question
about today, and a body that is the goal in more than one line, what was cut and why, and the
retrospective. `docs/sprints/Sprint 1.md` is the worked example this template ships with. It is cited by path
rather than linked, because a document the reader is told to delete is a wikilink waiting to
be dead.

No required sections, and one prohibition that matters more than a required section would: **a
sprint page never links a task**, in a list or in prose. Its contents are its backlinks. In prose
a task is named by its key in backticks — `` `HARBOR-12` `` — and rule 13 reports a page that does
otherwise.

## 8. Page

Everything the other four kinds are not. Notes, references, runbooks, glossaries, meeting
records, the pages that explain what a label means, the front page of the knowledge base. It goes
anywhere under `docs/`, carries the three properties from §2 and nothing more, and has no
required shape.

`page` is the default and most of a knowledge base is pages. It is not a lesser kind and not a
holding pen for documents nobody classified.

The one restriction applies to this kind more than the others, because this is the kind people
write indexes as: **a page whose purpose is to list other pages must not be written.** A list
connects everything on it, so it lands in the middle of the graph and collapses the distance
between clusters that have nothing to do with each other. The file explorer, the tag pane, the
quick switcher and backlinks are how a page is found, and none of them draws an edge.

## 9. Which kind — decision or design page

This is the call people get wrong, in both directions, and it is worth more words than the rest.

> **A decision has alternatives that were genuinely available and a cost that was accepted. A
> design page explains a mechanism.**

Two questions, and both have to be yes for a decision:

1. **Was there a fork?** Could somebody competent, knowing everything you knew at the time, have
   gone the other way and defended it? Not "was there another option in the abstract" — was there
   one somebody would have argued for.
2. **Was something given up?** Name what got worse. If nothing did, there was no trade, and a page
   with no trade in it is describing rather than deciding.

The test that settles most cases: **try writing `## Alternatives considered` with two entries a
colleague would have argued for.** If you cannot, write the design page.

**The common mistake is filing an explanation as a decision.** A page that argues a position, has
a costs section and compares itself to the alternative can still be a design page — and usually
is, when the fork it appears to describe was taken somewhere else and this page explains the
machine that the decision produced. The decision is the fork. The design page is everything
downstream of it.

**The damaging mistake is the reverse**: recording a real fork as a design page. Then the
alternatives are never written down at all, and in a year somebody proposes the rejected one and
nobody can say why it lost. A design page can be rewritten when it turns out to be wrong; a
decision is the thing that stops an argument being had twice, and it can only do that if it wrote
the losing side down.

**A decision and a design page usually come in pairs, and the split is clean.** The decision keeps
the fork, the alternatives and the price. The mechanism goes to the design page, which is free to
grow, be corrected and be rewritten, none of which a decision may do. When you find you have
written both halves in one file — a document that argues a choice for four paragraphs and then
explains how the resulting thing works for twelve — that is the seam to cut along.

Two smaller cases:

- **A choice that was forced is not a decision.** If there was one way to do it, write a design
  page saying how it works and why there was one way. The `## Alternatives considered` you would
  have to write is a list of things nobody would do.
- **A choice that is cheap to revisit is not a decision either.** The number is the cost of
  changing your mind, not the size of the thing. Which library to depend on is a decision if the
  code leans on its quirks and an ordinary commit if it does not.

## 10. Naming

**A decision is `NNNN-kebab-title.md`** (§4.2). **Everything else is named after its title,
exactly.**

Obsidian labels a graph node, a file explorer row, a backlink and a quick switcher result with
the file name and nothing else — not with the `title` property, not with an alias. A file called
`notes-2.md` is a node in the graph labelled `notes-2`, and a graph of those is a graph of
nothing. That is why a task's file is named after its task, and it applies to pages without
changing a word.

So `docs/design/How sessions work.md` holds `title: How sessions work`, and the title as written
goes into the name — in whatever language it was written in, with its capitals and its commas.
Only what a file name or a wikilink cannot hold is replaced: `/` and `\` would make folders,
`: * ? " < > |` are refused by one file system or another, and `# ^ [ ]` are wikilink syntax, so
a note holding them cannot be linked to.

An em dash `—` is the separator where a name needs one, matching the tasks. **No emoji in a file
name**: it is a graph label that says nothing at a distance, it sorts differently in every tool
that will touch this repository, and it makes the name harder to type into the quick switcher,
which is the thing the name is for.

**Two files here break the rule on purpose.** `docs/index.md` is named for its position rather
than for its title, because everything that makes, clones or renders a vault has to be able to
find the front page without first knowing what the project is called. This file is the second,
named to match the path the format's own specification uses, so that a finding printed against
`docs/spec/documents.md` names a file that is there. Both are exceptions with a reason written
down, which §13 allows and which a quiet one is not.

## 11. Linking

> **A page nothing links to is a page nobody finds.**

`docket graph` reports them — the notes that stand alone. Writing a page is not finished until
something links to it, and the link that fixes an orphan is the one that already wanted to exist:
the decision links the design page that explains what it produced, the spec links the design page
that argued for it, the task links the page that gives it context. It is never a line added to a
front page. A front page that gains an entry every time somebody writes a page is the index §8
refuses, and it will hold a fifth of this vault's edges within a year.

Which mechanism links what — `parent`, relations, `labels`, `sprint`, `tags` — is
[how things connect](https://github.com/didenkolab/docket-board/blob/main/docs/design/how-things-connect.md),
and the normative form of it is `AGENTS.md` and
[vault format §5](https://github.com/didenkolab/docket-board/blob/main/docs/spec/vault-format.md).

## 12. What is checked, and what is not

Rule 14 of the vault format is this document, and `docket check` reports:

- A page that does not say what kind it is.
- A `decision` missing any of its four sections, naming the ones it does have.
- A decision whose file name is not `NNNN-kebab-title.md`, and two decisions sharing a number.
- A decision keeping its status in a `## Status` section as well as in its frontmatter — one
  fact in two places, and the section is the copy nothing reads.
- A `status` that is not one of the three, and a decision with no `date`.
- A decision marked `superseded` that does not say by what, and a `supersedes` written as a
  string rather than a wikilink.

A `[[wikilink]]` that resolves to nothing is rule 8, everything about a sprint page is rule 13,
and a note nothing links to is `docket graph` rather than a finding, because an island is a
question and not always a fault. The order of a decision's sections, the folder each kind lives
in and §10's naming rule are rules here and are not machine-checked.

None of it says the document is any good. What a validator cannot read is exactly where the
judgement is:

- Whether `## Context` states a problem or announces a subject.
- Whether the alternatives were live options or filler written to fill the heading.
- Whether the cost named is the real cost or the cheapest one that could be admitted to. A
  heading called `What this costs` with "none, this is strictly better" under it passes every
  check there is and is almost always false.
- Whether this should have been a design page at all (§9).
- Whether a sentence in a spec is a rule or an opinion in the indicative mood.
- Whether a page that gathers a lot of links earned them.

The mechanical half is automated so that review attention goes to the other half. **A document
that passes `docket check` is not a good document; it is a document with nothing obviously
missing.**

## 13. Changing this document

This file arrived with the template and it is yours. A regime that cannot change gets worked
around, and being worked around is worse than being wrong, because nothing records that it
happened.

**A conflict between a rule here and what a document actually needs goes into a task, not into a
quiet exception.** Write the document the way the rule says, note where it fought you, and open a
task with the case. An exception nobody wrote down is indistinguishable from a mistake, and after
the second one nobody reads this file.

**When a rule is tightened, the documents already in this vault are brought into line in the same
commit.** A rule the vault itself violates is a rule nobody believes: the next author reads the
rule, opens three files that break it, and concludes — correctly — that this page is aspirational.
Where the migration is genuinely too large for one commit, the rule still lands, the exception is
written into this file where a reader will hit it, and the migration is a task with a number.

**Adding a value to `type` is the change to think hardest about.** Five kinds cover a knowledge
base, and a sixth is a claim that a document exists which is none of these — not a choice, not a
mechanism, not a rule, not a fortnight, and not a page. That claim is usually wrong, and the cost
of being wrong is a kind that half the vault does not use and every reader has to learn.

Changing what a document must contain is itself a decision, and gets a numbered file in
`docs/decisions/`. Clarifying what a section is for, adding an example, or fixing a rule that
turned out to be ambiguous is an ordinary edit to this page.
