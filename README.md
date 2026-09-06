# Harbor

An [docket](https://github.com/vadymdidenkolab/docket) vault: a task board and a knowledge base
kept as Markdown files in git.

Clone it, open the folder in Obsidian, and you get a board, a backlog and a wiki. There is
nothing to install and nothing to run — tasks and pages are plain Markdown with YAML
frontmatter, and git is the history.

| Path | What |
|---|---|
| `docket.yaml` | The projects this vault holds and the vocabulary they share |
| `HARBOR/` | One folder per project. `HARBOR-12 Its title.md` is the task `HARBOR-12` |
| `docs/` | Knowledge base — pages, decisions, specs and sprints. `docs/spec/documents.md` says what each one is |
| `boards/` | Obsidian Bases views: board, backlog, my tasks |
| `templates/` | Templates for a new task and a new page |
| `AGENTS.md` | How an agent works in this vault |

A key is `HARBOR-12`, and the file is named after the task, so the graph and the file
explorer say what each note is. Link to one by its whole name: `[[HARBOR-12 Its title]]`.

The format is specified in
[docket-board](https://github.com/vadymdidenkolab/docket-board/blob/main/docs/spec/vault-format.md).
