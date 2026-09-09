---
doc: decision
id: 0005
title: Supabase Auth as the identity provider, with Row Level Security
status: accepted
created: 2026-09-09
updated: 2026-09-09
supersedes: null
origin: user direction, 2026-09-09
---

# 0005 — Supabase Auth as the identity provider, with Row Level Security

## Context

[Decision 0002](./0002-v1-technology-stack.md) settled that auth is bought, not
built, and left which provider open. It has blocked two documents since: Q16 in
the product brief, and Q7 in the
[epic 000 PRD](../../features/000-ai-gateway/01-prd.md), where `user_id` cannot
exist until an identity provider does.

Slashit holds passport details, finances and family information for one person
per account. Principle 7 of the product brief states that user data never
crosses a user boundary, in storage or in a prompt. That principle needs a
mechanism, not a promise.

## Decision

Slashit uses Supabase Auth for identity, and PostgreSQL Row Level Security to
enforce the user boundary in the database rather than only in application code.

Three parts, all binding:

1. **Identity lives in `auth.users`, in Slashit's own PostgreSQL database.**
   Every table holding user data carries a foreign key to it.
2. **Row Level Security is enabled on every table holding user data.** A table
   without a policy is a defect, not a default.
3. **FastAPI verifies the Supabase-issued JWT on every GraphQL request.** The
   browser holds a session, never a service credential.

## Alternatives

| Option | Why it lost |
|---|---|
| Clerk | The best developer experience of the group, genuinely. It loses on one structural point: identity would live in a third-party system while records live in Slashit's PostgreSQL, kept in step by webhooks. Every missed webhook is a user who can sign in but owns no rows, or a row whose owner does not exist. That failure is silent and it appears in production |
| Auth0 | The same sync problem as Clerk, with more configuration surface than one account per user justifies, and a steeper price curve |
| AWS Cognito | Poor developer experience, and its free-tier structure has changed more than once. Nothing about it fits this product better than the alternatives |
| WorkOS AuthKit | A generous free allowance and the right answer if enterprise SSO were on the roadmap. It is not: teams and sharing are product non-goals |
| Better Auth, self-hosted | Owns its own data, which is attractive. It is TypeScript-first and the backend here is Python. Wrong language for the stack |
| Build in-house | Already rejected by decision 0002. One account per user makes it look small, and password reset, session revocation, OAuth and breach response are where that impression ends |

## Consequences

| Good | Bad |
|---|---|
| No identity synchronisation exists to break, because there is only one store | Auth and the database are now the same vendor. A Supabase outage takes both |
| Row Level Security makes principle 7 enforceable by PostgreSQL, so a resolver that forgets a `WHERE user_id` returns nothing rather than another user's records | RLS binds only when the request's identity reaches the connection. A service-role connection bypasses every policy silently, with no error to notice |
| Email, magic link and OAuth providers arrive configured rather than built | Provider-specific JWT verification in FastAPI, which is a small amount of code nobody else maintains |
| Free to fifty thousand monthly active users, an amount V1 will not approach | Migration away is costly, as below |
| `user_id` exists, so epic 000 can attribute every model call | |

## Obligations this creates

These belong in the epic 000 build plan.

1. **Every table holding user data has RLS enabled and a policy, in the same
   migration that creates the table.** Not a follow-up task.
2. **Decide how identity reaches the connection.** A pooled connection with
   `set_config('request.jwt.claims', ...)` per transaction, or a role switch per
   request. This is open question 2 of
   [decision 0004](./0004-v1-technology-stack-revised.md) and it is the single
   point where isolation is won or silently lost.
3. **The service-role key never reaches the browser, and never serves a request
   made on behalf of a user** unless the resolver has already established
   ownership. It is for migrations and background jobs.
4. **Every feature's build plan states its isolation rule explicitly.** Already
   required by section 6 of the process rules. "Same as the rest of the app" is
   not an answer.
5. **Test the boundary, do not assume it.** The test plan of any feature
   touching user data includes a case where user A requests user B's record and
   receives nothing.

## Reversibility

Costly, and known to be so. Decision 0002 said the same before a provider was
named.

Supabase exports users, so email addresses, identifiers and metadata are
portable. Password hashes are exportable but tie the destination to a
compatible hashing scheme, and OAuth provider links generally have to be
re-established by the user. A migration is a project, not a configuration
change.

The mitigation is that the foreign key from Slashit's tables points at a user
identifier that would survive a move. Nothing in the product's own schema
depends on Supabase's shape.

## Scope

Binds every feature that touches user data, which in V1 is every feature.
First applies at [epic 000](../../features/000-ai-gateway/), where `user_id`
becomes real.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created | User accepted the recommended stack, which named Supabase Auth. Closes Q16 in the product brief and Q7 in the epic 000 PRD | user |
