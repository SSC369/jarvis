# Decision Records

Decisions that bind more than one feature. A build plan that locks an
architecture decision affecting the wider product graduates it here.

Files are `NNNN-<slug>.md`, four digits, in decision order. Use
`../../templates/decision-record.template.md`.

A superseded decision is never deleted. Set its status to `superseded` and point
the new record at it.

| # | Decision | Status | Date |
|---|---|---|---|
| [0001](./0001-model-provider-gemini-free-tier.md) | Google Gemini free tier as the V1 model provider | superseded by 0006 | 2026-09-08 |
| [0002](./0002-v1-technology-stack.md) | V1 technology stack | superseded by 0004 | 2026-09-08 |
| [0003](./0003-product-name-and-mark.md) | Product name and mark | proposed | 2026-09-09 |
| [0004](./0004-v1-technology-stack-revised.md) | V1 technology stack, revised | accepted | 2026-09-09 |
| [0005](./0005-auth-supabase-and-data-isolation.md) | Supabase Auth as the identity provider, with Row Level Security | accepted | 2026-09-09 |
| [0006](./0006-model-provider-gemini-paid-tier.md) | Google Gemini paid tier as the V1 model provider | accepted | 2026-09-09 |

The current stack is [0004](./0004-v1-technology-stack-revised.md),
[0005](./0005-auth-supabase-and-data-isolation.md) and
[0006](./0006-model-provider-gemini-paid-tier.md). Read those three, not 0001
and 0002.
