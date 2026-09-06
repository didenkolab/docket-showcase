"""Ledgerline: bookkeeping for people who did not want to become bookkeepers.

Three epics between 15 June and 4 September 2026 — invoices, bank import and tax
periods — and the thirty-two pieces of work under them. The customers are a small
accounting firm, Bergstrom Accounting, who keep the books for about ninety sole traders,
and the sole traders themselves: a florist in Aalesund, a two-van plumber, a photographer
who invoices four times a year and forgets which four.

The shape of the twelve weeks, read off the sprint goals:

  * Sprint 1 is Harbor's, and Ledgerline puts one story in it — invoice numbering — so
    that the Friday demo is one flow across two products rather than two demos. The
    retrospective for Sprint 1 says exactly that, and this file is what makes it true.
  * Sprint 2 writes the invoice itself: the lines, the tax underneath them, the PDF.
  * Sprint 3 is Ledgerline's own goal, "bank import, first three banks", and it is the
    busiest fortnight in this file.
  * Sprints 4 and 5 are somebody else's — Fieldnote's offline day and Harbor's season
    launch — so matching, sending and the operational work carry on underneath them.
  * Sprint 6 is "tax periods, and the sync fix under load", and it is still running on
    the day the vault is read, which is why the tax epic is the unfinished one.

Nothing here plants an anomaly. Harbor owns all three of those, and a second `only-owner`
or a second one-sided relation arriving by accident would make the demonstration a lie —
so every parent has open children on more than one person, and every `blocks` written
here is written from both ends.

The one relationship this file must not write is `blocks` on
`ledger.invoices.credit-notes`: `harbor.py` writes both sides of the cross-project pair
(Harbor's refunds story is blocked by credit notes, dated 2026-08-25), and it can only do
that because the story exists by then. Credit notes are created on 2026-07-14 and are
still Ready on 4 September, unsized, on the agenda for the Sprint 7 planning that the
sprint page already names: "Refunds and credit notes together".
"""
from __future__ import annotations

import story

from . import common

PROJECT = "LEDGER"
PREFIX = "ledger."

# --- the epics ------------------------------------------------------------------------

EPICS = [
    dict(a="invoices", t="Invoices and credit notes", type="epic", who="ingrid", made="06-15 09:34",
         moves=[("06-15 11:50", "Ready"), ("06-16 09:18", "In progress")],
         why="A sole trader's invoice is a word-processor document with last month's numbers changed, "
             "saved over the top of the one before it, and emailed with the tax worked out on "
             "a calculator. Everything under this epic replaces that one habit: a document "
             "Ledgerline numbers, prices and sends, that the customer's accountant can file "
             "without ringing anybody to ask what the second line means.",
         ok=["A business can write an invoice, send it, and see that it was paid",
             "Every invoice has a number nobody else has and nobody can reuse",
             "The tax on the invoice is the tax that applied on the day it was issued"]),
    dict(a="bank", t="Bank import", type="epic", who="tomasz", made="06-15 09:35",
         moves=[("06-15 11:55", "Ready"), ("07-01 09:25", "In progress")],
         why="Half of bookkeeping is reading a bank statement and deciding what each line was. "
             "Bergstrom Accounting do it for ninety businesses by downloading a CSV a month and "
             "typing into a spreadsheet. This epic is the machine doing the typing: statements "
             "arrive on their own, the lines that obviously pay an invoice are matched, and a "
             "person only sees the ones that need a person.",
         ok=["A month of statements arrives without anybody downloading anything",
             "A line that pays an invoice is matched to it without being asked",
             "Importing the same statement twice changes nothing the second time"]),
    dict(a="tax", t="Tax periods", type="epic", who="tomasz", made="06-15 09:36",
         moves=[("06-15 12:00", "Ready"), ("08-24 10:50", "In progress")],
         why="A quarter ends, the numbers are agreed, the return is filed, and from that "
             "moment the quarter must stop changing — an invoice backdated into a period "
             "already reported is the one mistake in bookkeeping that costs money rather than "
             "time. This epic is the closing of a period and the report that comes out of it.",
         ok=["A quarter can be closed, and a closed quarter refuses new entries",
             "The return can be produced again months later and come out identical",
             "A rate that changed mid-quarter is applied by date, not by today"]),
]

# --- invoices ---------------------------------------------------------------------------

INVOICES = [
    dict(a="invoices.numbering", t="Number invoices in one unbroken sequence per business year",
         parent="invoices", who="tomasz", labels="invoicing", pts=3,
         made="06-15 09:55", sprint="Sprint 1",
         moves=[("06-15 11:25", "Ready"), ("06-17 09:45", "In progress"),
                ("06-19 16:10", "In review"), ("06-22 10:30", "QA", "mateo"),
                ("06-23 15:10", "Done", "mateo")],
         why="An invoice number is the only thing about an invoice that the tax office cares "
             "about before it cares about anything else: the sequence has to start at one each "
             "business year, have no gaps in it, and never give the same number to two "
             "documents. A gap has to be explainable and a duplicate is not explainable at all, "
             "which is why this is the first thing Ledgerline does rather than the last.",
         ok=["Each business gets its own sequence, starting again at the turn of its year",
             "Two invoices issued at the same moment get two different numbers",
             "A number is allocated when the invoice is issued, not when it is drafted"]),
    dict(a="invoices.compose", t="Write an invoice line by line with the tax shown separately",
         parent="invoices", who="priya", labels="invoicing", made="06-29 09:40", sprint="Sprint 2",
         moves=[("06-29 11:30", "Ready"), ("06-30 09:50", "In progress"),
                ("07-06 16:20", "In review"), ("07-07 10:40", "QA", "mateo"),
                ("07-08 15:30", "Done", "mateo")],
         why="The screen a florist looks at on a Sunday evening. Lines with a description, a "
             "quantity and a unit price; the tax for each line worked out where she can see it "
             "rather than folded into a total; and a running sum that does not move around the "
             "page as she types. Everything else in the product is behind this one form.",
         ok=["An invoice is written as lines with quantity, unit price and a tax rate each",
             "The tax and the totals are visible while the invoice is being written",
             "A half-written invoice survives closing the tab"]),
    dict(a="invoices.compose.1", t="Lay the invoice out as a table an accountant can read down",
         type="subtask", parent="invoices.compose", who="priya", pts=5, made="06-29 10:20",
         moves=[("06-30 09:55", "Ready"), ("06-30 10:30", "In progress"),
                ("07-02 15:40", "In review"), ("07-03 10:10", "QA", "mateo"),
                ("07-03 15:20", "Done", "mateo")],
         why="Columns in the order the eye reads them, numbers right-aligned on the decimal "
             "point, and a row that can be added or removed without the rest of the form "
             "jumping — an invoice form is a spreadsheet that has to behave itself."),
    dict(a="invoices.compose.2", t="Show the tax for every line and the totals underneath them",
         type="subtask", parent="invoices.compose", who="priya", pts=3, made="06-29 10:25",
         moves=[("07-01 09:40", "Ready"), ("07-03 09:50", "In progress"),
                ("07-06 15:10", "In review"), ("07-07 10:20", "QA", "mateo"),
                ("07-07 15:40", "Done", "mateo")],
         why="Two lines at different rates is the ordinary case and the one every home-made "
             "invoice gets wrong: the totals block has to show net, each rate's tax on its own "
             "row, and the gross, because that is the block the accountant checks first."),
    dict(a="invoices.pdf", t="Render an invoice as a PDF the customer's accountant will file",
         parent="invoices", who="tomasz", labels="invoicing", pts=5,
         made="06-29 09:45", sprint="Sprint 2",
         moves=[("06-29 11:40", "Ready"), ("07-01 10:10", "In progress"),
                ("07-07 16:40", "In review"), ("07-08 11:00", "QA", "mateo"),
                ("07-09 14:20", "Done", "mateo")],
         why="What actually leaves the building is a PDF, and it is read by somebody who has "
             "never seen Ledgerline and never will. It has to carry the business's registered "
             "name and number, the customer's address as the customer writes it, the lines, the "
             "tax rows and the payment details, on one page whenever one page is possible.",
         ok=["The PDF carries the registered details of both businesses and the invoice number",
             "An invoice of twenty lines still prints as a document rather than a spill",
             "The same invoice rendered twice produces the same bytes"]),
    dict(a="invoices.send", t="Email an invoice and know whether it arrived",
         parent="invoices", who="priya", labels="invoicing", pts=3,
         made="07-30 11:00", sprint=["Sprint 4", "Sprint 5"],
         moves=[("07-31 10:10", "Ready"), ("08-12 10:20", "In progress"),
                ("08-17 16:10", "In review"), ("08-18 11:00", "QA", "mateo"),
                ("08-19 14:50", "Done", "mateo")],
         why="An invoice nobody received is an invoice nobody is going to pay, and today the "
             "only evidence that it was sent is the sender's own memory of pressing the button. "
             "Sending has to be a thing the invoice remembers, with the address it went to, the "
             "moment it went, and whatever the mail server said afterwards.",
         ok=["Sending records the address, the moment, and what the mail server answered",
             "A bounce is visible on the invoice rather than in somebody's inbox",
             "The same invoice can be sent again without becoming a second invoice"]),
    dict(a="invoices.credit-notes",
         t="A refund is booked as a credit note against the invoice it came from",
         parent="invoices", who="tomasz", labels="invoicing,payments",
         made="07-14 10:00", moves=[("07-15 10:30", "Ready")],
         why="Money going back to a customer is not an invoice with a minus sign in front of "
             "it. It is its own document, with its own number, that points at the invoice it "
             "reverses and carries the same tax rates that invoice carried — because the "
             "quarter the refund lands in and the quarter the invoice landed in are usually not "
             "the same quarter, and the tax has to unwind where it was charged.",
         ok=["A credit note has its own number and names the invoice it reverses",
             "A partial refund credits part of an invoice and leaves the rest owing",
             "The credit note carries the tax rates of the invoice, not today's"],
         says=[("08-25 11:40", "ingrid",
                "Leaving this unsized on purpose until planning. Harbor's refunds story is now "
                "waiting on it, which means the two have to be estimated in the same room: the "
                "half of this that Harbor needs is a credit note produced by a refund, and the "
                "half Bergstrom asked for is a credit note somebody writes by hand against an "
                "invoice nobody is refunding. They may not be the same story.")]),
    dict(a="invoices.recurring", t="Repeat last month's invoice without retyping it",
         parent="invoices", who="priya", labels="invoicing", tags=("customer/bergstrom",),
         made="07-30 11:10", moves=[("07-31 10:20", "Ready")],
         why="Bergstrom's ninety businesses include forty that send the same invoice to the "
             "same customer every month with the date changed. They do it by opening last "
             "month's, editing it and saving it under a new name, which is how two of them "
             "ended up billing March twice.",
         ok=["An invoice can be marked as repeating monthly or quarterly",
             "The repeat is drafted rather than sent, so somebody still looks at it",
             "Stopping the repeat does not touch the invoices it already produced"]),
    dict(a="invoices.reminders", t="Chase a late invoice twice and then stop chasing it",
         parent="invoices", who="ingrid", labels="invoicing",
         made="07-20 11:20", moves=[("07-21 10:40", "Ready"), ("08-18 11:30", "Cancelled")],
         why="An invoice goes unpaid for a fortnight and nobody notices until the quarter is "
             "being closed. A reminder a week after the due date and a second one a fortnight "
             "after that is what a bookkeeper does by hand, badly, when they remember.",
         ok=["A late invoice produces a reminder the business can read before it goes",
             "Reminders stop when the invoice is paid, and stop after the second one either way"],
         says=[("08-18 11:20", "ingrid",
                "Cancelling this rather than carrying it a fourth sprint. Two of the three "
                "accountants we sat with chase late payers by ringing them, and the third does "
                "it from her own mail client with a template she likes better than anything we "
                "would write. Nobody asked for this; we wrote it down because it sounded like "
                "something an invoicing product has. The half worth building is knowing which "
                "invoices are late, and that is already on the invoice list.")]),
    dict(a="invoices.customer-import",
         t="Load Bergstrom Accounting's client list and their payment terms",
         type="task", parent="invoices", who="ola", by="ola", labels="invoicing", pts=3,
         tags=("customer/bergstrom",), made="06-29 10:00", sprint="Sprint 2",
         moves=[("06-30 09:35", "Ready"), ("07-01 13:50", "In progress"),
                ("07-02 11:30", "In review"), ("07-03 09:45", "QA", "tomasz"),
                ("07-03 15:50", "Done", "mateo")],
         why="Ninety businesses, each with its own customers, its own payment terms and its own "
             "idea of what a customer reference looks like, exported from the system Bergstrom "
             "have been using since 2011. Nothing about invoicing can be demonstrated on made-up "
             "customers, and the shape of the real ones is the argument we keep having.",
         ok=["Bergstrom's ninety businesses and their customers are in the vault's demo data",
             "A row that cannot be read stops the import and says which row and why"]),
    dict(a="invoices.same-number", t="Two invoices issued in the same minute get the same number",
         type="bug", parent="invoices", who="tomasz", priority="high", labels="invoicing",
         tags=("regress",), pts=2, made="07-06 14:30", sprint="Sprint 2",
         moves=[("07-06 15:10", "Ready"), ("07-07 09:50", "In progress"),
                ("07-08 15:40", "In review"), ("07-09 10:20", "QA", "mateo"),
                ("07-09 16:10", "Done", "mateo")],
         why="The next number is read, then written, and two issues that overlap read the same "
             "number before either writes it. The sequence is the one thing in the product that "
             "was supposed to be impossible to get wrong, and it is wrong in the ordinary way: "
             "a read and a write with nothing holding them together.",
         ok=["Two invoices issued at the same instant are given two different numbers",
             "The duplicate pair already in the demo data is renumbered and recorded"],
         says=[("07-06 14:40", "mateo",
                "Two invoices, both numbered 2026-0041, issued four seconds apart by the same "
                "business. I found it by clicking issue on two tabs, which is not a thing a "
                "person does on purpose but is exactly what the batch send will do a hundred "
                "times a minute. The sequence is read-then-write with a gap in the middle.")]),
    dict(a="invoices.pdf-total",
         t="The PDF total and the invoice total disagree by one cent on some invoices",
         type="bug", parent="invoices", who="tomasz", priority="normal", labels="invoicing,tax",
         pts=2, made="08-27 11:20", sprint="Sprint 6",
         moves=[("08-27 14:10", "Ready"), ("09-01 09:50", "In progress")],
         why="The invoice screen adds each line's tax and rounds once; the PDF rounds each "
             "line's tax and then adds. On most invoices the two agree, and on an invoice with "
             "seven lines at a reduced rate they are a cent apart — which means the document we "
             "send and the document we keep say different things.",
         ok=["The screen, the PDF and the stored total are computed once and shared",
             "The invoices in the demo data that disagree are listed and corrected"],
         says=[("08-27 11:30", "mateo",
                "A florist in Aalesund noticed before we did, which is the embarrassing part. "
                "Seven lines, two rates, screen says 4 218.60 and the PDF says 4 218.59. It is "
                "not the rounding rule that is wrong, it is that we have two of them.")]),
]

# --- bank import --------------------------------------------------------------------------

BANK = [
    dict(a="bank.connectors", t="Fetch a statement from the three banks our first accountants use",
         parent="bank", who="tomasz", labels="bank-import", tags=("area/api",),
         made="07-13 09:40", sprint="Sprint 3",
         moves=[("07-13 11:30", "Ready"), ("07-14 09:50", "In progress"),
                ("07-21 16:30", "In review"), ("07-22 10:50", "QA", "mateo"),
                ("07-23 15:20", "Done", "mateo")],
         why="Three banks cover every business Bergstrom keep the books for, and each of the "
             "three has its own idea of what a statement is: one paginates by day, one by "
             "transaction, and one will only tell you about the last ninety days and then "
             "silently gives you eighty-nine. One door into all three, and the rest of "
             "Ledgerline never learns which bank a line came from.",
         ok=["A statement can be fetched from each of the three banks for a chosen month",
             "The three banks' answers become one shape before anything else sees them",
             "A bank that stops answering is reported rather than treated as an empty month"]),
    dict(a="bank.connectors.1", t="Speak the first bank's statement API and its ninety-day window",
         type="subtask", parent="bank.connectors", who="tomasz", pts=5, made="07-13 10:20",
         moves=[("07-14 09:55", "Ready"), ("07-14 10:30", "In progress"),
                ("07-16 15:50", "In review"), ("07-17 10:10", "QA", "mateo"),
                ("07-17 15:10", "Done", "mateo")],
         why="Consent, refresh, and a window that is ninety days from the moment you ask rather "
             "than ninety days from the start of a month, which is the difference between a "
             "quarter that imports and a quarter that is one day short at the front."),
    dict(a="bank.connectors.2", t="Read the other two banks' formats through the same door",
         type="subtask", parent="bank.connectors", who="tomasz", pts=3, made="07-13 10:25",
         moves=[("07-15 09:45", "Ready"), ("07-17 09:50", "In progress"),
                ("07-20 16:00", "In review"), ("07-21 10:10", "QA", "mateo"),
                ("07-21 15:30", "Done", "mateo")],
         why="Two more banks behind the shape the first one settled, so that the importer holds "
             "one statement and not three, and adding a fourth bank later is a file rather than "
             "a fortnight."),
    dict(a="bank.csv", t="Import a statement from a CSV file when the bank has no feed",
         parent="bank", who="priya", labels="bank-import", pts=3,
         made="07-13 09:45", sprint="Sprint 3",
         moves=[("07-13 11:35", "Ready"), ("07-15 10:10", "In progress"),
                ("07-20 15:40", "In review"), ("07-21 11:20", "QA", "tomasz"),
                ("07-22 14:40", "Done", "mateo")],
         why="Three banks is not every bank, and the fourth one a business banks with will "
             "always be a small one that exports a CSV and nothing else. Dropping that file on "
             "a page has to produce the same statement the feeds produce, including the part "
             "where the columns are in an order nobody has seen before.",
         ok=["A dropped CSV becomes the same statement shape the bank feeds produce",
             "The columns are mapped by the person importing, and the mapping is remembered",
             "A file that is not a statement is refused before anything is written"]),
    dict(a="bank.dedupe", t="Importing the same statement twice does not produce two of everything",
         parent="bank", who="tomasz", labels="bank-import", tags=("area/api",), pts=5,
         made="07-13 09:50", sprint="Sprint 3",
         moves=[("07-14 11:10", "Ready"), ("07-16 09:45", "In progress"),
                ("07-20 16:20", "In review"), ("07-21 09:40", "In progress", "priya"),
                ("07-22 16:00", "In review"), ("07-23 10:20", "QA", "mateo"),
                ("07-24 14:30", "Done", "mateo")],
         why="Every accountant will import the same month twice, because the first import was "
             "before the last few days landed and because the feed will re-send a month on its "
             "own. Two of every transaction is worse than none: it doubles a business's turnover "
             "and nobody spots it until the quarter will not balance.",
         ok=["A line already imported is recognised and left alone on a second import",
             "A line the bank corrected replaces the old one rather than joining it",
             "The import says how many lines were new and how many it already had"],
         says=[("07-21 09:30", "priya",
                "Sending it back, sorry. Recognising a line by bank reference plus amount plus "
                "date is right until the bank corrects a line, which two of the three do by "
                "re-sending the month with the same reference and a different amount — and then "
                "we keep both. The correction case is in the acceptance and the import treats "
                "it as a new line.")]),
    dict(a="bank.match", t="Match a bank line to the invoice it pays",
         parent="bank", who="tomasz", labels="bank-import,invoicing",
         made="07-16 09:40", sprint=["Sprint 3", "Sprint 4"],
         moves=[("07-16 11:30", "Ready"), ("07-28 09:50", "In progress"),
                ("08-04 16:20", "In review"), ("08-05 10:40", "QA", "mateo"),
                ("08-06 15:10", "Done", "mateo")],
         why="This is the whole point of importing anything. A line of 4 218.60 arriving on the "
             "fourth with the invoice number in its reference is not a puzzle, and a person "
             "should never be shown it. What a person should be shown is the twenty per cent "
             "the machine could not be sure about, which is what the next story is for.",
         ok=["A line whose reference names an invoice is matched to it without being asked",
             "A line that matches an amount and a date but nothing else is offered, not decided",
             "A match can be undone, and undoing it puts the invoice back to unpaid"]),
    dict(a="bank.match.1", t="Match on amount, date and the reference the payer typed",
         type="subtask", parent="bank.match", who="tomasz", pts=5, made="07-27 10:20",
         moves=[("07-28 09:55", "Ready"), ("07-28 10:30", "In progress"),
                ("07-31 15:40", "In review"), ("08-03 10:10", "QA", "mateo"),
                ("08-03 15:20", "Done", "mateo")],
         why="Three signals, weighted: the reference is nearly proof, the exact amount is "
             "strong, and the date is only ever a tiebreak. What comes out is a match with a "
             "confidence attached to it rather than a yes."),
    dict(a="bank.match.2", t="Show the matched pair side by side before it is committed",
         type="subtask", parent="bank.match", who="priya", pts=3, made="07-27 10:25",
         moves=[("07-29 09:45", "Ready"), ("08-03 09:50", "In progress"),
                ("08-04 15:20", "In review"), ("08-05 10:20", "QA", "mateo"),
                ("08-05 15:40", "Done", "mateo")],
         why="The bank line on the left, the invoice on the right, and the three things that "
             "made the machine think they belong together highlighted in both — so that "
             "agreeing with it takes a glance rather than a comparison."),
    dict(a="bank.match-by-hand", t="Match by hand the lines the importer would not guess",
         parent="bank", who="priya", labels="bank-import", tags=("needs-design",), pts=5,
         made="08-10 09:55", sprint="Sprint 5",
         moves=[("08-11 10:30", "Ready"), ("08-12 09:50", "In progress"),
                ("08-18 16:20", "In review"), ("08-19 10:40", "QA", "mateo"),
                ("08-20 15:10", "Done", "mateo")],
         why="One payment covering three invoices, a payment short by the bank's own fee, a "
             "customer who pays two months at once in a round number. This is the screen "
             "Bergstrom will live in for two days at the end of every month, so it has to be "
             "fast under the hands rather than pretty in a screenshot.",
         ok=["A line can be split across several invoices, and the split has to add up",
             "An unmatched line can be booked as something other than a payment",
             "The screen can be worked through with the keyboard alone"]),
    dict(a="bank.sandbox-credentials",
         t="Get sandbox credentials and test statements from the three banks",
         type="task", parent="bank", who="ola", by="ola", labels="bank-import",
         tags=("area/api",), pts=2, made="06-30 15:30", sprint="Sprint 2",
         moves=[("07-01 09:35", "Ready"), ("07-02 13:40", "In progress"),
                ("07-07 11:10", "In review"), ("07-08 09:45", "QA", "tomasz"),
                ("07-08 15:50", "Done", "mateo")],
         why="Two of the three banks take a fortnight to approve a developer account and one of "
             "them wants a registered company number before it will talk at all. Started now "
             "because the sprint that needs them starts on the thirteenth and no amount of "
             "planning shortens a bank's approval queue.",
         ok=["A sandbox account and a test business exist at each of the three banks",
             "The credentials are in the deployment's secret store, not in the repository"]),
    dict(a="bank.nightly-fetch",
         t="Fetch each business's statements overnight instead of when a page is opened",
         type="task", parent="bank", who="ola", by="ola", labels="bank-import", pts=3,
         made="08-10 10:10", sprint="Sprint 5",
         moves=[("08-11 09:40", "Ready"), ("08-13 10:20", "In progress"),
                ("08-17 11:20", "In review"), ("08-18 09:50", "QA", "tomasz"),
                ("08-19 11:40", "Done", "mateo")],
         why="Fetching when somebody opens the page means the first page of the morning takes "
             "eleven seconds and the banks see ninety businesses arrive at nine o'clock. "
             "Overnight, spread out, with the failures visible in the morning rather than in "
             "front of the accountant who was trying to work.",
         ok=["Every connected business is fetched once overnight, spread across the window",
             "A bank that refused is retried and then reported, not silently skipped"]),
    dict(a="bank.sign", t="A refund on the statement is imported as money coming in",
         type="bug", parent="bank", who="tomasz", priority="high", labels="bank-import",
         tags=("regress",), pts=2, made="07-16 14:20", sprint="Sprint 3",
         moves=[("07-16 15:00", "Ready"), ("07-17 09:50", "In progress"),
                ("07-21 15:20", "In review"), ("07-22 09:40", "QA", "mateo"),
                ("07-23 10:50", "Done", "mateo")],
         why="One of the three banks reports a refund as a credit with a transaction code that "
             "says it reverses a debit, and the importer reads the sign and ignores the code. A "
             "business that refunded a customer four hundred appears to have been paid four "
             "hundred, and the month's turnover is eight hundred out.",
         ok=["A reversal is imported with the direction its transaction code says",
             "The demo data's three wrong-way lines are reimported and correct"],
         says=[("07-16 14:30", "mateo",
                "Caught it against the second bank's test statements, which are the only ones "
                "with a reversal in them. Three lines, all credits, all of them reversals of "
                "card refunds, all imported as income. The sign on the amount is right and the "
                "code beside it says the opposite, and we only read the sign.")]),
    dict(a="bank.encoding",
         t="A statement with the bank's own character set imports the names as question marks",
         type="bug", parent="bank", who="tomasz", priority="normal", labels="bank-import",
         tags=("customer/bergstrom",), pts=3, made="08-13 14:30", sprint="Sprint 5",
         moves=[("08-13 15:10", "Ready"), ("08-19 09:50", "In progress"),
                ("08-21 15:40", "In review")],
         why="The third bank's CSV is not UTF-8 and does not say so, and the importer assumes "
             "it is. Every Norwegian and Swedish letter in a payer's name comes through as a "
             "question mark, which means the matcher cannot match on the name and Bergstrom "
             "cannot read the ones it failed on.",
         ok=["A statement file's encoding is detected rather than assumed",
             "A file whose encoding cannot be established is refused with the reason"],
         says=[("08-13 14:40", "mateo",
                "Bergstrom sent us a real month from the third bank, with permission and with "
                "the amounts scrambled, and forty of its four hundred lines have a payer name "
                "full of question marks. It is the same failure as reading a marina's berth "
                "spreadsheet, so I have linked the two — whatever we do here should be the "
                "thing Harbor does as well.")]),
]

# --- tax periods ---------------------------------------------------------------------------

TAX = [
    dict(a="tax.rates", t="Keep the tax rate that applied on the day, not the one that applies now",
         parent="tax", who="tomasz", labels="tax", pts=5, made="08-24 09:40", sprint="Sprint 6",
         moves=[("08-24 11:30", "Ready"), ("08-25 09:50", "In progress"),
                ("08-28 16:10", "In review"), ("08-31 10:20", "QA", "mateo"),
                ("09-01 15:30", "Done", "mateo")],
         why="Rates change on a date somebody in a ministry chose, and every document already "
             "issued keeps the rate it was issued under for as long as it exists. A rate table "
             "with one current value in it is the bug that arrives eighteen months later, when "
             "a credit note against an old invoice quietly uses today's number.",
         ok=["A rate is looked up by the date of the document, not by today",
             "A rate change is entered once, with the date it takes effect",
             "Reissuing a document from last year produces last year's tax"]),
    dict(a="tax.close", t="Close a quarter so nothing can be booked into it afterwards",
         parent="tax", who="tomasz", labels="tax", pts=8, made="08-24 09:45", sprint="Sprint 6",
         moves=[("08-24 11:35", "Ready"), ("09-01 09:50", "In progress")],
         ticks="09-03 15:20", ticked=1,
         why="Closing is the moment the numbers stop being an opinion. After it, an invoice "
             "dated inside the quarter has to be refused rather than accepted quietly, a "
             "correction has to become a document of its own in the open quarter, and the "
             "closing itself has to be undoable by somebody senior and impossible by accident.",
         ok=["A closed quarter refuses any new entry dated inside it, and says why",
             "A correction to a closed quarter becomes a document in the open one",
             "Reopening a quarter is recorded with who did it and why"]),
    dict(a="tax.report", t="The quarterly return an accountant can hand to the tax office",
         parent="tax", who="priya", labels="tax", tags=("needs-design",), pts=5,
         made="08-24 09:50", sprint="Sprint 6",
         moves=[("08-25 10:40", "Ready"), ("08-26 09:50", "In progress"),
                ("09-02 16:20", "In review")],
         why="Bergstrom produce this ninety times a quarter, and today each one is a spreadsheet "
             "assembled by hand from four exports. The report is the boxes the tax office asks "
             "for, each one clickable down to the documents that made the number, because the "
             "question an accountant is asked is never the total but where it came from.",
         ok=["Every box on the return can be opened to the documents behind it",
             "The report can be produced again later and comes out identical",
             "A quarter with an unmatched bank line says so rather than reporting anyway"]),
    dict(a="tax.rounding", t="Round the tax per line or per invoice, whichever the country says",
         parent="tax", who="tomasz", labels="tax",
         made="08-19 11:40", moves=[("08-20 10:30", "Ready")],
         why="Norway rounds the tax on the invoice total and Sweden rounds it line by line, and "
             "on a seven-line invoice the two answers differ by a cent or two. It has to be a "
             "rule of the business's country rather than a habit of whichever function was "
             "written first, and it is the same argument as the PDF total bug.",
         ok=["The rounding rule is a property of the business's country, held in one place",
             "A business's invoices are consistent with each other whichever rule applies"]),
    dict(a="tax.rate-tables", t="Load four years of rate tables for Norway and Sweden",
         type="task", parent="tax", who="ola", by="ola", labels="tax", pts=3,
         made="08-24 10:15", sprint="Sprint 6",
         moves=[("08-25 09:35", "Ready"), ("08-27 10:20", "In progress")],
         why="The rate lookup is only as good as what is in the table, and what is in the table "
             "today is this year's three rates typed in by hand. Four years back covers every "
             "document Bergstrom would ever reissue, and the changes have dates that have to be "
             "read off the ministry's own notices rather than remembered.",
         ok=["Both countries' rates since 2022 are loaded with the dates they took effect",
             "Each rate row says which notice it came from"]),
    dict(a="tax.retention", t="Keep a closed quarter where an auditor can read it in five years",
         type="task", parent="tax", who="ola", by="ola", labels="tax",
         made="08-11 11:20", moves=[("08-12 10:30", "Ready"), ("09-01 11:40", "Cancelled")],
         why="A closed quarter has to still be readable long after the software that produced "
             "it has been rewritten twice, which usually means a file somewhere rather than a "
             "row in a database that has since been migrated.",
         ok=["A closed quarter is written out in a form that outlives the schema",
             "The written form can be read back and checked against the live data"],
         says=[("09-01 11:30", "ola",
                "Folding this into closing the period rather than doing it beside it. Writing "
                "the quarter out is what closing a quarter should mean — a close that leaves no "
                "artefact behind is a flag on a row, and a flag on a row is exactly the thing "
                "an auditor in five years cannot read. Tomasz has put it in that story's "
                "acceptance and I would rather it lived there than here.")]),
    dict(a="tax.quarter-edge",
         t="An invoice dated the last day of the quarter falls into the next one",
         type="bug", parent="tax", who="tomasz", priority="high", labels="tax", pts=2,
         made="08-27 11:10", sprint="Sprint 6",
         moves=[("08-27 14:20", "Ready"), ("08-31 09:50", "In progress"),
                ("09-02 16:00", "In review"), ("09-03 10:40", "QA", "mateo")],
         why="A quarter is held as a start and an end, and the end is compared with a less-than "
             "where it wants a less-than-or-equal. Every invoice issued on 31 March, 30 June, "
             "30 September and 31 December is reported in the quarter after the one it belongs "
             "to, which is four days a year and, for a business that invoices monthly, four "
             "invoices in the wrong return.",
         ok=["An invoice dated the last day of a quarter is reported in that quarter",
             "The demo data's misfiled invoices move to the right quarter when reimported"],
         says=[("08-27 11:20", "mateo",
                "Found it while building the quarter-close scenarios rather than in the wild, "
                "which is luck. Invoice dated 30 June appears in the July-to-September return. "
                "The start of the quarter is inclusive and the end is not, so the two ends of "
                "every quarter disagree about which side the boundary is on.")]),
]

WORK = EPICS + INVOICES + BANK + TAX

ALIASES: dict[str, str] = {PREFIX + spec["a"]: spec["t"] for spec in WORK}

# Both sides of everything with an inverse, so that Harbor's planted one-sided relation
# stays the only one in the vault. `relates` has no inverse and is written once.
RELATIONS = [
    ("07-28 11:20", "tomasz", "bank.match", dict(blocked_by=["bank.connectors"])),
    ("07-28 11:21", "tomasz", "bank.connectors", dict(blocks=["bank.match"])),
    # The bank's CSV and a marina's berth spreadsheet are the same problem wearing two
    # hats: a file a customer exported, in an encoding nobody wrote down.
    ("08-14 10:20", "mateo", "bank.encoding", dict(relates=["harbor.booking.import-berths"])),
    ("08-26 11:10", "priya", "tax.report", dict(blocked_by=["tax.rates"])),
    ("08-26 11:11", "priya", "tax.rates", dict(blocks=["tax.report"])),
    ("09-01 10:30", "tomasz", "invoices.pdf-total", dict(relates=["tax.rounding"])),
    ("09-01 11:35", "ola", "tax.retention", dict(duplicates=["tax.close"])),
    ("09-01 11:36", "ola", "tax.close", dict(duplicated_by=["tax.retention"])),
]


def events() -> list[story.Event]:
    common.leaves_only(WORK, PREFIX)
    out = []
    for index, spec in enumerate(WORK):
        out += common.lifecycle(spec, PROJECT, PREFIX, index)
    out += common.relation_events(RELATIONS, ALIASES, PREFIX)
    return out
