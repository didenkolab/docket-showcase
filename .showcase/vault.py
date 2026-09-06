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


# What a frontmatter value has to be quoted to survive as itself. A title with a colon
# in it — "Offline first: the phone is the source of truth" — is unquoted YAML for a
# mapping inside a mapping, and every reader of the vault rejects the file. docket quotes
# a task's title for this reason; a page's is written here, so it is quoted here.
_NEEDS_QUOTES = "-?:,[]{}#&*!|>'\"%@`"


def scalar(value) -> str:
    """A frontmatter value as YAML, quoted only when leaving it bare would change it."""
    text = str(value)
    if not text:
        return "''"
    if text[0] in _NEEDS_QUOTES or text[0] == " " or text[-1] in " :" or ": " in text or " #" in text:
        return "'%s'" % text.replace("'", "''")
    return text


def write_page(path, title, kind, updated, body, **extra):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = [f"title: {scalar(title)}", f"type: {kind}", f"updated: {updated.isoformat()}"]
    fm += [f"{k}: {scalar(v)}" for k, v in extra.items()]
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
