---
doc: epic
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 0
status: approved
owner: user
created: 2026-09-08
updated: 2026-09-08
approved_on: 2026-09-08
supersedes: null
---

# Epic — Capture and Records Foundation

> Written on 2026-09-08 as `00-context.md`, under the old intake contract: record
> the requirement, interpret it in the PRD. The stage 0 contract changed on
> 2026-09-09 to require pros, cons, best practices and alternatives. This
> document was renamed, not retrofitted, because the feature is already past this
> gate and into design. New features use
> [the epic template](../templates/00-epic.template.md).

This epic draws from the product-level intake. The full source, as the user
supplied it, is
[the V1 product definition](../product/intake/2026-09-08-personal-jarvis-v1.md).
Nothing is restated here that lives there.

## Requirement as stated

The sections of the source that define this epic. Reminders, §21, were part of
this epic until 2026-09-08 and now form epic 002.

| § | Topic |
|---|---|
| 7 | Slashit Command Center |
| 8 | Command System, syntax and the V1 command list |
| 9 | Command Discovery |
| 10 | Structured Records, the core V1 feature |
| 11 | Records, the structured view |
| 12 | All Records View |
| 13 | Task Records |
| 19 | Record Detail |
| 20 | Tasks |
| 35 | Confirmation Model |
| 36 | Record Creation Principle |

The user's own words on why this matters:

> Every time Slashit records something, the user should be able to view it as
> structured data. The user should never have to rely exclusively on asking the
> AI "What have I told you?" They can open Records and inspect everything.

> If Slashit can record it, the user can see it. If the user can see it, they can
> control it.

## Product details supplied

| Topic | Detail | Source |
|---|---|---|
| Input model | Commands and plain language both work, and coexist | §3.1 to §3.3 |
| Command syntax | `/command [natural-language arguments]` | §8.1 |
| Discovery | Typing `/` lists commands, typing `/add` filters them | §9 |
| Task fields | Title, due date, priority, recurrence, status, project link, goal link | §20 |
| Records columns | Type, title, date, status | §12 |
| Record detail | Every field, plus creation date and how it was created | §19 |
| Confirmation | Immediate on unambiguous, one question on ambiguous, explicit on destructive | §35 |

## Constraints given

- V1 targets one individual managing their own life, not teams.
- The dashboard supports the command experience rather than replacing it, so the
  command surface is the primary entry point.
- Advanced budgeting, autonomy and integrations are out of V1 entirely.

## Anything the user said not to do

The product non-goals in §41 apply. Specific to this epic: no voice-first input,
no third-party integration ecosystem, no autonomous action taken on the user's
behalf.

## Immediate unknowns

Carried into the PRD as open questions.

| # | Unknown |
|---|---|
| U1 | Which surface ships first, and therefore what "typing `/`" means physically |
| U2 | *Resolved and moved. Reminders are epic 002.* |
| U3 | Whether ₹ is the only currency, which matters once expenses arrive |
| U4 | What accuracy of classification and extraction counts as good enough |
| U5 | Whether project and goal links on a task are in scope here, given those epics land later |
