---
doc: prd
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 1
status: in-review
owner: user
created: 2026-09-08
updated: 2026-09-08
approved_on: null
supersedes: null
---

# Epic PRD — Capture and Records Foundation

Context: [Intake](./00-context.md) · [Product brief](../../product/product-brief.md) · [V1 epic map](../../product/v1-epic-map.md)

## 1. Problem

A person's life is scattered across a to-do app, a calendar, a notes app, a
spreadsheet and a chat window. Every time something worth keeping shows up, the
user first has to decide where it goes, and that decision is friction paid on
every single capture. The things that lose the coin toss never get recorded at
all.

Assistants that accept anything solve the capture problem and create a worse
one. What the user told them is invisible. The only way to find out what the
system holds is to ask it and hope the answer is complete.

This epic is the product's foundation: one place to say the thing, and a
structured record afterwards that the user can see, search and change.

## 2. Users and jobs

| User | Job to be done | Today's workaround |
|---|---|---|
| The fragmented individual | Record a task or a reminder in under five seconds without choosing an app first | Whichever app is already open, or a note to themselves they never revisit |
| The system-averse | Capture now, organise never | Abandoned productivity systems, then paper |
| Any user, days later | Confirm what the system actually holds, and correct it | Scrolling chat history, or re-asking the assistant |

Jobs served, from the brief: J1 what do I need to do, J5 what have I recorded.

## 3. Goals

| # | Goal | Metric | Baseline | Target | Source |
|---|---|---|---|---|---|
| G1 | Capture is faster than the app it replaces | Median seconds from first keystroke to confirmed record | None, new product | Under 8 s | proposed, needs Q7 |
| G2 | The user trusts what was recorded | Share of created records where the user does not immediately edit or delete | None | Over 90% | proposed, needs Q7 |
| G3 | The user inspects their data rather than only asking | Share of weekly active users who open a records view in a week | None | Over 60% | proposed, needs Q7 |
| G4 | Field extraction inside a command is good enough to rely on | Share of captures where every extracted field is correct without user correction | None | Over 90% | proposed, needs Q7 |

> Assumption: the source sets no numeric targets. Every target above is proposed
> and needs confirmation before this PRD is approved. See Q7.

## 4. Non-goals

- Any record type beyond tasks and reminders. Expenses, memories, events, goals,
  projects and notes are epics 002 and 004 to 007.
- Persistent memory and contextual retrieval. Epic 002 and 003.
- Search across record types. Epic 003. This epic searches records by text only.
- Today and Upcoming views, and the home dashboard. Epic 008.
- Proactive suggestions. Epic 009.
- Linking a task to a project or a goal. Those entities do not exist yet.
- Multi-user, sharing or collaboration of any kind.
- Voice input, offline capture, and importing from other apps.
- **Plain-language capture.** V1 records only what arrives as a command.
  Classifying a bare sentence into a record type is out, and so is conversing
  with Jarvis outside a command. Deferred, not cancelled.
- **Task priority and recurrence.** A task has a title, a due date and a status.
  Nothing else.

## 5. User stories

- **US-1.** As a user, I type a command and my task exists, so that capture costs one line.
- **US-2.** As a user, I type `/` and see what Jarvis can do, so that I do not have to memorise commands.
- **US-3.** As a user, I write the arguments the way I speak, so that I do not have to learn a syntax.
- **US-5.** As a user, I see what Jarvis extracted right after it creates the record, so that I catch a wrong date immediately.
- **US-6.** As a user, I open a list of everything Jarvis has recorded, so that I never have to ask the AI what it holds.
- **US-7.** As a user, I correct or delete anything Jarvis recorded, so that a mistake is not permanent.
- **US-9.** As a user, I type something without a command and Jarvis tells me how to record it, so that I am not left guessing why nothing happened.
- **US-8.** As a user, I get told about a reminder at the time I set, so that setting it was worth doing.

## 6. Functional requirements

### Capture

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-1 | Every capture starts with a command. Input that does not start with `/` creates nothing. | must | US-1 |
| FR-2 | Typing `/` presents the list of available commands, each with a one-line description. | must | US-2 |
| FR-3 | Typing further characters after `/` filters the list to commands whose name contains the typed text. `/add` yields every add command. | must | US-2 |
| FR-4 | A command accepts natural-language arguments and Jarvis extracts the structured fields for that record type from them. | must | US-3 |
| FR-5 | Relative dates and times in input resolve against the user's current date, time and timezone. "tomorrow at 7pm" and "yesterday" resolve to absolute values. | must | US-3 |
| FR-6 | When every required field for the record type is present, Jarvis creates the record without asking anything further. | must | US-1 |
| FR-7 | After creation, Jarvis shows the created record with every extracted field visible, in the same place the user typed. | must | US-5 |
| FR-8 | When a required field cannot be extracted, Jarvis asks exactly one question naming the missing field, and creates the record on the answer. | must | US-5 |
| FR-9 | Input submitted without a command tells the user that Jarvis records through commands, shows how to open the command list, and preserves what they typed so a command can be applied to it without retyping. | must | US-9 |
| FR-10 | *Withdrawn. Plain-language classification is out of V1.* | — | — |
| FR-11 | *Withdrawn. Conversation outside a command is out of V1.* | — | — |
| FR-12 | An unrecognised command name tells the user so and offers the closest matches, and creates nothing. | should | US-2 |

### Records

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-13 | Every record created by any input path is visible in the records view without the user reloading or waiting. | must | US-6 |
| FR-14 | The records view lists all records with type, title, date and status. | must | US-6 |
| FR-15 | The user can filter records by type. | must | US-6 |
| FR-16 | The user can text-search records by title and description. | must | US-6 |
| FR-17 | The user can sort records by created date and by due date. | should | US-6 |
| FR-18 | Opening a record shows every stored field, its creation time, and its origin: command, conversation, or a later edit. | must | US-6 |
| FR-19 | The user can edit any field they supplied, from the record detail. | must | US-7 |
| FR-20 | The user can delete a record, and deletion asks for confirmation naming the record. | must | US-7 |
| FR-21 | An action deleting more than one record states the count and requires explicit confirmation. | must | US-7 |
| FR-22 | Every record stores its origin and creation time at creation, and its last edit time on change. | must | US-6 |

### Tasks

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-23 | A task holds a title, an optional due date, and a status of pending or done. Priority and recurrence are out of V1. | must | US-1 |
| FR-24 | The user can create, complete, edit and delete a task by command and from the records view, with the same result either way. | must | US-1, US-7 |
| FR-25 | `/tasks` lists the user's open tasks, soonest due first. | must | US-1 |
| FR-26 | *Withdrawn. Task recurrence is out of V1.* | — | — |

### Reminders

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-27 | A reminder holds a description, a date and a time, and is one-time or recurring. | must | US-8 |
| FR-28 | A reminder without a time uses a default time the user can change once, in settings. | should | US-8 |
| FR-29 | The user is notified in the application at the reminder's time. | must | US-8 |
| FR-33 | The user is notified by email at the reminder's time. | must | US-8 |
| FR-34 | The user can turn either channel off, and the setting applies to all their reminders. | should | US-8 |
| FR-30 | The user can edit and delete a reminder, including its schedule. | must | US-7 |
| FR-31 | `/reminders` lists upcoming reminders, soonest first. | must | US-8 |
| FR-32 | A reminder whose delivery fails is retried, and a reminder that has still not been delivered is visible as undelivered rather than silently dropped. | must | US-8 |
| FR-35 | When a capture cannot be understood because the model is unavailable or the shared quota is exhausted, the user is told plainly and the input is preserved, never discarded. | must | US-1 |

## 7. Non-functional requirements

| id | Requirement | Number | How it is measured |
|---|---|---|---|
| NFR-1 | The command list appears while the user keeps typing. | Under 100 ms at p95 | Client instrumentation from keypress to list painted |
| NFR-2 | A capture is acknowledged quickly enough that the user does not wait on it. | First visible response under 1.5 s at p95, measured against Gemini free-tier latency | Server timing from submit to first byte of response |
| NFR-3 | A created record appears in the records view without a perceptible gap. | Under 1 s at p95 | Time from record creation to visible in a records query |
| NFR-4 | Field extraction is correct on unambiguous everyday input. | Over 90% of fields correct | Labelled evaluation set, built before build plan approval |
| NFR-5 | *Withdrawn. Plain-language classification is out of V1.* | — | — |
| NFR-6 | Reminders fire on time. | Within 60 s of the scheduled time at p99 | Delivery timestamp against scheduled timestamp |
| NFR-7 | A user's records are never readable by another user, in storage or in a model prompt. | Zero incidents | Authorisation tests on every record path |
| NFR-8 | The records view stays responsive as records accumulate. | Under 1 s at p95 for a user with 10,000 records | Load test |
| NFR-9 | No capture is lost once acknowledged. | Zero acknowledged captures without a record | Reconciliation of acknowledgements against records |
| NFR-10 | Model usage stays inside the shared free-tier quota under expected V1 load. | No user-visible refusal caused by quota exhaustion in normal operation | Requests against the provider limit, tracked daily and at peak |
| NFR-11 | A single user cannot exhaust the shared quota for everyone. | Per-user request cap, value set in the build plan | Requests per user per hour |
| NFR-12 | The model provider sits behind one boundary, so it can be replaced by configuration. | Zero model-provider references outside that boundary | Code review, enforced by a lint rule or an import check |

## 8. Success metrics

Measured thirty days after launch to the first users.

| Metric | Target | Instrumented by |
|---|---|---|
| Captures per active user per week | Needs Q7 | Record creation events, by origin |
| Share of sessions where the user typed without a command and had to restate it as one | Reported, no target. A high number is the case for adding plain language | FR-9 events |
| Share of weekly actives opening a records view | Over 60%, proposed | View events |
| Correction rate within five minutes of creation | Under 10%, proposed | Edit and delete events against creation time |
| Reminder delivery success | Over 99% | Delivery outcomes |
| Week-four retention | Needs Q7 | Cohort activity |

## 9. Dependencies

| Dependency | Type | Owner | Status |
|---|---|---|---|
| Web as the V1 surface | product | user | Settled 2026-09-08 |
| In-app and email notifications | product | user | Settled 2026-09-08 |
| Gemini free tier, shared key in server env | vendor | user | Settled 2026-09-08, see [decision 0001](../../product/decisions/0001-model-provider-gemini-free-tier.md) |
| Gemini free-tier rate limits, read from the provider's current documentation | vendor | Claude | Not started, needed before the build plan sets NFR-11 |
| Gemini free-tier data handling terms | vendor | user | Not read. Blocks launch, not the build. See Q10 |
| Email delivery service | vendor | user | Not chosen, blocks FR-33 in the build plan |
| Account and auth model, Q3 | platform | user | Open, blocks build plan |
| Labelled evaluation set for extraction and classification | internal | Claude, with user-supplied phrasings | Not started, needed before build plan approval |
| Numeric targets for the hypotheses, Q7 | product | user | Open, blocks approval of section 3 |

## 10. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction gets dates subtly wrong, so the user stops trusting capture | high | high | FR-7 shows every extracted field at creation, FR-10 and FR-19 make correction one action, NFR-4 sets a bar before launch |
| Commands-only capture is more friction than the user expects, and capture volume never reaches the level H1 needs | medium | high | FR-2 and FR-3 make the command list the discovery path so nothing must be memorised, FR-9 catches the user who types without a command. Plain language remains available as the first thing to add if H1 misses |
| One shared free-tier key means one shared quota, so one heavy user degrades the product for everyone | high | high | NFR-11 caps per-user requests, NFR-10 tracks headroom, FR-35 makes exhaustion honest rather than silent, a non-model fast path for unambiguous commands is a build plan question |
| Free-tier terms allow user data to improve the provider's products, in a product holding passports and finances | medium | high | Q10 must be answered before launch, not after. If the terms are unacceptable the tier changes or the user is told before their first capture |
| Free-tier models or limits change without notice | medium | medium | NFR-12 keeps the provider behind one boundary, so a switch is configuration |
| Reminders fire late or not at all, which destroys the reason to set them | medium | high | NFR-6 and FR-32, delivery is a build plan question, not an afterthought |
| The epic grows to cover every record type before shipping anything | high | medium | Non-goals list every excluded type explicitly, epic map holds the rest |
| Records view becomes a second, competing way to work, splitting the product | low | medium | Principle 2 in the brief, both paths write the same records |

## 11. Open questions

| # | Question | Blocks | Owner | Answer |
|---|---|---|---|---|
| ~~Q1~~ | Which surface ships first? | design, HLD | user | **Web.** Mobile and desktop are out of V1. |
| ~~Q2~~ | How does a reminder reach the user? | FR-29, design | user | **In-app and email.** No push. Assumption: both ship, user can disable either. |
| ~~Q3~~ | One personal account per user, or workspaces with members? | HLD, data model | user | **One account per user.** No workspaces, no members, no sharing in V1. |
| ~~Q4~~ | Which model provider, at what cost, at what latency? | NFR-2, NFR-4, NFR-10 | user | **Gemini free tier, single key in the server environment.** Recorded as decision 0001. Cost is zero, quota is the constraint. |
| Q10 | Do the Gemini free-tier data handling terms meet the bar for a product holding passports, finances and family details? | launch | user | |
| Q11 | When the shared quota is exhausted, does a capture queue, degrade to a non-model path, or refuse? | FR-35, HLD | user | |
| Q12 | Are we charging users in V1? Free model cost does not settle this by itself. | pricing | user | |
| ~~Q5~~ | Should plain-language capture create records directly, or propose them first? | FR-9, design | user | **Neither. Commands only in V1.** Plain-language capture is deferred. |
| ~~Q6~~ | Are task priority and recurrence needed in V1? | FR-23, FR-26 | user | **No.** Both are out. A task is a title, a due date and a status. |
| Q13 | Task recurrence is out. Are recurring **reminders** also out? They are the same scheduling machinery, so keeping them for reminders spends most of the cost the cut was meant to avoid. | FR-27, HLD | user | |
| Q14 | With conversation out of V1, does `/search` still answer questions in sentences, or only return matching records? Epic 003 owns search, but the answer changes what the command surface is. | epic 003 | user | |
| Q7 | What numeric targets make G1 to G4 and the V1 hypotheses pass or fail? | section 3, section 8 | user | |
| Q8 | Is there a settings surface in this epic at all, for the default reminder time and timezone, or does that wait? | FR-28, scope | user | |
| Q9 | Can the user see and edit records at all when a capture is ambiguous and unanswered, or is the pending question blocking? | FR-8, design | user | |

## 12. Out of scope

Everything in the product non-goals, plus the record types and views assigned to
epics 002 to 009 in the epic map, plus plain-language capture, conversation
outside a command, task priority and task recurrence. Also out: bulk import, data export, offline
capture, undo beyond edit and delete, attachments on records, and any sharing.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-08 | Created from the V1 product definition | First epic of V1 | pending |
| 2026-09-08 | Commands-only capture. FR-1 rewritten, FR-9 repurposed to handle non-command input, FR-10, FR-11, FR-26 and NFR-5 withdrawn, FR-23 reduced to title, due date and status. US-4 dropped, US-9 added. Q3, Q5, Q6 closed. Q13, Q14 opened. | User cut plain language, task priority and task recurrence from V1 | user |
| 2026-09-08 | Surface, notification channels and model provider settled. FR-29 split into FR-33 and FR-34, FR-35 added for quota failure, NFR-10 rewritten from cost to quota, NFR-11 and NFR-12 added, two risks added, Q10 to Q12 opened. | User answered Q1, Q2 and Q4 | user |
