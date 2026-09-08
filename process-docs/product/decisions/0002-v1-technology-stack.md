---
doc: decision
id: 0002
title: V1 technology stack
status: accepted
created: 2026-09-08
updated: 2026-09-08
supersedes: null
origin: user direction, 2026-09-08
---

# 0002 — V1 technology stack

## Context

V1 is a web application with one account per user, capture through commands, a
structured record store, and scheduled reminders delivered in-app and by email.
The build plan for epic 001 cannot start without a stack.

## Decision

| Layer | Choice |
|---|---|
| API | FastAPI |
| Database | PostgreSQL |
| Frontend | React, built with Vite |
| Repository | Turborepo monorepo |
| Frontend state | MobX |
| Components | shadcn/ui |
| Design system | Produced in Claude Design, stage 2 of each feature |
| Background jobs | Celery |
| Email | Resend |
| Model provider | Google Gemini free tier, see [decision 0001](./0001-model-provider-gemini-free-tier.md) |

## Alternatives

Chosen by the user without a comparison exercise. The stack is conventional for
this shape of product and nothing about V1 argues against any of it.

## Consequences

| Good | Bad |
|---|---|
| FastAPI and PostgreSQL are boring in the way infrastructure should be, and Postgres covers relational records, full-text search for `/search`, and JSON fields for per-type record data | Nothing significant |
| Turborepo makes room for a shared package between the web app and whatever comes after it | For one web app today it is overhead. It earns its place only if a second surface follows |
| shadcn/ui puts component source in the repository, so a Claude Design system can be applied directly to components rather than fought with | Component code becomes ours to maintain, including upstream fixes |
| Celery and Resend cover reminder scheduling and delivery in epic 002 | Celery needs a broker, so Redis joins the stack. Two services to run before a single reminder fires |

## Recommendations on top of the decision

Neither changes the decision. Both are worth a yes or no at the epic 001 build
plan.

**1. Do not hold server data in MobX.** Almost everything in Jarvis is server
state: records, lists, search results. MobX is a client state library, so using
it for server data means writing caching, refetching, invalidation and stale
handling by hand, and every one of those hand-written pieces is a place for the
records view to disagree with what was just captured. That disagreement breaks
the product's core promise, that the AI path and the structured path are never
separate sources of truth.

Recommended split, which keeps MobX:

| State | Held by |
|---|---|
| Records, lists, search results, anything from the API | TanStack Query |
| Command palette, the in-flight input, transient UI | MobX |

**2. Defer Turborepo until a second package exists.** One web app and one API do
not need monorepo tooling on day one, and adding it later is a smaller job than
working around it now. Keep it if a mobile client is coming, since then it pays
for itself.

## Open at the build plan

| # | Question |
|---|---|
| 1 | How do in-app notifications reach an open browser: polling, server-sent events, or websockets? Epic 002 needs this and it is the one transport decision the stack does not settle |
| 2 | Redis is implied by Celery. Confirmed, or is a database-backed job queue preferred to avoid a second service? |
| 3 | Where does this run, and does hosting constrain Celery and Redis? |
| 4 | Auth: built here, or a provider? One account per user makes this small either way |

## Reversibility

Costly for FastAPI and PostgreSQL, which is normal and acceptable. Cheap for
MobX, Turborepo and Resend, each replaceable behind a thin boundary. Decision
0001 already requires the model provider to sit behind one.

## Scope

Binds every feature in V1.
