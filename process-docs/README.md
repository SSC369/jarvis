# Process Docs

The source of truth for what we build in Slashit and why. Code answers the
questions these documents ask.

The rules Claude follows when writing anything here are in
[CLAUDE.md](./CLAUDE.md). The live list of features and their stages is in
[index.md](./index.md).

## The flow

Every feature moves through six gates, in order. Each gate needs the user's
approval before the next one starts.

```
User states the requirement
        │
        ▼
  0  Epic              00-epic.md               the feature argued  → user approves
        │                                       out: detail, pros,
        │                                       cons, alternatives
        ▼
  1  PRD               01-prd.md                what and why        → user approves
        │
        ▼
  2  Design            02-design.md             screens, flows,     → user approves
        │                                       design system          design fixed
        ▼
  3  Build plan (HLD)  03-build-plan.md         architecture, and   → user approves
        │                                       questions to the       HLD locked
        │                                       user
        ▼
  4  Implementation    04-implementation-plan   file-level LLD,     → user approves
     plan (LLD)                                 tasks, tests           or edits
        │
        ▼
  5  Dev               05-dev-log.md            build, and record what actually happened
```

Design work at stage 2 is done with Claude Design. The canvas link and exports
live in the feature's `assets/` folder.

When a feature is big, stage 4 splits. `04-implementation-plan.md` becomes an
index that locks the slicing and the contracts between slices, and each slice
gets its own `04.N-<slug>.md`. The index is approved first, then each sub-plan
before its own dev starts, so building one slice can overlap with drafting the
next. The thresholds for splitting, and the rule that slices are vertical and
never layers, are in [CLAUDE.md](./CLAUDE.md).

## Starting a feature

1. Copy `templates/` into `NNN-<slug>/`, dropping the `.template` from each
   filename.
2. Write `00-epic.md`. Open by quoting what the user said, unedited, then argue
   the feature out: requirements in detail, pros, cons, best practices,
   alternatives.
3. Once the epic is approved, draft the PRD. Ask the questions you need in one
   grouped pass.
4. Add the feature to `index.md`.

Then work the gates. Do not start a stage while the previous one is unapproved.

## Layout

| Path | What it holds |
|---|---|
| `CLAUDE.md` | Binding rules for writing these docs |
| `index.md` | Every feature, its stage and status |
| `tech-stack.md` | The stack, and why each choice won |
| `product/product.md` | What Slashit is, who it serves, the pillars, the name |
| `product/v1-features.md` | What V1 ships, the epic list, later versions |
| `product/intake/` | Product-level requirements exactly as supplied |
| `templates/` | Copy these, never edit in place |
| `NNN-<slug>/` | One folder per feature, six docs each |

Technology is named in `tech-stack.md` and nowhere else. Product documents and
PRDs never mention a framework, a vendor or a hosting choice.
