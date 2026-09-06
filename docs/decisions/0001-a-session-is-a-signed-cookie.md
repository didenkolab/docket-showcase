---
title: A session is a signed cookie
type: decision
status: accepted
date: 2026-01-08
updated: 2026-08-31
example: true
---

# ADR-0001 — A session is a signed cookie

This is the template's worked example. It is invented, and it is here to show what a decision
looks like rather than to be kept — delete it, or write over it with the first real one. What it
is trying to demonstrate is that the useful part of a decision is the two sections either side of
the choice: the alternatives that were live, and the price that was paid.

## Context

`HARBOR-12`, the login redirect loop, took two hours to fix and two days to argue about, and the
argument was not about the bug. It was about where a session is validated. The fix worked in the
web front end and failed behind the job runner, because the two had grown different answers to
"is this request signed in", and neither answer was written down anywhere.

There are three places a request can arrive — the browser, the job runner, and whatever we add
next — and a session has to mean the same thing in all of them. It also has to survive a restart,
because [[Sprint 1]] was the fortnight in which somebody who has never seen this project can sign
in and stay signed in for a week, and a session that lives in one process's memory does not
survive a deploy on a Tuesday afternoon.

Nothing here forces a choice about how long a session may live. That question is `HARBOR-9` and it
is deliberately left open below.

## Decision

**A session is a signed cookie. It carries the account id and an expiry, it is signed with a key
the server holds, and it is validated by checking the signature.**

Nothing is looked up to answer "is this request signed in". Every place a request can arrive can
answer the question with the key and the cookie in front of it, which is what makes the three
answers the same answer instead of three implementations that agree until they do not.

The cookie is `HttpOnly`, `Secure` and `SameSite=Lax`, so the browser will not hand it to a
script and will not send it on a cross-site form post. It carries the account id and nothing
else — no display name, no role, no preferences — because everything in it is a copy of a fact
that lives in the database, and a copy in a cookie is a copy nobody can update.

## What this costs

**A session cannot be ended before it expires.** There is nothing to delete, because there is
nothing stored. Signing somebody out clears the cookie in their browser and does not invalidate
the one they may have copied somewhere, and locking an account does not stop a session that is
already running. The remedy is rotating the signing key, which ends every session at once, and
that is a blunt instrument we will reach for perhaps twice.

That is the cost, it is the whole cost, and it is the reason this decision is worth writing down:
the day somebody needs to eject one person immediately, the answer will be that we cannot, and
this page is where they should find out why rather than discovering it under pressure.

**The expiry is now load-bearing.** With no store, the only thing limiting a session's life is
the number inside it, so choosing that number stops being a preference and becomes the whole
revocation story. `HARBOR-9` is where it gets chosen, and until it is chosen the value is short on
purpose.

**Key rotation is a real operation.** It needs two keys accepted and one key issued, for at least
as long as the longest session, or every signed-in person is thrown out at once. That is a small
amount of work nobody has done yet.

## Alternatives considered

**A sessions table, with the cookie holding an id.** The ordinary answer, and the one that gives
instant revocation: delete the row and the session is over. Rejected because every request then
costs a read, and because the job runner would need the same database connection as the front
end to answer a question that is not about its work. The revocation we would gain is worth less,
today, than the coupling we would pay for it — and this is the alternative to revisit first if
the cost above ever bites.

**A token in local storage instead of a cookie.** Avoids the cross-site question entirely and is
what a front end framework will suggest. Rejected because local storage is readable by any script
on the page, so one injected script is every session, whereas an `HttpOnly` cookie is not
readable at all.

**An identity provider, and no sessions of our own.** The right answer eventually and the wrong
one now: it is a dependency to configure, an outage we do not control, and a sign-up flow we
would have to build against before we know what our accounts are. Worth reopening when there is
a second application to sign into, which is the point at which it starts paying for itself.
