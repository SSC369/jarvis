---
doc: decision
id: 0002
title: V1 technology stack
status: superseded
created: 2026-09-08
updated: 2026-09-09
supersedes: null
superseded_by: ./0004-v1-technology-stack-revised.md
origin: user direction, 2026-09-08
---

# 0002 — V1 technology stack

> **Superseded** on 2026-09-09 by
> [decision 0004](./0004-v1-technology-stack-revised.md). The application layer
> here survives in 0004. The infrastructure layer does not: EC2, Celery, Redis
> and raw WebSockets are all replaced, the API medium is now GraphQL, and the
> auth provider left open here is settled in
> [decision 0005](./0005-auth-supabase-and-data-isolation.md). Kept as the
> record of what was decided first and why it changed.

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
| Background jobs | Celery with Redis as the broker |
| In-app notification transport | WebSockets |
| Backend hosting | AWS EC2 |
| Auth | A third-party provider, not built in-house. Which one is open |
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
| Celery, Redis and Resend cover reminder scheduling and delivery in epic 002 | Three processes on the EC2 instance before a single reminder fires: API, Celery worker, Celery beat, plus Redis |
| WebSockets deliver notifications the moment they fire, with no polling interval to tune | WebSockets need sticky routing or a shared backplane as soon as there is more than one server process. Single-instance EC2 hides this until it does not |

## Recommendations on top of the decision

Neither changes the decision. Both are worth a yes or no at the epic 001 build
plan.

**1. Do not hold server data in MobX.** Almost everything in Slashit is server
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

| # | Question | Answer |
|---|---|---|
| ~~1~~ | Notification transport | **WebSockets**, settled 2026-09-09 |
| ~~2~~ | Redis or a database-backed queue | **Redis**, settled 2026-09-09 |
| ~~3~~ | Where does this run | **Backend on AWS EC2**, settled 2026-09-09 |
| ~~4~~ | Auth built or bought | **A provider**, settled 2026-09-09 |
| 5 | Which auth provider? |  |
| 6 | Where does the frontend run: served from the same EC2 instance, S3 and CloudFront, or a separate host? |  |
| 7 | Is Redis self-managed on EC2 or ElastiCache? Self-managed is cheaper and is one more thing to keep alive |  |
| 8 | A WebSocket connection per user needs somewhere to terminate. On one EC2 instance this is simple. It stops being simple the moment there are two |  |

## Reversibility

Costly for FastAPI and PostgreSQL, which is normal and acceptable. Costly for
the auth provider, since user identities live there. Cheap for MobX, Turborepo,
Resend and Redis, each replaceable behind a thin boundary. Decision
0001 already requires the model provider to sit behind one.

## Scope

Binds every feature in V1.
