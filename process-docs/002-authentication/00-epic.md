---
doc: epic
feature: 002-authentication
title: Authentication
stage: 0
status: approved
owner: user
created: 2026-09-14
updated: 2026-09-14
approved_on: 2026-09-14
supersedes: null
---

# Epic — Authentication

> **Approved** by @user on 2026-09-14. Locked — changes require a change record (§7).

Context: [Product](../product/product.md) · [V1 features](../product/v1-features.md)

## As supplied

> plan for signup, login pages, manual signup with username, email. emaill
> verification process like send email to entered email, user will enter the
> otp from email in app. take ref from radius app for auth flow. ro do you
> suggest a good UX auth flow.
>
> this should be included as first slice in next feature.
>
> lets discuss and plan for auth flow

> go with supabase auth flow.
> plan for this as next immediate feature plan

Not in the source product definition. `product/v1-features.md` never scoped an
auth epic; 001 shipped its three slices against a dev-only console workaround
instead, recorded in `index.md` as the reason it is still `in-review`.

## Problem

001 has no real front door. Every session so far starts from a workaround typed
into a browser console, not a screen. Every entity in Slashit is scoped to one
owner (`product/product.md` §6, "one account per user"), and every table is
protected by row-level security keyed to `auth.users` (`tech-stack.md` §3,
`SET LOCAL ROLE authenticated`). Neither of those means anything until a person
can create an account and prove they own it without a developer's help. Nothing
built after 001 can be used by anyone but its own developers until this exists.

## What this feature is

A self-serve account system: a person signs up with a username, an email and a
password; proves the email is theirs by entering a six-digit code Slashit
emails them; and from then on signs in with email and password. Added
2026-09-14: a person can also sign up or sign in with Google instead, skipping
the password and the code entirely. It is the one screen every other feature
sits behind.

## Requirements in detail

| Area | What it has to do | Why it matters | Notes |
|---|---|---|---|
| Sign up | Collect username, email, password. Validate shape client-side before submit (email format, password rules, username characters) | Cheapest place to catch a bad value is before it leaves the browser | Server-side validation still required; client-side is UX only |
| Account creation | Create the identity record and the username record together | A user row with no username, or a username with no login, is a broken account | Username has nowhere to live in Supabase's own `auth.users`; it needs a table Slashit owns |
| Email OTP | On signup, send a six-digit code to the entered email. Hold the account unverified until the right code is entered | Matches "enter the otp from email in app" in the source, not a link | Code expiry and resend need explicit values, see Open questions |
| Verification screen | Code entry, resend action with a cooldown, distinct errors for wrong vs. expired code | A dead end here is the account's first impression of the product | |
| Unverified accounts | No session until verification succeeds | An unverified email is not a proven identity | What happens to an account nobody ever verifies is open, see Open questions |
| Sign in | Email and password. Route an unverified account back into the OTP screen instead of a bare error | A generic "sign-in failed" hides a fixable problem from the user | |
| Sign out | Added 2026-09-15. End the session from wherever the app already shows the account | A missing, obvious gap: nothing in this epic's original scope named it, but a shared or public device staying signed in indefinitely is a real cost | Supabase's own `signOut()`; the app's existing session-change listener handles the rest |
| Session | A successful sign-in establishes the Supabase session the rest of the app already expects | 001's real Gemini and real-DB testing already assumed a real Supabase session; this is what produces it | |
| Username uniqueness | Enforced at the database, not only in the form | Two accounts with the same handle is a support problem later, a constraint now | Case-insensitive, 3-20 chars, letters/numbers/underscore, per Q4 |
| Password reset | A user who forgets their password can request a reset, prove email ownership, and set a new one | Added 2026-09-14: without it, a forgotten password is a permanent lockout | Same OTP mechanism as signup verification, reused rather than a second pattern |
| Google sign-in | Added 2026-09-14. A person can create or access an account through Google, alongside manual signup, not instead of it | Removes the email round-trip entirely for a user willing to use it; Google has already verified the email | A Google sign-in on an email with an existing manual account merges into it, per Q6. Added 2026-09-15: Google's avatar is stored and shown, when it provides one (FR-21) |
| Rate limiting and lockout | Added 2026-09-14. Repeated failed sign-ins, repeated wrong codes, and repeated signups from one email or address are all throttled, not just OTP resend | An unthrottled password or code field is a brute-force target; this was underspecified before | Exact thresholds (attempt counts, cooldown lengths) are unset, see Open questions |

## Pros

- Unblocks every other epic. Nothing after 002 can leave developer hands
  without it (all of 003 to 011 now list 002 as a dependency in
  `v1-features.md`).
- Serves P4, "the user is in control" (`product/product.md` §3): control over a
  record presupposes an owner who can be told apart from every other owner.
- Serves principle 7, "user data never crosses a user boundary"
  (`product/product.md` §4): the boundary is an account, and there is not yet a
  real way to open one.
- OTP entered in-app, not a link opened from the email client, keeps the whole
  flow inside Slashit's own screens, in the spirit of pillar P1's "one place."
- No new infrastructure decision. Supabase Auth is already the locked provider
  (`tech-stack.md` §"Database and auth"); this epic is UX and schema on top of
  a choice that is made.
- Google sign-in (added 2026-09-14) removes the email round-trip for anyone
  willing to use it, and Supabase Auth supports it as a configuration, not a
  new provider.

## Cons

- Adds a mandatory email round-trip before first use. Every other product
  decision in V1 has minimized friction (principle 3, "minimize confirmation");
  this is friction nothing else in the roadmap has.
- OTP delivery depends on an email provider outside Slashit's control. A code
  stuck in spam or delayed by minutes blocks the user completely, with no
  fallback path defined yet.
- Username is a field Supabase's own `auth.users` does not carry. It forces a
  second table kept in step with the identity table, the same class of
  sync risk `tech-stack.md` §"Database and auth" already rejected Clerk and
  Auth0 over, now self-inflicted at a smaller scale.
- More states to design and support: expired codes, resend abuse, an account
  that signs up and never verifies.
- Google sign-in (added 2026-09-14), merging into an existing manual account
  by matching email (decided 2026-09-14, Q6), trusts Google's own email
  verification as much as this epic trusts its own OTP. That is consistent,
  not a new risk, but it does mean anyone who once verified an email address
  with Slashit can now also reach that account through Google, without ever
  having linked the two accounts themselves.

## Best practices and prior art

> Assumption: the user named "the radius app" as the reference for this flow.
> I don't know that product and won't guess at its screens. Logged as Q1.
> Entries below are patterns from products I can name and describe.

| Product | How they do it | What to take | What to avoid |
|---|---|---|---|
| Supabase Auth UI (the vendor's own reference implementation) | Email + password signup, then `verifyOtp` against a 6-digit code, all first-party inside the app | It is the exact primitive `tech-stack.md` already committed to; no adapter layer needed | Its default templates are bare; copy and layout still need real design work |
| Stripe Dashboard | Email + password, email verified async in the background, account usable before verification for low-risk actions | Shows that "usable before verified" is a legitimate choice, not just "blocked until verified" | Does not fit Slashit: every action here touches personal data, so gating on verification is the safer default |
| GitHub | Username + email + password at signup, verification by a link, a numeric device-verification code only for suspicious sign-ins later | Confirms username-plus-email as a normal shape for manual signup | Its link-based verification is the pattern this epic is deliberately not copying |
| Notion, Linear | Email/password (or email code) offered side by side with a Google button; picking Google skips password and email verification entirely | Confirms manual and OAuth sign-in coexisting, and that email verification is redundant on a Google account | Both treat "same email, different method" as a merge by default; neither surfaces that choice to the user, which is worth deciding on deliberately rather than copying quietly |

## Alternatives considered

| Option | What it gives | What it costs | Verdict |
|---|---|---|---|
| Do nothing, keep the console workaround | Zero build cost | No real user can ever reach the product | Rejected, blocks everything |
| Password + email OTP verification (as supplied) | One familiar credential (password) plus a lightweight, in-app proof of email ownership | The cons above: mandatory email round-trip, a second identity table | Chosen |
| Passwordless, OTP on every sign-in | No password to forget, reset, or leak | An email round-trip on every login, not just once, plus a device-trust mechanism this epic has not scoped | Rejected, more ongoing friction than the source asked for |
| Magic link instead of a typed code | Slightly less typing | Breaks cross-device flow (sign up on laptop, open email on phone) and needs deep-link handling the source did not ask for | Rejected, the source explicitly asked for a typed code |
| OAuth / social login only, replacing manual signup | No password to manage at all | No clean way to collect a username, and the source explicitly asked for manual signup | Rejected. Manual signup stays |
| Google sign-in alongside manual signup | Removes the email round-trip for anyone willing to use it, at no cost to the manual path | A second identity path to test | **Adopted 2026-09-14**, per this alternative's own framing above: an addition, not a replacement. Merges into a matching manual account, per Q6 |

## Risks and unknowns

| Risk | Likelihood | Impact | What would tell us early |
|---|---|---|---|
| Supabase's built-in email sending has a low default rate limit, unsuited to production signup volume | Medium | Signups fail silently past the limit | Check the limit against expected signup rate before build plan |
| Username stored outside `auth.users` drifts out of sync with the identity row | Low | A user with no visible handle, or a handle pointing at nothing | Same failure class `tech-stack.md` already named for Clerk/Auth0, mitigated by writing both in one transaction |
| Reusing the OTP mechanism for both signup verification and password reset conflates two flows in one code path | Low | A bug in one flow's edge cases (expiry, resend) leaks into the other | Keep them as two call sites over one shared component in the build plan, not one branching function |
| A Google sign-in silently reaches an account whose owner never linked Google themselves | Low | A user is surprised their Google identity now opens an existing Slashit account | Accepted per Q6's answer; surface this plainly the first time it happens, in the build plan |

## Open questions

| # | Question | Blocks | Owner |
|---|---|---|---|
| ~~Q1~~ | What does "the radius app" auth flow actually look like? | Best practices section, Design stage | **Dropped 2026-09-14.** User said no reference is needed; the Best practices section stands on the products already named above. |
| ~~Q2~~ | Is password reset / account recovery in this epic's scope, or a later slice? | PRD scope | **Answered 2026-09-14.** In scope, same feature. |
| ~~Q3~~ | Supabase's default email sending has production rate limits. Is custom SMTP needed for V1 launch, or can it wait? | Build plan | **Answered.** Already resolved in `tech-stack.md`'s stack table: Resend is the locked email vendor, not Supabase's built-in sender. Confirmed while drafting the build plan. |
| ~~Q4~~ | Username rules: case-sensitive, minimum length, reserved words? | PRD requirement wording | **Answered 2026-09-14.** Case-insensitive uniqueness, 3 to 20 characters, letters/numbers/underscore only, no reserved-word list for V1. |
| ~~Q5~~ | What happens to an account that signs up and never completes verification: expire it, or leave it pending indefinitely? | PRD, data model | **Answered 2026-09-14.** Expires 24h after signup; the email is freed for re-signup. |
| ~~Q6~~ | Does a Google sign-in on an email that already has a manually-created account merge with it, or get refused? | PRD scope, build plan | **Answered 2026-09-14.** Merges with it. |
| ~~Q7~~ | Exact rate-limit and lockout thresholds: failed sign-in attempts, wrong-code attempts, signups per email or address, before each locks out or cools down | PRD, build plan | **Answered 2026-09-14.** The drafted numbers stand: 5 attempts / 15-minute lockout on sign-in and codes, 5 signups per hour per email or address. |

## What this is not

- Not social login beyond Google specifically (no GitHub, Apple, etc. sign-in
  in this feature).
- Not multi-factor authentication beyond the email OTP used to verify signup.
- Not teams, invites, or multi-user accounts. Product is one account per user.
- Not profile or settings management beyond the fields signup collects.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-14 | Created | User asked to plan real signup, login and email verification as the next immediate feature | pending |
| 2026-09-14 | Approved | User approved, proceed to PRD | user |
| 2026-09-14 | Q2, Q4, Q5 answered: password reset added to scope in this feature (not deferred); username rules set to case-insensitive, 3-20 chars, letters/numbers/underscore; unverified accounts expire after 24h and free the email. Requirements, risks and exclusions updated to match. | User answered the PRD-blocking questions | user |
| 2026-09-14 | Scope widened during design: Google sign-in added as an addition alongside manual signup (reverses the "What this is not" exclusion and the Alternatives verdict), and rate limiting/lockout on sign-in, code attempts and signup added as a requirement area. Q1 dropped. Q6 (account-linking) and Q7 (exact thresholds) opened. Pros, cons, risks and best practices updated to match. Re-opens `01-prd.md` and `02-design.md`, both amended in the same change | User asked for Google sign-in and for rate-limit error cases to be added, and said the "radius app" reference is no longer needed | user |
| 2026-09-14 | Q6 answered: a Google sign-in merges into a matching manual account. Q7 answered: the drafted 5-attempt/15-minute and 5-per-hour numbers stand. Requirements, cons, alternatives and risks updated to match | User answered both build-plan-blocking questions | user |
| 2026-09-14 | Q3 answered: Resend, not Supabase's built-in sender, was already the locked email vendor in `tech-stack.md`. No custom-SMTP decision was actually needed | Found while reading `tech-stack.md` ahead of the build plan | user |
| 2026-09-15 | Google sign-in's requirement row extended: the avatar Google provides is stored and shown, not discarded. FR-21 added in `01-prd.md` | User asked for it once told Google sign-in was live but not capturing one | user |
| 2026-09-15 | Sign out added as its own requirement row. US-8, FR-22 added in `01-prd.md`. Built ahead of this write-up (`AppShell`'s account popover) since it was a real, unnamed gap, not a new direction | User asked for a sign-out option | user |
