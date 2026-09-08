# Claude Rules — Writing Process Docs

These rules govern every document under `process-docs/`. They are binding for
Claude. If a user request conflicts with a rule here, say so in one sentence,
then follow the user's decision.

---

## 1. What this folder is

`process-docs/` is the single source of truth for **why** and **what** we build
in Jarvis. Code is the answer; these docs are the question, the shape, and the
agreed plan. Nothing gets built that does not have a trail here.

Context is cumulative. A later doc never restates an earlier one — it links to
it. If a fact changes, it is changed **in the doc that owns it**, and the change
is logged.

---

## 2. The five stages

Every feature moves through the same gates, in order. Each stage produces one
document. A stage cannot start until the previous one is **Approved** by the
user.

| # | Stage | Document | Owner of the decision | Locks |
|---|-------|----------|----------------------|-------|
| 0 | Intake | `00-context.md` | User supplies, Claude records | Nothing |
| 1 | Epic PRD | `01-prd.md` | User approves | Scope, users, requirements, success criteria |
| 2 | Design | `02-design.md` | User approves after Claude Design work | Screens, flows, states, design-system tokens |
| 3 | Build Plan (HLD) | `03-build-plan.md` | User approves | High-level architecture, boundaries, data model, tech choices |
| 4 | Implementation Plan (LLD) | `04-implementation-plan.md` | User approves | File-level plan, contracts, task breakdown, test plan |
| 5 | Dev | `05-dev-log.md` | Claude writes as it builds | Nothing — it records reality |

**Gate rule.** Do not write stage N+1 while stage N is `draft` or `in-review`.
If asked to skip ahead, state the missing approval and ask for it. If the user
explicitly says to proceed anyway, proceed and add a `> Gate skipped:` note at
the top of the doc.

**Lock rule.** When the user approves a doc, set its status to `approved` and
add the approval line. An approved doc is not silently edited. Changes go
through §7 (Change Control).

---

## 3. Folder layout

```
process-docs/
├── CLAUDE.md                    ← these rules
├── README.md                    ← human-readable overview of the process
├── index.md                     ← registry of every feature and its stage
├── product/
│   ├── product-brief.md         ← what Jarvis is, who it serves, pillars
│   ├── glossary.md              ← one definition per domain term
│   └── decisions/               ← product- and platform-wide decision records
│       └── NNNN-<slug>.md
├── templates/                   ← copy these, never edit in place
└── features/
    └── NNN-<feature-slug>/
        ├── 00-context.md
        ├── 01-prd.md
        ├── 02-design.md
        ├── 03-build-plan.md
        ├── 04-implementation-plan.md
        ├── 05-dev-log.md
        └── assets/              ← exports, screenshots, canvas links
```

Feature folders are numbered in creation order, three digits, zero padded.
Slugs are lowercase kebab-case and describe the feature, not the ticket.

---

## 4. Front matter — required on every doc

Every document starts with this block. No exceptions.

```yaml
---
doc: prd | design | build-plan | implementation-plan | dev-log | context
feature: 003-workspace-memory
title: Workspace Memory
stage: 1
status: draft | in-review | approved | superseded
owner: user
created: YYYY-MM-DD
updated: YYYY-MM-DD
approved_on: YYYY-MM-DD | null
supersedes: null | <path>
---
```

Update `updated` on every edit. Never backdate.

Directly under the front matter, an approved doc carries:

```
> **Approved** by @user on YYYY-MM-DD. Locked — changes require a change record (§7).
```

---

## 5. How to write

**Write for the person who joins in three months.** They have the domain
knowledge and none of the conversation.

- Lead with the decision or the answer. Reasoning goes underneath it.
- One idea per sentence. Around twenty words. Every sentence has a verb.
- Prefer a table or a list to a paragraph for anything parallel: requirements,
  states, options, tasks, risks.
- No em-dashes, no arrows, no parenthetical asides stacked mid-sentence.
- Numbers, limits and measurements live in a table or on their own line, never
  buried in prose.
- Name a file, function or flag only where the reader must go there. Commands,
  schemas and snippets go in fenced code blocks.
- Never invent a fact. If something is unknown, it goes in **Open Questions**
  with a name against it.
- Never mark something done that is not done. Never soften a risk.

**Banned in these docs:** vague scope words with no owner (`robust`,
`seamless`, `enterprise-grade`), features described only as adjectives, and any
requirement that cannot be tested.

**Requirement style.** Every functional requirement is numbered `FR-n`, states
one behaviour, and is verifiable. Non-functional requirements are `NFR-n` and
carry a number.

Bad: `The assistant should respond quickly.`
Good: `NFR-3. Assistant streams the first token within 800 ms at p95.`

---

## 6. What each document must contain

Use the matching file in `templates/`. Sections marked required must exist even
when the answer is "none".

### 00-context.md — Intake
Raw capture of what the user asked for. Their words, lightly organised. Product
details, constraints, references, links, competitor notes. This is the only doc
where unresolved mess is allowed. Never edit the user's stated requirement into
something cleaner. Record it, then interpret it in the PRD.

### 01-prd.md — Epic PRD
Required: Problem, Users and jobs, Goals, Non-goals, User stories, Functional
requirements (FR-n), Non-functional requirements (NFR-n), Success metrics,
Dependencies, Risks, Open questions, Out of scope.

Rules:
- No solutions. The PRD says what and why, never how.
- No screen names, no component names, no table names, no framework names.
- Every goal has a metric. Every metric has a number and a source.
- The Non-goals section is mandatory and must not be empty.

### 02-design.md — Design
Required: Design intent, Screen inventory, Flows, States per screen (empty,
loading, error, success, permission-denied), Responsive behaviour, Design
system deltas, Accessibility notes, Copy, Open questions.

Rules:
- Every screen maps to at least one FR from the PRD. Cite the FR ids.
- Every interactive surface lists its five states. Missing states are the most
  common defect in this stage.
- Design system changes are listed as deltas: token added, token changed,
  component added. New one-off styles are a smell, call them out.
- Link the Claude Design canvas and store exports in `assets/`.
- The design is fixed when approved. Later code must match it or raise a change
  record.

### 03-build-plan.md — HLD
Required: Architecture summary, Component map, Data model, API surface,
Third-party and model choices, Cross-cutting concerns (auth, tenancy, limits,
cost, observability), Alternatives considered, Architecture decisions,
Questions for the user, Risks.

Rules:
- This document exists to **ask**, not only to state. It must contain a
  `Questions for the user` section covering direction, trade-offs, and anything
  with more than one defensible answer. Ask before choosing, when the choice is
  expensive to reverse.
- Every significant choice lists at least one alternative and why it lost.
- For anything calling a model: name the model, the token budget, the fallback
  and the cost per call. Guessed numbers are labelled `estimate`.
- Multi-tenancy, authorisation and data isolation are addressed explicitly on
  every feature that touches user data. "Same as the rest of the app" is not an
  answer; state the rule.
- HLD is locked on approval. Every locked decision is copied into
  `product/decisions/` if it affects more than this feature.

### 04-implementation-plan.md — LLD
Required: Scope recap, File-by-file plan, Interfaces and contracts, Data
migrations, State management, Error handling, Test plan, Rollout and flags,
Task breakdown, Definition of done.

Rules:
- List concrete paths. Say created, modified or deleted for each.
- Type signatures and schemas for anything crossing a boundary.
- Tasks are ordered, independently shippable where possible, and each carries a
  size (S, M, L) and its acceptance check.
- The test plan names the cases, not the intent. `covers FR-4: retry on 429` is
  a case. `good coverage` is not.
- No code is written before this document is approved.

### 05-dev-log.md — Dev
Appended during and after implementation. Records what actually happened: what
shipped, what deviated from the plan and why, what was deferred, what broke.
Deviation from an approved plan is always logged, never hidden.

---

## 7. Change control

An approved doc is a contract. To change it:

1. Add an entry to the doc's `Change Log` table at the bottom: date, what
   changed, why, who approved.
2. If the change alters scope, architecture or a locked design, say plainly
   which downstream docs are now stale and list them.
3. Re-run the gate. A PRD change re-opens design, build plan and implementation
   plan for review, in that order. Do not carry on building against a stale
   plan.
4. If a doc is replaced wholesale, set the old one to `superseded` and point
   `supersedes` on the new one at it. Never delete an approved doc.

---

## 8. Working rules for Claude

1. **Ask before you draft, once.** Read `00-context.md` and the product brief.
   List the questions you actually need answered, at most a handful, grouped.
   Then draft. Do not interview the user one question at a time.
2. **Never advance a gate on your own.** Approval is a user action, in words.
   Silence is not approval. "Looks good" is approval; record it with the date.
3. **State assumptions inline.** Any gap you filled yourself is marked
   `> Assumption:` in place, so the user can strike it during review.
4. **Keep the registry current.** Every stage change updates
   `process-docs/index.md` in the same commit.
5. **One doc per commit where practical.** Commit message:
   `docs(<feature-slug>): <stage> <verb>`, for example
   `docs(workspace-memory): prd approved`.
6. **Link, do not duplicate.** Reference `01-prd.md#fr-4`, do not restate FR-4.
7. **Cite the source of every number.** Benchmark, vendor page, measurement, or
   `estimate`.
8. **Product-wide learnings graduate.** Anything true beyond one feature moves
   into `product/product-brief.md`, `product/glossary.md`, or a decision record.
9. **Do not write code during stages 0 to 4.** Sketches inside the doc are
   fine. Files in the repo are not.
10. **Report honestly.** If a plan cannot be delivered as approved, say it in
    the dev log the day it becomes true.

---

## 9. Definition of ready and done

**A doc is ready for review when:** front matter is complete, every required
section exists, no `TBD` remains outside Open Questions, every claim is sourced,
and it links correctly to the previous stage.

**A feature is done when:** the dev log records every task in the
implementation plan as shipped or explicitly dropped, deviations are logged, the
design matches what was approved or a change record explains why not, and
`index.md` shows the feature as `shipped`.
