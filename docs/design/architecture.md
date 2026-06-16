---
title: Architecture
type: design
updated: 2026-06-16
---

# Architecture

Three products, one shared thing underneath them, and a deliberate refusal to share anything else. This page says what that shared thing is, why it is the only one, and what it costs to keep it that way.

![[architecture.svg]]

## Why anything is shared at all

A marina, an accountant and a maintenance company are three customers. They are also, often, the same customer: the marina that takes bookings in Harbor is invoiced by an accountant using Ledgerline, and the crew that services its pontoons works out of Fieldnote. Somebody at that marina should sign in once and see the two of those they pay for.

So one thing is shared, and it is the smallest thing that makes that possible: **a business, the people in it, and what each of them may see.** Everything else — berths, invoices, jobs — belongs to exactly one product and is not visible from the others except through a link somebody made on purpose.

## What is not shared, on purpose

There is no shared customer record. A marina in Harbor and a business in Ledgerline are different rows even when they are the same organisation, because what Harbor knows about a marina — berth count, pontoon layout, shore power — is nothing an accounting product should carry, and merging them would mean the union of two products' opinions about what a customer is.

There is no shared scheduling. Harbor's bookings and Fieldnote's jobs are both "somebody has a slot" and it is a false friend: a berth is booked for nights and a job is booked for hours, one is sold and the other is assigned, and the day we merge them is the day both get worse.

The one place we have deliberately allowed a dependency is money. Harbor and Ledgerline take payment through the same provider and the same internal module, and the reason is written down as a decision rather than left in the code.

## What this costs

Signing in once is the easy half; deciding what somebody may see is not. Permissions live in the shared service and the meaning of a permission lives in each product, so every new role is a change in two places and a conversation about which of them owns the word.

Three products in one repository and one vault means one deployment cadence. Fieldnote cannot ship on Tuesday because Harbor is mid-launch. We have accepted that at six people and it is the first thing that will have to change.

## What is not built

The accounts service is one database table and a session cookie. There is no organisation hierarchy, no invitation flow, and no way for a marina to give its accountant read access to its own bookings — which is the most requested thing that does not exist.
