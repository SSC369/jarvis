---
doc: epic-map
title: V1 Epic Map
status: in-review
owner: user
created: 2026-09-08
updated: 2026-09-08
---

# V1 Epic Map

How the [V1 product definition](./intake/2026-09-08-personal-jarvis-v1.md)
breaks into epics. Each epic gets its own folder under `features/` and runs the
five gates independently.

> This decomposition is a proposal. It is `in-review` until the user confirms
> the split and the order.

## Slicing rule

Epics are vertical slices, not layers. Every epic ends with something the user
can do end to end, because the core principle is that anything Jarvis records,
the user can see. An epic that stores records without a way to inspect them
would break that principle on the day it ships.

The consequence: epic 001 carries the foundation and proves it with two record
types. Every epic after it adds record types or capabilities onto a working
loop, which is why they get smaller as the list goes on.

## The epics

| # | Epic | Priority | Covers (source §) | Depends on |
|---|---|---|---|---|
| 001 | Capture and Records Foundation | P0 | Command Center §7, Command System §8, Command discovery §9, Structured Records §10 to §13, Record detail §19, Tasks §20, Reminders §21, Confirmation model §35, Record creation principle §36 | — |
| 002 | Persistent Memory | P0 | Memory §15 to §18 | 001 |
| 003 | Personal Search and Context | P0 | Personal search §27, Contextual intelligence §28 | 001, 002 |
| 004 | Expenses | P1 | Expenses §14, expense summaries | 001 |
| 005 | Events | P1 | Events §22 | 001 |
| 006 | Goals and Projects | P1 | Goals §23, Projects §24, goal-project-task relationships | 001, 003 |
| 007 | Notes | P1 | Notes and Ideas §25 | 001 |
| 008 | Daily Control | P1 | Today's view §29, Upcoming view §30, Home dashboard §32, Navigation §33 | 001, 004, 005, 006 |
| 009 | Proactive Jarvis | P2 | Proactive Jarvis §31, advanced contextual intelligence | 003, 008 |

## Why 001 is first and this shape

The Command Center, the command system and the records store are the product.
Every other epic is a record type or a view layered on them. Tasks and reminders
ride along in 001 rather than waiting, for two reasons: they are the highest
priority record types in the source, and a foundation that has never carried a
real record type twice is not proven. Reminders in particular force the first
scheduling and notification decisions, which are expensive to retrofit.

Memory is second because it is the stated differentiator and because search
in 003 is only interesting once there is memory to search.

## Deferred out of V1

Cut by the user on 2026-09-08, recorded here so the epic map does not silently
regrow them.

| Cut | Was part of | Why it goes |
|---|---|---|
| Plain-language capture, §3.3 | 001 | V1 captures through commands only |
| Life Inbox, §26 | 007 | It is capture without choosing a type, which commands-only forbids. It returns with plain language or not at all |
| Task priority and recurrence, §20 | 001 | Cost out of proportion to V1 |

## Sequencing note

Epics 004, 005 and 007 are near-identical in shape once 001 exists: a new record
type, its command set, its fields, its list view. They can run in any order, or
in parallel, once the foundation is approved. 008 needs the record types it
displays, so it lands after them.

## Open questions

| # | Question | Blocks |
|---|---|---|
| Q1 | Is this the right split, and is 001 the right first epic? | all |
| Q2 | Should tasks and reminders be pulled out of 001 into their own epic, accepting that 001 then ships without a proven record type? | 001 |
| Q3 | What is the V1 build window, and does anything need to be cut from V1 to hit it? | sequencing |

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-08 | Created | V1 product definition supplied | pending |
| 2026-09-08 | Epic 007 reduced to Notes. Life Inbox, plain-language capture, task priority and recurrence recorded as deferred. | User cut scope | user |
