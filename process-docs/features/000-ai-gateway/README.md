# 000 AI Gateway and Usage

| Field | Value |
|---|---|
| Priority | P0, platform |
| Stage | 3 Build plan |
| Status | PRD approved, no design stage |
| Started | 2026-09-09 |
| Owner | user |

## Documents

| Stage | Doc | Status | Approved |
|---|---|---|---|
| 0 Intake | [00-context.md](./00-context.md) | approved | 2026-09-09 |
| 1 PRD | [01-prd.md](./01-prd.md) | approved | 2026-09-09 |
| 2 Design | — | not applicable, no user-facing surface | — |
| 3 Build plan | 03-build-plan.md | not started | |
| 4 Implementation plan | 04-implementation-plan.md | not started | |
| 5 Dev | 05-dev-log.md | not started | |

## One-line summary

One Slashit-held provider credential, many authenticated users, every model call
attributed and limited per user, and the key never leaving the backend.

## Why this is 000

Epic 001 cannot resolve "tomorrow" in `/add-task Finish docs tomorrow` without a
model call, so the gateway is a dependency of the first epic rather than a
follow-on. It is numbered 000 because 001 is already approved and renumbering an
approved epic would break its references.
