---
doc: decision
id: 0003
title: Product name and mark
status: accepted
created: 2026-09-09
updated: 2026-09-09
supersedes: null
origin: features/001-capture-and-records-foundation/02-design.md section 5d
---

# 0003 — Product name and mark

## Context

The product has been called Jarvis since the first message, and that name is now
in the repository name, every document, the wordmark and the icon. The user
asked to settle the name and the mark before it goes further.

Four candidates are drawn on the design canvas, page "Name and logo", each with
a mark, an app icon and the identity applied inside the product.

## Decision

**Slash.** Chosen by the user on 2026-09-09.

The mark is the command character itself, a slash in a rounded square. The
wordmark is IBM Plex Mono, the same face the product uses for commands, so the
name and the thing it names are set in the same type.

My recommendation was Magpie, on trademark ownability. The user chose Slash. The
case for it is real and is the strongest of the four on one axis: no other
candidate explains the entire product in one glyph.

## Alternatives

| Option | The case | Why it might still win, or lose |
|---|---|---|
| Jarvis | Says AI assistant instantly. Already everywhere in the repository | Marvel's J.A.R.V.I.S. See the risk below |
| Almanac | A book of dates and records, which positions the product as a record rather than a chatbot | Sounds archival. The product also acts |
| Magpie | Collects everything, remembers where it put it. Short, warm, ownable | Playful. Magpies are associated with thieving, in a product holding private data |
| **Slash, chosen** | The product is the command character, so mark and interaction are one thing | Common word, violent second meaning, nearly unsearchable, names the mechanism rather than the value |

## The trademark question on Jarvis

Jasper.ai shipped as Jarvis.ai and renamed to Jasper in 2022 following a Marvel
trademark dispute. This is public record, not legal advice.

The consequence for this product is a question of timing rather than of law.
Nothing blocks development today. What a rename costs rises steeply once the
name is on a domain, an app listing, a signed-in user's home screen, or a
trademark filing. The cheapest moment to decide is now, before any of that
exists.

If Jarvis is kept, that should be a decision made knowingly, with an hour of a
lawyer's time behind it, rather than a decision made by never revisiting it.

## Consequences

| Good | Bad |
|---|---|
| The mark and the interaction are one thing. `/` is the logo, the first keystroke, and the whole product model | "Slash" is a common English word with a violent second meaning. Search and social handles will be hard |
| The trademark question on the incumbent name goes away entirely | The name describes the mechanism, not the value. If capture ever stops being commands-only, the name ages badly |
| Renamed while it cost almost nothing: no domain, no users, no listing | A rename pass across every document, done on 2026-09-09 |

## What the rename touched

| Changed | Left alone |
|---|---|
| Every document under `process-docs/` except the verbatim intake | `product/intake/`, which records the user's own words and must not be edited |
| Every design artboard except the four naming candidates | The four candidates, kept as the record of what was weighed |
| The wordmark, the app icon, the splash and the manifest | The GitHub repository, still named `jarvis` |

The repository name is the one loose end. Renaming it breaks every existing
clone and remote, so it is worth doing deliberately rather than as part of this
pass.

## Reversibility

Was cheap, and was spent. From here the cost rises with every user, listing and
link. Treat the name as settled.

## Scope

Binds the product, every document, the repository name and the design system's
brand mark.
