---
name: solopreneur-business-plan
description: Generates detailed solopreneur business plans for business ideas. Use when the user asks for a business plan, solopreneur plan, one-person business plan, or to evaluate or plan a startup idea. Emphasizes iterative refinement by asking clarifying questions instead of assuming; calls out risks, headwinds, and unrealistic elements rather than making plans appear successful.
---

# Solopreneur Business Plan Generator

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

Generate **detailed, honest** business plans for solopreneur (one-person) business ideas. Plans go beyond high-level market/opportunity/revenue to include operations, unit economics, risks, and viability. The skill is **iterative** and **truth-seeking**: ask clarifying questions when information is missing, and explicitly call out when a plan is unrealistic, too risky, or faces significant headwinds.

## When to Use

- User asks for a business plan, solopreneur plan, or one-person startup plan.
- User wants to evaluate or flesh out a business idea in depth.
- User mentions planning a side business, freelance positioning, or solo venture.

## Core Principles

1. **Ask before assuming** — When key facts are missing (customer, pricing, capacity, experience), ask the user. Do not invent plausible-sounding assumptions to make the plan look complete or attractive.
2. **Iterate with feedback** — Treat the first draft as a starting point. Flag gaps with "[Need your input: …]" or "To strengthen this, please share: …". Invite the user to correct or add information and revise.
3. **Call out problems** — If the idea has material headwinds, is unrealistic, too risky, or doesn't add up, say so in a dedicated **Reality check** section. Do not downplay risks to make the plan look good.

---

## Workflow

### 1. Discovery (before writing a full plan)

Gather enough context to avoid blind assumptions. Ask clarifying questions such as:

- **Idea**: What exactly are you selling (product/service), and in one sentence, to whom?
- **You**: What's your relevant experience, skills, and time/capital constraints?
- **Customer**: Who specifically is the customer (segment, geography, current behavior)? How do you know they have this problem or want this?
- **Evidence**: Any validation so far (conversations, pre-orders, past work, competitors you've studied)?
- **Constraints**: Timeline, budget, other commitments (e.g. full-time job, family)?

If the user only gives a vague idea, ask 3–5 of these before drafting. It's better to produce a shorter, grounded plan than a long, assumption-heavy one.

### 2. First draft

Use the **Plan structure** below. For any section where you had to assume:

- State the assumption clearly (e.g. "Assumption: …").
- Add a line like: **"[Need your input: …]"** so the user can correct or fill in.

Do not invent numbers (prices, TAM, conversion rates) to make the plan look profitable. Use placeholders (e.g. "[Your monthly capacity]" or "[CAC from your channels]") and explain what the user should replace them with.

### 3. Reality check (required)

Every plan must include a **Reality check / Viability** section that:

- Lists **headwinds** (market, competition, regulation, execution).
- States **why this might fail** or why demand might be weaker than assumed.
- Flags **optimistic assumptions** (e.g. "This plan assumes CAC stays under $X; if it's higher, unit economics break.").
- Notes **what must be true** for the plan to work (e.g. "You need at least 10 paying customers by month 6 to cover baseline costs.").

If the idea is **unrealistic, too risky, or doesn't make sense** given what the user shared, say so clearly and suggest what would need to change or what to validate first.

### 4. Iteration

After sharing the draft:

- Invite the user to supply missing inputs and to correct assumptions.
- Offer to revise specific sections (e.g. "If you share your actual CAC, I can update the financials and break-even.").
- Re-run the reality check when numbers or strategy change.

---

## Plan Structure

Use this outline. Depth matters: each section should be substantive, not one-line placeholders.

| Section | What to cover |
|--------|----------------|
| **1. Executive summary** | One paragraph: idea, target customer, business model, and 2–3 key milestones or success metrics. |
| **2. Problem & opportunity** | Who has the problem, what they do today, and why it's painful or costly. Evidence or signals (not just "people want X"). |
| **3. Solution & value proposition** | What you offer, how it solves the problem, and how it's different from alternatives (better/faster/cheaper or clear positioning). |
| **4. Target customer** | Specific segment (not "everyone"): who they are, where they are, how you reach them, and how you'll validate demand. |
| **5. Market & competition** | TAM/SAM/SOM with a clear basis (e.g. "X people in Y region who do Z"). Who else serves this need; how you're differentiated; why customers would switch or choose you. |
| **6. Business model & pricing** | How you make money (one-time, subscription, project, etc.). Pricing level and rationale. Unit economics: revenue per customer, direct costs, contribution margin. |
| **7. Go-to-market & acquisition** | How you'll get customers (channels, content, referrals, ads). Rough CAC if known; otherwise "[Your CAC]" and what drives it. Capacity limit as a solopreneur (how many clients/projects/month). |
| **8. Operations & delivery** | What you actually do to deliver (time, tools, partners). Where bottlenecks or scaling limits are. |
| **9. Financials** | Revenue model (e.g. 5 clients × $X/month). Fixed vs variable costs. Break-even (units or months). Runway or capital needs if relevant. State assumptions explicitly. |
| **10. Milestones & roadmap** | 3–6 concrete milestones (e.g. "10 discovery calls," "first paying customer," "repeatable offer"). Rough timeline. |
| **11. Assumptions & what must be true** | Bullet list of assumptions (pricing, conversion, capacity, retention). What has to hold for the plan to work. |
| **12. Reality check / Viability** | Headwinds, risks, why it might fail, optimistic assumptions, and an honest take: is this realistic for a solopreneur with the stated constraints? |

---

## Rules

- **Never assume** revenue, conversion, or demand to make the plan look successful. Ask or use placeholders and label assumptions.
- **Always include** the Reality check section. If the idea is weak or risky, say so and suggest validation steps or pivots.
- **Prefer short, honest plans** over long, assumption-heavy plans. Better to deliver a 2-page plan with clear gaps and a strong reality check than 10 pages of invented numbers.
- **Use the user's words and context** for customer, problem, and constraints. Don't replace their description with generic startup language.
- **Iterate explicitly**: after the first draft, ask "What would you like to refine or add?" and "Do you have numbers for [placeholders] so we can tighten the financials?"

For example clarifying questions and a reality-check checklist, see [reference.md](reference.md).
