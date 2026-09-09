---
doc: decision
id: 0003
title: Product name and mark
status: proposed
created: 2026-09-09
updated: 2026-09-09
supersedes: null
origin: features/001-capture-and-records-foundation/02-design.md section 5d
---

# 0003 — Product name and mark

> **Reopened 2026-09-09.** Slash was chosen, then found to collide with existing
> products. Round two is in section "Round two" below and on the canvas page
> "Name, round two". Slash remains the working name in the documents until a
> replacement is chosen, because churning every file twice costs more than
> waiting one decision.

## Context

The product has been called Jarvis since the first message, and that name is now
in the repository name, every document, the wordmark and the icon. The user
asked to settle the name and the mark before it goes further.

Four candidates are drawn on the design canvas, page "Name and logo", each with
a mark, an app icon and the identity applied inside the product.

## Decision

**Open.** Round two is running. Recommendation is **Cairn**.

Slash was chosen on 2026-09-09 and reopened the same day.

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

## Round two

Round one failed for one reason, and it is worth stating plainly because it
governs round two: **every candidate was a common English word.** Slash, Almanac,
Magpie and Trove-shaped names are the easiest to think of and the hardest to own.
A name you cannot own is a name you rent until someone with more lawyers asks for
it back.

Round two is built for distinctiveness: words with exact meanings that almost
nothing in software currently uses.

| Candidate | What it means | The case | The cost |
|---|---|---|---|
| **Cairn**, recommended | Stones stacked to mark a path so you find the way back | Plainest to say and spell. The mark draws itself. The metaphor is the product: small things set down deliberately, one on another | Quiet. Says nothing about software or intelligence, so first impressions rest on your copy |
| **Quipu** | The Inca knotted-cord system that recorded accounts and dates, readable for centuries | Literally this product, four hundred years early. By far the most ownable name here | Nobody can say it or spell it after hearing it. Every word-of-mouth referral leaks users |
| **Tessera** | One tile in a mosaic, and in Rome a token recording an entitlement | Each capture is one tile, the life is the mosaic. Holds all the way down, and the mark scales from favicon to wall | Three syllables and slightly precious. People will shorten it, so decide the short form now |
| **Kalend** | The first day of the Roman month, when debts were called in and books written up. Root of "calendar" | Reads as coined while carrying real meaning, which is the easiest combination to own | Looks like a misspelling of calendar. Expect corrections and lost typed traffic |

**Recommendation: Cairn.** It is the only one that is simultaneously easy to say,
easy to spell, easy to draw, and a true description of what the product does.

## What I cannot tell you

I have no way to check domain availability, app-store listings or trademark
registers from this session. Every collision note above is reasoning from general
knowledge, not a search. Before committing, someone has to actually look: the
register, the domain, the app stores, and a plain web search.

That is exactly the step that was skipped in round one.

## Reversibility

Still cheap. No users, no domain, no listing. The only cost of a second rename is
another pass over the documents and the canvas, which is an hour. That cost rises
steeply the moment anything is public, so this is the last comfortable moment to
get it right.

## Scope

Binds the product, every document, the repository name and the design system's
brand mark.
