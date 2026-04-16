---
name: pr-faq-generator
description: Generates PR-FAQ (Press Release + FAQ) documents for product ideas, features, or projects using the Working Backwards methodology. Use when the user asks for a PR-FAQ, press release and FAQ for a product/feature, working backwards document, or product one-pager in Amazon-style PR-FAQ format.
---

# PR-FAQ Generator

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

Generate **Press Release + FAQ** documents (PR-FAQ) for a project, product idea, or feature. PR-FAQs are a "working backwards" tool: you write as if the product has already launched, which forces customer-focused thinking and surfaces gaps before building.

## When to Use

- User asks for a PR-FAQ, "working backwards" doc, or press release + FAQ for a product/feature.
- User wants to vet or align on a product idea before implementation.
- User mentions Amazon-style product doc or one-pager for stakeholders.

## Output Format

Produce a single document with two main parts:

1. **Press Release** — customer-facing, benefit-led, no internal jargon.
2. **FAQ** — **External** (press/customers) and **Internal** (executives, eng, legal, ops, etc.).

Use the template below. Fill each section from the **customer's point of view** first; internal/technical details belong in the FAQ.

---

## Press Release Template

Use this structure. One sentence per heading/subheading; keep paragraphs to a few sentences each.

| Section | Guidance |
|--------|----------|
| **Heading** | Product name in one sentence the target customer understands. |
| **Subheading** | One sentence: who the customer is and what benefit they get. Be specific about the segment (e.g. "urban professionals 25–40" not "everyone"). |
| **Summary paragraph** | City, outlet, launch date. 3–5 sentences on the product and its benefits. |
| **Problem paragraph** | 3–5 sentences on the problem, from the **customer's** perspective. Focus on the problem with real TAM. |
| **Solution paragraph(s)** | How the product solves that problem. Include: "Today, customers use X, Y, Z; those fall short of [problem]. Our product addresses this by …" Differentiate; avoid feature lists. |
| **Quotes & Getting Started** | One internal quote (spokesperson), one external (hypothetical customer). Then how to get started and where to learn more (link or placeholder). |

**Rules for the PR:** No internal jargon. No "we think" or capability-led pitch. Describe the product as better, faster, or cheaper than current alternatives on at least one dimension.

---

## FAQ Template

### External FAQ (press and customers)

Answer in plain language. Typical questions:

- What is the price? How do I pay?
- How does it work? (high level)
- How do I get help or support?
- Where can I get it / sign up?

Add others that a journalist or first-time user would ask.

### Internal FAQ (executives and stakeholders)

Anticipate questions from product, engineering, finance, legal, ops, support. Include:

**Customer & market**

- Who is the target customer, and what do they use today to solve this problem?
- What problem(s) does this solve for customers?
- How is this product better, cheaper, or faster than alternatives?
- Who are the competitors?
- How large is the TAM? How many people have this problem and would pay to fix it?

**Product & execution**

- What happens when [edge case X]? How does the product handle it?
- What are the hard problems (technical, legal, UX, ops) we must solve?
- What new capabilities or partners do we need?
- What third-party tech or legal/regulatory issues exist?

**Business**

- What are per-unit economics (e.g. gross margin, contribution)?
- What's the upfront investment (people, tech, inventory, etc.)?
- How do we manage risk of that investment?
- How long until profitability under stated assumptions?
- What must be true for this to succeed? Top 3 reasons it might fail?

Answer with data and options where possible. Be optimistic but realistic; show you've considered failure modes.

---

## Workflow

1. **Gather context** — Product/feature name, target customer, problem, and high-level solution. If the user only gave a vague idea, ask for: customer segment, main problem, and how this is differentiated.
2. **Draft the PR first** — Write the press release using the template. No internal or technical details in the PR.
3. **Draft External FAQ** — Questions a reporter or customer would ask; keep language simple.
4. **Draft Internal FAQ** — Questions leadership and cross-functional stakeholders will ask; cover market, execution, and business.
5. **Differentiation check** — Ensure the solution paragraph explicitly states what customers use today and how this is meaningfully better/faster/cheaper. If it's not, note that the PR should be revised.

---

## Guidelines

- **Customer backwards, not skills forward** — Start from customer need and desired outcome; don't lead with "what we can build today."
- **One segment** — If the customer is "everyone," narrow to a specific segment for the PR.
- **Truth-seeking** — Internal FAQ should surface risks and "what must be true" rather than only selling the idea.
- **Competition** — Always name current solutions and state why customers would switch.

For common mistakes, review process, and reviewer checklist, see [reference.md](reference.md).
