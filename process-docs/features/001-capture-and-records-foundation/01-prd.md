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
| The fragmented individual | Record a task in under five seconds without choosing an app first | Whichever app is already open, or a note to themselves they never revisit |
| The system-averse | Capture now, organise never | Abandoned productivity systems, then paper |
| Any user, days later | Confirm what the system actually holds, and correct it | Scrolling chat history, or re-asking the assistant |

Jobs served, from the brief: J1 what do I need to do, J5 what have I recorded.

## 3. Goals

| # | Goal | What we measure |
|---|---|---|
| G1 | Capture is faster than the app it replaces | Median seconds from first keystroke to confirmed record |
| G2 | The user trusts what was recorded | Share of created records the user does not immediately edit or delete |
| G3 | The user inspects their data rather than only asking | Share of weekly active users who open a records view in a week |
| G4 | Field extraction inside a command is good enough to rely on | Share of captures where every extracted field is correct without user correction |

**No targets are set, by decision on 2026-09-08.** V1 has no users, so any target
would be invented. Each goal is instrumented from day one and the numbers are
read once real usage exists. Targets get set then, against a baseline that
actually happened.

This is a deliberate trade. Without a target, a result cannot fail, only inform.
That is acceptable while the question is "what does usage look like" rather than
"did we hit the bar". It stops being acceptable the moment a decision to keep
building or stop rests on these numbers.

The engineering numbers in section 7 are a different thing and stay. A
non-functional requirement without a number cannot be tested, so those are
build targets, not success bets.

## 4. Non-goals

- Any record type beyond tasks. **Reminders moved to epic 002.** Expenses,
  memories, events, goals, projects and notes are epics 003 to 008.
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
- **US-8.** *Moved to epic 002 with reminders.*

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

### Settings

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-27 | The user has a settings surface holding their timezone. | must | US-3 |
| FR-28 | Timezone is detected from the browser on first use and can be changed by the user. A change applies to how future input is resolved, and never rewrites dates already stored. | must | US-3 |

### Failure

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-35 | When a capture cannot be completed because the model is unavailable or the shared quota is exhausted, Jarvis refuses the capture, says plainly why and that it is temporary, and preserves what the user typed. Nothing is recorded half-formed. | must | US-1 |

## 7. Non-functional requirements

| id | Requirement | Number | How it is measured |
|---|---|---|---|
| NFR-1 | The command list appears while the user keeps typing. | Under 100 ms at p95 | Client instrumentation from keypress to list painted |
| NFR-2 | A capture is acknowledged quickly enough that the user does not wait on it. | First visible response under 1.5 s at p95, measured against Gemini free-tier latency | Server timing from submit to first byte of response |
| NFR-3 | A created record appears in the records view without a perceptible gap. | Under 1 s at p95 | Time from record creation to visible in a records query |
| NFR-4 | Field extraction is correct on unambiguous everyday input. | Over 90% of fields correct | Labelled evaluation set, built before build plan approval |
| NFR-5 | *Withdrawn. Plain-language classification is out of V1.* | — | — |
| NFR-6 | *Moved to epic 002 with reminders.* | — | — |
| NFR-7 | A user's records are never readable by another user, in storage or in a model prompt. | Zero incidents | Authorisation tests on every record path |
| NFR-8 | The records view stays responsive as records accumulate. | Under 1 s at p95 for a user with 10,000 records | Load test |
| NFR-9 | No capture is lost once acknowledged. | Zero acknowledged captures without a record | Reconciliation of acknowledgements against records |
| NFR-10 | Model usage stays inside the shared free-tier quota under expected V1 load. | No user-visible refusal caused by quota exhaustion in normal operation | Requests against the provider limit, tracked daily and at peak |
| NFR-11 | A single user cannot exhaust the shared quota for everyone. | Per-user request cap, value set in the build plan | Requests per user per hour |
| NFR-12 | The model provider sits behind one boundary, so it can be replaced by configuration. | Zero model-provider references outside that boundary | Code review, enforced by a lint rule or an import check |

## 8. Success metrics

Instrumented from launch, reported weekly, no targets set. See section 3.

| Metric | Instrumented by | What it tells us |
|---|---|---|
| Captures per active user per week | Record creation events | Whether the capture habit forms at all |
| Captures by command name | Record creation events | Which commands earn their place, and which are dead weight |
| Sessions where the user typed without a command | FR-9 events | The cost of the commands-only cut. A high number is the case for adding plain language |
| Weekly actives opening a records view | View events | Whether structured data is inspected or ignored |
| Corrections within five minutes of creation | Edit and delete events against creation time | Whether extraction is trusted |
| Week-four retention by signup cohort | Cohort activity | Whether accumulated context brings people back |
| Captures refused for quota or provider outage | FR-35 events | Whether the free tier can carry the product |

Quota refusals keep a count rather than a target. A refusal is a defect the
shared key made unavoidable, not a disappointing result.

## 9. Dependencies

| Dependency | Type | Owner | Status |
|---|---|---|---|
| Web as the V1 surface | product | user | Settled 2026-09-08 |
| In-app and email notifications | product | user | Settled 2026-09-08 |
| Gemini free tier, shared key in server env | vendor | user | Settled 2026-09-08, see [decision 0001](../../product/decisions/0001-model-provider-gemini-free-tier.md) |
| Gemini free-tier rate limits, read from the provider's current documentation | vendor | Claude | Not started, needed before the build plan sets NFR-11 |
| Gemini free-tier data handling terms | vendor | user | Not read. Blocks launch, not the build. See Q10 |
| Resend for email, Celery for background jobs | vendor | user | Settled 2026-09-08. Used by epic 002, not by this epic |
| One account per user | platform | user | Settled 2026-09-08 |
| Stack: FastAPI, PostgreSQL, React, Vite, Turborepo, MobX, shadcn/ui | platform | user | Settled 2026-09-08, see [decision 0002](../../product/decisions/0002-v1-technology-stack.md) |
| Labelled evaluation set for extraction and classification | internal | Claude, with user-supplied phrasings | Not started, needed before build plan approval |
| Numeric targets for the hypotheses | product | user | Deferred by decision, 2026-09-08. Not a blocker |

## 10. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction gets dates subtly wrong, so the user stops trusting capture | high | high | FR-7 shows every extracted field at creation, FR-10 and FR-19 make correction one action, NFR-4 sets a bar before launch |
| Commands-only capture is more friction than the user expects, and capture volume never reaches the level H1 needs | medium | high | FR-2 and FR-3 make the command list the discovery path so nothing must be memorised, FR-9 catches the user who types without a command. Plain language remains available as the first thing to add if H1 misses |
| One shared free-tier key means one shared quota, so one heavy user degrades the product for everyone | high | high | NFR-11 caps per-user requests, NFR-10 tracks headroom, FR-35 makes exhaustion honest rather than silent, a non-model fast path for unambiguous commands is a build plan question |
| Free-tier terms allow user data to improve the provider's products, in a product holding passports and finances | medium | high | Q10 must be answered before launch, not after. If the terms are unacceptable the tier changes or the user is told before their first capture |
| Free-tier models or limits change without notice | medium | medium | NFR-12 keeps the provider behind one boundary, so a switch is configuration |
| Splitting reminders out leaves 001 without the notification machinery, and epic 002 inherits all of the scheduling risk at once | medium | medium | 001 still ships a usable product on its own. Epic 002 carries scheduling, delivery and retry as its whole scope, which is the reason for the split |
| The epic grows to cover every record type before shipping anything | high | medium | Non-goals list every excluded type explicitly, epic map holds the rest |
| Records view becomes a second, competing way to work, splitting the product | low | medium | Principle 2 in the brief, both paths write the same records |

## 11. Open questions

| # | Question | Blocks | Owner | Answer |
|---|---|---|---|---|
| ~~Q1~~ | Which surface ships first? | design, HLD | user | **Web.** Mobile and desktop are out of V1. |
| ~~Q2~~ | How does a reminder reach the user? | epic 002 | user | **In-app and email.** No push. Both ship, user can disable either. Carried to epic 002. |
| ~~Q3~~ | One personal account per user, or workspaces with members? | HLD, data model | user | **One account per user.** No workspaces, no members, no sharing in V1. |
| ~~Q4~~ | Which model provider, at what cost, at what latency? | NFR-2, NFR-4, NFR-10 | user | **Gemini free tier, single key in the server environment.** Recorded as decision 0001. Cost is zero, quota is the constraint. |
| Q10 | Do the Gemini free-tier data handling terms meet the bar for a product holding passports, finances and family details? | launch | user | |
| ~~Q11~~ | When the shared quota is exhausted, does a capture queue, degrade, or refuse? | FR-35 | user | **Refuse, with an honest message.** No silent queueing, no half-formed record. FR-35 rewritten. |
| ~~Q12~~ | Are we charging users in V1? | pricing | user | **No.** Not charging for now. |
| ~~Q5~~ | Should plain-language capture create records directly, or propose them first? | FR-9, design | user | **Neither. Commands only in V1.** Plain-language capture is deferred. |
| ~~Q6~~ | Are task priority and recurrence needed in V1? | FR-23, FR-26 | user | **No.** Both are out. A task is a title, a due date and a status. |
| ~~Q13~~ | Are recurring reminders also out? | epic 002 | user | **In.** Reminders keep recurrence. Carried to epic 002 along with the scheduling machinery it needs. |
| Q14 | With conversation out of V1, does `/search` still answer questions in sentences, or only return matching records? Epic 004 owns search, but the answer changes what the command surface is. | epic 004 | user | |
| ~~Q7~~ | What numeric targets make G1 to G4 pass or fail? | section 3 | user | **Deferred.** No targets in V1. Instrument everything, set targets once there is real usage. |
| ~~Q8~~ | Is there a settings surface in this epic? | FR-27, scope | user | **Yes.** Timezone lives here, in FR-27 and FR-28. The default reminder time goes to epic 002 with reminders. |
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
| 2026-09-08 | Reminders split out into epic 002. FR-27 to FR-34 and NFR-6 removed from this epic, US-8 moved. Settings added as FR-27 and FR-28 for timezone. FR-35 rewritten to refuse honestly on quota exhaustion. Q8, Q11, Q12, Q13 closed. | User split the epic and settled the stack | user |
| 2026-09-08 | Numeric targets removed from goals and success metrics. Metrics are instrumented without targets. Engineering numbers in section 7 unchanged. Q7 closed as deferred. | User deferred targets until real usage exists | user |
| 2026-09-08 | Commands-only capture. FR-1 rewritten, FR-9 repurposed to handle non-command input, FR-10, FR-11, FR-26 and NFR-5 withdrawn, FR-23 reduced to title, due date and status. US-4 dropped, US-9 added. Q3, Q5, Q6 closed. Q13, Q14 opened. | User cut plain language, task priority and task recurrence from V1 | user |
| 2026-09-08 | Surface, notification channels and model provider settled. FR-29 split into FR-33 and FR-34, FR-35 added for quota failure, NFR-10 rewritten from cost to quota, NFR-11 and NFR-12 added, two risks added, Q10 to Q12 opened. | User answered Q1, Q2 and Q4 | user |
