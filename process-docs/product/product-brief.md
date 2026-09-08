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
| P1 | Capture without deciding | The user says the thing in one line and it is recorded. | Mandatory category pickers, rigid CLI syntax, forms as the primary input |
| P2 | Everything recorded is visible | Every item Jarvis creates appears as a structured record the user can inspect, search, edit and delete. | An opaque assistant whose memory can only be interrogated by asking it |
| P3 | Context accumulates and pays back | Information given once is used later, across conversations, and connected to related items without the user restating it. | Stateless chat, per-session memory, manual relationship management |
| P4 | The user is in control | View, search, edit, delete and forget are always available. Destructive actions confirm. | Silent retention, unforgettable memory, irreversible bulk actions |

> **P1 is partly deferred in V1.** The user decided on 2026-09-08 that V1
> captures through commands only. Picking `/add-task` is still the user deciding
> the type, so V1 delivers the smaller half of this pillar: one place instead of
> six apps. The larger half, saying a thing and having Jarvis work out what it
> is, waits. This is a deliberate cut, not an oversight, and it is the first
> thing to revisit if capture volume disappoints.

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
| P1 | Expenses, Events, Today's View, Upcoming View, Goals, Projects, Notes and Ideas, Memory Management |
| P2 | Proactive Suggestions, Advanced Contextual Intelligence |
| Deferred | Plain-language capture (§3.3), Life Inbox (§26), task priority and recurrence |

Cut from V1 on 2026-09-08. The Life Inbox is frictionless capture without
choosing a type, so it cannot exist while capture is commands-only. It returns
with plain-language capture or not at all.

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

| Area | Decision | Settled |
|---|---|---|
| Account model | One account per user. No workspaces, no members, no sharing. | 2026-09-08 |
| Surfaces | Web. V1 ships as a web application. Mobile and desktop are not V1. | 2026-09-08 |
| Notification delivery | In-app notifications and email. No push, no SMS. | 2026-09-08 |
| Model provider | Google Gemini, free tier, through a single API key held in the server environment. See [decision 0001](./decisions/0001-model-provider-gemini-free-tier.md). | 2026-09-08 |
| Stack | Not yet decided |  |
| Auth and account model | Not yet decided, see Q3 |  |
| Data stores | Not yet decided |  |
| Hosting | Not yet decided |  |

The undecided rows become decision records in `decisions/` at the build plan of
the feature that first needs them.

> Assumption: "in-app notifications or email" is read as both channels shipping,
> with the user choosing. If you meant one of the two, say which and this
> narrows.

## 12. Business model

| Question | Answer |
|---|---|
| Pricing shape | Not yet decided, see Q5 |
| Free tier | Not yet decided |
| Metered unit | Not yet decided |
| Marginal model cost per user | Zero in cash terms. The Gemini free tier is not billed. The real constraint is quota, not spend. See decision 0001. |
| Charging users in V1 | Unresolved, see Q10 |

> Assumption: "so we charge user now" is read as **we are not charging users at
> this stage**, because the model cost is zero. If you meant the opposite, that
> it makes charging viable, say so. It matters: charging for a product running
> on a free tier that may train on user data is a position we would need to
> take deliberately, not by accident.

## 13. Open questions

| # | Question | Blocks | Owner |
|---|---|---|---|
| ~~Q1~~ | ~~Which surface ships first?~~ **Answered 2026-09-08: web.** | — | — |
| ~~Q2~~ | ~~How do reminder notifications reach the user?~~ **Answered 2026-09-08: in-app and email.** | — | — |
| ~~Q3~~ | ~~One personal account per user, or workspaces with members?~~ **Answered 2026-09-08: one account per user.** | — | — |
| ~~Q4~~ | ~~Which model provider, at what cost ceiling?~~ **Answered 2026-09-08: Gemini free tier, key in server env.** | — | — |
| Q5 | Pricing shape and metered unit? | brief | user |
| Q10 | Does the Gemini free tier's data handling meet the bar for a product holding passports, finances and family details? The free tier's terms differ from the paid tier and must be read before launch, not after. | launch, decision 0001 | user |
| Q11 | One shared API key serves every user, so every user shares one quota. What happens when the quota is exhausted: queue, degrade, or refuse? | HLD | user |
| Q12 | Are we charging users in V1? | brief, pricing | user |
| Q6 | Currency and locale: is ₹ the only currency in V1? | PRD | user |
| Q7 | What numeric targets make each V1 hypothesis pass or fail? | PRD metrics | user |
| Q8 | Is offline capture required, and is data export a V1 promise? | PRD, HLD | user |
| Q9 | How long is the V1 build window, and is there a launch date to hit? | epic sequencing | user |

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-08 | Created as skeleton | Process bootstrap | — |
| 2026-09-08 | Filled from the V1 product definition | User supplied the product | pending |
| 2026-09-08 | Surface, notifications and model provider settled. Q1, Q2, Q4 closed. Q10 to Q12 opened. | User answered the blocking questions | user |
| 2026-09-08 | One account per user. Plain-language capture, the Life Inbox, and task priority and recurrence deferred out of V1. Pillar P1 marked as partly deferred. Q3 closed. | User cut scope | user |
