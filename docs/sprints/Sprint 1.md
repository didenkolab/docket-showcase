---
title: Sprint 1
type: sprint
starts: 2026-01-05
ends: 2026-01-16
updated: 2026-01-16
example: true
---

# Sprint 1

The goal: somebody who has never seen this project can sign in, and stay signed in for a week
without being asked again. Not the whole of accounts — no password reset, no second factor — only
the path from an empty browser to a session that survives a restart. If that works end to end,
the sprint did what it was for, whatever else moved.

We pulled four tasks and cut one on the second day. `HARBOR-9`, remembering the device between
sessions, went back to the backlog because it needs a decision about how long a session may live
that nobody here is in a position to make yet. Written down as a question is better than
half-built.

Thirteen points pulled, eight finished, and the eight were the four smallest — worth remembering
the next time somebody argues that a 5 is really a 3.

What actually happened: `HARBOR-12`, the redirect loop, was two hours of work and two days of
disagreement about where a session is validated. That argument is why the session model is written
down under `docs/` now, and having it once is cheaper than having it again in the next sprint.
`HARBOR-13` is carried into Sprint 2 — not because it was hard, but because it was picked up on the
last afternoon and should not have been started at all.

The one thing to do differently: estimate before pulling, not after. Two of the four tasks were
estimated on the Wednesday, by which point the number was a description rather than a decision.

Nothing here lists what was in this sprint. Each task carries `sprint: "[[Sprint 1]]"`, so the
backlinks of this page are its contents.
