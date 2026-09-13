---
doc: design
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 2
status: in-review
owner: user
created: 2026-09-09
updated: 2026-09-13
approved_on: null
supersedes: null
---

# Design — Capture and Records Foundation

Context: [PRD](./01-prd.md)
Canvas: https://claude.ai/code/artifact/f4b02674-cc87-486b-9250-dbeb8210e02b
Working files: `./assets/canvas/`

## 1. Design intent

Slashit should feel like a fast tool that keeps a careful record, not like a chat
window that happens to save things. Capture is one line and then it is over. The
record it produced is shown immediately, in full, so a wrong date is caught in
the second it is made rather than a week later.

The design is warm rather than technical. This is someone's life data, held for
years, so it reads as paper and ink rather than console green.

**Direction built:** warm paper, IBM Plex Sans for interface, IBM Plex Mono for
commands and data, Instrument Serif for display moments. One blue for action,
one amber that means "command". Two directions not taken sit on the Directions
page of the canvas.

## 2. Screen inventory

| Screen | Purpose | Serves | Artboard |
|---|---|---|---|
| Command Center, first use | Teach the command model with nothing recorded yet | FR-1, FR-2 | `Main` |
| Command discovery | Show every command on `/` | FR-2 | `CommandPalette` |
| Command filtering | Narrow the list as characters are typed | FR-3 | `CommandFilter` |
| Capture in flight | Show the model call is working, nothing saved yet | FR-6, NFR-2 | `CaptureLoading` |
| Capture confirmed | Show every extracted field at the moment of creation | FR-6, FR-7 | `CaptureSuccess` |
| Question waiting | A missing field asked for, blocking nothing | FR-8, FR-36 to FR-38 | `PendingQuestion` |
| Input without a command | Explain, preserve the text, offer the command | FR-9 | `NonCommandInput` |
| Capture refused | Shared limit or provider outage, nothing half-saved | FR-35 | `QuotaRefusal` |
| Records, all | Everything Slashit holds, in one list | FR-13, FR-14, FR-16, FR-17 | `Records` |
| Records, empty | First-run state | FR-14 | `RecordsEmpty` |
| Records, tasks | Type filter applied, and the `/tasks` destination | FR-15, FR-25 | `RecordsTasks` |
| Record detail | Every stored field, plus origin and what was typed | FR-18, FR-22 | `RecordDetail` |
| Record edit | Change any user-supplied field | FR-19 | `RecordEdit` |
| Delete confirmation | Naming the record being deleted | FR-20, FR-21 | `DeleteConfirm` |
| Settings | Timezone, detected and changeable | FR-27, FR-28 | `Settings` |
| Shared states | Loading, error, session ended, empty result | all surfaces | `EdgeStates` |
| Direction B, C | Alternatives not taken, low-fi | — | `DirectionB`, `DirectionC` |

### Mobile, 390 x 844

| Screen | Purpose | Serves | Artboard |
|---|---|---|---|
| Command Center | Capture on a phone, rail replaced by a bottom bar | FR-1, FR-2 | `MobileMain` |
| Command discovery | The command list as a tap-first sheet | FR-2, FR-3 | `MobileCommands` |
| Capture confirmed | Field card stacked instead of three-up | FR-6, FR-7 | `MobileCaptureSuccess` |
| Question waiting | The same non-blocking question, with the waiting chip | FR-8, FR-36 to FR-38 | `MobilePending` |
| Records | Table becomes stacked rows | FR-13 to FR-17 | `MobileRecords` |
| Record detail | Fields stacked, actions full width | FR-18, FR-19, FR-20 | `MobileRecordDetail` |

### Installed app

| Screen | Purpose | Serves | Artboard |
|---|---|---|---|
| Install invitation | Ask to add to the home screen, once | proposed FR-39 | `PWAInstall` |
| Offline | Records readable, capture honestly refused | proposed FR-40 | `PWAOffline` |
| Update waiting | A new version is ready to load | proposed FR-41 | `PWAUpdate` |
| Installed identity | Icons, maskable safe zone, splash, manifest values | proposed FR-39 | `PWAIdentity` |

### Dark theme

| Screen | Purpose | Serves | Artboard |
|---|---|---|---|
| Capture, dark | The command surface and a created record | proposed FR-42 | `DarkCapture` |
| Records, dark | The table on a dark ground | proposed FR-42 | `DarkRecords` |
| Record detail, dark | Fields and origin on a dark ground | proposed FR-42 | `DarkRecordDetail` |
| Mobile, dark | Command centre and records on a phone | proposed FR-42 | `DarkMobileMain`, `DarkMobileRecords` |
| Command discovery, dark | The palette on a dark ground | proposed FR-42 | `DarkCommandPalette` |
| Mobile capture, dark | A created record on a phone | proposed FR-42 | `DarkMobileCapture` |
| Token pairs | Every token, light beside dark, with its role | proposed FR-42 | `DarkTokens` |

### Theme toggle

| Screen | Purpose | Serves | Artboard |
|---|---|---|---|
| Settings, web, light | The theme control with light selected | proposed FR-42, FR-27 | `Settings` |
| Settings, web, dark | The same control with dark selected | proposed FR-42 | `DarkSettings` |
| Settings, mobile, light | Theme, timezone and account on a phone | proposed FR-42, FR-27 | `MobileSettings` |
| Settings, mobile, dark | The same, dark | proposed FR-42 | `DarkMobileSettings` |

### Name and logo candidates

Superseded by §5d, which carries the final round's candidates with an honest
case and cost for each. This table was never updated across three naming
rounds and pointed at an artboard, `NameSlashit`, that does not exist on the
canvas — the real artboard is `NameSlash`. Removed rather than fixed in place,
since §5d already says this once.

## 3. Flows

| Flow | Entry | Steps | Exit | Serves |
|---|---|---|---|---|
| Clean capture | Command Center | Type `/`, choose or type the command, add arguments, Enter | Record created, fields shown in place | FR-1 to FR-7 |
| Capture with a gap | Command Center | Command missing a required field, question appears, user answers now or later | Record created on the answer, or never | FR-8, FR-36 to FR-38 |
| Input without a command | Command Center | Plain text submitted, guidance shown, text preserved, command applied to it | Record created, or nothing | FR-9 |
| Inspect and correct | Records | Filter or search, open a record, edit or delete | Record changed or removed | FR-13 to FR-21 |
| Refusal | Command Center | Capture fails on quota or outage, input preserved, retry | Retry succeeds, or user waits | FR-35 |

## 4. States

Five states per surface. Where a state cannot occur, that is stated rather than
left blank.

### Command Center

| State | What the user sees | Copy |
|---|---|---|
| Empty | Centred prompt, input, three example commands | "Tell Slashit what to record." |
| Loading | Command echoed, skeleton field card | "Reading your command" · "Nothing is saved until every field is read" |
| Error | Refusal card, cause named, input preserved, retry | "Slashit is at its shared limit right now" |
| Success | Field card showing task, due with absolute date, status | "Task created" |
| No permission | Session ended, sign in again | "Your session ended" |

### Records list

| State | What the user sees | Copy |
|---|---|---|
| Empty | Icon, one line, route back to capture | "Nothing recorded yet" |
| Loading | Skeleton rows in the real table shape | — |
| Error | Card, reassurance that data is safe, retry | "Couldn't load your records" |
| Success | Table with type, title, date, status | "5 records" |
| No permission | Session ended | "Your session ended" |
| Empty result | Search matched nothing, clear search | "No records match 'passport'" |

### Record detail and edit

| State | What the user sees | Copy |
|---|---|---|
| Empty | Cannot occur. A detail view exists only for a record that exists | — |
| Loading | Skeleton in the field rows | — |
| Error | Card in place of the fields, retry | "Couldn't load this record" |
| Success | Fields, origin, original input, Edit and Delete | — |
| No permission | Session ended | "Your session ended" |

### Settings

| State | What the user sees | Copy |
|---|---|---|
| Empty | Cannot occur. Timezone always has a detected value | — |
| Loading | Skeleton in the control | — |
| Error | Inline message, current value kept | "Couldn't save that change" |
| Success | Value shown with its offset, note about future input | "Detected from your browser" |
| No permission | Session ended | "Your session ended" |

## 5. Responsive behaviour

Drawn at two widths. Tablet is described, because it is the width least likely
to matter first and the two drawn ends bound it.

| Breakpoint | Layout |
|---|---|
| Desktop, 1280 and up | Rail plus content, as drawn on the Capture and Records pages |
| Tablet, 768 to 1279 | Rail collapses to icons. The records table drops the type column when a single type is filtered. Not drawn |
| Mobile, under 768 | Drawn at 390 x 844. Rail becomes a bottom bar of three tabs. The records table becomes stacked rows, title first, type and date beneath, status on the right. The three-up field card stacks to labelled rows. The command list sits directly above the input and is tap-first, so the highlighted row is a default rather than a cursor |

**What is deliberately not drawn on the phone.** No status bar and no keyboard.
Both are painted by the device on top of the layout, and a drawn copy reads as
a doubled-up mistake. On `MobileCommands` the empty band below the input is
exactly the space the real keyboard occupies.

Touch targets are 44 px or taller everywhere, and the bottom bar keeps clear of
the home indicator.

## 5a. Installed app, PWA

Slashit installs to a home screen and runs without browser chrome. That adds
three surfaces a plain web page never has, plus an identity.

| Surface | Behaviour |
|---|---|
| Install invitation | Offered once per session, never twice, and dismissible. The browser then asks its own confirmation, which is not ours to draw |
| Offline | Records saved on the device stay readable, stamped with when they were saved. Capture is refused in the input itself, not after the user commits |
| Update waiting | A banner, never a forced reload. Anything typed survives it |
| Identity | Icon as the wordmark, since Slashit has no logo. 192, 512 and a maskable 512 with a safe zone Android can crop to. Standalone display, warm paper background, dark ink theme colour |

**Offline reads, it does not capture.** Capture needs a model call, so a queued
offline capture would be a promise Slashit cannot keep, and would contradict the
PRD's line that offline capture is out of scope. The input says so plainly
rather than accepting work it cannot finish.

**No push notification design, on purpose.** The approved decision is in-app and
email. Installing makes web push cheap to add, which is worth reopening at epic
002 with reminders, as a decision rather than a side effect.

## 5b. These surfaces exceed the approved PRD

The PRD is approved and locked. Mobile layout is inside it, because the PRD ships
web and a phone browser is web. **The installed-app surfaces are not**, so they
need a PRD change before they can be built.

Proposed requirements, for the user to approve or strike:

| Proposed | Requirement |
|---|---|
| FR-39 | Slashit can be installed to a home screen and runs without browser chrome, with an icon, a name and a splash. The invitation appears at most once per session and can be dismissed permanently. |
| FR-40 | With no connection, records already on the device stay readable and are stamped with when they were saved. Capture is refused before the user commits, and nothing is queued. |
| FR-41 | When a new version is available, the user is told and chooses when to load it. Anything typed survives the reload. |
| FR-42 | The interface follows the operating system's light or dark setting, and the user can override it. The override persists across sessions and devices. |

Approving these re-opens nothing downstream: no design, build plan or
implementation plan exists yet for this epic beyond this document.

## 5c. Dark theme

Dark is not the light palette inverted. The light theme is warm paper, so the
dark ground is warm near-black rather than blue-grey, and the two read as one
product rather than two. Accents lighten so they stay legible on a dark ground,
and a primary button becomes a light blue field with dark ink on it rather than
white on a mid blue.

`DarkTokens` carries every pair, token by token, with its role. Nothing in the
dark theme is a new decision about layout, spacing or type. Only colour changes.

**How the theme is chosen.** Three options, not two: System, Light, Dark. System
is the default and follows the device through the day, so a user who switches at
sunset does not have to switch twice.

The control carries two preview tiles beside it, one light and one dark, showing
a card, some text and a button in each. Without them a segmented control makes
you change the whole application to find out what you are choosing. The tiles
appear on the phone as well, where switching back and forth costs more.

The override is a setting the PRD does not currently have. It is proposed as
FR-42 below.

## 5d. Name and logo

Four candidates, each drawn as a mark, an app icon at three sizes, and the
identity applied inside the product. Each carries an honest case and an honest
cost, because a set where only the favourite gets defended is not a choice.

| Candidate | The case | The cost |
|---|---|---|
| Slashit | Says AI assistant before anyone reads a word, and every document and the repository already use it | It is Marvel's J.A.R.V.I.S. See the risk below |
| Almanac | A book of dates, records and things worth looking up, which is what this product is. Positions it as a record rather than a chatbot | Sounds archival rather than active, and the product also acts |
| Magpie | The metaphor is the product loop: gathers what catches the eye, knows where every piece is. Short, warm, easiest to own | Playful, and magpies carry a thieving reputation, which some will notice in a product holding private information |
| Slashit | The product is the command character, so the logo and the interaction are one thing | A common word with a violent second meaning, nearly unsearchable, and it names the mechanism rather than the value |

> **Settled: the product is Slashit**, chosen 2026-09-09 after Slash was found to
> collide. Three rounds and fourteen candidates ran; they stay on the canvas as
> the record. See [the product doc](../product/product.md#11-name-and-mark).

**Chosen: Slashit**, on 2026-09-09, recorded as
[the product doc](../product/product.md#11-name-and-mark). My
recommendation had been Magpie, on ownability. Slashit wins on a different axis and
it is a real one: no other candidate explains the whole product in one glyph.

The four candidates stay on the canvas as the record of what was weighed.

**What the name changed in the design.** Two things, both worth knowing.

The wordmark is now IBM Plex Mono, the same face the product sets commands in, so
the name and the thing it names share a typeface. The mark is the slash itself.

The navigation item that used to carry the product name is now **Capture**.
Calling a tab "Slashit" inside an app called Slashit says nothing, where "Capture"
says what the tab is for. The other two tabs, Records and Settings, are unchanged.

**The risk on the incumbent name.** Jasper.ai shipped as Slashit.ai and renamed to
Jasper in 2022 following a Marvel trademark dispute. That is a matter of public
record rather than legal advice, and it is a reason to spend twenty minutes with
someone who gives legal advice before the name goes on anything public. Nothing
here blocks development: the repository and the documents can keep the name until
a decision is made.

## 5e. Logo

Six sheets on the canvas page "Logo": primary lockup, wordmark treatments,
construction and clear space, lockups and one-colour forms, misuse, and applied.

**The mark is the keystroke.** Every record begins with a slash, so the logo is
the first thing the user types rather than a picture of something else. It is set
in a rounded ink square, cream slash, and it survives to 16 px because it is one
shape.

**The wordmark is `slash.it`**, set in IBM Plex Mono, the same face the product
sets commands in, with the dot in amber as the only colour.

**The wordmark is deliberately not the name.** Set as one undifferentiated
lowercase word, `slashit` breaks at the wrong place for many readers. Three of
the four treatments on the wordmark sheet break the word visibly and remove the
problem. `slash.it` is the one shipped. `slashit` is never permitted as a logo.

| Rule | Value |
|---|---|
| Corner radius | 22% of the mark's width |
| Slash angle | 20 degrees from vertical |
| Stroke width | 19% of the mark's width |
| Clear space | 25% of the mark's height on every side |
| Minimum mark | 16 px |
| Minimum lockup | 104 px wide |

The misuse sheet names six ways it will be broken. Five of them by well-meaning
people in a hurry.

## 6. Design system deltas

Everything here is new. Slashit has no prior design system, so this epic
establishes one.

| Change | Kind | Token or component | Note |
|---|---|---|---|
| Warm neutral palette | added | `paper`, `surface`, `ink`, `ink2`, `ink3`, `line`, `line2` | Warm whites, saturation kept very low |
| Action blue | added | `blue`, `blueWash` | Primary actions, focus rings, the waiting state |
| Command amber | added | `amber`, `amberWash` | The colour that means "a command". Same lightness and chroma as blue, different hue |
| Semantic red and green | added | `red`, `redWash`, `green`, `greenWash` | Destructive and complete |
| Type ramp | added | IBM Plex Sans, IBM Plex Mono, Instrument Serif | Mono is reserved for commands and captured text, never for interface labels |
| Command palette | added | component | Grouped list above the input, keyboard hints in the footer |
| Field card | added | component | Three-up extracted fields with an origin footer |
| Record table | added | component | Type, title, date, status, with a status pill |
| Status pill | added | component | Pending, done, waiting, error |
| Note block | added | component | Info, warning, error, used for guidance and refusals |

**Added 2026-09-09 with dark theme and identity:**

| Change | Kind | Token or component | Note |
|---|---|---|---|
| Dark value for every colour token | added | all colour tokens | Same names, second value. No token exists in one theme only |
| Warm near-black ground | added | `paper`, `surface`, `rail` dark values | Warm rather than blue-grey, to match the light theme's paper |
| Inverted primary button | changed | `.btn.pri` in dark | Light blue field, dark ink on it |
| Bottom tab bar | added | component | Mobile only, replaces the rail |
| Stacked record row | added | component | Mobile records, replaces the table row |
| Offline and update banners | added | component | Installed app only |
| Brand mark | added | component | Slashit. Mark, wordmark, lockups, one-colour forms, construction rules |

No one-off styles outstanding. Every colour and size in the canvas comes from
the set above.

## 7. Accessibility

| Area | Decision |
|---|---|
| Contrast | Body ink on paper is well past 4.5:1. Muted ink is used for secondary text only, never for the sole carrier of meaning |
| Colour is never alone | Status carries a word as well as a colour. The refusal card names its cause in text |
| Keyboard path | The input is the first focus. `/` opens the palette, arrows move, Enter chooses, Escape dismisses. Records rows are reachable in order, and every row action is a real control |
| Screen reader | The palette announces as a listbox with the active option. A created record is announced as a live region so the extracted fields are heard, not just seen |
| Motion | The only motion is the loading shimmer. It stops entirely under reduced-motion, leaving a flat placeholder |
| Focus order | Rail, then content, then the input dock. The pending question is reachable without leaving the keyboard |

## 8. Copy

| Location | Text | Note |
|---|---|---|
| First use | "Tell Slashit what to record." | Says the model out loud rather than teaching syntax |
| First use, sub | "Everything starts with a command. Whatever you record, you can find, change and delete afterwards." | The product promise in one line |
| Pending question | "You can answer this whenever you like. Leave it and nothing is recorded." | Makes non-blocking explicit |
| Non-command input | "Slashit records through commands" | States the rule without blaming |
| Non-command input, sub | "Nothing was recorded. Your text is kept below, so you can send it with a command instead of typing it again." | FR-9 in one sentence |
| Refusal | "Slashit is at its shared limit right now" | Names the cause, not "something went wrong" |
| Refusal, sub | "Nothing was saved and nothing was half-saved." | The reassurance that matters most |
| Delete | "Finish API docs will be removed from your records. This cannot be undone." | Names the record, per FR-20 |
| Timezone | "Changing it affects how Slashit reads dates from here on. Dates already recorded stay exactly as they are." | FR-28, said plainly |
| Records footer | "Every record here was created by a command" | Reinforces the one source of truth |

## 9. Open questions

| # | Question | Owner | Answer |
|---|---|---|---|
| ~~Q1~~ | Is the direction right? Two alternatives sit on the Directions page. | user | **Answered 2026-09-13.** Yes, the built direction is right. Directions B and C stay on the canvas as the record, not taken. |
| ~~Q2~~ | Four commands exist in this epic, so `/add` filters to one result. Does the discovery design need proving against a longer list now, or when the list grows? | user | **Answered 2026-09-13.** Prove it now. **Follow-up:** add a longer synthetic command list to `CommandPalette`/`CommandFilter` before stage 2 closes, so the filtering design is validated against more than four commands. |
| ~~Q3~~ | The records type filter shows All and Tasks only. Should the other types appear disabled so the shape is visible, or stay absent until they exist? Absent is drawn. | user | **Answered 2026-09-13.** Stay absent, as drawn. No change. |
| ~~Q4~~ | Overdue styling is drawn on the task list. The PRD does not mention lateness. In or out? | user | **Answered 2026-09-13.** In scope. **Follow-up:** lateness was not argued in `00-epic.md` and is not an `01-prd.md` requirement. Per root ruleset rule 3 and `process-docs/CLAUDE.md` §6, this needs a change record adding it to the epic and PRD before the design can rely on it, not a silent addition here. |
| ~~Q5~~ | The transcript keeps history. How far back, and does it survive a reload? The PRD does not say, and it changes the empty state. | user | **Answered 2026-09-13.** Survives reload, kept indefinitely, same durability as records. |
| ~~Q6~~ | Should a pending question be answerable from anywhere, or only from the Command Center where it was asked? Only there is drawn. | user | **Answered 2026-09-13.** Answerable from anywhere. **Follow-up:** not currently drawn; needs new design work (e.g. a way to answer from Records) before stage 2 closes. |
| ~~Q7~~ | Static mockups are drawn, not a clickable prototype. Is a clickable pass wanted before the build plan? | user | **Answered 2026-09-13.** Yes, wanted before the build plan starts. **Follow-up:** a clickable pass on the canvas is outstanding work, blocking stage 3. |
| ~~Q8~~ | Mobile is described, not drawn. Does phone use matter at launch? | user | **Drawn 2026-09-09** at 390 x 844, at the user's request. |
| ~~Q9~~ | Do you approve proposed FR-39 to FR-41, so the installed app can be built? Without them the PWA artboards are design with no requirement behind them. | user | **Answered 2026-09-13.** Approved. **Follow-up:** needs a change record adding FR-39 to FR-41 to `01-prd.md`, per §5b. |
| ~~Q10~~ | Offline reads but never captures. Is that the right line, or should an offline capture be held and sent when the connection returns? Holding it means a record that appears minutes later with a date resolved against the wrong moment. | user | **Answered 2026-09-13.** Offline reads only, as drawn. Consistent with FR-40 as proposed. |
| ~~Q11~~ | Tablet is neither drawn nor decided. Leave it to fall between the two drawn ends? | user | **Answered 2026-09-13.** Yes, interpolate. No dedicated tablet artboard. |
| ~~Q12~~ | Which name? Magpie is recommended. Keeping Slashit is a decision to make knowingly, given the trademark question. | user | **Settled 2026-09-09**, recorded in §5d: the product is Slashit, chosen knowingly against the recommendation and the trademark risk. This row was left open in error; closed here to match §5d. |
| ~~Q13~~ | Does the theme override belong in epic 001, as proposed FR-42, or does following the system setting suffice for V1? Following only is cheaper and removes a setting. | user | **Answered 2026-09-13.** Following the system setting only. FR-42 is not added. **Follow-up:** `Settings`, `DarkSettings`, `MobileSettings` and `DarkMobileSettings` currently draw a three-way override control (§5c). That control needs removing from those artboards, since there is no override to control. |
| ~~Q14~~ | If the name changes, when? | user | **Done 2026-09-09**, before any code existed. The GitHub repository is still named `jarvis` and is the one loose end. |
| ~~Q15~~ | Renaming the GitHub repository breaks every existing clone and remote. Do it now while there is one clone, or leave it? | user | **Answered 2026-09-13.** Rename now, to `slashit`. |
| ~~Q16~~ | The command-centre tab is renamed Capture, because a tab called Slashit inside Slashit says nothing. Agreed? | user | **Answered 2026-09-13.** Agreed, as already drawn. |

### What today's answers still leave open

Every question above has an answer, but four answers create new work rather than
closing outright. Stage 2 is not ready to approve until these are resolved:

1. **Q2, Q6, Q7** need canvas work: a longer command list proven against
   discovery, a way to answer a pending question from outside the Command
   Center, and a clickable pass over the key flows.
2. **Q13** needs canvas work in the other direction: the override control drawn
   in four Settings artboards must come out, since FR-42 was declined.
3. **Q4 and Q9** need a change record against `00-epic.md` and `01-prd.md`
   before this design can rely on overdue styling or the PWA requirements,
   per root ruleset rule 3.
4. **Q15** is an infrastructure action (the GitHub repository), tracked outside
   this document.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-13 | All sixteen open questions answered. §2's stale "Name and logo candidates" table removed (superseded by §5d, and referenced a non-existent artboard). Four answers open new work: canvas additions for Q2, Q6, Q7; a canvas removal for Q13; change records against the epic and PRD for Q4 and Q9. Not yet approved: those four items are still outstanding | User reviewed the canvas and went through §9 | pending |
| 2026-09-09 | Created. 18 artboards across four pages. | PRD approved, design stage started | pending |
| 2026-09-09 | Name settled as Slashit. Logo system drawn, six sheets. Product renamed across every artboard and document. Wordmark set as `slash.it`, and the lowercase misread documented as a permanent constraint on the wordmark. Section 5e added. Q12 closed, Q17 opened. | User chose Slashit and asked for a proper logo | pending |
| 2026-09-09 | Round three added: Docket, Kist, Sundry, Colophon, Mnemo, Keepsake, plus a shortlist sheet comparing all fourteen candidates with a risk read. | User asked for more options | pending |
| 2026-09-09 | Name reopened. Slashit collides with existing products. Four round-two candidates drawn, chosen for ownability: Cairn, Quipu, Tessera, Kalend. Q12 reopened. Documents keep Slashit as a working name until a replacement is chosen. | User reported the collision | pending |
| 2026-09-09 | Renamed to Slashit across every artboard and document, verbatim intake excepted. Wordmark set in IBM Plex Mono, mark is the slash. Command-centre tab renamed Capture. Theme toggle drawn on web and mobile in both themes, four artboards, with preview tiles. Two more dark artboards. Q12 and Q14 closed, Q15 and Q16 opened. | User chose Slashit and asked for the theme toggle | pending |
| 2026-09-09 | Dark theme drawn, six artboards, with a token sheet pairing every light and dark value. Four name and logo candidates drawn, each with its case and its cost. Sections 5c and 5d added. FR-42 proposed. Q12 to Q14 opened. | User asked for a dark theme and for name and logo options | pending |
| 2026-09-09 | Mobile drawn at 390 x 844, six artboards. Installed app added, four artboards. Responsive section rewritten from described to drawn. Section 5a and 5b added, with FR-39 to FR-41 proposed against the approved PRD. Q8 closed, Q9 to Q11 opened. | User asked for mobile and PWA alongside web | pending |
