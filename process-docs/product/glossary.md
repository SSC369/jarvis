---
doc: glossary
title: Glossary
status: draft
owner: user
created: 2026-09-08
updated: 2026-09-08
---

# Glossary

One definition per term. Docs use the term, never a synonym. If two docs need
two different meanings for one word, the word is wrong. Rename one.

Add a term the first time a doc needs it. Keep definitions to one or two
sentences.

## Product terms

| Term | Definition |
|---|---|
| Command Center | The primary Slash interface where the user types commands, converses, searches and retrieves. |
| Command | An explicit instruction starting with `/`, followed by natural-language arguments. `/add-task Finish API docs tomorrow`. |
| Command discovery | The list of available commands shown when the user types `/`, filtered as they type further characters. |
| Record | One structured item Slash has stored for the user: a task, reminder, expense, memory, event, goal, project or note. |
| Record type | The category a record belongs to. The V1 types are task, reminder, expense, memory, event, goal, project, note. |
| Records | The structured view of every record the user owns, browsable, searchable, filterable and editable. |
| Record detail | The view of a single record showing every stored field plus its origin and creation time. |
| Origin | How a record came to exist: a command, a conversation, or the Life Inbox. Stored on every record. |
| Memory | Information the user has asked Slash to retain as durable context, distinct from a task or a note. |
| Forget | Deleting a memory at the user's instruction. Destructive, so it confirms. |
| Life Inbox | Frictionless capture where the user dumps input without categorising it, and Slash proposes the record type for review. |
| Classification | Slash deciding which record type a piece of plain-language input becomes. |
| Extraction | Slash pulling the structured fields for a record type out of natural-language input. |
| Personal search | Unified search across every record type, so the user need not know which category holds the answer. |
| Contextual intelligence | Slash understanding relationships between records, such as a task belonging to a project that serves a goal. |
| Proactive suggestion | Information Slash surfaces without being asked. Relevant, limited, actionable, non-intrusive. |
| Today's view | The user's current situation: today's tasks, events, reminders and anything time-critical. |
| Upcoming view | A forward timeline of obligations and important dates. |
| Confirmation model | The rule for when Slash acts immediately, asks one question, or requires explicit confirmation. |

## Process terms

| Term | Definition |
|---|---|
| Epic PRD | The stage 1 document. States the problem, users, requirements and success metrics for a feature. Contains no solution. |
| Build plan | The stage 3 document. Locks high-level architecture and asks the user the direction questions. Also called the HLD. |
| Implementation plan | The stage 4 document. File-level plan, contracts, tasks and tests. Also called the LLD. |
| Gate | The approval a stage needs from the user before the next stage starts. |
| Locked | An approved doc whose decisions cannot change without a change record. |
| Design system delta | A token or component added or changed by a feature's design. |
