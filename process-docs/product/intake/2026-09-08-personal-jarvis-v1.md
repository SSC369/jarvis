---
doc: context
scope: product
title: Personal Jarvis V1 — Product Definition (as supplied)
stage: 0
status: approved
owner: user
created: 2026-09-08
updated: 2026-09-08
approved_on: 2026-09-08
supersedes: null
---

# Intake — Personal Jarvis V1

Supplied by the user on 2026-09-08 as "Personal Jarvis — V1 Product Requirements
Document". Transcribed below as given.

> **The product was renamed to Slash on 2026-09-09**, per
> [decision 0003](../decisions/0003-product-name-and-mark.md). This document is
> left exactly as it was supplied, because intake records the user's own words.
> Every other document uses the new name. This is the source document for
[the product brief](../product-brief.md) and [the V1 epic map](../v1-epic-map.md).

Nothing in this file is edited for style. Interpretation happens in the PRDs.

---

## As supplied

Product: Personal Jarvis
Version: V1
Category: AI Personal Operating System
Primary Interaction: Command-first AI
Status: V1 Product Definition

### 1. Product Vision

Personal Jarvis is an AI-powered personal operating system that helps users capture, remember, organize, retrieve, and act on information in their lives.

Instead of maintaining separate systems for tasks, reminders, expenses, notes, goals, projects, events, and personal information, users interact with one intelligent system.

The core experience:

```
User
  ↓
Command / Conversation
  ↓
Jarvis understands intent
  ↓
Record / Remember / Organize / Act
  ↓
Structured personal data
  ↓
Jarvis uses that context later
```

Product Promise

> Tell Jarvis what matters. Jarvis remembers it, organizes it, and helps you act on it.

### 2. Problem

A person's life is fragmented across many applications: Notes, Calendar, Reminders, Expense trackers, To-do apps, Documents, Spreadsheets, Messaging apps, Email, AI assistants.

The user is forced to decide: "Where should I put this?"

They also have to manually maintain relationships between pieces of information. For example:

```
Goal: Become a Backend Engineer
        ↓
Learn Spring Boot
        ↓
Build Backend Project
        ↓
Complete 5 tasks
```

Traditional applications treat these as separate pieces of data. Jarvis should understand them as parts of the user's life.

### 3. Product Philosophy

**3.1 Command-first.** Users should be able to explicitly tell Jarvis what they want.

```
/add-task Finish API documentation tomorrow
/add-expense ₹850 dinner
/remind Call Mom tomorrow at 7pm
/remember Passport expires in 2030
/add-goal Become a backend engineer
```

Commands make common actions fast and predictable.

**3.2 Natural language commands.** Commands should not be rigid CLI syntax. For example `/add-expense ₹850 dinner with friends yesterday`. Jarvis understands: Amount ₹850, Category Food, Description Dinner with friends, Date Yesterday. The command provides explicit intent while natural language provides flexibility.

**3.3 Normal conversation.** Users should also be able to communicate naturally: "I spent ₹850 on dinner yesterday." Jarvis can recognize this as an expense. Therefore: Commands = explicit actions, Natural language = flexible interaction. Both should coexist.

**3.4 Persistent context.** Jarvis should remember useful information across conversations. The user should not need to repeatedly explain the same context.

**3.5 User-controlled data.** Anything Jarvis records should be visible and manageable by the user. The user should be able to view, search, edit, delete and forget their information.

### 4. Target User

V1 is designed for an individual who wants one place to manage their personal life. The user may have multiple responsibilities, personal and professional goals, ongoing projects, recurring tasks, expenses, important dates, personal information, ideas, plans, and information scattered across applications.

The product should particularly appeal to users who dislike maintaining complex productivity systems.

### 5. Core User Jobs

Jarvis should help answer six fundamental questions:

1. What do I need to do? — Tasks and reminders.
2. What do I need to remember? — Memories and important information.
3. What is happening? — Events and upcoming commitments.
4. What am I working toward? — Goals and projects.
5. What have I recorded? — Structured records.
6. What do I already know? — Personal search and contextual retrieval.

### 6. Core V1 Product

The V1 product consists of seven major capabilities:

```
                 PERSONAL JARVIS
                       │
       ┌───────────────┼───────────────┐
       │               │               │
    COMMANDS        MEMORY          RECORDS
       │               │               │
       ├───────────────┼───────────────┤
       │               │               │
     TASKS          CONTEXT          SEARCH
       │               │               │
       └───────────────┼───────────────┘
                       │
                  DAILY CONTROL
                 Today / Upcoming
```

### 7. Jarvis Command Center

The Jarvis Command Center is the primary interface. Users can execute commands, have conversations, search their information, create records, retrieve information, and ask for summaries.

```
/add-task Finish project proposal tomorrow
/add-expense ₹1,200 dinner
/remind Renew insurance October 15
/search What am I working on this week?
```

### 8. Command System

Commands are a first-class V1 feature.

**8.1 Command Syntax:** `/command [natural-language arguments]`

**8.2 V1 Commands**

Tasks: `/add-task` `/complete-task` `/delete-task` `/tasks`
Reminders: `/remind` `/reminders`
Expenses: `/add-expense` `/expenses`
Memory: `/remember` `/add-memory` `/memory` `/memories` `/forget`
Events: `/add-event` `/events`
Goals: `/add-goal` `/goals` `/update-goal`
Projects: `/add-project` `/projects` `/add-project-task`
Search and overview: `/search` `/today` `/upcoming`

### 9. Command Discovery

When the user types `/`, Jarvis should show available commands.

```
Commands
/add-task        Create a task
/remind          Set a reminder
/add-expense     Record an expense
/remember        Save information
/add-goal        Create a goal
/add-project     Create a project
/add-event       Create an event
/search          Search your life
/today           Today's overview
```

Typing `/add` should filter to: `/add-task` `/add-expense` `/add-memory` `/add-goal` `/add-project` `/add-event`

### 10. Structured Records

This is a core V1 feature. Every time Jarvis records something, the user should be able to view it as structured data. The user should never have to rely exclusively on asking the AI "What have I told you?" They can open Records and inspect everything.

### 11. Records

The Records section is the user's structured view of their life data.

```
Records
├── All
├── Tasks
├── Expenses
├── Memories
├── Events
├── Goals
├── Projects
└── Notes / Ideas
```

Users should be able to view, search, filter, sort, open record details, edit and delete records.

### 12. All Records View

```
Records
[ All ] [ Tasks ] [ Expenses ] [ Memories ]
[ Events ] [ Goals ] [ Projects ]
Search records...
────────────────────────────────────────
Type       Title                    Date       Status
────────────────────────────────────────
Task       Finish API docs          Sep 8      Pending
Expense    Dinner                   Sep 8      ₹850
Memory     Passport expires         Sep 8      Saved
Goal       Backend Engineer         Sep 7      Active
Event      Mom's Birthday           Sep 7      Upcoming
Project    Personal Jarvis          Sep 7      Active
```

This gives the user a complete overview of what Jarvis has recorded.

### 13. Task Records

```
Tasks
Task                         Due          Status
──────────────────────────────────────────
Finish API documentation     Sep 10       Pending
Buy groceries               Sep 9        Pending
Call Rahul                  Sep 9        Done
```

Capabilities: create, complete, edit, delete, set due date, set priority, recurrence, view status.

### 14. Expense Records

```
Expenses
Date        Description       Category       Amount
──────────────────────────────────────────────
Sep 8       Dinner            Food           ₹850
Sep 7       Uber              Transport      ₹320
Sep 6       Groceries         Food           ₹2,100
```

Capabilities: add expense, category, amount, description, date, edit, delete, search, filter, basic summaries.

`/expenses this month` could return:

```
September Expenses
Food          ₹8,400
Transport     ₹4,200
Shopping      ₹6,800
Total        ₹19,400
```

Advanced budgeting is outside V1.

### 15. Memory Records

```
Memories
Memory                              Category
──────────────────────────────────────────────
Passport expires in 2030            Documents
Preferred airline is Emirates       Preference
Mom's birthday is Oct 12            Family
Learning Spring Boot                Career
```

Memory is specifically information Jarvis should retain as useful context.

### 16. Memory

Memory is one of the core differentiators of Jarvis. Users can explicitly tell Jarvis `/remember My passport expires in 2030` or `/add-memory My preferred airline is Emirates`.

Potential memory categories:

- Personal: preferences, important dates, interests, plans
- People: family, friends, colleagues, relationships
- Professional: career goals, skills, professional plans
- Life: subscriptions, purchases, travel information, important information, decisions

### 17. Memory Retrieval

Users can ask `/memories` or `/search What do you remember about my career?`. Jarvis should retrieve relevant memories. Example response:

> You previously told me that you want to become a backend engineer and are learning Spring Boot.

### 18. Memory Control

Users must have direct control over their memories. Supported actions: `/remember` `/memory` `/memories` `/forget`.

Users can view, edit, delete, explicitly save, and forget memories. For destructive actions, Jarvis should request confirmation where appropriate.

### 19. Record Detail

Every structured record should have a detail view.

```
Expense
₹850
Description  Dinner
Category     Food
Date         September 8, 2026
Created via  Jarvis
[ Edit ] [ Delete ]
```

```
Memory
Passport expires in 2030
Category   Documents
Created    September 8, 2026
Source     Jarvis conversation
[ Edit ] [ Forget ]
```

The user should understand what Jarvis recorded and why it exists.

### 20. Tasks

Tasks represent actions the user needs to perform. `/add-task Finish project proposal tomorrow` returns "Task created / Finish project proposal / Due: Tomorrow".

V1 capabilities: create, complete, edit, delete, due dates, priority, recurrence, status, project association, goal association.

### 21. Reminders

Reminders represent things Jarvis should bring back to the user's attention. `/remind Call Mom tomorrow at 7pm`.

V1 capabilities: one-time reminders, recurring reminders, date, time, description, edit, delete, notifications.

### 22. Events

Events represent things happening at a specific time. `/add-event Mom's birthday October 12`.

V1 capabilities: create, edit, delete, date, time, description, upcoming events.

### 23. Goals

Goals represent long-term outcomes. `/add-goal Become a backend engineer`, `/add-goal Save ₹2 lakh`, `/add-goal Launch Personal Jarvis`.

Goal capabilities: create, edit, delete, progress, status, associated projects, associated tasks.

```
/goals
Current Goals
Become a Backend Engineer   Progress: 35%
Launch Personal Jarvis      Progress: 60%
Save ₹2 lakh                Progress: 45%
```

### 24. Projects

Projects represent structured bodies of work. `/add-project Personal Jarvis`, then `/add-project-task Design dashboard`, `/add-project-task Build memory system`, `/add-project-task Launch MVP`.

Projects can connect to goals.

```
Goal
Become a Backend Engineer
        │
        ▼
Project
Backend Learning
        │
        ├── Learn Spring Boot
        ├── Build REST API
        └── Build Production Project
```

### 25. Notes & Ideas

Not everything belongs in a task or memory. Jarvis should support lightweight notes and ideas: `/add-note Idea: AI travel planner`, `/add-note Research AWS cost optimization`. These can be browsed in Records.

### 26. Life Inbox

The Life Inbox provides frictionless capture. Users can dump information without deciding how to categorize it:

```
Idea: build an AI travel planner
Need to buy a new charger
Maybe visit Goa in December
```

Jarvis can identify the appropriate type: Task, Idea, Reminder, Memory, Goal, Event. The user can review the inbox and confirm or modify classifications.

### 27. Personal Search

Jarvis should provide a unified search across the user's records.

`/search passport` results could include: MEMORY Passport expires in 2030; TASK Renew passport; REMINDER Check passport renewal requirements.

`/search backend` could return: GOAL Become a Backend Engineer; PROJECT Backend Learning; MEMORY Learning Spring Boot; TASK Build REST API.

The user shouldn't need to know which category contains the information.

### 28. Contextual Intelligence

Jarvis should understand relationships between records.

```
Goal
Become Backend Engineer
        │
        ├── Project: Backend Learning
        │       ├── Spring Boot
        │       └── REST API
        │
        └── Tasks
                ├── Complete course
                └── Build project
```

The user doesn't need to manually explain these relationships every time.

### 29. Today's View

The `/today` command provides the user's current situation.

```
TODAY
Tasks
• Finish project proposal
• Pay electricity bill
Events
• 7:00 PM — Gym
Reminders
• Call Mom
Important
• Insurance renewal in 10 days
```

The same information should also be available from the Home dashboard.

### 30. Upcoming View

```
/upcoming
UPCOMING
Tomorrow    • Submit project proposal
Sep 12      • Gym membership renewal
Sep 15      • Insurance renewal
Oct 12      • Mom's birthday
```

The user gets a timeline of upcoming obligations and important dates.

### 31. Proactive Jarvis

Jarvis can surface useful information without being explicitly asked:

> Your insurance renewal is coming up in 10 days.
> You have three unfinished tasks related to Personal Jarvis.
> You mentioned wanting to start learning system design this month.

Proactive behavior should be relevant, limited, actionable, non-intrusive. V1 should prioritize quality over frequency.

### 32. Home Dashboard

The dashboard answers: What should I know right now?

```
┌────────────────────────────────────┐
│              JARVIS                │
│       What do you want to do?      │
│       /add-task ...                │
├────────────────────────────────────┤
│ TODAY                              │
│ 3 Tasks · 1 Event · 2 Reminders    │
├────────────────────────────────────┤
│ UPCOMING                           │
│ Insurance · Birthday               │
├────────────────────────────────────┤
│ GOALS                              │
│ Backend Engineering     35%        │
│ Personal Jarvis         60%        │
└────────────────────────────────────┘
```

The dashboard should support the command experience rather than replace it.

### 33. Navigation

V1 navigation should remain simple: Home, Jarvis, Records, Today, Upcoming.

Within Records: All, Tasks, Expenses, Memories, Events, Goals, Projects, Notes.

The primary entry point remains Jarvis.

### 34. AI + Structured Data Model

A key product principle:

> AI is the interface for creating, understanding, and querying information. Structured views are the interface for inspecting and managing information.

```
User → /add-expense ₹850 dinner → Jarvis → Expense Record → Records → Expenses
```

The same record is available through AI and UI. Neither should be a separate source of truth from the user's perspective.

### 35. Confirmation Model

Jarvis should minimize unnecessary confirmation.

- Simple action: `/add-task Buy groceries tomorrow` → create immediately.
- Ambiguous action: `/add-expense 500` → Jarvis asks "What was the expense for?"
- Destructive action: `/forget all my memories` → "This will remove all saved memories. Are you sure?"

### 36. Record Creation Principle

Every record created through Jarvis should be visible in Records.

```
AI interaction → Structured record → Records UI → Search / Edit / Delete
```

This creates transparency and trust.

### 37. Core V1 Entities

At the product level: User, and under it Tasks, Reminders, Expenses, Memories, Events, Goals, Projects, Notes / Ideas, Conversations.

These entities can have contextual relationships.

### 38. Example End-to-End Experience

1. Goal: `/add-goal Become a backend engineer` → "Goal created."
2. Project: `/add-project Backend Learning`
3. Task: `/add-project-task Learn Spring Boot`
4. Reminder: `/remind Start Spring Boot tomorrow at 9am`
5. Retrieval, two weeks later: `/search What am I working toward?`

> Your active goal: Become a Backend Engineer
> Current project: Backend Learning
> Current focus: Spring Boot
> You have 2 incomplete tasks related to this goal.

6. Records: Records → Goals shows "Become a Backend Engineer, Progress: 35%, Status: Active". Records → Projects shows "Backend Learning, 8 Tasks, 35% Complete".

The AI experience and structured experience are connected.

### 39. V1 Core User Loop

```
                    CAPTURE
                       │
                       ▼
              Command / Chat
                       │
                       ▼
                  UNDERSTAND
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       RECORD       REMEMBER       ACT
          │            │            │
          └────────────┼────────────┘
                       ▼
                STRUCTURED DATA
                       │
                       ▼
                    RECORDS
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
           Search     Edit     Review
              │
              ▼
        Context accumulates
              │
              ▼
           Jarvis helps
              │
              └──────────► CAPTURE
```

This loop is the heart of Personal Jarvis.

### 40. V1 Feature Priorities

| Priority | Feature |
|---|---|
| P0 | Jarvis Command Center |
| P0 | Command System |
| P0 | Structured Records |
| P0 | Persistent Memory |
| P0 | Tasks |
| P0 | Reminders |
| P0 | Personal Search |
| P0 | Context Awareness |
| P1 | Expenses |
| P1 | Events |
| P1 | Today's View |
| P1 | Upcoming View |
| P1 | Goals |
| P1 | Projects |
| P1 | Notes / Ideas |
| P1 | Life Inbox |
| P1 | Memory Management |
| P2 | Proactive Suggestions |
| P2 | Advanced contextual intelligence |

### 41. V1 Non-Goals

V1 should not attempt to become a fully autonomous Jarvis. Out of scope: email management, banking integrations, automatic financial transactions, health integrations, smart-home control, autonomous purchasing, social networking, full document management, advanced financial planning, voice-first assistant, large third-party integration ecosystem, complex multi-agent workflows, fully autonomous decision-making.

These can be introduced after validating the core product.

### 42. V1 Success Criteria

V1 should validate three fundamental hypotheses.

**Hypothesis 1 — Users will record their life in Jarvis.** Users should naturally use commands such as `/add-task` `/add-expense` `/remind` `/remember` `/add-goal` `/add-project`.

**Hypothesis 2 — Users will inspect their structured data.** Users should regularly open Records → Tasks, Expenses, Memories, Goals, Projects, rather than treating Jarvis as an opaque AI.

**Hypothesis 3 — Persistent context creates recurring value.** Users should return to ask: What do I need to do? What's coming up? What are my goals? What did I record? What do you remember? What am I working on? What did I plan?

If users repeatedly capture and retrieve information, the fundamental product loop is validated.

### 43. The V1 Product Identity

Personal Jarvis should not be positioned as "Another AI chatbot." It should be positioned as "An AI-powered personal command center that remembers and organizes your life." The distinction is important.

```
Traditional Apps                  Personal Jarvis
Task App ────── Tasks                       JARVIS
Expense App ─── Expenses                       │
Notes ───────── Notes            ┌─────────────┼─────────────┐
Calendar ────── Events           ▼             ▼             ▼
Goal App ────── Goals          Record       Remember        Act
        ↓                        │             │             │
  Fragmented Life                └─────────────┼─────────────┘
                                               ▼
                                        Connected Context
                                               ▼
                                          User's Life OS
```

### 44. Final V1 Definition

> Personal Jarvis V1 is a command-first AI personal operating system where users can record tasks, reminders, expenses, memories, events, goals, projects, notes, and ideas through natural-language commands or conversation. Every recorded item is stored as structured personal data that users can browse, search, filter, edit, and delete through dedicated list/table views. Jarvis uses this accumulated context to answer questions, provide daily and upcoming views, connect related information, and proactively surface useful information.

Core V1 principle:

> If Jarvis can record it, the user can see it. If the user can see it, they can control it. If Jarvis has the context, it can use it to help them later.

---

## What this document does not settle

Recorded here so the gaps are visible, not buried. These are carried into the
product brief and the epic PRDs as open questions.

| # | Gap | Blocks |
|---|---|---|
| G1 | Which surface ships first: web, mobile, desktop, or a mix | design, HLD |
| G2 | How reminder notifications reach the user | PRD, HLD |
| G3 | Single personal account, or shared workspaces | HLD, data model |
| G4 | Model provider, cost ceiling per user, latency budget | HLD |
| G5 | Pricing shape and metered unit | product brief |
| G6 | Currency and locale handling beyond ₹ | PRD |
| G7 | Numeric targets for the three success hypotheses | PRD metrics |
| G8 | Offline capture and data export expectations | PRD, HLD |
