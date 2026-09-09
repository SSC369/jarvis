---
doc: tech-stack
title: Slashit Technical Stack
status: current
owner: user
created: 2026-09-09
updated: 2026-09-09
---

# Slashit — Technical Stack

The standing technical context every build plan inherits. Read this before
drafting a stage 3 build plan, the way you read
[the product doc](./product/product.md) before a PRD.

This document owns what the stack **is**. Each choice carries the alternatives
it beat, so the reasoning survives without a separate decision folder. When a
choice changes, it changes here, and the change log at the bottom records it.

---

## 1. The stack

| Layer | Choice |
|---|---|
| API medium | GraphQL |
| GraphQL server | Strawberry, mounted on FastAPI |
| API framework | FastAPI |
| Language | Python |
| Database | PostgreSQL, hosted by Supabase |
| Vector search | pgvector, in the same database |
| Auth | Supabase Auth |
| Data isolation | PostgreSQL Row Level Security |
| In-app notification transport | GraphQL subscriptions over WebSockets |
| Background jobs | Procrastinate, backed by PostgreSQL |
| Frontend | React, built with Vite |
| Server state | TanStack Query, over `graphql-request` |
| UI state | MobX |
| Typed client | `graphql-codegen` from the Strawberry schema |
| Components | shadcn/ui |
| Design system | Produced in Claude Design at stage 2 of each feature |
| Repository | Plain folders, `apps/web`, `apps/api`, `packages/` |
| Backend hosting | Managed container host. Render or Railway, undecided |
| Frontend hosting | Static host. Vercel or Cloudflare Pages, undecided |
| Email | Resend |
| Model provider | Google Gemini Flash, paid tier |
| LLM observability | Langfuse |

---

## 2. The Supabase boundary

This rule matters more than any single row above, and it is not optional.

**The browser talks to Supabase for authentication only. Every record read and
write goes through the Strawberry GraphQL endpoint.**

Supabase publishes its own data APIs, PostgREST and `pg_graphql`. Neither is
used. A client that reaches the database directly bypasses the AI gateway, the
per-user usage attribution required by [epic 000](./000-ai-gateway/), and every
business rule the resolvers hold. One door in, and it is ours.

---

## 3. Why each choice

### API medium: GraphQL

Chosen by the user on 2026-09-09.

| Alternative | Why it lost |
|---|---|
| REST with an OpenAPI-generated client | The cheaper path to a typed client, and still a valid one. Rejected by user direction |
| Supabase PostgREST or `pg_graphql` as the API | Bypasses the AI gateway and per-user usage attribution. Puts business rules in database policies, where they are hard to test |

**What it buys.** One typed contract, with `graphql-codegen` generating the
React hooks from the schema. The records surface fetches exactly the fields a
view needs, which suits a product where a task, an expense and a memory carry
different fields. Queries, mutations and subscriptions share one endpoint and
one auth path.

**What it costs.** N+1 queries are GraphQL's default failure mode, so DataLoader
is required from the first resolver rather than retrofitted. HTTP caching by URL
stops working, and caching moves into TanStack Query and the resolvers. A
careless or hostile deep query is expensive, so depth and complexity limits are
needed before public launch. Strawberry is a smaller ecosystem than FastAPI's
REST path.

### Database and auth: Supabase

| Alternative | Why it lost |
|---|---|
| Clerk for auth | The best developer experience of the group. It loses on one structural point: identity would live in a third-party system while records live in Slashit's PostgreSQL, kept in step by webhooks. Every missed webhook is a user who can sign in but owns no rows, or a row whose owner does not exist. That failure is silent and it appears in production |
| Auth0 | The same sync problem as Clerk, with more configuration surface than one account per user justifies, and a steeper price curve |
| AWS Cognito | Poor developer experience, and its free-tier structure has changed more than once |
| WorkOS AuthKit | A generous free allowance and the right answer if enterprise SSO were on the roadmap. It is not: teams and sharing are product non-goals |
| Better Auth, self-hosted | Owns its own data, which is attractive. It is TypeScript-first and the backend here is Python |
| Auth built in-house | One account per user makes it look small. Password reset, session revocation, OAuth and breach response are where that impression ends |
| Self-managed PostgreSQL on EC2 | Backups, upgrades, connection limits and pgvector installation all become the operator's job for no gain at this size |

**What it buys.** Identity lives in `auth.users`, in Slashit's own database, so
no synchronisation exists to break. One database serves relational records,
full-text search, semantic search through pgvector, and the job queue. Row Level
Security makes principle 7 of the product doc a database guarantee rather than a
code-review guarantee.

**What it costs.** Auth and the database are now the same vendor, so one outage
takes both. Free-tier projects pause after a period of inactivity, which a
product with real users cannot accept. Migration away is costly: users export,
but password hashes tie the destination to a compatible hashing scheme and OAuth
links generally have to be re-established by the user.

### Background jobs: Procrastinate on PostgreSQL

| Alternative | Why it lost |
|---|---|
| Celery with Redis | Three processes and a second stateful system before a single reminder fires, for a workload measured in dozens of jobs a day |
| Celery without Redis | Celery without a broker is not Celery. The dependency is the point |

**What it costs.** The queue shares a database with user traffic. At this size
that is fine. At ten thousand times this size it is not.

### Hosting: managed containers

| Alternative | Why it lost |
|---|---|
| AWS EC2 free tier | A `t3.micro` is 1 GiB of memory. An API process, a worker, a scheduler, Redis and PostgreSQL do not fit in it under real use. The saving is roughly twenty dollars a month against an operator cost measured in evenings |

**What it costs.** Four vendors instead of one, each a dependency and a bill.
Not free, unlike the EC2 free tier on paper.

### Frontend data layer: TanStack Query

| Alternative | Why it lost |
|---|---|
| urql or Apollo Client with a normalised cache | A normalised cache is a second store of what the server holds, with its own invalidation rules. Pillar P2 forbids the AI path and the structured path disagreeing, and a stale cache is precisely that disagreement. This product's data is document-shaped records rather than a densely connected graph, so normalisation earns little |

MobX keeps the command palette, the in-flight input and transient UI. It does
not hold server state.

### Repository: plain folders

Turborepo was the original choice and is deferred. A Python API and one web app
share no TypeScript package, so monorepo tooling has nothing to do yet. The
folder discipline is free, the tooling is not. Add it the day a second
JavaScript app exists.

### Model provider: Gemini Flash, paid tier

The provider was settled on 2026-09-08. The tier moved from free to paid on
2026-09-09.

| Alternative | Why it lost |
|---|---|
| The Gemini free tier | Free-tier terms generally permit a provider to use inputs to improve its products. This product holds passports, finances and family details. It also means one shared rate limit, exhaustible by one user, and the saving was around one dollar a month per hundred users |
| A paid tier on another vendor | No reason to move. The gateway boundary keeps this cheap to revisit if Gemini disappoints on quality or price |
| Per-user API keys | Asks a user to obtain a key before capturing anything, which kills the first run |
| Local or self-hosted model | Infrastructure out of proportion to a V1 |

**What it costs.** A billing relationship and a bill that can surprise. The
constraint moves from quota to spend, so a runaway user or a retry loop now
costs money rather than returning an error.

---

## 4. Standing technical rules

Binding on every build plan. A build plan that contradicts one of these says so
explicitly and argues for it.

| # | Rule |
|---|---|
| T1 | One door in. The browser reaches data only through the GraphQL endpoint, never through a Supabase data API |
| T2 | Row Level Security is enabled, with a policy, in the same migration that creates any table holding user data. A table without a policy is a defect, not a default |
| T3 | The service-role key never reaches the browser, and never serves a request made on behalf of a user unless the resolver has already established ownership. It is for migrations and background jobs |
| T4 | The model provider stays behind a boundary. Nothing above it knows which provider is in use, so a tier or vendor change is configuration, not a rewrite |
| T5 | DataLoader from the first resolver, not retrofitted after the N+1 appears |
| T6 | Prompt content never reaches the usage or analytics tables. Passports and finances do not belong in an observability store |
| T7 | Every feature touching user data tests the boundary: a case where user A requests user B's record and receives nothing |
| T8 | Every number in a build plan carries its source. A benchmark, a vendor page, a measurement, or the label `estimate` |

---

## 5. Cost envelope

> `estimate`. Stated from memory on 2026-09-09 and not read from a vendor page.
> See section 7.

| Item | At launch | With real users |
|---|---|---|
| Backend host | 0 to 7 USD | 7 to 20 USD |
| Supabase | 0 USD, free tier | 25 USD, Pro |
| Frontend host | 0 USD | 0 USD |
| Resend | 0 USD | 0 to 20 USD |
| Gemini Flash | under 1 USD | 1 to 5 USD |
| Langfuse | 0 USD | 0 USD |
| **Total** | **about 10 USD a month** | **about 50 to 70 USD a month** |

Model cost per capture is about 0.0001 USD, from 500 tokens in at 0.10 USD per
million and 150 tokens out at 0.40 USD per million. A user capturing 100 times a
month costs about one cent. This is why the free tier was not worth its terms.

---

## 6. Open

| # | Question | Blocks |
|---|---|---|
| T-Q1 | Render or Railway for the backend? | epic 000 build plan |
| T-Q2 | How does the authenticated user's identity reach the database connection so RLS applies: `set_config` per transaction on a pooled connection, or a role switch per request? Getting this wrong disables isolation with no error | epic 000 build plan |
| T-Q3 | What backplane carries GraphQL subscriptions when there is more than one API instance? One instance hides this until it does not | epic 002 |
| T-Q4 | What are the query depth and complexity limits, as numbers? | public launch |
| T-Q5 | Vercel or Cloudflare Pages for the frontend? | epic 001 build plan |
| T-Q6 | Supabase free-tier projects pause after inactivity. What is the current threshold, and on what date does the project move to Pro? | launch |
| T-Q7 | Does the GraphQL schema stay one graph as epics land, or split by domain? | epic 004 |
| T-Q8 | The model tier moved from free to paid, so a runaway user now costs money rather than exhausting a shared quota. Do epic 000's per-user caps keep request ceilings, or gain a spend ceiling? | epic 000 build plan |

---

## 7. Verification owed

Every price and free-tier limit in this document was stated from memory during
the 2026-09-09 discussion and **none has been checked against a vendor page**.
Confirm Supabase, Render, Railway, Vercel, Cloudflare, Resend and Gemini current
pricing before the first bill, and record each figure with its source, per rule
T8.

Two obligations sit alongside it:

1. **Read Gemini's paid-tier data-handling terms before launch.** Better terms
   than the free tier are the expectation, but expectation is not reading. Open
   as Q10 in the product doc.
2. **Set a provider-side billing alert and spend cap before the first real
   user.** A cap is the only defence that works while nobody is watching.

---

## 8. History

The stack was revised once, on 2026-09-09.

The original choice put FastAPI, Celery, Celery beat, Redis and PostgreSQL on a
single AWS EC2 instance, assumed a REST API, left the auth provider open, and
used the Gemini free tier. It was made on 2026-09-08, before any build plan
existed, and it was replaced the moment the product was aimed at real users:
operator hours became scarcer than hosting cash, and the free tier's terms
became indefensible for a product holding passports.

FastAPI, PostgreSQL, React, Vite, MobX, shadcn/ui, Resend and Gemini carried
over unchanged. Everything else in the infrastructure layer was replaced.

The full original records, and the ones that superseded them, are in git history
under `process-docs/product/decisions/`, removed on 2026-09-09 when the decision
folder was folded into this document.

---

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created, absorbing decision records 0004, 0005 and 0006 | User removed the decisions folder and asked for one technical document | user |
