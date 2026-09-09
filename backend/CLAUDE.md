# Slashit Backend

The Slashit API. Python, FastAPI, Strawberry GraphQL, PostgreSQL on Supabase.

No code exists here yet. This folder holds the rules that govern it when it
does.

## The binding ruleset

**Before writing any code in this folder, read
[`rules/repo-rules.md`](./rules/repo-rules.md).** It owns the directory layout,
the layer contract, how an API is written end to end, error handling, dependency
injection, testing, and naming.

The standing stack lives in
[`process-docs/tech-stack.md`](../process-docs/tech-stack.md) and is not
restated here. Where this folder contradicts it, the contradiction is named in
`rules/repo-rules.md` §2 rather than left for a reader to find.

## Rules that bind, stated in full

These seven survive a skipped link. Everything else is in the ruleset.

1. **Dependencies point one way.** Resolver depends on interactor, interactor on
   repository protocol, repository on model. Never the reverse, never sideways
   into another domain.
2. **The repository is the only place SQL lives.** It returns DTOs. A
   `Session`, a `Query` or a model instance never leaves it.
3. **Interactors hold the business rules and perform no I/O of their own.** They
   take collaborators in `__init__`. They never construct a repository, open a
   connection, or call a vendor.
4. **Business failures are typed data, not exceptions on the wire.** Every
   mutation returns a union of one success type and its named error types. A
   raised exception that reaches the client is a defect.
5. **Row Level Security is enabled, with a policy, in the same migration that
   creates any table holding user data.** This is rule T2 of the tech stack. A
   table without a policy is a defect, not a default.
6. **Authentication at the endpoint is not authorisation.** Every field declares
   its permission class. There is no ambient trust past the token check.
7. **One domain reaches another only through a published service, a port the
   consumer owns, and an adapter in the consumer.** Nothing else crosses. A
   domain's `public.py` is its whole contract, and the dependency graph between
   domains stays acyclic.

## Gate reminder

Root [`CLAUDE.md`](../CLAUDE.md) rule 1 stands: no code before that feature's
stage 4 is approved. This ruleset says what the code looks like when it is
allowed. It is not permission to start.
