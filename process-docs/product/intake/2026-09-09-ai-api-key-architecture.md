---
doc: context
scope: product
title: AI API Key Architecture (as supplied)
stage: 0
status: approved
owner: user
created: 2026-09-09
updated: 2026-09-09
approved_on: 2026-09-09
supersedes: null
---

# Intake — AI API Key Architecture

Supplied by the user on 2026-09-09. Transcribed as given. Source document for
[epic 000, the AI Gateway](../../features/000-ai-gateway/).

---

## As supplied

### Overview

Jarvis V1 uses Jarvis-managed AI API keys.

Users never provide or receive AI provider API keys. All AI requests go through
the Jarvis backend, which securely uses Jarvis's own provider credentials.

```
User → Chat request → Jarvis App → Authenticated request → Jarvis Backend
  ├── Identify User
  ├── Check Usage / Limits
  ▼
AI Gateway → Jarvis-managed API Key → AI Provider → AI Response
  → Jarvis Backend → Jarvis App
```

### 1. User Authentication

Every user has a unique `user_id`. The app authenticates the user and sends
their authentication token with each request.

```
POST /api/chat
Authorization: Bearer <user-token>
```

The client does not send an OpenAI/Anthropic API key.

### 2. AI API Key

Jarvis owns the AI provider credentials. For V1, one Jarvis account holds one
provider API key, stored securely on the backend or server environment.

```
OPENAI_API_KEY=********
```

The API key must never be:

- Stored in the mobile/web app
- Sent to the client
- Returned in API responses
- Stored in normal application logs
- Exposed to users

### 3. AI Request Flow

When a user sends a message:

```
User "Add ₹500 dinner expense" → Jarvis App → POST /api/chat → Jarvis Backend
  ├── Authenticate user
  ├── Get user_id
  ├── Check usage/limits
  ▼
AI Gateway
  ├── Select provider
  ├── Select model
  └── Load Jarvis API credential
  ▼
AI Provider → AI Response → AI Gateway → Jarvis Backend → Jarvis App
```

### 4. User Does Not Own an API Key

```
User → user_id → Plan, Usage, Limits
Jarvis → AI Provider Credentials
```

There is no API key stored per user.

```
User A ─┐
User B ─┼──> Jarvis AI Gateway ──> Jarvis API Key ──> OpenAI
User C ─┘
```

All users share the same Jarvis-managed provider credential.

### 5. Usage Tracking

Although the API key is shared, usage is tracked separately for every user.

```
User → Usage Service
  ├── Requests
  ├── Input tokens
  ├── Output tokens
  ├── Total tokens
  └── Estimated cost
```

Example:

```
user_id: 123
requests: 42
input_tokens: 18,200
output_tokens: 7,800
estimated_cost: $0.XX
```

This allows Jarvis to implement limits later:

```
Free User → Monthly AI limit
Pro User  → Higher AI limit
```

### 6. V1 Components

```
Jarvis App → Authentication → Jarvis Backend
  ├── User Service
  ├── Usage Service
  └── AI Gateway → AI Provider
```

**AI Gateway responsibilities:** calling AI providers, managing provider
credentials, selecting the model, handling AI requests, handling streaming
responses, basic error handling, tracking token usage, tracking estimated AI
cost.

### 7. V1 Database Concept

```
users                    ai_usage
----------------         ----------------
id                       id
email                    user_id
plan                     provider
created_at               model
                         input_tokens
                         output_tokens
                         total_tokens
                         estimated_cost
                         created_at
```

The API key is not stored in these tables.

### 8. Security Boundary

```
        TRUSTED
   ┌───────────────┐
   │ Jarvis Backend│
   │ API Key       │
   │ AI Gateway    │
   └───────┬───────┘
           ▼
      AI Provider

       UNTRUSTED
   ┌───────────────┐
   │ Jarvis App    │
   │ NO API KEY    │
   └───────────────┘
```

The frontend only knows about Jarvis APIs, never the underlying AI provider
credentials.

### V1 Architecture Principle

> One Jarvis-managed AI credential, many authenticated users, with usage tracked
> independently per user.

This is the simplest architecture for Jarvis V1 and leaves room to add multiple
providers, API-key pools, BYOK, model routing, and advanced cost optimization
later.

---

## Reconciliation with decisions already made

Recorded so the differences are visible rather than resolved silently.

| Point in the source | What is already settled | Reading |
|---|---|---|
| `OPENAI_API_KEY`, "OpenAI/Anthropic" | [Decision 0001](../decisions/0001-model-provider-gemini-free-tier.md) sets Google Gemini free tier | The examples are illustrative. The gateway is provider-agnostic by design and V1 configures Gemini |
| "Chat request", "user sends a message" | V1 capture is commands-only | The gateway serves field extraction inside a command, not open chat. The shape of the flow is unchanged |
| `estimated_cost` tracking | The free tier is not billed | Cost is an estimate against zero spend. The number that matters in V1 is requests against the shared quota |
| `plan` on `users`, free and pro limits | Not charging in V1 | The column exists with one value. Tiering is post-V1 |
| "Handling streaming responses" | Extraction returns a structured record, not prose | Streaming may not be needed in V1. Open as a question |

## What this document does not settle

| # | Gap |
|---|---|
| G1 | What the per-user request limit actually is |
| G2 | Whether `ai_usage` rows are retained forever, and what they may contain |
| G3 | Whether streaming is needed in V1 at all |
| G4 | How estimated cost is computed for a tier that bills nothing |
