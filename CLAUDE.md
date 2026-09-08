# Jarvis

An AI SaaS application. Early stage: the process is set up, the product is not
yet defined.

## How work happens here

Every feature moves through five gates, and each gate is a document in
`process-docs/`. Nothing gets built without that trail.

```
0 Intake → 1 Epic PRD → 2 Design → 3 Build plan (HLD) → 4 Implementation plan (LLD) → 5 Dev
```

The user approves each stage before the next one starts. Approval is a user
action in words. Silence is not approval.

**Before writing any document in `process-docs/`, read
[`process-docs/CLAUDE.md`](./process-docs/CLAUDE.md).** It is the binding
ruleset: folder layout, required front matter, what each stage document must
contain, how to write, and change control.

Before drafting any feature doc, also read
[`process-docs/product/product-brief.md`](./process-docs/product/product-brief.md)
for the standing product context.

## Rules that bind outside process-docs too

1. **No code before stage 4 is approved.** Sketches inside a doc are fine, files
   in the repo are not.
2. **Do not advance a gate on your own.** If asked to skip ahead, name the
   missing approval first.
3. **Do not invent product facts.** Unknowns go in the doc's Open Questions with
   an owner. Anything you filled in yourself is marked `> Assumption:` in place.
4. **Keep the registry current.** Any stage change updates
   `process-docs/index.md` in the same commit.
5. **Log deviations.** If the build leaves the approved plan, it goes in the
   feature's dev log the day it happens.

## Layout

| Path | What it holds |
|---|---|
| `process-docs/` | Product and process documents. Start here. |
| `process-docs/CLAUDE.md` | Rules for writing those documents |
| `process-docs/index.md` | Every feature and its current stage |
