---
name: commitment-extractor
description: Extract and track commitments, promises, and deadlines from emails, meetings, and contracts - identifies who committed to what by when
---

# Commitment extractor

Turn vague promises into trackable commitments.

## Overview

Every meeting, email, and contract is full of commitments. "I'll send that by Friday." "We guarantee 99.9% uptime." "The team will deliver next quarter."

Most of these get lost. This skill extracts them, categorizes them, and makes them trackable.

You're an accountability engine, not a stenographer. Find what people actually committed to, flag the timelines, identify who's responsible. Make promises concrete.

## When to Use

Use after any communication with commitments:

- Meeting notes or transcripts
- Email threads with deliverables
- Contract negotiations or agreements
- Project kickoffs or status updates
- Customer promises or SLAs
- Internal team commitments

Don't use for:

- Pure information sharing (no commitments made)
- Historical analysis without action needed
- Content where commitments aren't relevant

## The Process

**First, scan for commitment language:**
Look for promise markers:

- "Will", "shall", "must", "commit to"
- "By [date]", "within [timeframe]", "before [deadline]"
- "Responsible for", "owns", "delivers", "ensures"
- "Guarantee", "promise", "pledge", "agree to"

**Then, extract the components:**
For each commitment, identify:

1. **Who** - The committer (person, team, company)
2. **What** - The deliverable or action
3. **When** - Deadline or timeframe (if specified)
4. **Strength** - Hard vs. soft commitment
5. **Conditions** - Any "if/then" dependencies

**Categorize by strength:**

- **Hard Commitment:** Definite promise with accountability ("We will deliver by Friday")
- **Soft Commitment:** Intent without firm guarantee ("We'll try to finish this week")
- **Conditional:** Depends on external factors ("If approved, we'll start Monday")
- **Aspirational:** Goal without commitment ("We hope to launch in Q2")

**Finally, structure the output:**

- List all commitments clearly
- Group by committer or by timeline
- Flag missing components (no deadline, no owner)
- Highlight conflicts or dependencies

## Commitment Strength Indicators

**Hard Commitments (Definite promises):**

- "Will deliver", "guarantee", "commit to", "shall"
- Specific dates: "by Friday", "on March 15"
- Legal language: "agrees to", "is obligated to"
- SLA language: "ensures", "maintains", "provides"

**Soft Commitments (Best effort):**

- "Will try to", "aim to", "plan to", "hope to"
- Vague timelines: "soon", "shortly", "in the near future"
- Qualified: "if possible", "assuming no blockers"
- "Should", "would like to", "intend to"

**Conditional Commitments:**

- "If X, then we will Y"
- "Once approved, we'll..."
- "Pending review, we commit to..."
- "Assuming budget, we guarantee..."

**Aspirational (Not real commitments):**

- "We hope", "we'd love to", "ideally"
- "Our goal is", "we're working towards"
- No specific action or timeline

## Output Format

Keep it scannable. Show who committed to what, when, and how firm it is.

```
📋 COMMITMENT extractor
━━━━━━━━━━━━━━━━━━━━

Source: [Meeting/Email/Contract Title]
Date: [When these commitments were made]
Total Commitments: 7 (5 hard, 2 soft)

━━━━━━━━━━━━━━━━━━━━
💪 HARD COMMITMENTS
━━━━━━━━━━━━━━━━━━━━

#1 - Engineering Team
What: Deploy authentication feature to production
When: Friday, Feb 2, 2026 by 5pm
Who: Sarah (Engineering Lead)
Strength: HARD ("will deploy")
Dependencies: None

#2 - Legal Team
What: Complete contract review
When: Within 3 business days
Who: Legal department
Strength: HARD ("commits to")
Dependencies: Requires final draft from sales

#3 - Product Team
What: Provide API documentation
When: Before March 1, 2026
Who: Alex (Product Manager)
Strength: HARD ("will provide")
Dependencies: None

━━━━━━━━━━━━━━━━━━━━
⚡ SOFT COMMITMENTS
━━━━━━━━━━━━━━━━━━━━

#4 - Marketing Team
What: Create launch materials
When: "Soon" (no specific date)
Who: Marketing
Strength: SOFT ("will try to have ready")
Note: ⚠️ No deadline specified

#5 - Design Team
What: Update mockups based on feedback
When: "This week if possible"
Who: Jordan (Designer)
Strength: SOFT ("aim to")
Note: ⚠️ Conditional on availability

━━━━━━━━━━━━━━━━━━━━
🔄 CONDITIONAL
━━━━━━━━━━━━━━━━━━━━

#6 - Finance
What: Approve additional budget
When: Next board meeting (Feb 15)
Who: CFO
Strength: CONDITIONAL ("if approved by board")
Condition: Board approval required

━━━━━━━━━━━━━━━━━━━━
⚠️  ISSUES & GAPS
━━━━━━━━━━━━━━━━━━━━

• Commitment #4: No specific deadline (blocks testing)
• Commitment #2: Dependent on sales (not yet delivered)
• Missing: No commitment from Sales on final draft timeline

━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY BY OWNER
━━━━━━━━━━━━━━━━━━━━

Engineering (Sarah): 1 hard commitment, due Feb 2
Legal: 1 hard commitment, due Feb 5 (blocked)
Product (Alex): 1 hard commitment, due Mar 1
Marketing: 1 soft commitment, no deadline
Design (Jordan): 1 soft commitment, conditional
Finance (CFO): 1 conditional, pending board

━━━━━━━━━━━━━━━━━━━━
⏰ TIMELINE VIEW
━━━━━━━━━━━━━━━━━━━━

This Week:
  Feb 2: Engineering - Deploy auth feature [HARD]

Next Week:
  Feb 5: Legal - Contract review [HARD, BLOCKED]

This Month:
  Feb 15: Finance - Budget approval [CONDITIONAL]
  Mar 1: Product - API docs [HARD]

No Deadline:
  Marketing - Launch materials [SOFT]
  Design - Mockup updates [SOFT]
```

## Extraction Examples

**From Meeting Notes:**

```
Input: "Sarah mentioned the auth feature will be deployed by Friday.
Legal said they'll try to review the contract this week if they have time."

Output:
#1 - HARD: Sarah commits to deploying auth feature by Friday
#2 - SOFT: Legal will try to review contract this week (conditional on time)
```

**From Email:**

```
Input: "We commit to 99.9% uptime as outlined in the SLA. Our team
will provide 24/7 support. We hope to improve response times soon."

Output:
#1 - HARD: Commit to 99.9% uptime (SLA term)
#2 - HARD: Will provide 24/7 support
#3 - ASPIRATIONAL: Hope to improve response times (not a commitment)
```

**From Contract:**

```
Input: "Vendor shall deliver all materials by March 31, 2026.
If Client approves the scope change, Vendor will complete phase 2 by May 15."

Output:
#1 - HARD: Vendor delivers materials by March 31, 2026
#2 - CONDITIONAL: Vendor completes phase 2 by May 15 (if scope approved)
```

## Common Patterns

**Implicit Commitments:**
Sometimes commitments are implied, not explicit.
"We're launching next quarter" = Soft commitment to launch in Q2
"I own the API work" = Soft commitment to deliver API work
Flag these but mark as IMPLICIT.

**Delegated Commitments:**
"I'll have my team send that over" = Speaker commits on behalf of team
Track both: Who made the commitment + who will execute

**Recurring Commitments:**
"We'll send weekly reports" = Ongoing commitment
Mark as RECURRING and specify frequency

**Broken Commitments:**
If analyzing follow-up communications:
"Sorry, we couldn't finish the contract review" = Broken commitment
Cross-reference with original commitment and flag as BROKEN

## Do's and Don'ts

**DO:**

- Extract every commitment, even small ones
- Identify who's responsible (even if implicit)
- Flag missing deadlines or owners
- Categorize by strength (hard/soft/conditional)
- Group by timeline for easy tracking
- Note dependencies that could block commitments
- Mark aspirational statements as NOT commitments

**DON'T:**

- Treat aspirations as commitments ("we hope" ≠ commitment)
- Miss conditional dependencies ("if X" matters)
- Ignore soft commitments (they're still promises)
- Forget to extract the deadline even if vague
- Skip implicit commitments (own = commit)
- Miss delegated commitments (I'll have team do X)
- Confuse discussion with commitment ("maybe we could" ≠ commitment)

## Watch Out For

**Vague timelines:**
"Soon", "shortly", "in the near future" → Flag as NO SPECIFIC DEADLINE

**Ambiguous owners:**
"The team will handle it" → WHO on the team?
"We'll take care of that" → WHO is "we"?

**Hidden conditions:**
"We'll deliver assuming no blockers" → CONDITIONAL
"Standard timeline unless issues arise" → CONDITIONAL

**Past commitments:**
"We were supposed to finish last week" → BROKEN COMMITMENT
Track these separately for accountability

**Competing commitments:**
Person A: "I'll review by Monday"
Person B: "We need the review by Friday"
→ FLAG CONFLICT

## Integration Workflows

**After meetings:**

1. Run commitment extractor on notes/transcript
2. Generate action items from hard commitments
3. Send summary to participants
4. Track in project management tool

**Contract review:**

1. Extract all commitments from both parties
2. Flag mutual obligations
3. Identify missing deadlines or unclear owners
4. Cross-check with legal requirements

**Email follow-up:**

1. Extract commitments from email thread
2. Compare with previous commitments
3. Flag broken or delayed commitments
4. Generate follow-up template

**Project tracking:**

1. Extract commitments from project docs
2. Map to timeline and dependencies
3. Track status over time
4. Flag at-risk commitments

## Key Principles

- **Every commitment has three parts:** Who, What, When (if missing, flag it)
- **Strength matters:** Hard commitments need tracking, soft ones need clarification
- **Dependencies block execution:** Always note "if/then" conditions
- **Implicit counts:** "I own X" is a commitment even without "I will"
- **Aspirations aren't commitments:** "Hope to" and "would like to" don't count
- **Context matters:** Same words mean different things (contract vs. casual email)
- **Track the extractor:** Re-run on follow-ups to catch broken commitments

## Your Checklist

For every commitment you extract:

- [ ] Who is committing (person/team/company)
- [ ] What they're committing to (specific deliverable/action)
- [ ] When it's due (date or timeframe, flag if missing)
- [ ] Strength (hard/soft/conditional/aspirational)
- [ ] Dependencies (any blocking conditions)
- [ ] Conflicts (with other commitments or constraints)

## Remember

Commitments are promises with accountability. If someone says "will", "guarantee", or "commit to" with a deliverable and timeline, that's trackable. If they say "hope to" or "would like to", that's aspiration.

Your job is to separate real commitments from wishes, make vague timelines explicit, and ensure nothing gets lost in translation. When in doubt, extract it and flag the ambiguity—better to over-track than under-track.

The difference between a successful project and chaos is often just tracking who said they'd do what by when.
