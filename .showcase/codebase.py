"""The `northlight` code repository, written on the same timeline as the vault.

The vault says a team booked berths, imported bank statements and lost an afternoon's
work off a phone. This module writes the code that team would have had to write, into a
git repository beside the vault, with the same six people committing at the same hours of
the same twelve weeks. It exists so the vault's coverage links point at real files and its
executions run real scenarios: a task key in a commit subject is only worth something if
the commit is there.

    events(code_root) -> list[engine.Event]

Every event is of kind `raw`. The engine's own `commit` is for the vault; each event here
writes files into `code_root` and commits them there itself, with the author, the
committer and both dates taken from the event, so two replays of the same story produce
the same SHAs.

**How a file at a date is worked out.** Nothing here stores a whole file per commit. A
file is a list of named blocks, each with the moment it was written:

    _b("harbor/booking.py", "overlaps", "06-15 11:20", "def overlaps(...): ...")
    _b("harbor/booking.py", "overlaps", "06-18 09:45", "def overlaps(...): ...")

The file as of a moment is every block whose name has a version by then, newest version
of each, in the order the names were first declared. A second block under the same name
is a rewrite and keeps the first one's place in the file; a new name is an addition. So
the history is written the way it happened -- this function grew, that one was replaced --
and a commit's `git add` picks up exactly the paths that have a block stamped with its
own minute. A commit with no block at its minute is a mistake, and so is one whose files
come out byte-for-byte the same as the commit before: both refuse at build time.

**Subjects.** A subject is `"{alias}: what was done"`, and the alias is resolved through
the vault engine's `_KeyMap` at replay time, when the task it names has a key. An alias
the engine has not created yet would be left as a literal `{harbor.booking.week}` in the
code history, which is worse than a crash, so `events()` checks every alias against the
products' own specs before anything is written, and the commit itself refuses again if
the key is missing at the moment it runs.

**What is true of the code.** The modules are real: pure functions over dicts and frozen
dataclasses, no I/O, no clock. The scenarios are real behave scenarios whose steps import
those modules and assert on what comes back. Two of them fail at HEAD, on purpose, and
they are the two the vault has open bugs for.
"""
from __future__ import annotations

import datetime as dt
import os
import pathlib
import shutil
import string
import subprocess

import engine
from products.common import office_hours, when
from story import PEOPLE

KEEP = {".venv", "reports"}          # never removed when the repository is re-initialised
SEPARATORS = {".py": "\n\n\n", ".feature": "\n\n", ".md": "\n\n", ".toml": "\n\n"}

BLOCKS: dict[str, list[tuple[str, dt.datetime, str]]] = {}


def _b(path: str, name: str, moment: str, text: str) -> None:
    """One named piece of one file, as it was written at one minute of the story."""
    BLOCKS.setdefault(path, []).append((name, when(moment), text.strip("\n")))


# ======================================================================================
# The repository's own furniture
# ======================================================================================

_b("README.md", "head", "06-15 09:05", """
# Northlight

Harbor, Ledgerline and Fieldnote: three small products belonging to a company that does
not exist. This repository is the code; the vault beside it is the same team's issue
tracker.
""")

_b("README.md", "invented", "06-26 10:40", """
## None of this is real

Northlight is invented. The company, the three products, the six people in the commit
log, the marinas, the accountants and the field crews are all made up for a demonstration
of an issue tracker that keeps its issues in Markdown. Nothing here has ever charged a
card or imported a bank statement, and no real company, product or person is meant by any
name in it.
""")

_b("README.md", "quickstart", "09-03 10:00", """
## Quick start

    git clone https://github.com/vadymdidenkolab/northlight.git
    cd northlight
    python3 -m venv .venv && .venv/bin/pip install behave
    .venv/bin/behave features

Sixty scenarios run, and two of them fail on purpose:

  * `HARBOR-PAY-004`, *A refund larger than the invoice it credits is refused* — it is
    not refused. Twenty-five thousand cents go back against a charge of eighteen.
  * *A job finished offline keeps its photographs* — it comes back one photograph short.
    Nobody tagged that scenario, so it is known by the id derived from its own name,
    `FIELD-GEN-04E49B`.

Both are bugs, and both are written up in the vault next door. Everything else passes.
""")

_b("README.md", "requirements", "09-03 10:00", """
## Requirements

| | |
|---|---|
| Python 3.11 or newer | `pyproject.toml` asks for it, and nothing here needs anything newer |
| behave | The one dependency, and only for the scenarios. The three packages import nothing but the standard library |
""")

_b("README.md", "install", "09-03 10:00", """
## Install

Nothing to install. Clone the repository and the packages are importable from the
checkout; the virtualenv above exists for `behave` and for nothing else.
""")

_b("README.md", "usage", "09-03 10:00", """
## Usage

One product's suite at a time:

    .venv/bin/behave features/harbor

The Cucumber JSON the vault imports, which is how a run gets onto the board:

    .venv/bin/behave features/harbor -q --no-summary -f json -o reports/harbor.json

One feature file, the way the board's own button runs it — the second argument says
where to leave the JUnit XML:

    ./run-tests features/harbor/booking.feature reports/junit.xml
""")

_b("README.md", "configuration", "09-03 10:00", """
## Configuration

None. No environment variable and no file outside this checkout changes what the
scenarios do; the virtualenv is the whole of the setup.
""")

_b("README.md", "how", "06-26 10:40", """
## What is in here

    harbor/       berths, what a stay costs, and taking the money for it
    ledgerline/   invoice numbers, bank statements and tax periods
    fieldnote/    a crew's day, the order they drive it in, and a phone with no signal
    features/     the same three, as behave scenarios

Every module is pure: a function is handed the state it needs and gives back a new one.
Nothing here opens a socket, reads a file it was not given, or asks what time it is.
""")

_b("README.md", "how", "09-03 10:00", """
## How it works

    harbor/       berths, what a stay costs, and taking the money for it
    ledgerline/   invoice numbers, bank statements and tax periods
    fieldnote/    a crew's day, the order they drive it in, and a phone with no signal
    features/     the same three, as behave scenarios, three files per product

Every module is pure: a function is handed the state it needs and gives back a new one.
Nothing here opens a socket, reads a file it was not given, or asks what time it is,
which is why a suite can be run against a checkout from three months ago and mean
something.

Some scenarios carry a case id — `@HARBOR-PAY-004` — and some carry nothing. A tagged one
keeps its identity when somebody rewords it. An untagged one is identified by its feature
file's name and its own, hashed into `FIELD-GEN-04E49B` and the like. Both kinds are
imported; an untagged scenario is not second class.

Results reach the board from the vault, not from here. Somebody runs a suite and hands
the JSON to `hooks/import-cucumber.sh` in `docket-showcase`, which writes one execution
and one run per scenario, each attached to its test by that same id. Those ids and the
task key every commit message here opens with are the only things joining the two
repositories — the key is how the vault blames a scenario's lines back to a ticket.
""")

_b("README.md", "where", "09-03 10:00", """
## Where things are

  * [docket-showcase](https://github.com/vadymdidenkolab/docket-showcase) — the vault: the
    same team's board, backlog, wiki, and the test results these scenarios produce.
  * [docket](https://github.com/vadymdidenkolab/docket) — the tracker the vault is kept in.
""")

_b("README.md", "contributing", "09-03 10:00", """
## Contributing

Put a scenario in the feature file for the area it belongs to. Tag it with a case id if
it settles a case somebody wrote down, and leave it untagged if it does not.

Do not rename a feature file, and do not rename a scenario that has runs against it. An
untagged scenario's id is derived from those two names, so a rename starts a new test and
leaves the old one holding the history. Once a scenario is tagged, reword it freely.

There is no other test suite. Run it before you push:

    .venv/bin/behave features
""")

_b("README.md", "license", "06-15 09:05", """
## License

MIT. See [LICENSE](LICENSE).
""")

_b("LICENSE", "mit", "06-15 09:05", """
MIT License

Copyright (c) 2026 Vadym Didenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

_b("pyproject.toml", "project", "06-15 09:05", """
[project]
name = "northlight"
version = "0.1.0"
description = "Harbor, Ledgerline and Fieldnote - the code behind an invented company's vault."
requires-python = ">=3.11"
""")

_b("pyproject.toml", "project", "09-04 09:30", """
[project]
name = "northlight"
version = "0.1.0"
description = "Harbor, Ledgerline and Fieldnote - the code behind an invented company's vault."
requires-python = ">=3.11"

[project.optional-dependencies]
test = ["behave>=1.2.6"]
""")

_b("pyproject.toml", "packages", "06-15 09:05", """
[tool.setuptools]
packages = ["harbor", "ledgerline", "fieldnote"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
""")

_b(".gitignore", "all", "06-15 09:05", """
.venv/
__pycache__/
reports/
""")

_b("run-tests", "all", "06-25 14:00", """
#!/bin/sh
set -eu
exec "$(dirname "$0")/.venv/bin/behave" "$1" --junit --junit-directory reports --no-summary -q
""")

_b("run-tests", "all", "08-21 14:00", """
#!/bin/sh
set -eu
exec "$(dirname "$0")/.venv/bin/behave" "$1" --junit --junit-directory "$(dirname "$2")" --no-summary -q
""")


# ======================================================================================
# harbor/ -- berths, what a stay costs, and taking the money for it
# ======================================================================================

_b("harbor/__init__.py", "head", "06-15 11:20", '''
"""Harbor: a marina's berths, the boats in them and the money for the nights."""
''')

_b("harbor/booking.py", "head", "06-15 11:20", '''
"""Berths, and which boat has one for which nights.

Every function is handed the calendar it should look at and gives back a new one; nothing
here edits what it was passed. A calendar is a plain list of Booking, oldest first, and a
stay runs from the first night to the morning the boat leaves -- so the day in `end` is
somebody else's night, not this boat's.
"""
from __future__ import annotations

import dataclasses as dc
import datetime as dt
''')

_b("harbor/booking.py", "Booking", "06-15 11:20", '''
@dc.dataclass(frozen=True)
class Booking:
    """A boat, a berth, and the nights between two dates."""

    ref: str
    berth: str
    boat: str
    start: dt.date
    end: dt.date
    status: str = "confirmed"
''')

_b("harbor/booking.py", "nights", "06-15 11:20", '''
def nights(start: dt.date, end: dt.date) -> int:
    """How many nights a boat is charged for. Arriving and leaving on the same day is
    nought nights, not one day."""
    return (end - start).days
''')

_b("harbor/booking.py", "overlaps", "06-15 11:20", '''
def overlaps(taken: "Booking", start: dt.date, end: dt.date) -> bool:
    """True when a stay from start to end wants a night the booking already has."""
    return taken.start <= end and start <= taken.end
''')

_b("harbor/booking.py", "overlaps", "06-18 09:45", '''
def overlaps(taken: "Booking", start: dt.date, end: dt.date) -> bool:
    """True when a stay from start to end wants a night the booking already has.

    Both ranges end on the morning the boat leaves, and that morning is not a night, so
    a stay beginning on the day another one ends is not a clash. Comparing the dates as
    if they were inclusive kept a berth off the market for a night nobody was in it.
    """
    return taken.start < end and start < taken.end
''')

_b("harbor/booking.py", "reserve", "06-15 11:20", '''
def reserve(calendar: list, booking: "Booking") -> dict:
    """Put a booking on the calendar, or say which booking is in the way."""
    if nights(booking.start, booking.end) < 1:
        return {"ok": False, "reason": "a stay is at least one night", "calendar": calendar}
    for taken in calendar:
        if taken.berth == booking.berth and overlaps(taken, booking.start, booking.end):
            return {"ok": False, "reason": "berth taken", "clash": taken.ref, "calendar": calendar}
    return {"ok": True, "booking": booking, "calendar": calendar + [booking]}
''')

_b("harbor/booking.py", "free_berths", "06-17 10:30", '''
def free_berths(calendar: list, berths, start: dt.date, end: dt.date) -> list:
    """The berths with nothing in them for the whole of a stay."""
    taken = {b.berth for b in calendar if overlaps(b, start, end)}
    return [berth for berth in berths if berth not in taken]
''')

_b("harbor/booking.py", "free_berths", "07-03 09:40", '''
def free_berths(calendar: list, berths, start: dt.date, end: dt.date) -> list:
    """The berths with nothing in them for the whole of a stay, in berth order.

    The harbour office reads this list down a screen and off a printout, so the order is
    the marina's own and not whatever order the berths happened to be loaded in.
    """
    taken = {b.berth for b in calendar if overlaps(b, start, end)}
    return sorted(berth for berth in berths if berth not in taken)
''')

_b("harbor/booking.py", "berths_from_rows", "06-19 15:10", '''
def berths_from_rows(rows) -> list:
    """The marina's own spreadsheet, as berths.

    Their file writes lengths with a comma for a decimal point and keeps shore power in
    a column called `note2`, which is a column name and not a mistake: an empty cell
    means the berth has no power on it.
    """
    berths = []
    for row in rows:
        berths.append({
            "berth": row["berth"].strip(),
            "metres": float(row["length"].strip().replace(",", ".")),
            "power": bool(row.get("note2", "").strip()),
        })
    return berths
''')

_b("harbor/booking.py", "Hold", "06-29 09:55", '''
@dc.dataclass(frozen=True)
class Hold:
    """A berth kept back for a guest who is typing a card number."""

    ref: str
    berth: str
    start: dt.date
    end: dt.date
    until: dt.datetime
''')

_b("harbor/booking.py", "hold", "06-29 09:55", '''
def hold(calendar: list, holds: list, hold_ref: str, berth: str, start: dt.date,
         end: dt.date, at: dt.datetime, minutes: int = 20) -> dict:
    """Keep a berth for twenty minutes while the guest pays for it.

    A hold that has run out is not a hold, so the ones that expired before `at` are
    dropped rather than swept up later by something that has to be remembered.
    """
    live = [h for h in holds if h.until > at]
    for taken in calendar:
        if taken.berth == berth and overlaps(taken, start, end):
            return {"ok": False, "reason": "berth taken", "clash": taken.ref, "holds": live}
    kept = Hold(hold_ref, berth, start, end, at + dt.timedelta(minutes=minutes))
    return {"ok": True, "hold": kept, "holds": live + [kept]}
''')

_b("harbor/booking.py", "hold", "07-02 15:30", '''
def hold(calendar: list, holds: list, hold_ref: str, berth: str, start: dt.date,
         end: dt.date, at: dt.datetime, minutes: int = 20) -> dict:
    """Keep a berth for twenty minutes while the guest pays for it.

    A hold that has run out is not a hold, so the ones that expired before `at` are
    dropped rather than swept up later by something that has to be remembered.

    A berth somebody else is holding is as unavailable as a berth somebody else has
    booked. Looking only at the calendar meant two guests who clicked within the same
    minute were both told to go and pay, and one of them was going to be turned away at
    the pontoon.
    """
    live = [h for h in holds if h.until > at]
    for taken in calendar:
        if taken.berth == berth and overlaps(taken, start, end):
            return {"ok": False, "reason": "berth taken", "clash": taken.ref, "holds": live}
    for other in live:
        if other.berth == berth and other.start < end and start < other.end:
            return {"ok": False, "reason": "berth held", "clash": other.ref, "holds": live}
    kept = Hold(hold_ref, berth, start, end, at + dt.timedelta(minutes=minutes))
    return {"ok": True, "hold": kept, "holds": live + [kept]}
''')

_b("harbor/booking.py", "cancel", "07-01 11:05", '''
def cancel(calendar: list, ref: str) -> dict:
    """Take a booking off the calendar. Cancelling twice is not cancelling twice as
    hard; the second time is a refusal, because somebody may have taken the nights."""
    kept = [b for b in calendar if b.ref != ref]
    if len(kept) == len(calendar):
        return {"ok": False, "reason": "no such booking", "calendar": calendar}
    return {"ok": True, "calendar": kept}
''')

_b("harbor/booking.py", "cancel", "08-06 11:00", '''
def cancel(calendar: list, ref: str) -> dict:
    """Take a booking off the calendar and say which nights it gave back.

    Cancelling twice is not cancelling twice as hard; the second time is a refusal,
    because by then somebody may have taken the nights.
    """
    gone = next((b for b in calendar if b.ref == ref), None)
    if gone is None:
        return {"ok": False, "reason": "no such booking", "calendar": calendar}
    return {"ok": True, "calendar": [b for b in calendar if b.ref != ref],
            "freed": {"berth": gone.berth, "start": gone.start, "end": gone.end}}
''')


_b("harbor/invoice.py", "head", "06-18 14:20", '''
"""What a stay costs, and the invoice that says so.

Money is in whole cents, everywhere, because a marina that prices a season in fractions
of a cent is a marina with a rounding argument to have with an accountant.
"""
from __future__ import annotations

import dataclasses as dc
import datetime as dt

from harbor import booking as booking_module
''')

_b("harbor/invoice.py", "Line", "06-18 14:20", '''
@dc.dataclass(frozen=True)
class Line:
    """One line of an invoice: what it is for, how many, and what one costs."""

    description: str
    quantity: int
    unit_cents: int
''')

_b("harbor/invoice.py", "Invoice", "06-18 14:20", '''
@dc.dataclass(frozen=True)
class Invoice:
    """An invoice as the guest gets it."""

    number: str
    booking_ref: str
    lines: tuple
    issued: dt.date
    currency: str = "EUR"
''')

_b("harbor/invoice.py", "line_cents", "06-18 14:20", '''
def line_cents(line: "Line") -> int:
    return line.quantity * line.unit_cents
''')

_b("harbor/invoice.py", "total_cents", "06-18 14:20", '''
def total_cents(invoice: "Invoice") -> int:
    return sum(line_cents(line) for line in invoice.lines)
''')

_b("harbor/invoice.py", "invoice_for", "06-18 14:20", '''
def invoice_for(booking, night_cents: int, number: str, issued: dt.date) -> "Invoice":
    """One line, for the nights the boat is here."""
    stayed = booking_module.nights(booking.start, booking.end)
    line = Line("Berth %s, %d nights" % (booking.berth, stayed), stayed, night_cents)
    return Invoice(number, booking.ref, (line,), issued)
''')

_b("harbor/invoice.py", "rate_on", "06-19 11:00", '''
def rate_on(rates, day: dt.date) -> int:
    """The rate the marina was charging on that day.

    `rates` is a list of (from_date, cents) in any order, and the newest one that had
    already started on `day` is the one that applies. A price change in August is not
    allowed to reprice a booking made in June, which is what happens if the invoice
    reaches for whatever the current rate happens to be.
    """
    applicable = [(start, cents) for start, cents in rates if start <= day]
    if not applicable:
        raise ValueError("no rate applies on %s" % day)
    return max(applicable)[1]
''')

_b("harbor/invoice.py", "invoice_for", "06-19 11:00", '''
def invoice_for(booking, rates, number: str, issued: dt.date) -> "Invoice":
    """One line, for the nights the boat is here, at the rate on the day it was booked."""
    stayed = booking_module.nights(booking.start, booking.end)
    night_cents = rate_on(rates, booking.start)
    line = Line("Berth %s, %d nights" % (booking.berth, stayed), stayed, night_cents)
    return Invoice(number, booking.ref, (line,), issued)
''')

_b("harbor/invoice.py", "SEASON_NIGHTS", "08-20 10:40", '''
SEASON_NIGHTS = 28          # from here up, a stay is a season and is priced by the month
MONTH_NIGHTS = 30
''')

_b("harbor/invoice.py", "invoice_for", "08-20 10:40", '''
def invoice_for(booking, rates, number: str, issued: dt.date, month_rates=()) -> "Invoice":
    """The nights the boat is here, at the rates that applied on the day it was booked.

    A stay of four weeks or more is a season, and a season is sold by the month: the
    marina's month rate is cheaper than thirty nights of the nightly one, which is the
    whole point of taking a season berth. Whatever is left over after the whole months
    is charged by the night.
    """
    stayed = booking_module.nights(booking.start, booking.end)
    night_cents = rate_on(rates, booking.start)
    if stayed >= SEASON_NIGHTS and month_rates:
        months, rest = divmod(stayed, MONTH_NIGHTS)
        lines = [Line("Berth %s, %d months" % (booking.berth, months), months,
                      rate_on(month_rates, booking.start))]
        if rest:
            lines.append(Line("Berth %s, %d nights" % (booking.berth, rest), rest, night_cents))
        return Invoice(number, booking.ref, tuple(lines), issued)
    line = Line("Berth %s, %d nights" % (booking.berth, stayed), stayed, night_cents)
    return Invoice(number, booking.ref, (line,), issued)
''')


_b("harbor/payments.py", "head", "06-30 10:30", '''
"""Charging a card for a booking, and giving the money back.

The ledger is a list of Charge, oldest first, and a refund is a charge with a negative
amount rather than a second kind of thing: whatever is in the list for a booking always
adds up to what the guest is really out of pocket.
"""
from __future__ import annotations

import dataclasses as dc
''')

_b("harbor/payments.py", "Charge", "06-30 10:30", '''
@dc.dataclass(frozen=True)
class Charge:
    """One movement of money for one booking."""

    reference: str
    booking_ref: str
    amount_cents: int
''')

_b("harbor/payments.py", "Charge", "07-02 10:45", '''
@dc.dataclass(frozen=True)
class Charge:
    """One movement of money for one booking.

    `intent` is what the confirmation said it was for. Two confirmations of the same
    booking by the same guest carry the same intention, however many times the button
    was pressed, and that is what tells a retry apart from a second stay.
    """

    reference: str
    booking_ref: str
    amount_cents: int
    intent: str = ""
''')

_b("harbor/payments.py", "capture", "06-30 10:30", '''
def capture(ledger: list, booking_ref: str, amount_cents: int, reference: str) -> dict:
    """Charge the card when the booking is confirmed."""
    if amount_cents <= 0:
        return {"ok": False, "reason": "nothing to charge", "ledger": ledger}
    charge = Charge(reference, booking_ref, amount_cents)
    return {"ok": True, "charge": charge, "ledger": ledger + [charge]}
''')

_b("harbor/payments.py", "capture", "07-02 10:45", '''
def capture(ledger: list, booking_ref: str, amount_cents: int, reference: str,
            intent: str) -> dict:
    """Charge the card when the booking is confirmed.

    The confirmation carries an intention, so a guest who presses the button again gets
    back the charge that was already taken rather than a second one.
    """
    if amount_cents <= 0:
        return {"ok": False, "reason": "nothing to charge", "ledger": ledger}
    last = ledger[-1] if ledger else None
    if last is not None and last.booking_ref == booking_ref and last.intent == intent:
        return {"ok": True, "charge": last, "repeat": True, "ledger": ledger}
    charge = Charge(reference, booking_ref, amount_cents, intent)
    return {"ok": True, "charge": charge, "repeat": False, "ledger": ledger + [charge]}
''')

_b("harbor/payments.py", "capture", "07-10 09:20", '''
def capture(ledger: list, booking_ref: str, amount_cents: int, reference: str,
            intent: str) -> dict:
    """Charge the card when the booking is confirmed.

    The confirmation carries an intention, so a guest who presses the button again gets
    back the charge that was already taken rather than a second one.

    The whole ledger is looked at, not the end of it. Checking only the last charge
    worked in a demonstration and did not work on a Wednesday afternoon: another
    marina's confirmation landing between a guest's two tries made the retry look new,
    and three guests were charged twice for one booking each.
    """
    if amount_cents <= 0:
        return {"ok": False, "reason": "nothing to charge", "ledger": ledger}
    for taken in ledger:
        if taken.booking_ref == booking_ref and taken.intent == intent:
            return {"ok": True, "charge": taken, "repeat": True, "ledger": ledger}
    charge = Charge(reference, booking_ref, amount_cents, intent)
    return {"ok": True, "charge": charge, "repeat": False, "ledger": ledger + [charge]}
''')

_b("harbor/payments.py", "charged_cents", "06-30 10:30", '''
def charged_cents(ledger: list, booking_ref: str) -> int:
    """What the guest is out of pocket for a booking, refunds included."""
    return sum(c.amount_cents for c in ledger if c.booking_ref == booking_ref)
''')

_b("harbor/payments.py", "charges_for", "06-30 10:30", '''
def charges_for(ledger: list, booking_ref: str) -> list:
    """Every movement of money for a booking, oldest first."""
    return [c for c in ledger if c.booking_ref == booking_ref]
''')

_b("harbor/payments.py", "start", "06-30 14:15", '''
def start(pending: dict, booking_ref: str, token: str) -> dict:
    """The guest leaves for the bank's own page. `token` is what will come back."""
    return {"ok": True, "pending": {**pending, token: booking_ref}}
''')

_b("harbor/payments.py", "resume", "06-30 14:15", '''
def resume(pending: dict, token: str) -> dict:
    """Hand the guest back to the booking they went away to pay for.

    The bank's page returns them to us with nothing but the token, and a guest who comes
    back to the wrong booking -- or to a list -- has to work out for themselves whether
    they paid.
    """
    if token not in pending:
        return {"ok": False, "reason": "unknown token"}
    return {"ok": True, "booking_ref": pending[token]}
''')

_b("harbor/payments.py", "split_deposit", "08-19 10:00", '''
def split_deposit(total_cents: int, percent: int) -> dict:
    """What is taken now and what is left to pay on arrival.

    The remainder is the total minus the deposit rather than its own percentage, so the
    two halves always add back up to the price the guest was quoted.
    """
    if not 0 < percent < 100:
        return {"ok": False, "reason": "a deposit is part of the price, not all of it"}
    now = total_cents * percent // 100
    return {"ok": True, "now_cents": now, "on_arrival_cents": total_cents - now}
''')

_b("harbor/payments.py", "refund", "08-25 14:30", '''
def refund(ledger: list, booking_ref: str, amount_cents: int, reference: str) -> dict:
    """Give money back to the card it came from.

    A refund goes into the same ledger as a negative charge, so `charged_cents` stays
    the one answer to what the guest paid.
    """
    if amount_cents <= 0:
        return {"ok": False, "reason": "a refund is a positive amount", "ledger": ledger}
    charge = Charge(reference, booking_ref, -amount_cents, "")
    return {"ok": True, "charge": charge, "ledger": ledger + [charge]}
''')


_b("harbor/checkin.py", "head", "07-28 15:20", '''
"""Checking a guest in from the pontoon, which is where the signal is not.

Nothing here talks to a server. A check-in made on the pontoon is put on a queue, and the
queue is handed to `flush` by whatever finds itself with a connection.
"""
from __future__ import annotations

import dataclasses as dc
import datetime as dt
''')

_b("harbor/checkin.py", "CheckIn", "07-28 15:20", '''
@dc.dataclass(frozen=True)
class CheckIn:
    """A guest, on their boat, at a moment the phone believed in."""

    booking_ref: str
    at: dt.datetime
    by: str
    source: str = "pontoon"
''')

_b("harbor/checkin.py", "CheckIn", "09-02 14:20", '''
@dc.dataclass(frozen=True)
class CheckIn:
    """A guest, on their boat, at a moment the phone believed in."""

    booking_ref: str
    at: dt.datetime
    by: str
    source: str = "pontoon"
    papers: tuple = ()
''')

_b("harbor/checkin.py", "queue", "07-28 15:20", '''
def queue(pending: list, entry: "CheckIn") -> list:
    """Keep a check-in on the phone until there is something to send it to."""
    return pending + [entry]
''')

_b("harbor/checkin.py", "flush", "07-28 15:20", '''
def flush(pending: list, arrived) -> dict:
    """Send the queue. A guest the office already has is not checked in twice."""
    seen = list(arrived)
    applied = []
    for entry in pending:
        if entry.booking_ref in seen:
            continue
        seen.append(entry.booking_ref)
        applied.append(entry)
    return {"ok": True, "applied": applied, "arrived": seen, "pending": []}
''')

_b("harbor/checkin.py", "flush", "07-29 11:10", '''
def flush(pending: list, arrived) -> dict:
    """Send the queue, oldest first. A guest the office already has is not checked in
    twice.

    The order matters because the office reads the arrivals as a list of what happened,
    and a phone that has been dark since breakfast has a morning's worth of them. Sending
    them in the order the phone happened to hold them put half past nine after half past
    four.
    """
    seen = list(arrived)
    applied = []
    for entry in sorted(pending, key=lambda e: (e.at, e.booking_ref)):
        if entry.booking_ref in seen:
            continue
        seen.append(entry.booking_ref)
        applied.append(entry)
    return {"ok": True, "applied": applied, "arrived": seen, "pending": []}
''')

_b("harbor/checkin.py", "booking_for_code", "08-11 11:00", '''
def booking_for_code(calendar: list, codes: dict, code: str, night: dt.date) -> dict:
    """The code painted on the pontoon, and whose booking is on that berth tonight.

    The crew scan it standing next to the boat, so the answer has to be the one booking
    rather than a search screen with the right one somewhere in it.
    """
    berth = codes.get(code)
    if berth is None:
        return {"ok": False, "reason": "unknown code"}
    for taken in calendar:
        if taken.berth == berth and taken.start <= night < taken.end:
            return {"ok": True, "booking_ref": taken.ref, "berth": berth}
    return {"ok": False, "reason": "nothing booked on %s" % berth, "berth": berth}
''')

_b("harbor/checkin.py", "correct", "08-13 14:50", '''
def correct(entry: "CheckIn", phone_now: dt.datetime, server_now: dt.datetime) -> "CheckIn":
    """Move a check-in onto the server's clock, keeping the phone's order.

    A phone that has been off all winter comes back believing it is March. What it is
    right about is the order things happened in and how far apart they were, so the whole
    queue is shifted by one difference rather than each entry being stamped with the
    moment it happened to arrive.
    """
    return dc.replace(entry, at=entry.at + (server_now - phone_now))
''')

_b("harbor/checkin.py", "with_papers", "09-02 14:20", '''
def with_papers(entry: "CheckIn", papers) -> "CheckIn":
    """The boat's papers, photographed at the pontoon.

    Crews photograph the same page twice when the first one looks blurred on a screen in
    the sun, so the same page named twice is one page and the order they were taken in
    is kept.
    """
    kept = tuple(dict.fromkeys(tuple(entry.papers) + tuple(papers)))
    return dc.replace(entry, papers=kept)
''')


# ======================================================================================
# ledgerline/ -- invoice numbers, bank statements and tax periods
# ======================================================================================

_b("ledgerline/__init__.py", "head", "06-22 10:20", '''
"""Ledgerline: what a small accountancy practice needs a ledger to be sure of."""
''')

_b("ledgerline/invoices.py", "head", "06-22 10:20", '''
"""Invoice numbers, the lines under them and the tax on each line.

An invoice number is the one thing in this product that cannot be reissued, reused or
guessed at: a tax office reads the sequence and a gap in it is a question.
"""
from __future__ import annotations

import dataclasses as dc
''')

_b("ledgerline/invoices.py", "next_number", "06-22 10:20", '''
def next_number(sequence: dict, year: int) -> dict:
    """The next invoice number, and the sequence to keep for the one after it.

    The caller stores what it is given back rather than counting for itself, because two
    people counting is how a sequence grows a gap.
    """
    used = sequence.get("last", 0) + 1
    return {"number": "%d-%04d" % (year, used), "sequence": {"last": used}}
''')

_b("ledgerline/invoices.py", "next_number", "06-23 09:50", '''
def next_number(sequence: dict, year: int) -> dict:
    """The next invoice number for a business year, and the sequence to keep.

    Each business year has its own unbroken run: 2026-0001 up, and then 2027-0001, not
    2027-0349. The caller stores what it is given back rather than counting for itself,
    because two people counting is how a sequence grows a gap.
    """
    used = sequence.get(year, 0) + 1
    return {"number": "%d-%04d" % (year, used), "sequence": {**sequence, year: used}}
''')

_b("ledgerline/invoices.py", "next_number", "07-08 09:30", '''
def next_number(sequence: dict, year: int, expect=None) -> dict:
    """The next invoice number for a business year, and the sequence to keep.

    Each business year has its own unbroken run: 2026-0001 up, and then 2027-0001, not
    2027-0349.

    `expect` is the last number the caller believes was handed out. Two invoices raised
    in the same minute both read the sequence, both saw 41, and both wrote 42; passing
    back what was read turns the second one into a refusal it can retry rather than a
    duplicate nobody notices until the quarter is filed.
    """
    used = sequence.get(year, 0)
    if expect is not None and expect != used:
        return {"ok": False, "reason": "the sequence has moved on", "sequence": sequence}
    return {"ok": True, "number": "%d-%04d" % (year, used + 1),
            "sequence": {**sequence, year: used + 1}}
''')

_b("ledgerline/invoices.py", "Line", "07-06 10:20", '''
@dc.dataclass(frozen=True)
class Line:
    """One line of an invoice, with the tax rate that line is charged at."""

    description: str
    quantity: int
    unit_cents: int
    tax_percent: int
''')

_b("ledgerline/invoices.py", "net_cents", "07-06 10:20", '''
def net_cents(line: "Line") -> int:
    return line.quantity * line.unit_cents
''')

_b("ledgerline/invoices.py", "tax_cents", "07-06 10:20", '''
def tax_cents(line: "Line") -> int:
    return round(net_cents(line) * line.tax_percent / 100)
''')

_b("ledgerline/invoices.py", "gross_cents", "07-06 10:20", '''
def gross_cents(line: "Line") -> int:
    return net_cents(line) + tax_cents(line)
''')

_b("ledgerline/invoices.py", "compose", "07-06 10:20", '''
def compose(number: str, customer: str, lines) -> dict:
    """An invoice laid out the way an accountant reads one: a table you can read down,
    with the tax shown against every line rather than gathered up at the bottom."""
    return {
        "number": number,
        "customer": customer,
        "lines": [{"description": line.description, "quantity": line.quantity,
                   "unit_cents": line.unit_cents, "tax_percent": line.tax_percent,
                   "net_cents": net_cents(line), "tax_cents": tax_cents(line),
                   "gross_cents": gross_cents(line)} for line in lines],
    }
''')

_b("ledgerline/invoices.py", "totals", "07-07 11:40", '''
def totals(invoice: dict) -> dict:
    """The three numbers under the table, each of them the sum of the column above it."""
    return {
        "net_cents": sum(line["net_cents"] for line in invoice["lines"]),
        "tax_cents": sum(line["tax_cents"] for line in invoice["lines"]),
        "gross_cents": sum(line["gross_cents"] for line in invoice["lines"]),
    }
''')

_b("ledgerline/invoices.py", "credit_note", "07-14 14:30", '''
def credit_note(invoice: dict, amount_cents: int, reason: str, number: str) -> dict:
    """A refund is not a negative invoice; it is a credit note against the one it undoes.

    An invoice that has been issued stays issued, so the money going back is its own
    document with its own number and a line pointing at what it credits. More than the
    invoice was for is refused: there is nothing there to credit.
    """
    if amount_cents <= 0:
        return {"ok": False, "reason": "a credit note is for a positive amount"}
    if amount_cents > totals(invoice)["gross_cents"]:
        return {"ok": False, "reason": "more than the invoice it credits"}
    return {"ok": True, "note": {"number": number, "against": invoice["number"],
                                 "amount_cents": amount_cents, "reason": reason}}
''')

_b("ledgerline/invoices.py", "reminders_due", "07-22 09:50", '''
def reminders_due(due_day, today, sent) -> dict:
    """Whether to chase a late invoice, and what to say.

    Twice: a week over, and a month over. After that it stops on its own and a person
    decides what to do, because a machine that chases for ever is how a practice loses a
    client it could have kept by ringing them up.
    """
    if len(sent) >= 2:
        return {"send": False, "reason": "chased twice already"}
    overdue = (today - due_day).days
    for stage, after in ((1, 7), (2, 30)):
        if overdue >= after and len(sent) < stage:
            return {"send": True, "stage": stage, "overdue_days": overdue}
    return {"send": False, "reason": "not late enough yet"}
''')

_b("ledgerline/invoices.py", "delivery", "07-30 14:00", '''
def delivery(message_id: str, events) -> dict:
    """What became of an invoice we sent.

    The practice's question is not whether we pressed send; it is whether the client can
    say they never got it. An address that bounced is worth knowing about the same
    morning, and silence is reported as silence rather than as success.
    """
    mine = [e for e in events if e.get("message_id") == message_id]
    for state in ("bounced", "delivered"):
        if any(e.get("state") == state for e in mine):
            return {"state": state, "known": True}
    return {"state": "unknown", "known": False}
''')

_b("ledgerline/bankimport.py", "head", "07-13 10:10", '''
"""Bank statements, however the bank hands them over.

Three banks, three ideas of what a statement is: two of them answer a request and one of
them sends a file. `normalise` is where they stop disagreeing, and everything after it
works on lines that have a date, an amount in cents and whatever the payer typed.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
''')

_b("ledgerline/bankimport.py", "normalise", "07-13 10:10", '''
def normalise(line: dict) -> dict:
    """One statement line, in the shape the ledger keeps them in."""
    return {"date": line["date"], "cents": int(line["cents"]),
            "reference": (line.get("reference") or "").strip(),
            "counterparty": (line.get("counterparty") or "").strip()}
''')

_b("ledgerline/bankimport.py", "normalise", "07-17 10:30", '''
def normalise(line: dict) -> dict:
    """One statement line, in the shape the ledger keeps them in."""
    return {"date": line["date"], "cents": signed_cents(line),
            "reference": (line.get("reference") or "").strip(),
            "counterparty": (line.get("counterparty") or "").strip()}
''')

_b("ledgerline/bankimport.py", "signed_cents", "07-17 10:30", '''
def signed_cents(line: dict) -> int:
    """Money leaving the account is negative, whichever way the bank writes it.

    Two of our three put the direction in a column of its own and leave the amount
    positive, so a refund sent to a customer read as a payment received and the day's
    takings came out at twice what the practice had actually taken.
    """
    cents = int(line["cents"])
    direction = (line.get("direction") or "").strip().lower()
    if direction in ("debit", "out", "d"):
        return -abs(cents)
    if direction in ("credit", "in", "c"):
        return abs(cents)
    return cents
''')

_b("ledgerline/bankimport.py", "statement_hash", "07-13 10:10", '''
def statement_hash(account: str, lines) -> str:
    """What makes two statements the same statement.

    The account and the lines, in the order the bank gave them; nothing about when we
    asked, so asking twice is not two statements.
    """
    body = json.dumps([account] + [normalise(line) for line in lines],
                      sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
''')

_b("ledgerline/bankimport.py", "import_statement", "07-13 10:10", '''
def import_statement(ledger: dict, account: str, lines) -> dict:
    """Put a statement into the ledger."""
    digest = statement_hash(account, lines)
    kept = list(ledger.get("lines", [])) + [normalise(line) for line in lines]
    return {"ok": True, "imported": len(lines), "digest": digest, "repeat": False,
            "ledger": {"seen": list(ledger.get("seen", [])) + [digest], "lines": kept}}
''')

_b("ledgerline/bankimport.py", "import_statement", "07-14 09:50", '''
def import_statement(ledger: dict, account: str, lines) -> dict:
    """Put a statement into the ledger, once.

    Importing the same statement twice is something people do -- the connection dropped,
    the page was refreshed, the accountant was not sure it had worked -- and until this
    it produced two of everything and a reconciliation nobody could finish. The digest is
    of the statement itself, so the second import is recognised rather than merely
    tolerated.
    """
    digest = statement_hash(account, lines)
    if digest in ledger.get("seen", []):
        return {"ok": True, "imported": 0, "digest": digest, "repeat": True, "ledger": ledger}
    kept = list(ledger.get("lines", [])) + [normalise(line) for line in lines]
    return {"ok": True, "imported": len(lines), "digest": digest, "repeat": False,
            "ledger": {"seen": list(ledger.get("seen", [])) + [digest], "lines": kept}}
''')

_b("ledgerline/bankimport.py", "lines_from_csv", "07-15 10:20", '''
def lines_from_csv(text: str, columns: dict) -> list:
    """A statement that arrives as a file rather than through a door.

    `columns` says which of the file's own headings holds the date, the amount and the
    reference, because no two of them agree and the third bank changes its mind about
    the order every spring.
    """
    rows = csv.DictReader(io.StringIO(text))
    lines = []
    for row in rows:
        amount = row[columns["cents"]].strip().replace(" ", "").replace(",", ".")
        lines.append({"date": row[columns["date"]].strip(),
                      "cents": int(round(float(amount) * 100)),
                      "reference": row.get(columns.get("reference", ""), "") or "",
                      "counterparty": row.get(columns.get("counterparty", ""), "") or "",
                      "direction": row.get(columns.get("direction", ""), "") or ""})
    return lines
''')

_b("ledgerline/bankimport.py", "match", "07-21 11:30", '''
def match(lines, invoices) -> dict:
    """Pair the bank's lines with the invoices they pay.

    The amount has to be right, and then the reference the payer typed has to name the
    invoice. Anything that needs more cleverness than that is left unmatched on purpose:
    a wrong pairing costs a person an hour to find and a right one saves them a minute.
    """
    left = list(invoices)
    matched, unmatched = [], []
    for index, line in enumerate(lines):
        found = None
        for invoice in left:
            if invoice["cents"] != line["cents"]:
                continue
            if invoice["number"] not in (line.get("reference") or ""):
                continue
            found = invoice
            break
        if found is None:
            unmatched.append(index)
        else:
            left.remove(found)
            matched.append({"line": index, "invoice": found["number"]})
    return {"matched": matched, "unmatched": unmatched}
''')

_b("ledgerline/bankimport.py", "match_by_hand", "08-10 14:00", '''
def match_by_hand(result: dict, line_index: int, invoice_number: str) -> dict:
    """A pairing a person made, which the importer would not have guessed.

    Half a practice's payments arrive with the wrong reference or none at all, and the
    person who knows it is Bergstrom paying three invoices at once should be able to say
    so once rather than argue with a matcher.
    """
    if line_index not in result["unmatched"]:
        return {"ok": False, "reason": "that line is already matched", **result}
    return {"ok": True,
            "matched": result["matched"] + [{"line": line_index, "invoice": invoice_number,
                                             "by_hand": True}],
            "unmatched": [i for i in result["unmatched"] if i != line_index]}
''')

_b("ledgerline/bankimport.py", "decode", "08-14 10:30", '''
def decode(raw: bytes, charset: str) -> str:
    """A statement in whatever character set the bank still writes in.

    One of the three sends its files in a single-byte Nordic set, and a name spelled with
    an o-slash came into the ledger as a question mark -- which is a customer's name
    spelled wrong on an invoice, not a display problem.
    """
    try:
        return raw.decode(charset)
    except (LookupError, UnicodeDecodeError):
        return raw.decode("utf-8", "replace")
''')


_b("ledgerline/tax.py", "head", "08-19 15:10", '''
"""Tax rates, the quarter a day falls in, and closing one.

A closed quarter is the point of the module: once the return has gone to the tax office,
what it was made of has to stay what it was made of.
"""
from __future__ import annotations

import datetime as dt
''')

_b("ledgerline/tax.py", "period_of", "08-19 15:10", '''
def period_of(day: dt.date) -> str:
    """The quarter a day belongs to."""
    return "%d-Q%d" % (day.year, day.month // 3 + 1)
''')

_b("ledgerline/tax.py", "period_of", "08-27 15:20", '''
def period_of(day: dt.date) -> str:
    """The quarter a day belongs to.

    January to March is the first quarter, and that includes the thirty-first of March.
    Dividing the month number by three put the last day of every quarter into the next
    one, which is only wrong four days a year and is wrong on the four days an accountant
    is looking.
    """
    return "%d-Q%d" % (day.year, (day.month - 1) // 3 + 1)
''')

_b("ledgerline/tax.py", "rounding", "08-19 15:10", '''
def rounding(lines, mode: str) -> int:
    """The tax on an invoice, rounded the way the invoice's country rounds it.

    Some countries round the tax on every line and add the results up; some add the lines
    up per rate and round once. The two answers differ by a cent often enough that an
    accountant notices, and which one is right is not ours to choose.
    """
    if mode == "per-line":
        return sum(round(line["net_cents"] * line["tax_percent"] / 100) for line in lines)
    if mode == "per-invoice":
        by_rate = {}
        for line in lines:
            by_rate[line["tax_percent"]] = by_rate.get(line["tax_percent"], 0) + line["net_cents"]
        return sum(round(net * rate / 100) for rate, net in sorted(by_rate.items()))
    raise ValueError("unknown rounding mode %r" % mode)
''')

_b("ledgerline/tax.py", "close_period", "08-24 14:00", '''
def close_period(ledger: dict, period: str) -> dict:
    """Close a quarter. Closing one that is already closed changes nothing."""
    closed = sorted(set(ledger.get("closed", [])) | {period})
    return {"ok": True, "ledger": {**ledger, "closed": closed}}
''')

_b("ledgerline/tax.py", "book", "08-24 14:00", '''
def book(ledger: dict, entry: dict) -> dict:
    """Put an entry in the ledger, unless its quarter has gone to the tax office.

    The refusal names the period rather than saying no, because the accountant's next
    move is to date it into the open quarter and they should not have to work out which
    one that is.
    """
    period = period_of(entry["date"])
    if period in ledger.get("closed", []):
        return {"ok": False, "reason": "%s is closed" % period, "period": period,
                "ledger": ledger}
    return {"ok": True, "period": period,
            "ledger": {**ledger, "entries": list(ledger.get("entries", [])) + [entry]}}
''')

_b("ledgerline/tax.py", "rate_on", "08-25 11:00", '''
def rate_on(rates, day: dt.date) -> float:
    """The tax rate that applied on the day of the invoice.

    A rate that changes in January does not change what was owed in December, and a
    quarter reopened to correct one line must come out at the same total it did before.
    """
    applicable = [(start, percent) for start, percent in rates if start <= day]
    if not applicable:
        raise ValueError("no rate applies on %s" % day)
    return max(applicable)[1]
''')


# ======================================================================================
# fieldnote/ -- a crew's day, the order they drive it in, and a phone with no signal
# ======================================================================================

_b("fieldnote/__init__.py", "head", "07-15 15:00", '''
"""Fieldnote: the day a two-person crew actually has, on a phone that keeps losing signal."""
''')

_b("fieldnote/jobs.py", "head", "07-15 15:00", '''
"""What a crew is going to today, and in what order.

A board is a list of Job. Everything here takes one and gives back another; the
dispatcher's screen is somewhere else's problem.
"""
from __future__ import annotations

import dataclasses as dc
import datetime as dt
''')

_b("fieldnote/jobs.py", "Job", "07-15 15:00", '''
@dc.dataclass(frozen=True)
class Job:
    """One visit: whose it is, which day, when it starts and how long it is meant to take."""

    id: str
    crew: str
    day: dt.date
    start: dt.time
    minutes: int
    address: str
    status: str = "planned"
''')

_b("fieldnote/jobs.py", "Job", "08-12 09:50", '''
@dc.dataclass(frozen=True)
class Job:
    """One visit: whose it is, which day, when it starts and how long it is meant to take."""

    id: str
    crew: str
    day: dt.date
    start: dt.time
    minutes: int
    address: str
    status: str = "planned"
    note: str = ""
''')

_b("fieldnote/jobs.py", "ends", "07-15 15:00", '''
def ends(job: "Job") -> dt.time:
    """When the crew is meant to be back in the van."""
    return (dt.datetime.combine(job.day, job.start) + dt.timedelta(minutes=job.minutes)).time()
''')

_b("fieldnote/jobs.py", "day_list", "07-15 15:00", '''
def day_list(board: list, crew: str, day: dt.date) -> list:
    """One crew's day, in the order it is meant to happen.

    Sorted by the clock and then by job id, so two jobs planned for the same minute come
    out in the same order every time the crew opens the phone.
    """
    theirs = [job for job in board if job.crew == crew and job.day == day]
    return sorted(theirs, key=lambda job: (job.start, job.id))
''')

_b("fieldnote/jobs.py", "clashes", "07-16 11:00", '''
def clashes(board: list, job: "Job") -> list:
    """The jobs already on this crew's day that want the same minutes.

    A job that finishes exactly as the next one starts is not a clash; it is a tight day.
    """
    same_day = [other for other in board
                if other.crew == job.crew and other.day == job.day and other.id != job.id]
    return [other for other in same_day
            if other.start < ends(job) and job.start < ends(other)]
''')

_b("fieldnote/jobs.py", "assign", "07-16 11:00", '''
def assign(board: list, job: "Job") -> dict:
    """Put a job on a crew. Two o'clock belongs to one job, not two.

    The dispatcher gets the job that is in the way rather than a refusal, because their
    next question is always which one.
    """
    clash = clashes(board, job)
    if clash:
        return {"ok": False, "reason": "the crew is already out", "clash": clash[0].id,
                "board": board}
    return {"ok": True, "job": job, "board": board + [job]}
''')

_b("fieldnote/jobs.py", "move_crew", "07-24 10:00", '''
def move_crew(board: list, job_id: str, crew: str) -> dict:
    """Hand a job to another crew, if their day has room for it."""
    job = next((j for j in board if j.id == job_id), None)
    if job is None:
        return {"ok": False, "reason": "no such job", "board": board}
    moved = dc.replace(job, crew=crew)
    rest = [j for j in board if j.id != job_id]
    clash = clashes(rest, moved)
    if clash:
        return {"ok": False, "reason": "the crew is already out", "clash": clash[0].id,
                "board": board}
    return {"ok": True, "job": moved, "board": rest + [moved]}
''')

_b("fieldnote/jobs.py", "write_up", "08-12 09:50", '''
def write_up(board: list, job_id: str, note: str, status: str = "done") -> dict:
    """The crew writes the job up from the van, before it drives off and forgets.

    Written up is finished: the note and the status move together, because a job with a
    note and no status is one the office has to ring the crew about.
    """
    job = next((j for j in board if j.id == job_id), None)
    if job is None:
        return {"ok": False, "reason": "no such job", "board": board}
    if not note.strip():
        return {"ok": False, "reason": "a write-up says something", "board": board}
    done = dc.replace(job, note=note.strip(), status=status)
    return {"ok": True, "job": done,
            "board": [done if j.id == job_id else j for j in board]}
''')

_b("fieldnote/jobs.py", "arrival_window", "08-26 15:00", '''
def arrival_window(job: "Job", minutes: int = 120) -> dict:
    """The two hours we promise the customer, around the time we mean to be there.

    The planned minute sits in the middle rather than at the start, so a crew running
    half an hour early is still inside the window they were promised instead of knocking
    on a door nobody is behind yet.
    """
    middle = dt.datetime.combine(job.day, job.start)
    opens = middle - dt.timedelta(minutes=minutes // 2)
    return {"from": opens.time(), "to": (opens + dt.timedelta(minutes=minutes)).time()}
''')

_b("fieldnote/jobs.py", "move_to", "08-31 10:30", '''
def move_to(board: list, job_id: str, day: dt.date) -> dict:
    """Move a job to another day. It leaves the day it was on.

    Both lists are made from the one board here, so a job cannot be on today and
    tomorrow at once however the phone happens to have cached them.
    """
    job = next((j for j in board if j.id == job_id), None)
    if job is None:
        return {"ok": False, "reason": "no such job", "board": board}
    moved = dc.replace(job, day=day)
    return {"ok": True, "job": moved,
            "board": [moved if j.id == job_id else j for j in board]}
''')


_b("fieldnote/routes.py", "head", "07-17 14:40", '''
"""Putting a crew's stops into an order the day can actually be driven in.

Distances are in minutes, because a crew asks how long it takes and never how far it is.
`roads` holds the pairs we have a real time for; everything else is guessed, and the
guess says out loud that it is one.
"""
from __future__ import annotations

import datetime as dt
''')

_b("fieldnote/routes.py", "travel_minutes", "07-17 14:40", '''
def travel_minutes(roads: dict, here: str, there: str):
    """How long the road between two stops takes, or None if we have never driven it."""
    if (here, there) in roads:
        return roads[(here, there)]
    if (there, here) in roads:
        return roads[(there, here)]
    return None
''')

_b("fieldnote/routes.py", "straight_minutes", "07-20 10:15", '''
def straight_minutes(places: dict, here: str, there: str) -> int:
    """A number for a road we have no time for.

    The straight line, and then a third again, because no road is the line -- least of
    all round a fjord, where the line is water. It is a guess and the plan is allowed to
    say so; what it must not do is call it nothing.
    """
    (here_x, here_y), (there_x, there_y) = places[here], places[there]
    line = ((here_x - there_x) ** 2 + (here_y - there_y) ** 2) ** 0.5
    return int(round(line * 1.3))
''')

_b("fieldnote/routes.py", "leg_minutes", "07-20 10:15", '''
def leg_minutes(roads: dict, places: dict, here: str, there: str) -> int:
    """The road if we know it, the guess if we do not."""
    known = travel_minutes(roads, here, there)
    return known if known is not None else straight_minutes(places, here, there)
''')

_b("fieldnote/routes.py", "order_stops", "07-17 14:40", '''
def order_stops(depot: str, stops, roads: dict) -> list:
    """Nearest first, from the depot and then from wherever the crew has got to.

    Not the shortest possible day -- that is a harder problem than the difference is
    worth on eleven stops -- but a day that never sends a van back past where it has
    already been.
    """
    remaining, order, here = list(stops), [], depot
    while remaining:
        remaining.sort()
        nearest = min(remaining, key=lambda stop: (travel_minutes(roads, here, stop) or 999, stop))
        remaining.remove(nearest)
        order.append(nearest)
        here = nearest
    return order
''')

_b("fieldnote/routes.py", "order_stops", "07-20 10:15", '''
def order_stops(depot: str, stops, roads: dict, places: dict) -> list:
    """Nearest first, from the depot and then from wherever the crew has got to.

    Not the shortest possible day -- that is a harder problem than the difference is
    worth on eleven stops -- but a day that never sends a van back past where it has
    already been.
    """
    remaining, order, here = sorted(stops), [], depot
    while remaining:
        nearest = min(remaining, key=lambda stop: (leg_minutes(roads, places, here, stop), stop))
        remaining.remove(nearest)
        order.append(nearest)
        here = nearest
    return order
''')

_b("fieldnote/routes.py", "plan_day", "07-23 14:10", '''
def plan_day(depot: str, stops, roads: dict, places: dict) -> list:
    """The whole day, depot to depot.

    The van starts at the depot and has to get back to it, and a plan that stops at the
    last customer hides an hour of driving from the crew who has to do it.
    """
    return [depot] + order_stops(depot, stops, roads, places) + [depot]
''')

_b("fieldnote/routes.py", "reflow", "08-31 15:00", '''
def reflow(times, from_stop: str, overrun_minutes: int) -> list:
    """A job has overrun. Move the rest of the day rather than breaking it.

    Everything after the stop that ran over shifts by the same amount, which is what the
    crew is going to experience anyway; replanning the order from where they are standing
    sends them back past two customers who are already expecting them.
    """
    shifted, moving = [], False
    for entry in times:
        if moving:
            entry = {**entry, "at": entry["at"] + dt.timedelta(minutes=overrun_minutes)}
        shifted.append(entry)
        if entry["stop"] == from_stop:
            moving = True
    return shifted
''')

_b("fieldnote/routes.py", "ferry_breaks", "08-27 09:30", '''
def ferry_breaks(times, ferries: dict) -> list:
    """The crossings the crew would reach after the last boat of the day.

    A plan that puts a stop on the far side at five past six is not a plan, it is a night
    in a car park, so the legs that cannot be made are handed back and the day is replanned
    on one side of the water.
    """
    missed = []
    for entry in times:
        last = ferries.get(entry["stop"])
        if last is not None and entry["at"].time() > last:
            missed.append({"stop": entry["stop"], "at": entry["at"], "last_crossing": last})
    return missed
''')


_b("fieldnote/sync.py", "head", "07-27 09:50", '''
"""Putting a phone that has been dark all day back together with the board.

Nothing here decides when to sync. It is handed what the phone has and what the server
has, and it says what the day was.
"""
from __future__ import annotations
''')

_b("fieldnote/sync.py", "merge", "07-27 09:50", '''
def merge(phone: dict, server: dict) -> dict:
    """What the phone and the board together say the day was.

    A job comes from the board, so the board's version of one it knows about is the one
    that is kept, and anything the phone made while it was dark is added to it.
    """
    jobs = {job["id"]: dict(job) for job in server.get("jobs", [])}
    for job in phone.get("jobs", []):
        jobs.setdefault(job["id"], dict(job))
    return {"jobs": [jobs[key] for key in sorted(jobs)], "conflicts": []}
''')

_b("fieldnote/sync.py", "merge", "07-31 14:00", '''
def merge(phone: dict, server: dict) -> dict:
    """What the phone and the board together say the day was.

    A job comes from the board, so the board's version of one it knows about is the one
    that is kept, and anything the phone made while it was dark is added to it.

    Where the two disagree about a job they both know, the disagreement is reported
    rather than swallowed: we cannot yet say which side should win, but we can stop
    pretending there was nothing to decide.
    """
    jobs = {job["id"]: dict(job) for job in server.get("jobs", [])}
    conflicts = []
    for job in phone.get("jobs", []):
        theirs = jobs.get(job["id"])
        if theirs is None:
            jobs[job["id"]] = dict(job)
            continue
        if theirs.get("status") != job.get("status"):
            conflicts.append({"id": job["id"], "phone": job.get("status"),
                              "server": theirs.get("status")})
    return {"jobs": [jobs[key] for key in sorted(jobs)], "conflicts": conflicts}
''')

_b("fieldnote/sync.py", "PHONE_WINS", "08-05 09:40", '''
# What each side is the authority on. The crew standing in somebody's garden knows
# whether the work is done; the dispatcher at a desk knows whose job it is and which day
# it is on. Nothing is on both lists, and anything on neither keeps the server's value.
PHONE_WINS = ("status", "note", "finished_at", "signature")
SERVER_WINS = ("crew", "day", "start", "address", "customer")
''')

_b("fieldnote/sync.py", "merge", "08-05 09:40", '''
def merge(phone: dict, server: dict) -> dict:
    """What the phone and the board together say the day was.

    The fields split rather than one side winning the whole job. Letting the server win
    outright lost a crew their whole afternoon: eleven jobs they had finished on the
    mountain road came back as still planned, because the board had never heard
    otherwise and the board was the record of truth.

    Where the two disagree the disagreement is still reported, so the dispatcher can see
    what was decided for them.
    """
    jobs = {job["id"]: dict(job) for job in server.get("jobs", [])}
    conflicts = []
    for job in phone.get("jobs", []):
        theirs = jobs.get(job["id"])
        if theirs is None:
            jobs[job["id"]] = dict(job)
            continue
        merged = dict(theirs)
        for field in PHONE_WINS:
            if field in job:
                merged[field] = job[field]
        for field in SERVER_WINS:
            if field in theirs:
                merged[field] = theirs[field]
        if theirs.get("status") != job.get("status"):
            conflicts.append({"id": job["id"], "phone": job.get("status"),
                              "server": theirs.get("status")})
        jobs[job["id"]] = merged
    return {"jobs": [jobs[key] for key in sorted(jobs)], "conflicts": conflicts}
''')

_b("fieldnote/sync.py", "queue_edit", "07-28 10:40", '''
def queue_edit(pending: list, edit: dict) -> list:
    """An edit the crew made while the phone was dark, kept in the order they made it."""
    return list(pending) + [dict(edit)]
''')

_b("fieldnote/sync.py", "apply_edits", "07-28 10:40", '''
def apply_edits(day, pending) -> list:
    """Replay a phone's queue onto the day, oldest first.

    The order is the whole point. A job set to 'on the way' and then to 'done' is done,
    and replaying the two the other way round sends a crew back to a job they finished
    an hour ago.
    """
    by_id = {job["id"]: dict(job) for job in day}
    for edit in pending:
        job = by_id.get(edit["id"])
        if job is not None:
            job[edit["field"]] = edit["value"]
    return [by_id[key] for key in sorted(by_id)]
''')

_b("fieldnote/sync.py", "photos_for", "08-27 11:40", '''
def photos_for(phone: dict, server: dict, job_id: str) -> list:
    """The photographs of a job, from wherever they have got to.

    The newest one on the phone may still be going up when the merge runs, so it is left
    for the next sync rather than recorded as arrived and then never sent.
    """
    kept = {photo["id"]: photo for photo in server.get("photos", [])
            if photo["job"] == job_id}
    on_phone = [photo for photo in phone.get("photos", []) if photo["job"] == job_id]
    for photo in on_phone[:-1]:
        kept.setdefault(photo["id"], photo)
    return [kept[key] for key in sorted(kept)]
''')

_b("fieldnote/sync.py", "merge", "08-27 11:40", '''
def merge(phone: dict, server: dict) -> dict:
    """What the phone and the board together say the day was.

    The fields split rather than one side winning the whole job. Letting the server win
    outright lost a crew their whole afternoon: eleven jobs they had finished on the
    mountain road came back as still planned, because the board had never heard
    otherwise and the board was the record of truth.

    Where the two disagree the disagreement is still reported, so the dispatcher can see
    what was decided for them. A job's photographs come along with it.
    """
    jobs = {job["id"]: dict(job) for job in server.get("jobs", [])}
    conflicts = []
    for job in phone.get("jobs", []):
        theirs = jobs.get(job["id"])
        if theirs is None:
            jobs[job["id"]] = dict(job)
            continue
        merged = dict(theirs)
        for field in PHONE_WINS:
            if field in job:
                merged[field] = job[field]
        for field in SERVER_WINS:
            if field in theirs:
                merged[field] = theirs[field]
        if theirs.get("status") != job.get("status"):
            conflicts.append({"id": job["id"], "phone": job.get("status"),
                              "server": theirs.get("status")})
        jobs[job["id"]] = merged
    return {"jobs": [jobs[key] for key in sorted(jobs)], "conflicts": conflicts,
            "photos": {key: photos_for(phone, server, key) for key in sorted(jobs)}}
''')

_b("fieldnote/sync.py", "dedupe", "09-01 11:15", '''
def dedupe(jobs) -> list:
    """The same job sent twice from a phone is one job.

    A phone that loses signal halfway through sending has no way of knowing whether the
    board heard it, so it sends again; what makes the two the same is the id the phone
    made when the crew created the job, not when either sending arrived. The first one
    wins, because it is the one anything else may already be pointing at.
    """
    seen, kept = set(), []
    for job in jobs:
        made_by = job.get("client_id") or job.get("id")
        if made_by in seen:
            continue
        seen.add(made_by)
        kept.append(job)
    return kept
''')


# ======================================================================================
# features/ -- the same three products, as scenarios
# ======================================================================================

_b("features/environment.py", "head", "06-16 15:40", '''
"""What behave needs to know before it runs anything.

The board's button runs one feature file from wherever the board happens to be, so the
repository root goes on the path here rather than being assumed to be the working
directory.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
''')

_b("features/environment.py", "before_all", "08-04 11:00", '''
def before_all(context):
    """Say once why the suite cannot run, instead of sixty times.

    A checkout whose packages will not import reports every scenario as broken and none
    of them as the reason. Importing them here turns that into one error with a
    traceback in it.
    """
    import fieldnote          # noqa: F401
    import harbor            # noqa: F401
    import ledgerline        # noqa: F401
''')


# -- Harbor -----------------------------------------------------------------------------

_b("features/harbor/booking.feature", "head", "06-16 15:40", '''
Feature: Berth booking
  A berth belongs to one boat for a range of nights. Before the marina can sell a week it
  has to know which berths are free for it, and it has to keep saying no to the second
  guest who wants the same one.

  Background:
    Given the marina has berths A1, A2 and B7
''')

_b("features/harbor/booking.feature", "bkg001", "06-16 15:40", '''
  @HARBOR-BKG-001
  Scenario: A boat takes a berth for a range of nights
    When Kittiwake books berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    Then the booking is taken
    And the calendar holds H-1001
''')

_b("features/harbor/booking.feature", "bkg002", "06-16 15:40", '''
  @HARBOR-BKG-002
  Scenario: A second boat cannot have nights that are already sold
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When Puffin books berth A1 from 2026-07-03 to 2026-07-08 as H-1002
    Then the booking is refused because berth taken
    And the refusal names H-1001
''')

_b("features/harbor/booking.feature", "bkg004", "06-17 10:30", '''
  @HARBOR-BKG-004
  Scenario: The berths that are free for a week
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When the office asks which berths are free from 2026-07-02 to 2026-07-04
    Then the free berths are A2 and B7
''')

_b("features/harbor/booking.feature", "bkg003", "06-18 09:45", '''
  @HARBOR-BKG-003
  Scenario: The morning a boat leaves, its berth is somebody else's night
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When Puffin books berth A1 from 2026-07-05 to 2026-07-09 as H-1002
    Then the booking is taken
''')

_b("features/harbor/booking.feature", "spreadsheet", "06-19 15:10", '''
  Scenario: The marina's own spreadsheet becomes a berth list
    When the marina's berth spreadsheet is imported
    Then the berths read are A1, A2 and B7
    And berth A1 has shore power
    And berth A2 has no shore power
''')

_b("features/harbor/booking.feature", "bkg006", "06-29 09:55", '''
  @HARBOR-BKG-006
  Scenario: A berth is held for twenty minutes while the guest pays
    When Puffin holds berth A2 from 2026-07-01 to 2026-07-03 as H-1003 at 10:00
    Then the hold is taken
    And the hold runs out at 10:20
''')

_b("features/harbor/booking.feature", "cancel", "07-01 11:05", '''
  Scenario: A cancelled booking gives its nights back to the free list
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When booking H-1001 is cancelled
    Then the free berths from 2026-07-02 to 2026-07-04 are A1, A2 and B7
''')

_b("features/harbor/booking.feature", "cancel", "08-06 11:00", '''
  Scenario: A cancelled booking gives its nights back to the free list
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When booking H-1001 is cancelled
    Then the free berths from 2026-07-02 to 2026-07-04 are A1, A2 and B7
    And the cancellation says it gave back berth A1
''')

_b("features/harbor/booking.feature", "doubleclick", "07-02 15:30", '''
  Scenario: Two guests clicking at the same moment do not both get the berth
    Given Puffin holds berth A2 from 2026-07-01 to 2026-07-03 as H-1003 at 10:00
    When Guillemot holds berth A2 from 2026-07-02 to 2026-07-04 as H-1004 at 10:01
    Then the hold is refused because berth held
''')

_b("features/harbor/booking.feature", "bkg005", "07-03 09:40", '''
  @HARBOR-BKG-005
  Scenario: The free berths come back in the marina's own order
    Given the marina has berths B7, A2 and A1
    When the office asks which berths are free from 2026-07-02 to 2026-07-04
    Then the free berths are A1, A2 and B7
''')


_b("features/harbor/payments.feature", "head", "06-18 14:20", '''
Feature: What a stay costs and who pays for it
  An invoice for the nights the boat was here, at the price the marina was charging on the
  day the booking was made, and a card charged once for it however many times the guest
  presses the button.

  Background:
    Given the marina has berths A1, A2 and B7
    And the marina charges 4500 cents a night from 2026-01-01
''')

_b("features/harbor/payments.feature", "pay001", "06-18 14:20", '''
  @HARBOR-PAY-001
  Scenario: An invoice for the nights that were booked
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When the invoice for H-1001 is made out as 2026-0001
    Then the invoice totals 18000 cents
    And the invoice is numbered 2026-0001
''')

_b("features/harbor/payments.feature", "pay002", "06-19 11:00", '''
  @HARBOR-PAY-002
  Scenario: The rate on the day of the booking, not today's
    Given the marina charges 5200 cents a night from 2026-08-01
    And Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    When the invoice for H-1001 is made out as 2026-0002
    Then the invoice totals 18000 cents
''')

_b("features/harbor/payments.feature", "pay003", "06-30 10:30", '''
  @HARBOR-PAY-003
  Scenario: The card is charged when the booking is confirmed
    When H-1001 is confirmed for 18000 cents
    Then the card has been charged 18000 cents for H-1001
''')

_b("features/harbor/payments.feature", "bankpage", "06-30 14:15", '''
  Scenario: The guest comes back from the bank's page to their own booking
    Given H-1001 sends the guest away to pay with token tok-9
    And H-1002 sends the guest away to pay with token tok-4
    When the guest comes back with token tok-9
    Then they are put back on booking H-1001
''')

_b("features/harbor/payments.feature", "pay005", "07-02 10:45", '''
  @HARBOR-PAY-005
  Scenario: A retried confirmation charges the card once
    Given H-1001 is confirmed for 18000 cents with intent conf-1
    And H-1043 is confirmed for 9000 cents with intent conf-2
    When H-1001 is confirmed for 18000 cents with intent conf-1
    Then the card has been charged 18000 cents for H-1001
    And the ledger holds 2 charges
''')

_b("features/harbor/payments.feature", "pay006", "08-19 10:00", '''
  @HARBOR-PAY-006
  Scenario: A deposit now and the rest on arrival
    When 18000 cents is split into a 30 per cent deposit
    Then 5400 cents is taken now and 12600 cents on arrival
''')

_b("features/harbor/payments.feature", "season", "08-20 10:40", '''
  Scenario: A stay of a month or more is priced by the month
    Given the marina charges 90000 cents a month from 2026-01-01
    And Kittiwake has berth A1 from 2026-06-01 to 2026-07-01 as H-2001
    When the invoice for H-2001 is made out as 2026-0044
    Then the invoice totals 90000 cents
''')

_b("features/harbor/payments.feature", "pay004", "08-28 11:50", '''
  @HARBOR-PAY-004
  Scenario: A refund larger than the invoice it credits is refused
    Given H-1001 is confirmed for 18000 cents with intent conf-1
    When 25000 cents are refunded to H-1001
    Then the refund is refused because more than was charged
''')


_b("features/harbor/checkin.feature", "head", "07-28 15:20", '''
Feature: Checking a guest in from the pontoon
  The pontoon is where the guests are and where the signal is not, so a check-in is made
  on the phone and goes up when there is something to send it to.

  Background:
    Given the marina has berths A1, A2 and B7
''')

_b("features/harbor/checkin.feature", "chk001", "07-28 15:20", '''
  @HARBOR-CHK-001
  Scenario: A guest is checked in with no signal to check them in on
    Given the phone has no signal
    When ola checks H-1001 in at 09:40
    Then the phone is holding H-1001
    When the phone finds a signal
    Then the office has H-1001 as arrived
''')

_b("features/harbor/checkin.feature", "chk002", "07-29 11:10", '''
  @HARBOR-CHK-002
  Scenario: A morning's queue goes up in the order it happened
    Given the phone has no signal
    When ola checks H-1003 in at 16:30
    And ola checks H-1001 in at 09:40
    And ola checks H-1002 in at 11:15
    And the phone finds a signal
    Then the office has H-1001, H-1002 and H-1003 as arrived
''')

_b("features/harbor/checkin.feature", "chk003", "08-11 11:00", '''
  @HARBOR-CHK-003
  Scenario: The code painted on the berth opens the right booking
    Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
    And berth A1 is painted with code NL-A1
    When the crew scan NL-A1 on 2026-07-02
    Then the scan opens booking H-1001
''')

_b("features/harbor/checkin.feature", "chk004", "08-13 14:50", '''
  @HARBOR-CHK-004
  Scenario: A phone with the wrong clock keeps the order it saw
    Given the phone has no signal
    When ola checks H-1001 in at 09:40
    And ola checks H-1002 in at 10:10
    And the phone's clock is put right by 95 minutes
    And the phone finds a signal
    Then the check-ins are stamped 11:15 and 11:45
''')

_b("features/harbor/checkin.feature", "papers", "09-02 14:20", '''
  Scenario: The boat's papers are photographed once, however many times they are taken
    Given the phone has no signal
    When ola checks H-1001 in at 09:40
    And the papers reg-page, reg-page and insurance are photographed for H-1001
    Then the check-in carries the papers reg-page and insurance
''')


# -- Ledgerline -------------------------------------------------------------------------

_b("features/ledgerline/invoices.feature", "head", "06-22 10:20", '''
Feature: Invoice numbers and the lines under them
  A tax office reads the sequence of invoice numbers, and a gap in it is a question
  somebody has to answer. Under the number, the lines, and the tax against each of them.

  Background:
    Given the ledger has issued no invoices
''')

_b("features/ledgerline/invoices.feature", "inv001", "06-22 10:20", '''
  @LEDGER-INV-001
  Scenario: Invoice numbers run without a gap in them
    When 3 invoices are numbered for 2026
    Then the numbers are 2026-0001, 2026-0002 and 2026-0003
''')

_b("features/ledgerline/invoices.feature", "inv002", "06-23 09:50", '''
  @LEDGER-INV-002
  Scenario: A new business year starts the sequence again
    Given 2 invoices are numbered for 2026
    When 1 invoice is numbered for 2027
    Then the numbers are 2026-0001, 2026-0002 and 2027-0001
''')

_b("features/ledgerline/invoices.feature", "inv003", "07-06 10:20", '''
  @LEDGER-INV-003
  Scenario: Every line shows the tax it is charged
    When an invoice is composed for Bergstrom Accounting
      | description | quantity | unit_cents | tax_percent |
      | Bookkeeping | 10       | 8000       | 25          |
      | Year end    | 1        | 45000      | 25          |
    Then line 1 shows 80000 net, 20000 tax and 100000 gross
''')

_b("features/ledgerline/invoices.feature", "inv004", "07-07 11:40", '''
  @LEDGER-INV-004
  Scenario: The totals underneath add the lines up
    When an invoice is composed for Bergstrom Accounting
      | description | quantity | unit_cents | tax_percent |
      | Bookkeeping | 10       | 8000       | 25          |
      | Year end    | 1        | 45000      | 25          |
    Then the invoice totals 125000 net, 31250 tax and 156250 gross
''')

_b("features/ledgerline/invoices.feature", "samenumber", "07-08 09:30", '''
  Scenario: Two invoices numbered from the same reading do not get the same number
    Given 1 invoice is numbered for 2026
    When two invoices are numbered from one reading of the sequence for 2026
    Then the second one is refused because the sequence has moved on
''')

_b("features/ledgerline/invoices.feature", "inv005", "07-14 14:30", '''
  @LEDGER-INV-005
  Scenario: A refund is a credit note against the invoice it undoes
    Given an invoice 2026-0007 for Bergstrom Accounting
      | description | quantity | unit_cents | tax_percent |
      | Bookkeeping | 10       | 8000       | 25          |
    When 20000 cents are credited against it as 2026-C002
    Then the credit note is made out against 2026-0007
    And crediting 200000 cents is refused because more than the invoice it credits
''')

_b("features/ledgerline/invoices.feature", "reminders", "07-22 09:50", '''
  Scenario: A late invoice is chased twice and then left alone
    Given an invoice fell due on 2026-07-01
    When it is 2026-07-09 and nothing has been chased yet
    Then a reminder goes out
    When it is 2026-08-05 and 1 reminder has been sent
    Then a reminder goes out
    When it is 2026-09-01 and 2 reminders have been sent
    Then no reminder goes out because chased twice already
''')

_b("features/ledgerline/invoices.feature", "delivery", "07-30 14:00", '''
  Scenario: An invoice that bounced is not an invoice that arrived
    Given these things happened to our messages
      | message_id | state     |
      | m-1        | delivered |
      | m-2        | bounced   |
    When we ask what became of m-2
    Then what became of it is bounced
    When we ask what became of m-3
    Then what became of it is unknown
''')


_b("features/ledgerline/bankimport.feature", "head", "07-13 10:10", '''
Feature: Importing a bank statement
  Three banks and three ideas of what a statement is. What the ledger keeps is a date, an
  amount in cents, and whatever the payer typed in the reference.

  Background:
    Given an empty ledger
''')

_b("features/ledgerline/bankimport.feature", "bnk001", "07-13 10:10", '''
  @LEDGER-BNK-001
  Scenario: A statement is imported into the ledger
    When the statement for account NO-1 is imported
      | date       | cents | reference | counterparty |
      | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
      | 2026-07-02 | 12000 | 2026-0008 | Havn AS      |
    Then the ledger holds lines dated 2026-07-01 and 2026-07-02
''')

_b("features/ledgerline/bankimport.feature", "bnk002", "07-14 09:50", '''
  @LEDGER-BNK-002
  Scenario: The same statement twice is the same statement
    Given the statement for account NO-1 is imported
      | date       | cents | reference | counterparty |
      | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
    When the statement for account NO-1 is imported
      | date       | cents | reference | counterparty |
      | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
    Then the import is recognised as one we already have
    And the ledger holds lines dated 2026-07-01
''')

_b("features/ledgerline/bankimport.feature", "bnk003", "07-15 10:20", '''
  @LEDGER-BNK-003
  Scenario: A statement that arrives as a file
    When this file is read as a statement
      """
      date,amount,message
      2026-07-01,450.00,2026-0007
      2026-07-02,120.00,2026-0008
      """
    Then the file gives lines dated 2026-07-01 and 2026-07-02
    And the first line of the file is 45000 cents
''')

_b("features/ledgerline/bankimport.feature", "bnk004", "07-17 10:30", '''
  @LEDGER-BNK-004
  Scenario: Money leaving the account is a negative line
    When the statement for account NO-1 is imported
      | date       | cents | direction | reference | counterparty |
      | 2026-07-01 | 45000 | credit    | 2026-0007 | Bergstrom    |
      | 2026-07-02 | 12000 | debit     | refund    | Havn AS      |
    Then the ledger's amounts are 45000 and -12000
''')

_b("features/ledgerline/bankimport.feature", "bnk005", "07-21 11:30", '''
  @LEDGER-BNK-005
  Scenario: A bank line is matched to the invoice it pays
    Given the ledger is owed
      | number    | cents |
      | 2026-0007 | 45000 |
      | 2026-0008 | 12000 |
    When these lines are matched
      | date       | cents | reference           |
      | 2026-07-01 | 45000 | payment 2026-0007   |
      | 2026-07-02 | 12000 | 2026-0008 thank you |
    Then the lines are matched to 2026-0007 and 2026-0008
''')

_b("features/ledgerline/bankimport.feature", "byhand", "07-21 11:30", '''
  Scenario: A line nobody can match is left for a person
    Given the ledger is owed
      | number    | cents |
      | 2026-0007 | 45000 |
    When these lines are matched
      | date       | cents | reference |
      | 2026-07-01 | 45000 | inv 7     |
    Then line 0 is left unmatched
''')

_b("features/ledgerline/bankimport.feature", "byhand", "08-10 14:00", '''
  Scenario: A line nobody can match is left for a person
    Given the ledger is owed
      | number    | cents |
      | 2026-0007 | 45000 |
    When these lines are matched
      | date       | cents | reference |
      | 2026-07-01 | 45000 | inv 7     |
    Then line 0 is left unmatched
    When a person matches line 0 to 2026-0007
    Then line 0 is matched to 2026-0007 by hand
''')

_b("features/ledgerline/bankimport.feature", "encoding", "08-14 10:30", '''
  Scenario: A name in the bank's own character set survives the import
    When the bank's bytes are decoded as latin-1
    Then the name reads Sørensen
''')


_b("features/ledgerline/tax.feature", "head", "08-19 15:10", '''
Feature: Tax rates, quarters, and closing one
  A quarter that has gone to the tax office has to stay what it was when it went, and the
  rate on an invoice is the rate that applied the day it was written.

  Background:
    Given an empty ledger
''')

_b("features/ledgerline/tax.feature", "tax001", "08-19 15:10", '''
  @LEDGER-TAX-001
  Scenario: The tax is rounded on every line
    When the tax on these lines is worked out per-line
      | net_cents | tax_percent |
      | 333       | 25          |
      | 333       | 25          |
      | 333       | 25          |
    Then the tax comes to 249 cents
''')

_b("features/ledgerline/tax.feature", "tax002", "08-19 15:10", '''
  @LEDGER-TAX-002
  Scenario: The tax is rounded once, on the total
    When the tax on these lines is worked out per-invoice
      | net_cents | tax_percent |
      | 333       | 25          |
      | 333       | 25          |
      | 333       | 25          |
    Then the tax comes to 250 cents
''')

_b("features/ledgerline/tax.feature", "tax003", "08-24 14:00", '''
  @LEDGER-TAX-003
  Scenario: A closed quarter takes nothing more
    Given the quarter 2026-Q3 is closed
    When an entry dated 2026-08-15 is booked
    Then the entry is refused because 2026-Q3 is closed
''')

_b("features/ledgerline/tax.feature", "tax004", "08-25 11:00", '''
  @LEDGER-TAX-004
  Scenario: The rate that applied on the day of the invoice
    Given the tax rate was 25 from 2020-01-01 and 22 from 2026-09-01
    When the rate for 2026-08-31 is looked up
    Then the rate is 25
''')

_b("features/ledgerline/tax.feature", "quarteredge", "08-27 15:20", '''
  Scenario: The last day of March is in the first quarter
    When the quarter of 2026-03-31 is worked out
    Then the quarter is 2026-Q1
''')


# -- Fieldnote --------------------------------------------------------------------------

_b("features/fieldnote/jobs.feature", "head", "07-15 15:00", '''
Feature: A crew's day
  What a two-person crew is going to today, in the order they are going to it, with nobody
  promised the same two o'clock twice.

  Background:
    Given an empty board
''')

_b("features/fieldnote/jobs.feature", "job001", "07-15 15:00", '''
  @FIELD-JOB-001
  Scenario: The day comes back in the order it is meant to happen
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address      |
      | J-3 | north | 2026-07-16 | 14:00 | 60      | Storgata 4   |
      | J-1 | north | 2026-07-16 | 08:30 | 90      | Havnegata 12 |
      | J-2 | north | 2026-07-16 | 11:00 | 45      | Fjellveien 7 |
    When the north crew's day for 2026-07-16 is read
    Then the day is J-1, J-2 and J-3
''')

_b("features/fieldnote/jobs.feature", "job002", "07-16 11:00", '''
  @FIELD-JOB-002
  Scenario: A crew cannot be in two places at two o'clock
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address    |
      | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
    When J-2 is put on the north crew for 2026-07-16 at 14:30 for 30 minutes
    Then the job is refused because the crew is already out
    And the job in the way is J-1
''')

_b("features/fieldnote/jobs.feature", "job003", "07-24 10:00", '''
  @FIELD-JOB-003
  Scenario: A job is handed to another crew from the board
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address    |
      | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
    When J-1 is handed to the south crew
    Then the job is taken
    And the south crew's day for 2026-07-16 is J-1
''')

_b("features/fieldnote/jobs.feature", "job004", "08-12 09:50", '''
  @FIELD-JOB-004
  Scenario: The crew write the job up from the van
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address    |
      | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
    When J-1 is written up as Replaced the pump and ran it for ten minutes
    Then the job is taken
    And J-1 is done and says Replaced the pump and ran it for ten minutes
''')

_b("features/fieldnote/jobs.feature", "job005", "08-26 15:00", '''
  @FIELD-JOB-005
  Scenario: The customer is promised two hours, not a minute
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address    |
      | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
    When the arrival window for J-1 is worked out
    Then the window runs from 13:00 to 15:00
''')

_b("features/fieldnote/jobs.feature", "tomorrow", "08-31 10:30", '''
  Scenario: A job moved to tomorrow leaves today's list
    Given these jobs are on the board
      | id  | crew  | day        | start | minutes | address    |
      | J-1 | north | 2026-07-16 | 14:00 | 60      | Storgata 4 |
    When J-1 is moved to 2026-07-17
    Then the north crew's day for 2026-07-16 holds nothing
    And the north crew's day for 2026-07-17 is J-1
''')


_b("features/fieldnote/routes.feature", "head", "07-17 14:40", '''
Feature: Ordering a crew's day
  Eleven stops and one van. Not the shortest day that could exist, but one that never
  sends the van back past a house it has already been to.

  Background:
    Given the roads we know
      | from  | to    | minutes |
      | depot | north | 20      |
      | depot | west  | 35      |
      | depot | east  | 50      |
      | north | west  | 25      |
      | north | east  | 40      |
      | west  | east  | 30      |
''')

_b("features/fieldnote/routes.feature", "rte001", "07-17 14:40", '''
  @FIELD-RTE-001
  Scenario: The nearest stop first
    When the stops north, west and east are ordered from depot
    Then the order is north, west and east
''')

_b("features/fieldnote/routes.feature", "rte002", "07-20 10:15", '''
  @FIELD-RTE-002
  Scenario: A road we have never driven is guessed from the distance
    Given where the stops are
      | stop  | x  | y  |
      | depot | 0  | 0  |
      | north | 0  | 20 |
      | west  | 30 | 0  |
      | east  | 40 | 40 |
      | isle  | 0  | 60 |
    When the leg from north to isle is worked out
    Then the leg is 52 minutes
''')

_b("features/fieldnote/routes.feature", "rte003", "07-23 14:10", '''
  @FIELD-RTE-003
  Scenario: The depot is both ends of the day
    Given where the stops are
      | stop  | x  | y  |
      | depot | 0  | 0  |
      | north | 0  | 20 |
      | west  | 30 | 0  |
      | east  | 40 | 40 |
    When the day through north, west and east is planned from depot
    Then the plan is depot, north, west, east and depot
''')

_b("features/fieldnote/routes.feature", "rte004", "08-27 09:30", '''
  @FIELD-RTE-004
  Scenario: A stop the crew would reach after the last ferry is handed back
    Given the crew get there at
      | stop | at    |
      | west | 15:20 |
      | isle | 18:40 |
    And the last crossings are
      | stop | at    |
      | isle | 17:45 |
    When the day is checked against the ferries
    Then the crossing to isle is missed
''')

_b("features/fieldnote/routes.feature", "reflow", "08-31 15:00", '''
  Scenario: When a job overruns, the rest of the day moves
    Given the crew get there at
      | stop | at    |
      | west | 10:00 |
      | east | 11:30 |
      | isle | 13:00 |
    When west overruns by 45 minutes
    Then the crew now get there at 10:00, 12:15 and 13:45
''')


_b("features/fieldnote/sync.feature", "head", "07-27 09:50", '''
Feature: Putting a phone back together with the board
  A crew phone that has been dark since breakfast, and a dispatcher's board that has
  carried on without it. Between them they know what the day was.

  Background:
    Given nothing on the phone and nothing on the board
''')

_b("features/fieldnote/sync.feature", "syn001", "07-27 09:50", '''
  @FIELD-SYN-001
  Scenario: Work done with the phone offline survives the sync
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | north | planned |
    And the phone has these jobs
      | id  | crew  | status |
      | J-1 | north | done   |
    When the phone and the board are merged
    Then J-1 comes back as done
''')

_b("features/fieldnote/sync.feature", "syn002", "07-27 09:50", '''
  @FIELD-SYN-002
  Scenario: A job the phone has never seen comes down from the board
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | north | planned |
      | J-2 | north | planned |
    And the phone has these jobs
      | id  | crew  | status |
      | J-1 | north | done   |
    When the phone and the board are merged
    Then the merged day is J-1 and J-2
''')

_b("features/fieldnote/sync.feature", "edits", "07-28 10:40", '''
  Scenario: The edits made while the phone was dark are replayed in the order they were made
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | north | planned |
    And the phone queued these edits
      | id  | field  | value      |
      | J-1 | status | on the way |
      | J-1 | status | done       |
    When the queued edits are replayed onto the board
    Then J-1 comes back as done
''')

_b("features/fieldnote/sync.feature", "syn003", "07-31 14:00", '''
  @FIELD-SYN-003
  Scenario: What the two sides disagreed about is written down
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | north | planned |
    And the phone has these jobs
      | id  | crew  | status |
      | J-1 | north | done   |
    When the phone and the board are merged
    Then the merge reports J-1 as done on the phone and planned on the board
''')

_b("features/fieldnote/sync.feature", "syn004", "08-05 09:40", '''
  @FIELD-SYN-004
  Scenario: The dispatcher's crew and day win over the phone's
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | south | planned |
    And the phone has these jobs
      | id  | crew  | status |
      | J-1 | north | done   |
    When the phone and the board are merged
    Then J-1 comes back as done
    And J-1 belongs to the south crew
''')

_b("features/fieldnote/sync.feature", "photos", "08-27 11:40", '''
  Scenario: A job finished offline keeps its photographs
    Given the board has these jobs
      | id  | crew  | status  |
      | J-1 | north | planned |
    And the phone has these jobs
      | id  | crew  | status |
      | J-1 | north | done   |
    And the phone has photographs P-1, P-2 and P-3 for J-1
    When the phone and the board are merged
    Then J-1 comes back with photographs P-1, P-2 and P-3
''')

_b("features/fieldnote/sync.feature", "syn005", "09-01 11:15", '''
  @FIELD-SYN-005
  Scenario: The same job sent twice from a phone is one job
    When these sendings are put together
      | id   | client_id | status |
      | J-9  | c-77      | done   |
      | J-10 | c-77      | done   |
      | J-11 | c-78      | done   |
    Then what is left is J-9 and J-11
''')


# -- The steps ---------------------------------------------------------------------------

_b("features/steps/harbor_steps.py", "head", "06-16 15:40", '''
"""The steps the Harbor scenarios are written in.

Every one of them calls the package and looks at what came back. Nothing here stands in
for a module or reaches inside one, so a scenario that passes is the code doing the work.
"""
import datetime as dt

from behave import given, step, then, when

from harbor import booking
''')

_b("features/steps/harbor_steps.py", "head", "06-18 14:20", '''
"""The steps the Harbor scenarios are written in.

Every one of them calls the package and looks at what came back. Nothing here stands in
for a module or reaches inside one, so a scenario that passes is the code doing the work.
"""
import datetime as dt

from behave import given, step, then, when

from harbor import booking, invoice
''')

_b("features/steps/harbor_steps.py", "head", "06-30 10:30", '''
"""The steps the Harbor scenarios are written in.

Every one of them calls the package and looks at what came back. Nothing here stands in
for a module or reaches inside one, so a scenario that passes is the code doing the work.
"""
import datetime as dt

from behave import given, step, then, when

from harbor import booking, invoice, payments
''')

_b("features/steps/harbor_steps.py", "head", "07-28 15:20", '''
"""The steps the Harbor scenarios are written in.

Every one of them calls the package and looks at what came back. Nothing here stands in
for a module or reaches inside one, so a scenario that passes is the code doing the work.
"""
import datetime as dt

from behave import given, step, then, when

from harbor import booking, checkin, invoice, payments
''')

_b("features/steps/harbor_steps.py", "helpers", "06-16 15:40", '''
def _names(text):
    """A list the way a person writes one: "A1, A2 and B7"."""
    return [part.strip() for part in text.replace(" and ", ", ").split(",") if part.strip()]


def _day(text):
    return dt.date.fromisoformat(text)


def _clock(text):
    """A time of day, on the one day the scenarios all happen to be about."""
    hour, minute = (int(part) for part in text.split(":"))
    return dt.datetime(2026, 7, 16, hour, minute)
''')

_b("features/steps/harbor_steps.py", "berths", "06-16 15:40", '''
@given("the marina has berths {names}")
def step_marina_has_berths(context, names):
    context.berths = _names(names)
    context.calendar = []
    context.holds = []
    context.result = None
''')

_b("features/steps/harbor_steps.py", "berths", "06-18 14:20", '''
@given("the marina has berths {names}")
def step_marina_has_berths(context, names):
    context.berths = _names(names)
    context.calendar = []
    context.holds = []
    context.rates = []
    context.result = None
''')

_b("features/steps/harbor_steps.py", "berths", "06-30 10:30", '''
@given("the marina has berths {names}")
def step_marina_has_berths(context, names):
    context.berths = _names(names)
    context.calendar = []
    context.holds = []
    context.rates = []
    context.ledger = []
    context.tokens = {}
    context.result = None
''')

_b("features/steps/harbor_steps.py", "berths", "07-28 15:20", '''
@given("the marina has berths {names}")
def step_marina_has_berths(context, names):
    context.berths = _names(names)
    context.calendar = []
    context.holds = []
    context.rates = []
    context.ledger = []
    context.tokens = {}
    context.queue = []
    context.arrived = []
    context.codes = {}
    context.result = None
''')

_b("features/steps/harbor_steps.py", "berths", "08-20 10:40", '''
@given("the marina has berths {names}")
def step_marina_has_berths(context, names):
    context.berths = _names(names)
    context.calendar = []
    context.holds = []
    context.rates = []
    context.month_rates = []
    context.ledger = []
    context.tokens = {}
    context.queue = []
    context.arrived = []
    context.codes = {}
    context.result = None
''')

_b("features/steps/harbor_steps.py", "reserve", "06-16 15:40", '''
@given("{boat} has berth {berth} from {start} to {end} as {ref}")
def step_has_berth(context, boat, berth, start, end, ref):
    made = booking.reserve(context.calendar,
                           booking.Booking(ref, berth, boat, _day(start), _day(end)))
    assert made["ok"], made
    context.calendar = made["calendar"]


@when("{boat} books berth {berth} from {start} to {end} as {ref}")
def step_books_berth(context, boat, berth, start, end, ref):
    context.result = booking.reserve(context.calendar,
                                     booking.Booking(ref, berth, boat, _day(start), _day(end)))
    context.calendar = context.result["calendar"]


@then("the booking is taken")
def step_booking_taken(context):
    assert context.result["ok"] is True, context.result


@then("the booking is refused because {reason}")
def step_booking_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result


@then("the refusal names {ref}")
def step_refusal_names(context, ref):
    assert context.result["clash"] == ref, context.result


@then("the calendar holds {refs}")
def step_calendar_holds(context, refs):
    assert [b.ref for b in context.calendar] == _names(refs), context.calendar
''')

_b("features/steps/harbor_steps.py", "free", "06-17 10:30", '''
@when("the office asks which berths are free from {start} to {end}")
def step_asks_free(context, start, end):
    context.free = booking.free_berths(context.calendar, context.berths, _day(start), _day(end))


@then("the free berths are {names}")
def step_free_berths_are(context, names):
    assert context.free == _names(names), context.free
''')

_b("features/steps/harbor_steps.py", "spreadsheet", "06-19 15:10", '''
SPREADSHEET = [{"berth": " A1 ", "length": "9,5", "note2": "16A"},
               {"berth": "A2", "length": "12,0", "note2": ""},
               {"berth": "B7", "length": "7,25", "note2": " 10A "}]


@when("the marina's berth spreadsheet is imported")
def step_import_spreadsheet(context):
    context.read_berths = booking.berths_from_rows(SPREADSHEET)


@then("the berths read are {names}")
def step_berths_read(context, names):
    assert [b["berth"] for b in context.read_berths] == _names(names), context.read_berths


@then("berth {berth} has shore power")
def step_has_power(context, berth):
    found = next(b for b in context.read_berths if b["berth"] == berth)
    assert found["power"] is True, found


@then("berth {berth} has no shore power")
def step_has_no_power(context, berth):
    found = next(b for b in context.read_berths if b["berth"] == berth)
    assert found["power"] is False, found
''')

_b("features/steps/harbor_steps.py", "hold", "06-29 09:55", '''
@step("{boat} holds berth {berth} from {start} to {end} as {ref} at {clock}")
def step_holds_berth(context, boat, berth, start, end, ref, clock):
    context.result = booking.hold(context.calendar, context.holds, ref, berth,
                                  _day(start), _day(end), _clock(clock))
    context.holds = context.result["holds"]


@then("the hold is taken")
def step_hold_taken(context):
    assert context.result["ok"] is True, context.result


@then("the hold runs out at {clock}")
def step_hold_runs_out(context, clock):
    assert context.result["hold"].until == _clock(clock), context.result


@then("the hold is refused because {reason}")
def step_hold_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result
''')

_b("features/steps/harbor_steps.py", "cancel", "07-01 11:05", '''
@when("booking {ref} is cancelled")
def step_cancel_booking(context, ref):
    context.result = booking.cancel(context.calendar, ref)
    assert context.result["ok"], context.result
    context.calendar = context.result["calendar"]


@then("the free berths from {start} to {end} are {names}")
def step_free_between(context, start, end, names):
    free = booking.free_berths(context.calendar, context.berths, _day(start), _day(end))
    assert free == _names(names), free
''')

_b("features/steps/harbor_steps.py", "cancel_freed", "08-06 11:00", '''
@then("the cancellation says it gave back berth {berth}")
def step_cancellation_freed(context, berth):
    assert context.result["freed"]["berth"] == berth, context.result
''')

_b("features/steps/harbor_steps.py", "rates", "06-18 14:20", '''
@given("the marina charges {cents:d} cents a night from {day}")
def step_night_rate(context, cents, day):
    context.rates = context.rates + [(_day(day), cents)]
''')

_b("features/steps/harbor_steps.py", "month_rates", "08-20 10:40", '''
@given("the marina charges {cents:d} cents a month from {day}")
def step_month_rate(context, cents, day):
    context.month_rates = context.month_rates + [(_day(day), cents)]
''')

_b("features/steps/harbor_steps.py", "invoice_when", "06-18 14:20", '''
@when("the invoice for {ref} is made out as {number}")
def step_invoice_for(context, ref, number):
    made = next(b for b in context.calendar if b.ref == ref)
    context.invoice = invoice.invoice_for(made, context.rates[0][1], number, _day("2026-07-06"))
''')

_b("features/steps/harbor_steps.py", "invoice_when", "06-19 11:00", '''
@when("the invoice for {ref} is made out as {number}")
def step_invoice_for(context, ref, number):
    made = next(b for b in context.calendar if b.ref == ref)
    context.invoice = invoice.invoice_for(made, context.rates, number, _day("2026-07-06"))
''')

_b("features/steps/harbor_steps.py", "invoice_when", "08-20 10:40", '''
@when("the invoice for {ref} is made out as {number}")
def step_invoice_for(context, ref, number):
    made = next(b for b in context.calendar if b.ref == ref)
    context.invoice = invoice.invoice_for(made, context.rates, number, _day("2026-07-06"),
                                          context.month_rates)
''')

_b("features/steps/harbor_steps.py", "invoice_then", "06-18 14:20", '''
@then("the invoice totals {cents:d} cents")
def step_invoice_totals(context, cents):
    assert invoice.total_cents(context.invoice) == cents, context.invoice


@then("the invoice is numbered {number}")
def step_invoice_numbered(context, number):
    assert context.invoice.number == number, context.invoice
''')

_b("features/steps/harbor_steps.py", "confirm", "06-30 10:30", '''
@step("{ref} is confirmed for {cents:d} cents")
def step_confirmed(context, ref, cents):
    context.result = payments.capture(context.ledger, ref, cents,
                                      "ch-%d" % (len(context.ledger) + 1))
    context.ledger = context.result["ledger"]


@then("the card has been charged {cents:d} cents for {ref}")
def step_card_charged(context, cents, ref):
    assert payments.charged_cents(context.ledger, ref) == cents, context.ledger
''')

_b("features/steps/harbor_steps.py", "confirm", "07-02 10:45", '''
@step("{ref} is confirmed for {cents:d} cents")
def step_confirmed(context, ref, cents):
    context.result = payments.capture(context.ledger, ref, cents,
                                      "ch-%d" % (len(context.ledger) + 1), ref)
    context.ledger = context.result["ledger"]


@then("the card has been charged {cents:d} cents for {ref}")
def step_card_charged(context, cents, ref):
    assert payments.charged_cents(context.ledger, ref) == cents, context.ledger
''')

_b("features/steps/harbor_steps.py", "confirm_intent", "07-02 10:45", '''
@step("{ref} is confirmed for {cents:d} cents with intent {intent}")
def step_confirmed_with_intent(context, ref, cents, intent):
    context.result = payments.capture(context.ledger, ref, cents,
                                      "ch-%d" % (len(context.ledger) + 1), intent)
    context.ledger = context.result["ledger"]


@then("the ledger holds {count:d} charges")
def step_ledger_holds(context, count):
    assert len(context.ledger) == count, context.ledger
''')

_b("features/steps/harbor_steps.py", "tokens", "06-30 14:15", '''
@given("{ref} sends the guest away to pay with token {token}")
def step_sends_away(context, ref, token):
    context.tokens = payments.start(context.tokens, ref, token)["pending"]


@when("the guest comes back with token {token}")
def step_comes_back(context, token):
    context.result = payments.resume(context.tokens, token)


@then("they are put back on booking {ref}")
def step_put_back_on(context, ref):
    assert context.result["ok"], context.result
    assert context.result["booking_ref"] == ref, context.result
''')

_b("features/steps/harbor_steps.py", "deposit", "08-19 10:00", '''
@when("{cents:d} cents is split into a {percent:d} per cent deposit")
def step_split_deposit(context, cents, percent):
    context.result = payments.split_deposit(cents, percent)


@then("{now:d} cents is taken now and {later:d} cents on arrival")
def step_deposit_halves(context, now, later):
    assert context.result["ok"], context.result
    assert context.result["now_cents"] == now, context.result
    assert context.result["on_arrival_cents"] == later, context.result
''')

_b("features/steps/harbor_steps.py", "refund", "08-28 11:50", '''
@when("{cents:d} cents are refunded to {ref}")
def step_refund(context, cents, ref):
    context.result = payments.refund(context.ledger, ref, cents, "rf-1")
    context.ledger = context.result["ledger"]


@then("the refund is refused because {reason}")
def step_refund_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result
''')

_b("features/steps/harbor_steps.py", "checkin", "07-28 15:20", '''
@given("the phone has no signal")
def step_no_signal(context):
    context.queue = []
    context.arrived = []


@step("{who} checks {ref} in at {clock}")
def step_checks_in(context, who, ref, clock):
    context.queue = checkin.queue(context.queue, checkin.CheckIn(ref, _clock(clock), who))


@then("the phone is holding {refs}")
def step_phone_holding(context, refs):
    assert [entry.booking_ref for entry in context.queue] == _names(refs), context.queue


@step("the phone finds a signal")
def step_finds_signal(context):
    context.result = checkin.flush(context.queue, context.arrived)
    context.arrived = context.result["arrived"]
    context.queue = context.result["pending"]


@then("the office has {refs} as arrived")
def step_office_has(context, refs):
    assert context.arrived == _names(refs), context.arrived
''')

_b("features/steps/harbor_steps.py", "qr", "08-11 11:00", '''
@given("berth {berth} is painted with code {code}")
def step_painted_code(context, berth, code):
    context.codes = {**context.codes, code: berth}


@when("the crew scan {code} on {day}")
def step_scan_code(context, code, day):
    context.result = checkin.booking_for_code(context.calendar, context.codes, code, _day(day))


@then("the scan opens booking {ref}")
def step_scan_opens(context, ref):
    assert context.result["ok"], context.result
    assert context.result["booking_ref"] == ref, context.result
''')

_b("features/steps/harbor_steps.py", "skew", "08-13 14:50", '''
@step("the phone's clock is put right by {minutes:d} minutes")
def step_clock_put_right(context, minutes):
    phone_now = _clock("12:00")
    context.queue = [checkin.correct(entry, phone_now, phone_now + dt.timedelta(minutes=minutes))
                     for entry in context.queue]


@then("the check-ins are stamped {clocks}")
def step_checkins_stamped(context, clocks):
    stamped = [entry.at.strftime("%H:%M") for entry in context.result["applied"]]
    assert stamped == _names(clocks), stamped
''')

_b("features/steps/harbor_steps.py", "papers", "09-02 14:20", '''
@step("the papers {names} are photographed for {ref}")
def step_papers_taken(context, names, ref):
    context.queue = [checkin.with_papers(entry, _names(names))
                     if entry.booking_ref == ref else entry for entry in context.queue]


@then("the check-in carries the papers {names}")
def step_papers_kept(context, names):
    assert list(context.queue[0].papers) == _names(names), context.queue[0]
''')


_b("features/steps/ledgerline_steps.py", "head", "06-22 10:20", '''
"""The steps the Ledgerline scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from ledgerline import invoices
''')

_b("features/steps/ledgerline_steps.py", "head", "07-13 10:10", '''
"""The steps the Ledgerline scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from ledgerline import bankimport, invoices
''')

_b("features/steps/ledgerline_steps.py", "head", "08-19 15:10", '''
"""The steps the Ledgerline scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from ledgerline import bankimport, invoices, tax
''')

_b("features/steps/ledgerline_steps.py", "helpers", "06-22 10:20", '''
def _names(text):
    """A list the way a person writes one."""
    return [part.strip() for part in text.replace(" and ", ", ").split(",") if part.strip()]


def _day(text):
    return dt.date.fromisoformat(text)
''')

_b("features/steps/ledgerline_steps.py", "numbering", "06-22 10:20", '''
@given("the ledger has issued no invoices")
def step_no_invoices_yet(context):
    context.sequence = {}
    context.numbers = []
    context.result = None


@step("{count:d} invoices are numbered for {year:d}")
@step("{count:d} invoice is numbered for {year:d}")
def step_number_invoices(context, count, year):
    for _ in range(count):
        made = invoices.next_number(context.sequence, year)
        context.sequence = made["sequence"]
        context.numbers.append(made["number"])


@then("the numbers are {numbers}")
def step_numbers_are(context, numbers):
    assert context.numbers == _names(numbers), context.numbers
''')

_b("features/steps/ledgerline_steps.py", "same_number", "07-08 09:30", '''
@when("two invoices are numbered from one reading of the sequence for {year:d}")
def step_two_from_one_reading(context, year):
    read = context.sequence.get(year, 0)
    first = invoices.next_number(context.sequence, year, expect=read)
    assert first["ok"], first
    context.sequence = first["sequence"]
    context.result = invoices.next_number(context.sequence, year, expect=read)


@then("the second one is refused because {reason}")
def step_second_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result
''')

_b("features/steps/ledgerline_steps.py", "compose", "07-06 10:20", '''
def _invoice_lines(table):
    return [invoices.Line(row["description"], int(row["quantity"]), int(row["unit_cents"]),
                          int(row["tax_percent"])) for row in table]


@when("an invoice is composed for {customer}")
def step_compose_invoice(context, customer):
    context.invoice = invoices.compose("2026-0001", customer, _invoice_lines(context.table))


@then("line {index:d} shows {net:d} net, {tax_amount:d} tax and {gross:d} gross")
def step_line_shows(context, index, net, tax_amount, gross):
    line = context.invoice["lines"][index - 1]
    assert line["net_cents"] == net, line
    assert line["tax_cents"] == tax_amount, line
    assert line["gross_cents"] == gross, line
''')

_b("features/steps/ledgerline_steps.py", "totals", "07-07 11:40", '''
@then("the invoice totals {net:d} net, {tax_amount:d} tax and {gross:d} gross")
def step_invoice_totals(context, net, tax_amount, gross):
    got = invoices.totals(context.invoice)
    assert got["net_cents"] == net, got
    assert got["tax_cents"] == tax_amount, got
    assert got["gross_cents"] == gross, got
''')

_b("features/steps/ledgerline_steps.py", "credit", "07-14 14:30", '''
@given("an invoice {number} for {customer}")
def step_an_invoice(context, number, customer):
    context.invoice = invoices.compose(number, customer, _invoice_lines(context.table))


@when("{cents:d} cents are credited against it as {number}")
def step_credit_against(context, cents, number):
    context.result = invoices.credit_note(context.invoice, cents, "cancelled", number)


@then("the credit note is made out against {number}")
def step_credit_note_against(context, number):
    assert context.result["ok"], context.result
    assert context.result["note"]["against"] == number, context.result


@step("crediting {cents:d} cents is refused because {reason}")
def step_credit_refused(context, cents, reason):
    refused = invoices.credit_note(context.invoice, cents, "cancelled", "2026-C999")
    assert refused["ok"] is False, refused
    assert refused["reason"] == reason, refused
''')

_b("features/steps/ledgerline_steps.py", "reminders", "07-22 09:50", '''
@given("an invoice fell due on {day}")
def step_fell_due(context, day):
    context.due = _day(day)


@step("it is {day} and nothing has been chased yet")
def step_nothing_chased(context, day):
    context.result = invoices.reminders_due(context.due, _day(day), [])


@step("it is {day} and {count:d} reminder has been sent")
@step("it is {day} and {count:d} reminders have been sent")
def step_some_chased(context, day, count):
    context.result = invoices.reminders_due(context.due, _day(day), ["sent"] * count)


@then("a reminder goes out")
def step_reminder_goes_out(context):
    assert context.result["send"] is True, context.result


@then("no reminder goes out because {reason}")
def step_no_reminder(context, reason):
    assert context.result["send"] is False, context.result
    assert context.result["reason"] == reason, context.result
''')

_b("features/steps/ledgerline_steps.py", "delivery", "07-30 14:00", '''
@given("these things happened to our messages")
def step_message_events(context):
    context.events = [row.as_dict() for row in context.table]


@when("we ask what became of {message_id}")
def step_ask_what_became(context, message_id):
    context.result = invoices.delivery(message_id, context.events)


@then("what became of it is {state}")
def step_what_became(context, state):
    assert context.result["state"] == state, context.result
''')

_b("features/steps/ledgerline_steps.py", "import", "07-13 10:10", '''
@given("an empty ledger")
def step_empty_ledger(context):
    context.ledger = {}
    context.result = None


@step("the statement for account {account} is imported")
def step_import_statement(context, account):
    lines = [row.as_dict() for row in context.table]
    context.result = bankimport.import_statement(context.ledger, account, lines)
    context.ledger = context.result["ledger"]


@then("the ledger holds lines dated {days}")
def step_ledger_dated(context, days):
    assert [line["date"] for line in context.ledger["lines"]] == _names(days), context.ledger
''')

_b("features/steps/ledgerline_steps.py", "dedupe", "07-14 09:50", '''
@then("the import is recognised as one we already have")
def step_import_repeat(context):
    assert context.result["repeat"] is True, context.result
''')

_b("features/steps/ledgerline_steps.py", "csv", "07-15 10:20", '''
FILE_COLUMNS = {"date": "date", "cents": "amount", "reference": "message"}


@when("this file is read as a statement")
def step_read_file(context):
    context.lines = bankimport.lines_from_csv(context.text, FILE_COLUMNS)


@then("the file gives lines dated {days}")
def step_file_dated(context, days):
    assert [line["date"] for line in context.lines] == _names(days), context.lines


@then("the first line of the file is {cents:d} cents")
def step_file_first_line(context, cents):
    assert context.lines[0]["cents"] == cents, context.lines[0]
''')

_b("features/steps/ledgerline_steps.py", "sign", "07-17 10:30", '''
@then("the ledger's amounts are {amounts}")
def step_ledger_amounts(context, amounts):
    want = [int(part) for part in _names(amounts)]
    assert [line["cents"] for line in context.ledger["lines"]] == want, context.ledger
''')

_b("features/steps/ledgerline_steps.py", "match", "07-21 11:30", '''
@given("the ledger is owed")
def step_ledger_owed(context):
    context.invoices = [{"number": row["number"], "cents": int(row["cents"])}
                        for row in context.table]


@when("these lines are matched")
def step_lines_matched(context):
    lines = [{"date": row["date"], "cents": int(row["cents"]), "reference": row["reference"]}
             for row in context.table]
    context.result = bankimport.match(lines, context.invoices)


@then("the lines are matched to {numbers}")
def step_matched_to(context, numbers):
    got = [pair["invoice"] for pair in context.result["matched"]]
    assert got == _names(numbers), context.result


@then("line {index:d} is left unmatched")
def step_line_unmatched(context, index):
    assert index in context.result["unmatched"], context.result
''')

_b("features/steps/ledgerline_steps.py", "by_hand", "08-10 14:00", '''
@when("a person matches line {index:d} to {number}")
def step_person_matches(context, index, number):
    context.result = bankimport.match_by_hand(context.result, index, number)


@then("line {index:d} is matched to {number} by hand")
def step_matched_by_hand(context, index, number):
    made = [pair for pair in context.result["matched"] if pair["line"] == index]
    assert made, context.result
    assert made[0]["invoice"] == number, made
    assert made[0].get("by_hand") is True, made
''')

_b("features/steps/ledgerline_steps.py", "encoding", "08-14 10:30", '''
@when("the bank's bytes are decoded as {charset}")
def step_decode_bytes(context, charset):
    context.decoded = bankimport.decode(b"S\\xf8rensen", charset)


@then("the name reads {name}")
def step_name_reads(context, name):
    assert context.decoded == name, context.decoded
''')

_b("features/steps/ledgerline_steps.py", "rounding", "08-19 15:10", '''
@when("the tax on these lines is worked out {mode}")
def step_tax_rounding(context, mode):
    lines = [{"net_cents": int(row["net_cents"]), "tax_percent": int(row["tax_percent"])}
             for row in context.table]
    context.tax = tax.rounding(lines, mode)


@then("the tax comes to {cents:d} cents")
def step_tax_comes_to(context, cents):
    assert context.tax == cents, context.tax
''')

_b("features/steps/ledgerline_steps.py", "closing", "08-24 14:00", '''
@given("the quarter {period} is closed")
def step_quarter_closed(context, period):
    context.ledger = tax.close_period(context.ledger, period)["ledger"]


@when("an entry dated {day} is booked")
def step_entry_booked(context, day):
    context.result = tax.book(context.ledger, {"date": _day(day), "cents": 1000})
    context.ledger = context.result["ledger"]


@then("the entry is refused because {reason}")
def step_entry_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result
''')

_b("features/steps/ledgerline_steps.py", "tax_rates", "08-25 11:00", '''
@given("the tax rate was {first:d} from {first_day} and {second:d} from {second_day}")
def step_tax_rate_history(context, first, first_day, second, second_day):
    context.tax_rates = [(_day(first_day), first), (_day(second_day), second)]


@when("the rate for {day} is looked up")
def step_rate_looked_up(context, day):
    context.rate = tax.rate_on(context.tax_rates, _day(day))


@then("the rate is {percent:d}")
def step_rate_is(context, percent):
    assert context.rate == percent, context.rate
''')

_b("features/steps/ledgerline_steps.py", "quarters", "08-27 15:20", '''
@when("the quarter of {day} is worked out")
def step_quarter_of(context, day):
    context.quarter = tax.period_of(_day(day))


@then("the quarter is {period}")
def step_quarter_is(context, period):
    assert context.quarter == period, context.quarter
''')


_b("features/steps/fieldnote_steps.py", "head", "07-15 15:00", '''
"""The steps the Fieldnote scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from fieldnote import jobs
''')

_b("features/steps/fieldnote_steps.py", "head", "07-17 14:40", '''
"""The steps the Fieldnote scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from fieldnote import jobs, routes
''')

_b("features/steps/fieldnote_steps.py", "head", "07-27 09:50", '''
"""The steps the Fieldnote scenarios are written in."""
import datetime as dt

from behave import given, step, then, when

from fieldnote import jobs, routes, sync
''')

_b("features/steps/fieldnote_steps.py", "helpers", "07-15 15:00", '''
def _names(text):
    """A list the way a person writes one."""
    return [part.strip() for part in text.replace(" and ", ", ").split(",") if part.strip()]


def _day(text):
    return dt.date.fromisoformat(text)


def _time(text):
    hour, minute = (int(part) for part in text.split(":"))
    return dt.time(hour, minute)


def _clock(text):
    return dt.datetime.combine(dt.date(2026, 7, 16), _time(text))
''')

_b("features/steps/fieldnote_steps.py", "board", "07-15 15:00", '''
@given("an empty board")
def step_empty_board(context):
    context.board = []
    context.result = None


@given("these jobs are on the board")
def step_jobs_on_board(context):
    context.board = [jobs.Job(row["id"], row["crew"], _day(row["day"]), _time(row["start"]),
                              int(row["minutes"]), row["address"]) for row in context.table]


@when("the {crew} crew's day for {day} is read")
def step_read_crew_day(context, crew, day):
    context.day = jobs.day_list(context.board, crew, _day(day))


@then("the day is {ids}")
def step_day_is(context, ids):
    assert [job.id for job in context.day] == _names(ids), context.day
''')

_b("features/steps/fieldnote_steps.py", "assign", "07-16 11:00", '''
@when("{job_id} is put on the {crew} crew for {day} at {start} for {minutes:d} minutes")
def step_put_on_crew(context, job_id, crew, day, start, minutes):
    context.result = jobs.assign(context.board,
                                 jobs.Job(job_id, crew, _day(day), _time(start), minutes,
                                          "Somewhere 1"))
    context.board = context.result["board"]


@then("the job is taken")
def step_job_taken(context):
    assert context.result["ok"] is True, context.result


@then("the job is refused because {reason}")
def step_job_refused(context, reason):
    assert context.result["ok"] is False, context.result
    assert context.result["reason"] == reason, context.result


@then("the job in the way is {job_id}")
def step_job_in_the_way(context, job_id):
    assert context.result["clash"] == job_id, context.result
''')

_b("features/steps/fieldnote_steps.py", "hand_over", "07-24 10:00", '''
@when("{job_id} is handed to the {crew} crew")
def step_handed_to_crew(context, job_id, crew):
    context.result = jobs.move_crew(context.board, job_id, crew)
    context.board = context.result["board"]


@then("the {crew} crew's day for {day} is {ids}")
def step_crew_day_is(context, crew, day, ids):
    got = jobs.day_list(context.board, crew, _day(day))
    assert [job.id for job in got] == _names(ids), got
''')

_b("features/steps/fieldnote_steps.py", "write_up", "08-12 09:50", '''
@when("{job_id} is written up as {note}")
def step_written_up(context, job_id, note):
    context.result = jobs.write_up(context.board, job_id, note)
    context.board = context.result["board"]


@then("{job_id} is done and says {note}")
def step_done_and_says(context, job_id, note):
    job = next(j for j in context.board if j.id == job_id)
    assert job.status == "done", job
    assert job.note == note, job
''')

_b("features/steps/fieldnote_steps.py", "window", "08-26 15:00", '''
@when("the arrival window for {job_id} is worked out")
def step_arrival_window(context, job_id):
    job = next(j for j in context.board if j.id == job_id)
    context.window = jobs.arrival_window(job)


@then("the window runs from {opens} to {closes}")
def step_window_runs(context, opens, closes):
    assert context.window["from"] == _time(opens), context.window
    assert context.window["to"] == _time(closes), context.window
''')

_b("features/steps/fieldnote_steps.py", "move_day", "08-31 10:30", '''
@when("{job_id} is moved to {day}")
def step_moved_to_day(context, job_id, day):
    context.result = jobs.move_to(context.board, job_id, _day(day))
    context.board = context.result["board"]


@then("the {crew} crew's day for {day} holds nothing")
def step_crew_day_empty(context, crew, day):
    got = jobs.day_list(context.board, crew, _day(day))
    assert got == [], got
''')

_b("features/steps/fieldnote_steps.py", "roads", "07-17 14:40", '''
@given("the roads we know")
def step_roads_we_know(context):
    context.roads = {(row["from"], row["to"]): int(row["minutes"]) for row in context.table}
    context.places = {}
''')

_b("features/steps/fieldnote_steps.py", "order", "07-17 14:40", '''
@when("the stops {stops} are ordered from {depot}")
def step_order_stops(context, stops, depot):
    context.order = routes.order_stops(depot, _names(stops), context.roads)


@then("the order is {stops}")
def step_order_is(context, stops):
    assert context.order == _names(stops), context.order
''')

_b("features/steps/fieldnote_steps.py", "order", "07-20 10:15", '''
@when("the stops {stops} are ordered from {depot}")
def step_order_stops(context, stops, depot):
    context.order = routes.order_stops(depot, _names(stops), context.roads, context.places)


@then("the order is {stops}")
def step_order_is(context, stops):
    assert context.order == _names(stops), context.order
''')

_b("features/steps/fieldnote_steps.py", "places", "07-20 10:15", '''
@given("where the stops are")
def step_where_stops_are(context):
    context.places = {row["stop"]: (float(row["x"]), float(row["y"])) for row in context.table}


@when("the leg from {here} to {there} is worked out")
def step_leg_worked_out(context, here, there):
    context.leg = routes.leg_minutes(context.roads, context.places, here, there)


@then("the leg is {minutes:d} minutes")
def step_leg_is(context, minutes):
    assert context.leg == minutes, context.leg
''')

_b("features/steps/fieldnote_steps.py", "plan", "07-23 14:10", '''
@when("the day through {stops} is planned from {depot}")
def step_plan_day(context, stops, depot):
    context.plan = routes.plan_day(depot, _names(stops), context.roads, context.places)


@then("the plan is {stops}")
def step_plan_is(context, stops):
    assert context.plan == _names(stops), context.plan
''')

_b("features/steps/fieldnote_steps.py", "ferries", "08-27 09:30", '''
@given("the crew get there at")
def step_crew_get_there(context):
    context.times = [{"stop": row["stop"], "at": _clock(row["at"])} for row in context.table]


@given("the last crossings are")
def step_last_crossings(context):
    context.ferries = {row["stop"]: _time(row["at"]) for row in context.table}


@when("the day is checked against the ferries")
def step_check_ferries(context):
    context.missed = routes.ferry_breaks(context.times, context.ferries)


@then("the crossing to {stop} is missed")
def step_crossing_missed(context, stop):
    assert [entry["stop"] for entry in context.missed] == [stop], context.missed
''')

_b("features/steps/fieldnote_steps.py", "reflow", "08-31 15:00", '''
@when("{stop} overruns by {minutes:d} minutes")
def step_overruns(context, stop, minutes):
    context.times = routes.reflow(context.times, stop, minutes)


@then("the crew now get there at {clocks}")
def step_now_get_there(context, clocks):
    got = [entry["at"].strftime("%H:%M") for entry in context.times]
    assert got == _names(clocks), got
''')

_b("features/steps/fieldnote_steps.py", "sync", "07-27 09:50", '''
@given("nothing on the phone and nothing on the board")
def step_nothing_anywhere(context):
    context.phone = {"jobs": [], "photos": []}
    context.server = {"jobs": [], "photos": []}
    context.edits = []


@given("the board has these jobs")
def step_board_jobs(context):
    context.server = {**context.server, "jobs": [row.as_dict() for row in context.table]}


@given("the phone has these jobs")
def step_phone_jobs(context):
    context.phone = {**context.phone, "jobs": [row.as_dict() for row in context.table]}


@when("the phone and the board are merged")
def step_merged(context):
    context.merged = sync.merge(context.phone, context.server)


@then("{job_id} comes back as {status}")
def step_comes_back_as(context, job_id, status):
    job = next(j for j in context.merged["jobs"] if j["id"] == job_id)
    assert job["status"] == status, job


@then("the merged day is {ids}")
def step_merged_day(context, ids):
    assert [job["id"] for job in context.merged["jobs"]] == _names(ids), context.merged
''')

_b("features/steps/fieldnote_steps.py", "edits", "07-28 10:40", '''
@given("the phone queued these edits")
def step_queued_edits(context):
    for row in context.table:
        context.edits = sync.queue_edit(context.edits, row.as_dict())


@when("the queued edits are replayed onto the board")
def step_replay_edits(context):
    context.merged = {"jobs": sync.apply_edits(context.server["jobs"], context.edits),
                      "conflicts": []}
''')

_b("features/steps/fieldnote_steps.py", "conflicts", "07-31 14:00", '''
@then("the merge reports {job_id} as {phone_status} on the phone and {board_status} on the board")
def step_merge_reports(context, job_id, phone_status, board_status):
    found = [row for row in context.merged["conflicts"] if row["id"] == job_id]
    assert found, context.merged
    assert found[0]["phone"] == phone_status, found
    assert found[0]["server"] == board_status, found
''')

_b("features/steps/fieldnote_steps.py", "planning_wins", "08-05 09:40", '''
@then("{job_id} belongs to the {crew} crew")
def step_belongs_to_crew(context, job_id, crew):
    job = next(j for j in context.merged["jobs"] if j["id"] == job_id)
    assert job["crew"] == crew, job
''')

_b("features/steps/fieldnote_steps.py", "photos", "08-27 11:40", '''
@given("the phone has photographs {ids} for {job_id}")
def step_phone_photos(context, ids, job_id):
    context.phone = {**context.phone,
                     "photos": [{"id": name, "job": job_id} for name in _names(ids)]}


@then("{job_id} comes back with photographs {ids}")
def step_comes_back_with_photos(context, job_id, ids):
    got = [photo["id"] for photo in context.merged["photos"][job_id]]
    assert got == _names(ids), got
''')

_b("features/steps/fieldnote_steps.py", "dedupe", "09-01 11:15", '''
@when("these sendings are put together")
def step_sendings_together(context):
    context.kept = sync.dedupe([row.as_dict() for row in context.table])


@then("what is left is {ids}")
def step_what_is_left(context, ids):
    assert [job["id"] for job in context.kept] == _names(ids), context.kept
''')


# ======================================================================================
# The commits themselves
# ======================================================================================
#
# One line, one commit: when, who, and the subject. Which files the commit carries is not
# written here -- it is every path with a block stamped at that same minute, which is the
# only way the two can be kept from drifting apart.

COMMITS = [
    ("06-15 09:05", "tomasz", "chore: an empty repository for Northlight"),
    ("06-15 11:20", "tomasz", "{harbor.booking.week}: a berth is taken for a range of nights"),
    ("06-16 15:40", "mateo", "chore: behave, and somewhere to keep the scenarios"),
    ("06-17 10:30", "tomasz", "{harbor.booking.availability}: which berths are free for a week"),
    ("06-18 09:45", "priya", "{harbor.booking.availability}: the night a boat leaves belongs to the next guest"),
    ("06-18 14:20", "tomasz", "{harbor.booking.invoice}: an invoice for the nights that were booked"),
    ("06-19 11:00", "priya", "{harbor.booking.invoice}: the rate on the day it was booked, not today's"),
    ("06-19 15:10", "tomasz", "{harbor.booking.import-berths}: read the marina's own berth spreadsheet"),
    ("06-22 10:20", "tomasz", "{ledger.invoices.numbering}: invoice numbers with no gap in them"),
    ("06-23 09:50", "priya", "{ledger.invoices.numbering}: a new business year starts the sequence again"),
    ("06-25 14:00", "mateo", "chore: a script that runs one feature file and writes the JUnit"),
    ("06-26 10:40", "ingrid", "chore: the README says out loud that all of this is invented"),
    ("06-29 09:55", "tomasz", "{harbor.booking.hold}: hold a berth for twenty minutes while the guest pays"),
    ("06-30 10:30", "tomasz", "{harbor.payments.capture}: charge the card when the booking is confirmed"),
    ("06-30 14:15", "aiko", "{harbor.payments.capture.2}: hand the guest back to the booking they were paying for"),
    ("07-01 11:05", "tomasz", "{harbor.booking.cancel}: cancel a booking and give the berth back"),
    ("07-02 10:45", "tomasz", "{harbor.payments.capture.3}: a confirmation carries an intention and the charge carries it too"),
    ("07-02 15:30", "mateo", "{harbor.booking.double-book}: a berth somebody is holding is as taken as a booked one"),
    ("07-03 09:40", "priya", "{harbor.booking.availability}: the free berths come back in the marina's own order"),
    ("07-06 10:20", "tomasz", "{ledger.invoices.compose}: an invoice is lines, with the tax against each of them"),
    ("07-07 11:40", "priya", "{ledger.invoices.compose.2}: the totals underneath add the lines up"),
    ("07-08 09:30", "tomasz", "{ledger.invoices.same-number}: the sequence is handed over, not read and written"),
    ("07-10 09:20", "tomasz", "{harbor.payments.double-charge}: the same intention gets the charge it already made"),
    ("07-13 10:10", "tomasz", "{ledger.bank.connectors}: one door for three banks' statements"),
    ("07-14 09:50", "tomasz", "{ledger.bank.dedupe}: the same statement twice is the same statement"),
    ("07-14 14:30", "priya", "{ledger.invoices.credit-notes}: a refund is a credit note against the invoice it undoes"),
    ("07-15 10:20", "tomasz", "{ledger.bank.csv}: a statement that arrives as a file"),
    ("07-15 15:00", "aiko", "{field.jobs.day}: a crew's day, in the order it is meant to happen"),
    ("07-16 11:00", "aiko", "{field.jobs.overlap}: a crew cannot be in two places at two o'clock"),
    ("07-17 10:30", "tomasz", "{ledger.bank.sign}: money leaving the account is a negative line"),
    ("07-17 14:40", "aiko", "{field.routes.order}: order a crew's stops so the day is driveable"),
    ("07-20 10:15", "aiko", "{field.routes.travel}: the road between two stops, not the line"),
    ("07-21 11:30", "tomasz", "{ledger.bank.match}: a bank line and the invoice it pays"),
    ("07-22 09:50", "priya", "{ledger.invoices.reminders}: chase a late invoice twice, then leave it alone"),
    ("07-23 14:10", "aiko", "{field.routes.order.1}: the depot is both ends of the day"),
    ("07-24 10:00", "aiko", "{field.jobs.assign}: hand a job to another crew from the board"),
    ("07-27 09:50", "aiko", "{field.offline.day}: a day's work that survives the phone going dark"),
    ("07-28 10:40", "aiko", "{field.offline.day.2}: the edits made while the phone was dark, in the order they were made"),
    ("07-28 15:20", "aiko", "{harbor.checkin.pontoon}: check a guest in from the pontoon with no signal"),
    ("07-29 11:10", "aiko", "{harbor.checkin.pontoon.2}: the queue goes up oldest first"),
    ("07-30 14:00", "tomasz", "{ledger.invoices.send}: an invoice that bounced is not an invoice that arrived"),
    ("07-31 14:00", "aiko", "{field.offline.sync-loss}: write down what the two sides disagreed about"),
    ("08-04 11:00", "ola", "chore: say once why the suite cannot run, instead of sixty times"),
    ("08-05 09:40", "aiko", "{field.offline.sync-loss}: the phone's word on what happened, the board's on what was planned"),
    ("08-06 11:00", "tomasz", "{harbor.booking.cancel}: a cancellation says which nights it gave back"),
    ("08-10 14:00", "tomasz", "{ledger.bank.match-by-hand}: the lines the importer would not guess"),
    ("08-11 11:00", "aiko", "{harbor.checkin.qr}: the code painted on the berth opens the right booking"),
    ("08-12 09:50", "aiko", "{field.jobs.notes}: the crew write the job up from the van"),
    ("08-13 14:50", "aiko", "{harbor.checkin.clock-skew}: trust the server's clock, keep the phone's order"),
    ("08-14 10:30", "tomasz", "{ledger.bank.encoding}: a statement in the bank's own character set"),
    ("08-19 10:00", "tomasz", "{harbor.payments.deposit}: a deposit now and the rest on arrival"),
    ("08-19 15:10", "tomasz", "{ledger.tax.rounding}: round the tax per line or per invoice, whichever the country says"),
    ("08-20 10:40", "priya", "{harbor.booking.season-rate}: a season is priced by the month, not by the night"),
    ("08-21 14:00", "ola", "chore: run-tests writes the JUnit where the board asks for it"),
    ("08-24 14:00", "tomasz", "{ledger.tax.close}: a closed quarter takes nothing more"),
    ("08-25 11:00", "tomasz", "{ledger.tax.rates}: the rate that applied on the day of the invoice"),
    ("08-25 14:30", "tomasz", "{harbor.payments.refunds}: give the money back to the card it came from"),
    ("08-26 15:00", "aiko", "{field.jobs.window}: a two-hour arrival window we can keep"),
    ("08-27 09:30", "aiko", "{field.routes.ferry}: the last crossing is the end of that side of the day"),
    ("08-27 11:40", "aiko", "{field.offline.attachments}: a job's photographs come back with it"),
    ("08-27 15:20", "tomasz", "{ledger.tax.quarter-edge}: the last day of a quarter is in the quarter it ends"),
    ("08-28 11:50", "mateo", "{harbor.payments.refund-over}: a refund larger than the invoice, as a scenario"),
    ("08-31 10:30", "aiko", "{field.jobs.tomorrow}: a job moved to tomorrow leaves today's list"),
    ("08-31 15:00", "aiko", "{field.routes.reflow}: when a job overruns, the rest of the day moves"),
    ("09-01 11:15", "aiko", "{field.offline.duplicate-job}: the same job sent twice from a phone is one job"),
    ("09-02 14:20", "priya", "{harbor.checkin.photo}: the boat's papers, photographed at the pontoon"),
    ("09-03 10:00", "ingrid", "chore: the README says how to run the scenarios and which two fail today"),
    ("09-04 09:30", "ola", "chore: pin behave and say which Python this needs"),
]


# ======================================================================================
# Rendering a file, checking the story, and writing it into git
# ======================================================================================

def _render(path: str, moment: dt.datetime):
    """The file as it stood at a moment, or None if it had not been written yet.

    Every block name keeps the place it was first declared in, so a rewrite lands where
    the function already was rather than at the bottom of the file.
    """
    chosen: dict[str, tuple] = {}
    order: list[str] = []
    for name, since, text in BLOCKS[path]:
        if name not in order:
            order.append(name)
        if since <= moment and (name not in chosen or since >= chosen[name][0]):
            chosen[name] = (since, text)
    if not chosen:
        return None
    joiner = SEPARATORS.get(pathlib.PurePath(path).suffix, "\n")
    return joiner.join(chosen[name][1] for name in order if name in chosen) + "\n"


def _paths_at(moment: dt.datetime) -> list:
    """The files a commit carries: every path with a block written at its own minute."""
    return sorted(path for path, blocks in BLOCKS.items()
                  if any(since == moment for _, since, _ in blocks))


def _aliases(subject: str) -> list:
    """The {alias} placeholders in a commit subject."""
    return [field for _, field, _, _ in string.Formatter().parse(subject) if field]


def _made_dates() -> dict:
    """When each of the products' tasks was written down, by alias.

    The engine's `_KeyMap` leaves an alias it does not know as a literal `{alias}`, so a
    commit naming a task the vault has not created yet would put a raw placeholder into
    the code history. Checked here, against the specs, before anything is written.
    """
    from products import fieldnote, harbor, ledgerline

    made = {}
    for module in (harbor, ledgerline, fieldnote):
        for spec in module.WORK:
            made[module.PREFIX + spec["a"]] = when(spec["made"])
    return made


def _timeline() -> list:
    """Every commit, checked: in order, inside office hours, carrying files that changed,
    and naming only tasks that exist by then."""
    made = _made_dates()
    stamps = {since for blocks in BLOCKS.values() for _, since, _ in blocks}
    commits, state, previous = [], {}, None

    for text, handle, subject in COMMITS:
        moment = office_hours(when(text), subject)
        if previous is not None and moment <= previous:
            raise ValueError("%s is not after the commit before it" % subject)
        previous = moment

        for alias in _aliases(subject):
            if alias not in made:
                raise ValueError("%s names {%s}, which no product writes down" % (subject, alias))
            if made[alias] >= moment:
                raise ValueError("%s names {%s}, which is only written down at %s"
                                 % (subject, alias, made[alias]))

        touched = _paths_at(moment)
        if not touched:
            raise ValueError("%s carries no files" % subject)
        changed = False
        for path in touched:
            written = _render(path, moment)
            changed = changed or state.get(path) != written
            state[path] = written
        if not changed:
            raise ValueError("%s leaves every file it touches byte for byte the same" % subject)

        commits.append((moment, PEOPLE[handle], subject))
        stamps.discard(moment)

    if stamps:
        raise ValueError("blocks written at %s, when no commit happens"
                         % ", ".join(sorted(str(s) for s in stamps)))
    return commits


def _origin(root: pathlib.Path) -> str:
    """Where this checkout pushes, or empty if it is not a repository or pushes nowhere."""
    try:
        return _git(root, "remote", "get-url", "origin").strip()
    except (RuntimeError, OSError):
        return ""


def _init(root: pathlib.Path) -> None:
    """An empty repository, however the last run left this one.

    Everything the generator wrote is removed and git is started again, so a second
    replay is a first replay. The virtualenv and the reports the test runs leave behind
    are not ours to delete and are kept where they are.

    `origin` is the one thing about the old repository that is not the generator's to
    throw away: it says where this checkout belongs, a person put it there, and deleting
    `.git` takes it with everything else. It is read before the wipe and written back
    after `git init`, so a rebuild leaves a repository that can still be pushed.
    """
    root.mkdir(parents=True, exist_ok=True)
    origin = _origin(root)
    for entry in sorted(root.iterdir()):
        if entry.name in KEEP:
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    _git(root, "init", "-q", "-b", "main")
    if origin:
        _git(root, "remote", "add", "origin", origin)


def _git(root: pathlib.Path, *args, env=None) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                          env={**os.environ, **(env or {})})
    if done.returncode != 0:
        raise RuntimeError("git %s in %s failed:\n%s%s"
                           % (" ".join(args), root, done.stdout, done.stderr))
    return done.stdout


def _write(root: pathlib.Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    if path == "run-tests":
        os.chmod(target, 0o755)


def _record(root: pathlib.Path, message: str, event) -> None:
    """One commit in the code repository, with the event's own author, committer and date.

    Both dates and both identities come from the story rather than from the machine this
    is replayed on, which is what makes two replays produce the same SHAs.
    """
    stamp = event.when.replace(tzinfo=dt.timezone.utc).isoformat()
    _git(root, "add", "-A", "--", ".")
    if not _git(root, "status", "--porcelain").strip():
        raise RuntimeError("nothing to commit for %r" % message)
    _git(root, "-c", "commit.gpgsign=false", "commit", "-q", "-m", message,
         "--author", "%s <%s>" % (event.who.name, event.who.email),
         env={"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp,
              "GIT_AUTHOR_NAME": event.who.name, "GIT_AUTHOR_EMAIL": event.who.email,
              "GIT_COMMITTER_NAME": event.who.name, "GIT_COMMITTER_EMAIL": event.who.email})


def _writer(root: pathlib.Path, index: int, moment: dt.datetime, subject: str):
    def fn(eng, event):
        if index == 0:
            _init(root)
        for path in _paths_at(moment):
            _write(root, path, _render(path, moment))
        for alias in _aliases(subject):
            if alias not in eng.keys:
                raise ValueError("the code commit at %s names {%s}, which the vault has "
                                 "not created yet" % (moment, alias))
        _record(root, subject.format_map(engine._KeyMap(eng)), event)
        return []

    return fn


def events(code_root) -> list:
    """Every commit the code repository ever had, as events on the vault's timeline."""
    root = pathlib.Path(code_root)
    return [engine.Event(moment, who, "raw",
                         {"fn": _writer(root, index, moment, subject)}, subject)
            for index, (moment, who, subject) in enumerate(_timeline())]
