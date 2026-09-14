---
doc: epic
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 0
status: approved
owner: user
created: 2026-09-08
updated: 2026-09-14
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
this epic until 2026-09-08 and now form epic 003.

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
| U2 | *Resolved and moved. Reminders are epic 003.* |
| U3 | Whether ₹ is the only currency, which matters once expenses arrive |
| U4 | What accuracy of classification and extraction counts as good enough |
| U5 | Whether project and goal links on a task are in scope here, given those epics land later |

## Addendum, 2026-09-13: task lateness

This doc predates the pros/cons/alternatives contract (see the note under the
title), so this is argued here directly rather than retrofitted into a section
that does not exist above.

The design (`02-design.md`, records list) drew overdue styling on the task list
before this was argued anywhere. The user approved adding it, so the argument
is made now, after the fact, rather than left unrecorded.

**Pro.** A task past its due date and undone is exactly the information a
records view exists to surface (per the epic's own line: "if Slashit can record
it, the user can see it"). It costs nothing to store: overdue is derived from a
due date and a status Slashit already has, not a new field.

**Con.** The PRD explicitly scoped a task down to title, due date and status,
cutting priority and recurrence (§4, non-goals). Lateness is adjacent scope
creep on a deliberately minimal entity, and it implies a visual state (a color,
a label) that needs its own accessibility treatment, per `02-design.md` §7.

**Decision.** In scope, as `FR-43` in `01-prd.md`. The con is accepted because
the cost is purely presentational: no new stored field, no new command, no new
extraction behaviour.

## Addendum, 2026-09-14: capture history and loading feedback

Argued directly, same treatment as the 2026-09-13 lateness addendum above: this
doc predates the pros/cons contract, so the argument is made here rather than
retrofitted into a section that does not exist.

**Capture history.** Nothing today distinguishes an answered, discarded or
refused capture turn from one that never happened: `pending_captures` (FR-8,
FR-37) holds a question only until it is answered, and the frontend's in-memory
turn list is lost on reload. Nothing persists what was typed or what happened
to it once resolved.

Pro: a persisted turn log costs one small table and gives the user a record of
what they asked and what came of it, useful when a capture was refused (FR-35)
or a task was found weeks later against wording nobody remembers typing.

Con: widens the capture domain for a capability not asked for at launch, and a
turn is not itself a record type FR-13 to FR-22 already cover, so it needs its
own light entity rather than reusing `tasks` or `pending_captures`.

Decision: in scope, as FR-44 and FR-45 in `01-prd.md`. A session-only history
(kept only in browser memory, gone on reload) was considered and rejected: it
defeats the purpose of a history view, which is to survive exactly the reload
that clears it.

**Loading feedback.** The design (`02-design.md` §4) already gives the Command
Center a loading state for the first capture, and Records and Record detail a
loading state for their initial fetch. Nothing covers the moment between a
click and a response for two interactions approved earlier: saving a task's
edit form, which is the one control FR-19 and FR-24 both save through today,
and answering a pending question (FR-37). Today the user sees nothing happen
until the result appears.

Checked against the actual `RecordEditForm` while drafting this: due date
renders read-only there, not as an editable field, and a `completeTask`
mutation exists with no UI calling it — completion happens by setting status
to Done in the same form. FR-19's "any field the user supplied" is therefore
not fully built yet for due date. That gap is real but is not this
addendum's to fix; FR-46 below covers the one Save action that exists, not
the fields it does not yet let the user change.

Pro: this only extends a pattern the PRD already approved for capture to the
two interactions that currently give no feedback at all. It changes no data,
no contract, no requirement already locked.

Con: none material.

Decision: in scope, as FR-46.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-14 | Both "epic 002" references (Reminders) renumbered to "epic 003" | Epic 002, Authentication, inserted ahead of it; `product/v1-features.md` renumbered 002 to 010 as 003 to 011 on 2026-09-14 | user |
| 2026-09-14 | Addendum added, arguing capture history and loading feedback. `01-prd.md` FR-44 to FR-46 and US-11 added in the same change | User asked for a history action on the Capture page and loading feedback on in-flight edits, and to add both as a fourth slice of this feature | user |
| 2026-09-13 | Addendum added, arguing task lateness after the design drew it. `01-prd.md` FR-43 added in the same change | User approved overdue styling while reviewing the design canvas | user |
