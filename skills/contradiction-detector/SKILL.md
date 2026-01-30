---
name: contradiction-detector
description: Detect contradictory statements within texts or across multiple generations, using claim-pair analysis for logical inconsistencies
---

# Contradiction Detection Pipeline

Find and fix contradictions before they cause problems.

## Overview

Hunt down statements that can't both be true. Compare claim pairs systematically. Flag the conflicts. Explain why they contradict. Suggest fixes.

You're a logic checker, not a mind reader. If two claims directly conflict, say so. If they're just different perspectives on compatible facts, don't flag them.

## When to Use

Use before publishing anything:
- Long documents or reports that need internal consistency
- Multi-agent outputs where different agents might conflict
- Multiple versions of the same content
- Argumentative text that needs logical coherence
- AI-generated content before merging or release

Don't use for:
- Creative fiction (intentional contradictions are fine)
- Brainstorming sessions (contradictions help explore ideas)
- Comparing genuinely different scenarios or conditions

## The Process

**First, extract the claims:**
- Break text into atomic statements
- One fact per claim
- Resolve pronouns ("he" → "the CEO")
- Keep context (line numbers, version IDs, agent sources)

**Then, compare systematically:**
- Start with claims about the same entity or topic
- Don't waste time comparing unrelated claims
- Check each pair for the 7 contradiction types (see below)
- Score severity: Definite → Likely → Possible → Apparent

**Finally, report what you found:**
- Show both contradicting claims with full context
- Explain WHY they contradict (don't just say "these conflict")
- Suggest how to fix it when obvious
- Prioritize definite contradictions over possible ones

**IMPORTANT:** Assume the text author is competent but human. Most contradictions are accidents, not fundamental misunderstandings. Flag them constructively.

## The 7 Contradiction Types

Know these patterns. Check for them systematically.

**1. Direct Negation**
"X is Y" vs. "X is not Y"
Always definite. No wiggle room.

**2. Numerical Mismatch**
"500 participants" vs. "All 300 participants completed..."
Check: Do the numbers make sense together? If not, flag it.

**3. Temporal Impossibility**
"Founded in 2020" vs. "10th anniversary in 2025"
Math doesn't work. Timeline is broken.

**4. Logical Incompatibility**
"All employees got a raise" vs. "Some employees saw no salary change"
All ≠ Some not. Basic logic violation.

**5. Scope Conflict**
"Applies to everyone in dept" vs. "Contractors are exempt"
Only contradicts if contractors ARE in the department. Context matters.

**6. Causal Mismatch**
"Sales dropped because of price increase" vs. "Sales dropped despite stable prices"
Can't have both causes. Pick one.

**7. State/Attribute Conflict**
"Drug is approved" vs. "Drug is still in trials"
Mutually exclusive states (unless referring to different jurisdictions—check context!).

## How to Actually Do This

**Step 1: Clean up the claims**
Resolve pronouns. Make references explicit. Fix "it", "he", "they", "yesterday" to actual entities and dates.

**Step 2: Filter by relevance**
Only compare claims about the same thing.
- "Paris has 2.2M people" vs. "London has 9M people" → Skip (different cities)
- "Paris has 2.2M people" vs. "The city lost population in 2020" → Compare (might be same city)

**Step 3: Run the logic tests**
- **Negation:** Does B directly negate A?
- **Mutual exclusivity:** Can both be true at once?
- **Numbers:** Do the quantities work together?
- **Timeline:** Is the sequence physically possible?
- **Implications:** Do they lead to opposite conclusions?

**Step 4: Score it**
- **DEFINITE (95-100%):** Logically or mathematically impossible
- **LIKELY (70-94%):** Highly improbable without extra context
- **POSSIBLE (40-69%):** Depends on interpretation
- **APPARENT (10-39%):** Looks contradictory but probably isn't

Don't overthink borderline cases. When in doubt, round up severity and flag it—better safe than sorry.

## Output Format

Keep it clean. Show the contradiction, explain why, suggest a fix.

```
🔍 CONTRADICTION REPORT
━━━━━━━━━━━━━━━━━━━━

Document: [Title/ID]
47 claims analyzed, 3 contradictions found

⛔ DEFINITE #1
━━━━━━━━━━━━

Claim A (Line 12): "The project was completed in June 2023."
Claim B (Line 45): "As of May 2023, the project was still in development."

Why it contradicts: Project can't be "still in development" in May if it was "completed" by June. Timeline doesn't work unless "completed in June" means late June.

Fix: Specify exact dates or change "in June" to "by late June."

⚠️  LIKELY #2
━━━━━━━━━━

Claim A (Line 28): "All participants were over 18 years old."
Claim B (Line 67): "The study included teenagers aged 16-17."

Why it contradicts: "All over 18" excludes 16-17 year olds.

Fix: Either remove "all" or correct the age range.

📊 SUMMARY
━━━━━━━━━

Definite: 1 | Likely: 2 | Possible: 0
Consistency: 94% (3 issues / 47 claims)
```

**For multi-version comparison:**

```
🔍 CROSS-VERSION ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━

V1 (Jan 15) | V2 (Jan 20) | V3 (Jan 25)
124 total claims (V1: 42, V2: 45, V3: 37)
5 contradictions across versions

⛔ Version 1 vs. Version 2
━━━━━━━━━━━━━━━━━━━━━━━━

V1: "The algorithm achieves 95% accuracy."
V2: "The algorithm achieves 87% accuracy."

Why: Can't have both 95% and 87% simultaneously.
Likely: Different test sets or conditions.
Fix: Specify which number applies when.

📈 EVOLUTION TRACK
━━━━━━━━━━━━━━━━

"System processes 1000 requests/second"
V1: ✓ | V2: ✗ (changed to 500) | V3: ✓ (back to 1000)

This claim flip-flopped. Investigate why.
```

**For complex documents with clusters:**

```
🕸️  CONTRADICTION CLUSTERS
━━━━━━━━━━━━━━━━━━━━━━━━

Revenue Claims (3 contradictions): Claims 5, 12, 23
→ Fix: Reconcile all financial figures

Timeline Claims (1 contradiction): Claims 18, 31
→ Fix: Establish single timeline
```

## Key Principles

- **Context is king:** Different time periods, scopes, or conditions = not a contradiction
- **Explain, don't just flag:** Show WHY claims contradict, not just that they do
- **Severity matters:** Fix definite contradictions first, possible ones later
- **Suggest fixes:** Don't just identify problems, help solve them
- **Track entities:** Keep pronouns resolved, references clear
- **Avoid false positives:** When uncertain, investigate before flagging
- **Assume competence:** Most contradictions are accidents, not incompetence

## Watch Out For These Edge Cases

**Time-sensitive claims:**
"CEO resigned in March" vs. "CEO is leading initiative"
→ Only contradicts if both refer to the same time period. Check dates.

**Conditional statements:**
"If X, then Y" vs. "Y didn't happen"
→ Not a contradiction. X might not have happened. Only flag if "X occurred" is also stated.

**Uncertainty expressions:**
"Likely to increase" vs. "Unlikely to increase" → Contradiction
"Possible to increase" vs. "Unlikely to increase" → Compatible (possible but unlikely makes sense)

**Different scopes:**
"Crime decreased in the city" vs. "Crime increased downtown"
→ Not contradictory if downtown ≠ whole city

**Opinions vs. facts:**
"The design is excellent" vs. "The design has flaws"
→ Opinions can differ. Only flag factual contradictions.

## Common Workflows

**Quality check before publishing:**
1. Extract claims with /extract-claims
2. Run contradiction detection
3. Fix the contradictions
4. Re-run to verify they're gone

**Multi-agent validation:**
1. Collect outputs from all agents
2. Extract claims from each
3. Run cross-agent detection
4. Flag which agents contradict each other
5. Implement arbitration or voting

**Version tracking:**
1. Extract claims from each version
2. Compare across versions
3. Identify when contradictions were introduced
4. Track fixes over time

## What This Can't Do

- Can't tell you which claim is correct (only that they conflict)
- Can't resolve contradictions for you (only detect them)
- May flag apparent contradictions with valid explanations
- Needs clear entity references (pronouns make this harder)
- Works best on factual text, not opinions or creative writing
- May miss contradictions requiring deep domain expertise

## Do's and Don'ts

**DO:**
- Extract and normalize claims before comparing
- Explain WHY claims contradict, not just that they do
- Prioritize definite over possible contradictions
- Suggest fixes when obvious
- Track sources (line numbers, versions, agents)
- Re-run after fixes to verify resolution

**DON'T:**
- Flag different time periods as contradictions
- Flag different scopes as contradictions
- Flag compatible uncertainty ("might" vs. "might not")
- Give vague explanations like "these conflict"
- Ignore context that reconciles apparent contradictions
- Forget to show both claims with full context

## Your Checklist

For every contradiction you report:
- [ ] Both claims shown with full context
- [ ] Type identified (temporal, numerical, logical, etc.)
- [ ] Severity scored (definite, likely, possible, apparent)
- [ ] Explanation of WHY they contradict
- [ ] Suggested fix (when obvious)
- [ ] Source tracking (line numbers, versions, agents)

## Works Well With

Combine with these other skills:
- **/extract-claims** - Get clean atomic claims before detecting contradictions
- **/uncertainty-quantification** - Check if contradictions involve uncertain claims
- Version control - Track when contradictions were introduced

## Remember

You're looking for statements that can't both be true, not statements that are just different. Context, time, and scope matter. Explain clearly. Suggest fixes. Prioritize by severity. Don't waste time on apparent contradictions that make sense with a bit more context.
