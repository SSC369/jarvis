# Slashit Frontend

The Slashit web client. React, Vite, TypeScript, Apollo Client, MobX.

No code exists here yet. This folder holds the rules that govern it when it
does.

## The binding ruleset

**Before writing any code in this folder, read
[`rules/repo-rules.md`](./rules/repo-rules.md).** It owns the directory layout,
the Apollo layer, the four-file operation folder, the state boundary, the design
system, and the component conventions.

The standing stack lives in
[`process-docs/tech-stack.md`](../process-docs/tech-stack.md) and is not
restated here. This folder contradicts it in two rows, both by user direction on
2026-09-09. Both are named in `rules/repo-rules.md` §2.

Design tokens and screens are produced in Claude Design at stage 2 of each
feature. This ruleset governs how they are structured in code. It does not
decide what they look like.

## Rules that bind, stated in full

These six survive a skipped link. Everything else is in the ruleset.

1. **MobX stores are the source of truth for server state. The Apollo cache is
   a transport detail.** Operations fetch with `network-only`. A component
   reads a store, never a query result directly.
2. **One folder per GraphQL operation, four files.** `operation.graphql`, the
   generated file, `responseHandler.ts`, `useOperation.ts`. No operation is
   defined anywhere else.
3. **Every response is unwrapped by a `__typename` switch** with a `never`
   exhaustiveness check. A new backend error type breaks the build rather than
   falling through to a toast.
4. **`observer` wraps only at the default export.** `export default observer(Thing)`.
   Never inside the `const`.
5. **Never put a function, a store or a model in a hook dependency array.**
   Not to satisfy `react-hooks/exhaustive-deps`, not ever.
6. **No raw colour and no arbitrary Tailwind value in a feature.** Every visual
   value comes from a token. A hex code outside the token file is a defect.

## Committing

Never run `git commit` here until the user asks for it. Finish the work, leave it
in the working tree, and report what changed. Root [`CLAUDE.md`](../CLAUDE.md)
rule 7.

## Gate reminder

Root [`CLAUDE.md`](../CLAUDE.md) rule 1 stands: no code before that feature's
stage 4 is approved. This ruleset says what the code looks like when it is
allowed. It is not permission to start.
