---
title: Sprint 2
type: sprint
updated: 2026-07-10
starts: 2026-06-29
ends: 2026-07-10
---

# Sprint 2

Card payments end to end on staging

## Retrospective

A guest can pay for a berth on staging: the card is charged when the booking is confirmed, the bank's own page hands the guest back to the right booking, and the provider's reference ends up on the booking so the marina's bookkeeper can match the two. The twenty-minute hold (`HARBOR-30`) went in beside it, which is what stops two people buying the same berth while one of them is typing a card number.

It was not a clean two weeks. The card-payment story (`HARBOR-33`) failed in QA on the Thursday: a declined card rolled back the charge and not the booking, so the berth stayed held for a guest who had not paid — the failure path had been tested by reasoning about it rather than by declining a real sandbox card. On top of that, the double-booking bug (`HARBOR-38`) found on the first day of the sprint took a day and a half because the availability check and the write were two separate reads with nothing between them, and fixing it properly meant changing how a hold is created rather than adding a lock. Ola also found the sandbox keys sitting in the repository (`HARBOR-37`), which is a sprint's worth of unpleasantness we bought ourselves in Sprint 1.

From now on a payment story is not in review until its unhappy half has been run against the provider's sandbox, and QA gets the sandbox account rather than sharing ours. The keys are in the deployment's secret store and the committed ones are rotated.
