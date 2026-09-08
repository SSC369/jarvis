---
doc: product-brief
title: Jarvis Product Brief
status: in-review
owner: user
created: 2026-09-08
updated: 2026-09-08
---

# Personal Jarvis — Product Brief

The standing context every feature inherits. Read this before drafting any PRD.

Source: [V1 product definition](./intake/2026-09-08-personal-jarvis-v1.md),
supplied 2026-09-08. Where this brief states something the source does not, it
is marked as an assumption.

## 1. What Jarvis is

Personal Jarvis is a command-first AI personal operating system. The user
records tasks, reminders, expenses, memories, events, goals, projects and notes
by typing a command or speaking plainly, and every one of them becomes a
structured record the user can browse, search, edit and delete. Jarvis uses that
accumulated context to answer questions about the user's own life.

**Promise.** Tell Jarvis what matters. Jarvis remembers it, organizes it, and
helps you act on it.

**Positioning.** Not another AI chatbot. An AI-powered personal command center
that remembers and organizes your life.

## 2. Who it is for

| Segment | Who they are | What they are trying to do | Why today is hard |
|---|---|---|---|
| The fragmented individual | One person carrying personal and professional responsibilities, goals, projects, recurring tasks, expenses and important dates | Keep one place for everything in their life and get it back when they need it | Their life is split across notes, calendar, reminders, expense trackers, to-do apps, spreadsheets, email and chat. Every capture starts with "where should I put this?" |
| The system-averse | People who dislike maintaining complex productivity systems | Capture without deciding on a taxonomy first | Existing tools ask for structure up front and decay when the user stops maintaining them |

V1 targets a single individual managing their own life. Teams are not a V1
audience.

## 3. Product pillars

Every feature must serve at least one. A feature serving none is a signal to
reconsider it.

| # | Pillar | What it means | What it rules out |
|---|---|---|---|
| P1 | Capture without deciding | The user says the thing. Jarvis works out what kind of thing it is. Commands give explicit intent, plain language gives flexibility, both work. | Mandatory category pickers, rigid CLI syntax, forms as the primary input |
| P2 | Everything recorded is visible | Every item Jarvis creates appears as a structured record the user can inspect, search, edit and delete. | An opaque assistant whose memory can only be interrogated by asking it |
| P3 | Context accumulates and pays back | Information given once is used later, across conversations, and connected to related items without the user restating it. | Stateless chat, per-session memory, manual relationship management |
| P4 | The user is in control | View, search, edit, delete and forget are always available. Destructive actions confirm. | Silent retention, unforgettable memory, irreversible bulk actions |

## 4. Principles

Standing rules for every feature, so each PRD does not restate them.

| # | Principle | Source |
|---|---|---|
| 1 | If Jarvis can record it, the user can see it. If the user can see it, they can control it. | Core V1 principle, §44 |
| 2 | AI is the interface for creating and querying. Structured views are the interface for inspecting and managing. Neither is a separate source of truth. | §34 |
| 3 | Minimize confirmation. Create immediately when the input is unambiguous, ask one question when it is not, always confirm destructive actions. | §35 |
| 4 | Proactive behaviour is relevant, limited, actionable and non-intrusive. Quality over frequency. | §31 |
| 5 | Every record carries its origin and creation time, so the user can see why it exists. | §19, §36 |
| 6 | Model cost and latency are product decisions, budgeted per feature. | proposed |
| 7 | User data never crosses a user boundary, in storage or in a prompt. | proposed |

> Assumption: principles 6 and 7 are proposed defaults, not stated in the source.
> Confirm or strike them.

## 5. Core user jobs

Jarvis answers six questions.

| # | Question | Served by |
|---|---|---|
| J1 | What do I need to do? | Tasks, Reminders |
| J2 | What do I need to remember? | Memory |
| J3 | What is happening? | Events, Upcoming |
| J4 | What am I working toward? | Goals, Projects |
| J5 | What have I recorded? | Records |
| J6 | What do I already know? | Personal search, contextual retrieval |

## 6. Core entities

One user owns everything. Entities may relate to each other.

```
User
 ├── Tasks          ├── Memories      ├── Projects
 ├── Reminders      ├── Events        ├── Notes / Ideas
 ├── Expenses       ├── Goals         └── Conversations
```

Known relationships: a task may belong to a project or a goal, a project may
serve a goal. Others emerge per feature.

## 7. The core loop

```
Capture (command or chat) → Understand → Record / Remember / Act
        → Structured data → Records (search, edit, review)
        → Context accumulates → Jarvis helps → Capture
```

## 8. V1 scope

Eleven capability areas, prioritised in the source at §40 and grouped into
epics in [the V1 epic map](./v1-epic-map.md).

| Priority | Capabilities |
|---|---|
| P0 | Command Center, Command System, Structured Records, Persistent Memory, Tasks, Reminders, Personal Search, Context Awareness |
| P1 | Expenses, Events, Today's View, Upcoming View, Goals, Projects, Notes and Ideas, Life Inbox, Memory Management |
| P2 | Proactive Suggestions, Advanced Contextual Intelligence |

## 9. Product non-goals

V1 does not attempt to be a fully autonomous Jarvis. Feature PRDs inherit these.

- Email management
- Banking integrations and automatic financial transactions
- Health integrations
- Smart-home control
- Autonomous purchasing
- Social networking
- Full document management
- Advanced financial planning and budgeting
- Voice-first assistant
- A large third-party integration ecosystem
- Complex multi-agent workflows
- Fully autonomous decision-making
- Teams, sharing and collaboration

These may be revisited once the core product is validated.

## 10. Success criteria

V1 exists to test three hypotheses. Targets are proposed and need confirmation
before the first PRD is approved.

| # | Hypothesis | Signal | Proposed target |
|---|---|---|---|
| H1 | Users will record their life in Jarvis | Capture commands per active user per week | Needs a number, see Q7 |
| H2 | Users will inspect their structured data | Share of active users who open a records view weekly | Needs a number, see Q7 |
| H3 | Persistent context creates recurring value | Retrieval actions per user per week, and week-four retention | Needs a number, see Q7 |

> Assumption: the source states the hypotheses but sets no numbers. Every metric
> above is unusable until Q7 is answered.

## 11. Platform baseline

| Area | Decision |
|---|---|
| Surfaces | Not yet decided, see Q1 |
| Stack | Not yet decided |
| Auth and account model | Not yet decided, see Q3 |
| Model providers | Not yet decided, see Q4 |
| Data stores | Not yet decided |
| Notification delivery | Not yet decided, see Q2 |
| Hosting | Not yet decided |

Each becomes a decision record in `decisions/` once settled, at the build plan
of the feature that first needs it.

## 12. Business model

| Question | Answer |
|---|---|
| Pricing shape | Not yet decided, see Q5 |
| Free tier | Not yet decided |
| Metered unit | Not yet decided |
| Cost ceiling per user per month | Not yet decided, see Q4 |

## 13. Open questions

| # | Question | Blocks | Owner |
|---|---|---|---|
| Q1 | Which surface ships first: web, mobile, desktop, or a mix? | design, HLD | user |
| Q2 | How do reminder notifications reach the user: push, email, in-app only? | PRD, HLD | user |
| Q3 | One personal account per user, or workspaces with members? | HLD, data model | user |
| Q4 | Which model providers, at what cost ceiling per user per month, at what latency budget? | HLD | user |
| Q5 | Pricing shape and metered unit? | brief | user |
| Q6 | Currency and locale: is ₹ the only currency in V1? | PRD | user |
| Q7 | What numeric targets make each V1 hypothesis pass or fail? | PRD metrics | user |
| Q8 | Is offline capture required, and is data export a V1 promise? | PRD, HLD | user |
| Q9 | How long is the V1 build window, and is there a launch date to hit? | epic sequencing | user |

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-08 | Created as skeleton | Process bootstrap | — |
| 2026-09-08 | Filled from the V1 product definition | User supplied the product | pending |
