---
name: decision-extractor
description: Extract decisions and their rationale from meetings, documents, and discussions - maps what was decided, why, by whom, and what alternatives were considered
---

# Decision extractor

Turn discussions into documented decisions.

## Overview

Every meeting, document, and conversation contains decisions. "We're going with React." "Let's postpone the launch." "The team decided against microservices."

Most decisions are forgotten or lost in chat history. This skill extracts them, documents the reasoning, and tracks who decided what.

You're a decision logger, not a discussion summarizer. Find what was actually decided, capture the reasoning, identify alternatives that were rejected. Make choices explicit and traceable.

## When to Use

Use after any communication with decisions:

- Architecture discussions or design reviews
- Strategy meetings or planning sessions
- Product roadmap prioritization
- Technical approach debates
- Policy or process changes
- Vendor or tool selection
- Project scope or timeline decisions
- Go/no-go launch decisions

Don't use for:

- Pure brainstorming (no decisions made yet)
- Information sharing without choices
- Questions without answers
- Discussions still in progress

## The Process

**First, scan for decision language:**
Look for decision markers:

- "Decided to", "decided on", "chose", "selected"
- "Going with", "we'll use", "approved", "rejected"
- "Won't do", "won't use", "ruled out"
- "Agreed to", "consensus on", "final call"
- Past tense: "went with", "picked", "settled on"

**Then, extract the components:**
For each decision, identify:

1. **What** - The specific decision or choice made
2. **Who** - Decision maker(s) or deciding body
3. **When** - When the decision was made
4. **Why** - Rationale, reasoning, or constraints
5. **Alternatives** - Options considered but rejected
6. **Impact** - What this affects or changes

**Categorize by type:**

- **Technical:** Architecture, tools, frameworks, infrastructure
- **Product:** Features, scope, priorities, timeline
- **Strategic:** Direction, goals, market positioning
- **Operational:** Process, policy, team structure
- **Financial:** Budget, pricing, resource allocation

**Track status:**

- **FINAL:** Confirmed, implemented, or locked in
- **PROVISIONAL:** Decided but subject to validation
- **PENDING:** Needs approval or further input
- **REVERSED:** Previously decided, now changed
- **OPEN:** Discussed but not yet decided

**Finally, structure the output:**

- List all decisions clearly
- Group by type or impact
- Show reasoning explicitly
- Note alternatives considered
- Flag decisions that reverse previous ones

## Decision Indicators

**Explicit Decisions:**

- "We decided to use PostgreSQL"
- "The team chose option A over option B"
- "Leadership approved the budget increase"
- "We're not doing microservices"

**Implicit Decisions:**

- "Let's go with the simpler approach" → Decided: simpler approach
- "We'll stick with the current design" → Decided: keep current design
- "That's not a priority right now" → Decided: defer or reject

**Negative Decisions (What was rejected):**

- "We ruled out MongoDB" → Decided against MongoDB
- "Not doing real-time features" → Decided: no real-time
- "Too expensive for now" → Decided: reject due to cost

**Conditional Decisions:**

- "If performance is an issue, we'll add caching" → Conditional
- "We'll revisit after Q1 results" → Deferred decision

## Output Format

Keep it clear. Show what was decided, why, and by whom.

```
📋 DECISION LOG
━━━━━━━━━━━━━━━━━━━━

Source: [Meeting/Doc Title]
Date: [When decisions were made]
Total Decisions: 6 (4 final, 1 provisional, 1 open)

━━━━━━━━━━━━━━━━━━━━
✅ FINAL DECISIONS
━━━━━━━━━━━━━━━━━━━━

#1 - Use PostgreSQL for primary database
Type: Technical (Infrastructure)
Decided by: Engineering team + CTO
When: Feb 1, 2026
Why: Need strong ACID guarantees, team has PostgreSQL expertise, scales
     to our projected load, better JSON support than MySQL
Alternatives Considered:
  • MySQL - Rejected: weaker JSON support
  • MongoDB - Rejected: eventual consistency too risky for financial data
Impact: All new services use PostgreSQL, migration from MySQL planned for Q2
Status: ✅ FINAL

#2 - Postpone mobile app launch to Q3
Type: Product (Timeline)
Decided by: Product leadership
When: Feb 1, 2026
Why: Web app needs stability first, mobile team understaffed,
     market research shows web priority higher
Alternatives Considered:
  • Q2 launch - Rejected: too rushed, quality would suffer
  • Hire contractors - Rejected: budget constraints
Impact: Shifts mobile engineering resources to web app quality
Status: ✅ FINAL

#3 - No microservices architecture for now
Type: Technical (Architecture)
Decided by: Architecture review board
When: Jan 30, 2026
Why: Team too small to manage distributed systems, current monolith scales
     fine, premature optimization, adds operational complexity
Alternatives Considered:
  • Full microservices - Rejected: over-engineering for current scale
  • Modular monolith - Adopted instead
Impact: Continue with modular monolith, revisit at 10M+ users
Status: ✅ FINAL

#4 - Approve additional $50K for Q1 marketing
Type: Financial (Budget)
Decided by: CFO + CEO
When: Jan 29, 2026
Why: Strong Q4 performance, customer acquisition cost trending down,
     competitor launched similar product, need market presence
Alternatives Considered:
  • Wait until Q2 - Rejected: would lose momentum
  • Reduce to $25K - Rejected: insufficient impact
Impact: Marketing team can proceed with paid campaigns
Status: ✅ FINAL

━━━━━━━━━━━━━━━━━━━━
⏳ PROVISIONAL
━━━━━━━━━━━━━━━━━━━━

#5 - Adopt TypeScript for new frontend code
Type: Technical (Language)
Decided by: Frontend team
When: Feb 1, 2026
Why: Type safety reduces bugs, better tooling, team wants to learn it
Alternatives Considered:
  • Keep JavaScript - Rejected: too many runtime errors
  • Flow - Rejected: community smaller than TypeScript
Impact: New components in TypeScript, gradual migration planned
Status: ⏳ PROVISIONAL (pending CTO approval)
Note: ⚠️ Needs final approval before implementation

━━━━━━━━━━━━━━━━━━━━
❓ OPEN DECISIONS
━━━━━━━━━━━━━━━━━━━━

#6 - Pricing model for enterprise tier
Type: Product (Pricing)
Discussed by: Product + Sales + Finance
When: Feb 1, 2026
Options on Table:
  • Per-user pricing (Sales preference)
  • Flat rate + overage (Finance preference)
  • Usage-based (Product preference)
Why Not Decided: Need more customer interviews, pricing research incomplete
Next Steps: Product to run pricing survey by Feb 15
Status: ❓ OPEN
Note: ⚠️ Blocks enterprise launch timeline

━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY BY TYPE
━━━━━━━━━━━━━━━━━━━━

Technical: 3 decisions (PostgreSQL, No microservices, TypeScript)
Product: 1 decision (Postpone mobile launch)
Financial: 1 decision (Marketing budget)
Operational: 0 decisions

━━━━━━━━━━━━━━━━━━━━
👥 SUMMARY BY DECIDER
━━━━━━━━━━━━━━━━━━━━

Engineering team: 1 final, 1 provisional
Product leadership: 1 final
Architecture board: 1 final
CFO + CEO: 1 final

━━━━━━━━━━━━━━━━━━━━
⚠️  DECISION DEPENDENCIES
━━━━━━━━━━━━━━━━━━━━

• Decision #5 (TypeScript): Blocks new component development
• Decision #6 (Pricing): Blocks enterprise launch
• Decision #2 (Mobile delay): Frees resources for web app quality

━━━━━━━━━━━━━━━━━━━━
🔄 REVERSALS & CHANGES
━━━━━━━━━━━━━━━━━━━━

None in this session.
```

## Extraction Examples

**From Architecture Discussion:**

```
Input: "After discussing various options, we decided to go with PostgreSQL
instead of MongoDB. The team felt ACID guarantees were more important than
horizontal scaling for our use case."

Output:
Decision: Use PostgreSQL for primary database
Who: Team consensus
Why: ACID guarantees more important than horizontal scaling
Alternative: MongoDB (rejected due to eventual consistency)
Type: Technical
Status: FINAL
```

**From Product Meeting:**

```
Input: "We're not building the mobile app this quarter. It's just not a
priority given our resources. Web needs to be solid first."

Output:
Decision: Defer mobile app to future quarter
Who: Product team (implied)
Why: Resource constraints, web app takes priority
Alternative: Build mobile now (rejected - insufficient resources)
Type: Product
Status: FINAL
```

**From Strategy Session:**

```
Input: "The team discussed switching to usage-based pricing but decided to
table that decision until we have more data from customer interviews."

Output:
Decision: Defer pricing model decision
Who: Team
Why: Insufficient data, need customer interviews first
Alternative: Usage-based pricing (under consideration)
Type: Product/Financial
Status: OPEN (pending customer research)
```

**From Email Thread:**

```
Input: "Based on everyone's feedback, I'm making the call to use React over
Vue. Most of the team knows React, and it has better enterprise support."

Output:
Decision: Use React for frontend framework
Who: Sender (executive decision)
Why: Team expertise + enterprise support
Alternative: Vue (rejected - less team familiarity)
Type: Technical
Status: FINAL
```

## Common Patterns

**Implicit Approval:**
"No objections to the proposal" → Decision: Approved
"Sounds good to everyone" → Decision: Consensus reached
Track these even if informal.

**Deferred Decisions:**
"Let's revisit next quarter" → Decision: Deferred
"We'll decide after the pilot" → Decision: Pending validation
Mark as PENDING with trigger condition.

**Reversed Decisions:**
"Actually, let's go back to the old approach" → Reversal
"We're switching from X to Y" → Decision changed
Flag reversals explicitly and link to original.

**Delegated Decisions:**
"Sarah will make the final call" → Decision maker identified
"Let's let the team decide" → Delegation documented

**Non-Decisions:**
"We should probably do X" → Not decided yet
"I think we might go with Y" → Speculation, not decision
Don't log these as decisions.

## Decision Strength

**FINAL (Locked in):**

- Explicit approval or consensus
- Executive decision made
- Already implemented or in progress
- No reversibility mentioned

**PROVISIONAL (Subject to validation):**

- "Let's try X and see how it goes"
- "Pending approval from Y"
- "We'll do X unless problems arise"
- Pilot or experiment phase

**PENDING (Not yet finalized):**

- "We're leaning towards X"
- "Probably going with Y but need to confirm"
- Awaiting additional input or data

**REVERSED (Previously decided, now changed):**

- Explicit change from previous decision
- "We're no longer doing X"
- "Switching from Y to Z"

**OPEN (Discussed but not decided):**

- Options presented but no choice made
- "We need to decide between X and Y"
- Still gathering information

## Do's and Don'ts

**DO:**

- Extract every decision, even small ones
- Document the "why" explicitly
- Capture alternatives that were considered
- Note who made the decision (even if team consensus)
- Flag decisions that need approval
- Track reversals of previous decisions
- Mark deferred decisions with trigger conditions
- Link related decisions

**DON'T:**

- Confuse discussion with decision
- Skip negative decisions (what was rejected)
- Ignore implicit decisions ("let's go with X")
- Miss conditional decisions ("if X, then Y")
- Forget to note alternatives considered
- Skip the reasoning (why matters!)
- Treat speculation as decision
- Miss delegated decision-making authority

## Watch Out For

**Hidden decisions:**
"We'll stick with the current approach" → Decision to not change
"That's out of scope" → Decision to exclude
These are decisions too.

**Decision vs. Discussion:**
"We talked about using Redis" → Discussion, not decision
"We're using Redis" → Decision
Only log actual decisions.

**Who really decided:**
"The team discussed and agreed" → Team decision
"I'm making the call" → Individual decision
"Approved by leadership" → Leadership decision
Track the actual decider, not just who spoke.

**Missing reasoning:**
"We chose option A" → Why?
Always look for the "because" or infer from context.

**Conflicting decisions:**
Decision A says "use SQL", Decision B says "use NoSQL"
Flag conflicts and note if one reverses the other.

## Integration Workflows

**After architecture reviews:**

1. Extract all technical decisions
2. Document in Architecture Decision Records (ADR)
3. Link to related decisions
4. Track reversals over time
5. Share with engineering team

**During product planning:**

1. Extract product decisions from roadmap sessions
2. Map to features and priorities
3. Track scope changes
4. Document trade-offs made
5. Communicate to stakeholders

**For strategic planning:**

1. Extract strategic decisions from leadership meetings
2. Document rationale and alternatives
3. Track against company goals
4. Monitor for pivots or reversals
5. Maintain decision history

**In daily operations:**

1. Log operational decisions from standups
2. Track process changes
3. Document policy decisions
4. Note temporary vs. permanent choices
5. Build institutional knowledge

## Key Principles

- **Every decision has three parts:** What, Who, Why (flag if missing)
- **Alternatives matter:** Show the road not taken
- **Reversals happen:** Track them explicitly, don't hide them
- **Reasoning is critical:** "Why" is more important than "what"
- **Implicit counts:** "Let's go with X" is a decision even without "decided"
- **Context matters:** Same decision means different things in different contexts
- **Non-decisions are valid:** Deferring is a decision too
- **Track the decider:** Who has authority matters

## Your Checklist

For every decision you extract:

- [ ] What was decided (specific, clear)
- [ ] Who decided (person, team, or body)
- [ ] When it was decided (date or timeframe)
- [ ] Why it was decided (rationale, constraints)
- [ ] What alternatives were considered (and why rejected)
- [ ] What this impacts (consequences, scope)
- [ ] Status (final, provisional, pending, open, reversed)
- [ ] Dependencies (what this blocks or enables)

## Works Well With

Combine with these other skills:

- **/action-item-extractor** - Decisions often lead to action items
- **/commitment-extractor** - Decisions can include commitments
- Architecture Decision Records (ADR) - Export to ADR format
- Version control - Track decision evolution over time

## Remember

Decisions are the turning points in projects. "We chose React." "We're not doing microservices." "Launch is postponed."

Your job is to find every decision, document why it was made, capture the alternatives that were rejected, and make the reasoning traceable. Don't let choices disappear into chat history or forgotten meeting notes.

The difference between a well-documented project and institutional amnesia is often just writing down what was decided and why.
