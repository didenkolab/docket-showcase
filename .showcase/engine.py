"""Replays a story into a vault: one event, one docket command, one commit with its own date."""
from __future__ import annotations
import dataclasses as dc
import datetime as dt
import os
import pathlib
import subprocess
import vault

CORE_RELATIONS = {"blocks", "blocked_by", "duplicates", "duplicated_by", "causes", "caused_by", "relates"}


def declared_relations(root) -> set[str]:
    """Every relation alias the vault's docket.yaml declares, plus the seven core relations it
    never bothers to (the vault format assumes them). Parsed with a small stdlib line scanner
    rather than PyYAML, since all we need is the `name:`/`inverse:` values inside the top-level
    `relations:` block."""
    names = set(CORE_RELATIONS)
    path = pathlib.Path(root) / "docket.yaml"
    if not path.exists():
        return names
    lines = path.read_text().splitlines()
    in_block = False
    for line in lines:
        if line.startswith("relations:"):
            in_block = True
            continue
        if in_block:
            if line.strip() == "" or line.startswith(" ") or line.startswith("\t"):
                stripped = line.strip().lstrip("-").strip()
                if stripped.startswith("name:"):
                    names.add(stripped.split(":", 1)[1].strip())
                elif stripped.startswith("inverse:"):
                    names.add(stripped.split(":", 1)[1].strip())
                continue
            break
    return names


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


class _Ref:
    """One {alias} in a commit message, still being spelled out.

    str.format_map splits a field name on its dots and asks the mapping only for the first
    part, then takes attributes off whatever comes back. Aliases are dotted — a story is
    `harbor.payments.refunds` — so what comes back has to survive `.payments.refunds` and
    resolve to the key it stands for only at the end, when it is formatted."""
    __slots__ = ("engine", "alias")

    def __init__(self, engine, alias):
        self.engine = engine
        self.alias = alias

    def __getattr__(self, part):
        return _Ref(self.engine, "%s.%s" % (self.alias, part))

    def __format__(self, spec):
        return format(self.engine.keys.get(self.alias, self.alias), spec)

    def __str__(self):
        return self.__format__("")


class _KeyMap(dict):
    """Formats {alias} placeholders in a commit message against the engine's assigned keys,
    leaving an unknown alias as-is rather than raising."""
    def __init__(self, engine):
        self.engine = engine

    def __missing__(self, alias):
        return _Ref(self.engine, alias)


class Engine:
    def __init__(self, root, docket="docket", dry=False):
        self.root = pathlib.Path(root)
        self.docket = docket
        self.dry = dry
        self.keys: dict[str, str] = {}
        self.relations = declared_relations(self.root)

    # -- plumbing ---------------------------------------------------------
    def run(self, *args):
        # `docket new` takes its title as the sole positional argument (a
        # directory is only accepted via -C); every other subcommand takes
        # the vault directory as a trailing positional. Appending "." to
        # `new` would read as a second title and be rejected.
        tail = () if args and args[0] == "new" else (".",)
        out = subprocess.run([self.docket, *args, *tail], cwd=self.root, capture_output=True, text=True)
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
        self.git("add", "-A", "--", ".", ":!.showcase", ":!.superpowers")
        if not self.git("status", "--porcelain").strip():
            return
        when = event.when.replace(tzinfo=dt.timezone.utc).isoformat()
        message = event.message.format_map(_KeyMap(self))
        self.git("commit", "-q", "-m", message, "--author", f"{event.who.name} <{event.who.email}>",
                 env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when,
                      "GIT_COMMITTER_NAME": event.who.name, "GIT_COMMITTER_EMAIL": event.who.email})

    def apply(self, event):
        touched = getattr(self, "on_" + event.kind)(event) or []
        for alias in list(event.args.get("touch", [])) + list(touched):
            vault.stamp(self.path(alias), event.when)
        self.commit(event)

    def replay(self, events):
        for event in sorted(events, key=lambda e: e.when):
            self.apply(event)

    # -- handlers -----------------------------------------------------------
    def on_new(self, event):
        a = event.args
        cmd = ["new", "--type", a.get("type", "task"), "--project", a["project"]]
        for flag in ("assignee", "priority", "labels", "status"):
            if a.get(flag):
                cmd += ["--" + flag, a[flag]]
        if a.get("parent"):
            cmd += ["--parent", self.key(a["parent"])]
        cmd += [a["title"]]
        line = self.run(*cmd)
        key = line.split()[0]
        self.keys[a["alias"]] = key
        path = vault.task_path(self.root, key)
        if a.get("body"):
            vault.set_body(path, a["body"])
        vault.stamp(path, event.when, created=True)
        return []

    def on_set(self, event):
        a = dict(event.args)
        task = a.pop("task")
        a.pop("touch", None)
        pairs = []
        for name, value in a.items():
            if name in self.relations:
                value = ",".join(self.key(v) for v in (value if isinstance(value, list) else [value]))
            pairs.append(f"{name}={value}")
        self.run("set", self.key(task), *pairs, "--quiet")
        return [task]

    def on_comment(self, event):
        vault.append_comment(self.path(event.args["task"]), event.who.handle, event.when, event.args["text"])
        return [event.args["task"]]

    def on_page(self, event):
        a = event.args
        body = a["body"].format_map(_KeyMap(self)) if a.get("keys") else a["body"]
        vault.write_page(self.root / a["path"], a["title"], a["kind"], event.when.date(), body, **a.get("extra", {}))
        return []

    def on_person(self, event):
        a = event.args
        vault.write_person(self.root / "people" / f"{a['handle']}.md", a["handle"], a["name"])
        return []

    def on_raw(self, event):
        return event.args["fn"](self, event) or []
