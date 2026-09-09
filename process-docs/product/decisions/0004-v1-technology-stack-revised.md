---
doc: decision
id: 0004
title: V1 technology stack, revised
status: accepted
created: 2026-09-09
updated: 2026-09-09
supersedes: ./0002-v1-technology-stack.md
origin: user direction, 2026-09-09
---

# 0004 — V1 technology stack, revised

## Context

[Decision 0002](./0002-v1-technology-stack.md) settled a stack before any build
plan existed. It put four stateful systems on a single AWS EC2 instance, left
the auth provider open, and assumed a REST API. Two things changed on
2026-09-09. The user stated that Slashit is intended for real users and a
company after that, which makes operator hours the scarce resource rather than
hosting cash. The user also chose GraphQL as the API medium, which 0002 did not
contemplate.

The application layer of 0002 was right and survives here. The infrastructure
layer did not survive.

## Decision

V1 runs a GraphQL API on FastAPI, against Supabase Postgres, on managed
hosting, with no Redis and no self-managed servers.

| Layer | Choice |
|---|---|
| API medium | GraphQL |
| GraphQL server | Strawberry, mounted on FastAPI |
| API framework | FastAPI |
| Database | PostgreSQL, hosted by Supabase |
| Vector search | pgvector, in the same database |
| Auth | Supabase Auth, see [decision 0005](./0005-auth-supabase-and-data-isolation.md) |
| Data isolation | PostgreSQL Row Level Security |
| In-app notification transport | GraphQL subscriptions over WebSockets |
| Background jobs | Procrastinate, backed by PostgreSQL |
| Frontend | React, built with Vite |
| Server state | TanStack Query, over `graphql-request` |
| UI state | MobX |
| Typed client | `graphql-codegen` from the Strawberry schema |
| Components | shadcn/ui |
| Repository | Plain folders, `apps/web`, `apps/api`, `packages/`. No Turborepo yet |
| Backend hosting | Managed container host, Render or Railway. Which one is open |
| Frontend hosting | Vercel or Cloudflare Pages. Which one is open |
| Email | Resend |
| Model provider | Gemini Flash, paid tier, see [decision 0006](./0006-model-provider-gemini-paid-tier.md) |
| LLM observability | Langfuse |

### The Supabase boundary

This rule matters more than any single row above, and it is not optional.

**The browser talks to Supabase for authentication only. Every record read and
write goes through the Strawberry GraphQL endpoint.**

Supabase publishes its own data APIs, PostgREST and `pg_graphql`. Neither is
used. A client that reaches the database directly bypasses the AI gateway, the
per-user usage attribution required by
[epic 000](../../features/000-ai-gateway/), and every business rule the
resolvers hold. One door in, and it is ours.

### What changed from 0002

| Layer | 0002 | Here | Why |
|---|---|---|---|
| API medium | REST, implied | GraphQL | User direction |
| Database | PostgreSQL, host unstated | Supabase Postgres | Brings auth, pgvector and backups with it |
| Auth provider | Open | Supabase Auth | Identity sits in the same database as the records |
| Background jobs | Celery with Redis | Procrastinate on PostgreSQL | Removes a second stateful system for dozens of jobs a day |
| Notification transport | Raw WebSockets | GraphQL subscriptions | One endpoint, one contract, one auth path |
| Backend hosting | AWS EC2 | Managed container host | See Alternatives |
| Frontend hosting | Unstated | Vercel or Cloudflare Pages | Static assets do not belong on an application server |
| Repository | Turborepo | Plain folders | A Python API and one web app share no TypeScript package |
| Server state | TanStack Query, recommended | TanStack Query, decided | 0002 raised it as a recommendation and it is now settled |
| Observability | Absent | Langfuse | 0002 had no answer for debugging model output |

FastAPI, PostgreSQL, React, Vite, MobX, shadcn/ui and Resend carry over
unchanged.

## Alternatives

| Option | Why it lost |
|---|---|
| Keep 0002 as written: EC2, Celery, Redis, REST | The AWS free tier `t3.micro` is 1 GiB of memory. FastAPI, a Celery worker, Celery beat, Redis and PostgreSQL do not fit in it under real use. The saving is roughly twenty dollars a month against an operator cost measured in evenings |
| REST with an OpenAPI-generated client | Rejected by user direction. It was the cheaper path to a typed client and it remains a valid one |
| Supabase PostgREST or `pg_graphql` as the API | Bypasses the AI gateway and per-user usage attribution. Puts business rules in database policies where they are hard to test |
| urql or Apollo Client with a normalised cache | A normalised cache is a second store of what the server holds, with its own invalidation rules. Pillar P2 forbids the AI path and the structured path disagreeing, and a stale cache is precisely that disagreement. TanStack Query's explicit invalidation is easier to reason about, and this product's data is document-shaped records rather than a densely connected graph |
| Supabase Realtime for in-app notifications | Two realtime mechanisms and two auth paths for one product. Kept as the fallback if subscriptions prove awkward to scale |
| Celery kept, Redis dropped | Celery without a broker is not Celery. The dependency is the point |
| AWS Cognito for auth | Poor developer experience and tier limits that have changed repeatedly. See decision 0005 |
| Self-managed PostgreSQL on EC2 | Backups, upgrades, connection limits and pgvector installation all become the operator's job for no gain at this size |

## Consequences

| Good | Bad |
|---|---|
| Nothing to patch, restart or keep alive. Deploys are a git push | Four vendors instead of one. Each is a dependency and a bill |
| One database serves relational records, full-text search, semantic search through pgvector, and the job queue | Supabase free-tier projects pause after a period of inactivity. Unacceptable once a real user exists, so Pro starts the day the product does |
| GraphQL gives one typed contract, and `graphql-codegen` generates the React hooks from the schema. No hand-written client | N+1 queries are GraphQL's default failure mode. DataLoader is required from the first resolver, not retrofitted |
| The records surface fetches exactly the fields a view needs, which suits a product where a task, an expense and a memory carry different fields | HTTP caching by URL stops working. Caching moves into TanStack Query and into the resolvers |
| Queries, mutations and subscriptions share one endpoint and one auth path | A careless or hostile deep query is expensive. Depth and complexity limits are needed before public launch, not after |
| Row Level Security makes principle 7 a database guarantee rather than a code-review guarantee | RLS only binds if the request's identity reaches the connection. Getting that wrong silently disables it. See the open questions |
| Removing Redis removes an entire stateful system, its persistence question, and its failure modes | A PostgreSQL-backed queue shares its database with user traffic. At this size that is fine, and at ten thousand times this size it is not |
| Roughly ten dollars a month to start, fifty to seventy with real users | Not free, unlike the EC2 free tier on paper |
| Strawberry is type-hint native, so the Python types and the GraphQL schema are one definition | Fewer Python GraphQL engineers than REST engineers, and Strawberry is a smaller ecosystem than FastAPI's REST path |

## Open at the build plan

| # | Question | Blocks |
|---|---|---|
| 1 | Render or Railway, and does the choice have to be made before epic 000 ships? | epic 000 HLD |
| 2 | How does the authenticated user's identity reach the database connection so RLS applies: `set_config` per transaction on a pooled connection, or a role switch per request? Getting this wrong disables isolation without any error | epic 000 HLD, decision 0005 |
| 3 | What backplane carries GraphQL subscriptions when there is more than one API instance? One instance hides this until it does not | epic 002 |
| 4 | What are the query depth and complexity limits, as numbers? | public launch |
| 5 | Vercel or Cloudflare Pages for the frontend | epic 001 HLD |
| 6 | Supabase free-tier projects pause after inactivity. Confirm the current threshold and name the date Pro starts | launch |
| 7 | Does the GraphQL schema stay one graph as epics land, or split by domain? | epic 004 |

## Verification owed

Every price and free-tier limit in this record was stated from memory during the
2026-09-09 discussion and **none has been checked against a vendor page**.
Confirm Supabase, Render, Railway, Vercel, Cloudflare, Resend and Gemini
current pricing before the first bill, and record the figures with their source
per rule 7 of the process.

## Reversibility

| Layer | Cost to undo |
|---|---|
| Supabase Auth | Costly. User identities live there. See decision 0005 |
| PostgreSQL | Costly, and normal |
| GraphQL as the medium | Costly once clients are built against the schema |
| Supabase as the Postgres host | Moderate. It is standard PostgreSQL, so a dump and restore moves it, but auth and RLS policies come with it |
| Managed host | Cheap. A container runs anywhere |
| Procrastinate, TanStack Query, MobX, Resend, Langfuse | Cheap. Each sits behind a thin boundary |
| Model provider | Cheap, if obligation 3 of decision 0006 holds |

## Scope

Binds every feature in V1.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created, superseding decision 0002 | User accepted a revised stack and chose GraphQL as the API medium | user |
