---
doc: design
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 2
status: in-review
owner: user
created: 2026-09-09
updated: 2026-09-09
approved_on: null
supersedes: null
---

# Design — Capture and Records Foundation

Context: [PRD](./01-prd.md)
Canvas: https://claude.ai/code/artifact/f4b02674-cc87-486b-9250-dbeb8210e02b
Working files: `./assets/canvas/`

## 1. Design intent

Jarvis should feel like a fast tool that keeps a careful record, not like a chat
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
| Records, all | Everything Jarvis holds, in one list | FR-13, FR-14, FR-16, FR-17 | `Records` |
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
| Empty | Centred prompt, input, three example commands | "Tell Jarvis what to record." |
| Loading | Command echoed, skeleton field card | "Reading your command" · "Nothing is saved until every field is read" |
| Error | Refusal card, cause named, input preserved, retry | "Jarvis is at its shared limit right now" |
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

Jarvis installs to a home screen and runs without browser chrome. That adds
three surfaces a plain web page never has, plus an identity.

| Surface | Behaviour |
|---|---|
| Install invitation | Offered once per session, never twice, and dismissible. The browser then asks its own confirmation, which is not ours to draw |
| Offline | Records saved on the device stay readable, stamped with when they were saved. Capture is refused in the input itself, not after the user commits |
| Update waiting | A banner, never a forced reload. Anything typed survives it |
| Identity | Icon as the wordmark, since Jarvis has no logo. 192, 512 and a maskable 512 with a safe zone Android can crop to. Standalone display, warm paper background, dark ink theme colour |

**Offline reads, it does not capture.** Capture needs a model call, so a queued
offline capture would be a promise Jarvis cannot keep, and would contradict the
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
| FR-39 | Jarvis can be installed to a home screen and runs without browser chrome, with an icon, a name and a splash. The invitation appears at most once per session and can be dismissed permanently. |
| FR-40 | With no connection, records already on the device stay readable and are stamped with when they were saved. Capture is refused before the user commits, and nothing is queued. |
| FR-41 | When a new version is available, the user is told and chooses when to load it. Anything typed survives the reload. |

Approving these re-opens nothing downstream: no design, build plan or
implementation plan exists yet for this epic beyond this document.

## 6. Design system deltas

Everything here is new. Jarvis has no prior design system, so this epic
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
| First use | "Tell Jarvis what to record." | Says the model out loud rather than teaching syntax |
| First use, sub | "Everything starts with a command. Whatever you record, you can find, change and delete afterwards." | The product promise in one line |
| Pending question | "You can answer this whenever you like. Leave it and nothing is recorded." | Makes non-blocking explicit |
| Non-command input | "Jarvis records through commands" | States the rule without blaming |
| Non-command input, sub | "Nothing was recorded. Your text is kept below, so you can send it with a command instead of typing it again." | FR-9 in one sentence |
| Refusal | "Jarvis is at its shared limit right now" | Names the cause, not "something went wrong" |
| Refusal, sub | "Nothing was saved and nothing was half-saved." | The reassurance that matters most |
| Delete | "Finish API docs will be removed from your records. This cannot be undone." | Names the record, per FR-20 |
| Timezone | "Changing it affects how Jarvis reads dates from here on. Dates already recorded stay exactly as they are." | FR-28, said plainly |
| Records footer | "Every record here was created by a command" | Reinforces the one source of truth |

## 9. Open questions

| # | Question | Owner | Answer |
|---|---|---|---|
| Q1 | Is the direction right? Two alternatives sit on the Directions page. | user | |
| Q2 | Four commands exist in this epic, so `/add` filters to one result. Does the discovery design need proving against a longer list now, or when the list grows? | user | |
| Q3 | The records type filter shows All and Tasks only. Should the other types appear disabled so the shape is visible, or stay absent until they exist? Absent is drawn. | user | |
| Q4 | Overdue styling is drawn on the task list. The PRD does not mention lateness. In or out? | user | |
| Q5 | The transcript keeps history. How far back, and does it survive a reload? The PRD does not say, and it changes the empty state. | user | |
| Q6 | Should a pending question be answerable from anywhere, or only from the Command Center where it was asked? Only there is drawn. | user | |
| Q7 | Static mockups are drawn, not a clickable prototype. Is a clickable pass wanted before the build plan? | user | |
| ~~Q8~~ | Mobile is described, not drawn. Does phone use matter at launch? | user | **Drawn 2026-09-09** at 390 x 844, at the user's request. |
| Q9 | Do you approve proposed FR-39 to FR-41, so the installed app can be built? Without them the PWA artboards are design with no requirement behind them. | user | |
| Q10 | Offline reads but never captures. Is that the right line, or should an offline capture be held and sent when the connection returns? Holding it means a record that appears minutes later with a date resolved against the wrong moment. | user | |
| Q11 | Tablet is neither drawn nor decided. Leave it to fall between the two drawn ends? | user | |

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created. 18 artboards across four pages. | PRD approved, design stage started | pending |
| 2026-09-09 | Mobile drawn at 390 x 844, six artboards. Installed app added, four artboards. Responsive section rewritten from described to drawn. Section 5a and 5b added, with FR-39 to FR-41 proposed against the approved PRD. Q8 closed, Q9 to Q11 opened. | User asked for mobile and PWA alongside web | pending |
