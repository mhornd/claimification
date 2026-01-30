---
name: uncertainty-quantification
description: Analyze text for uncertainty markers and confidence levels, mapping linguistic hedging to quantified scores with visualization
---

# Uncertainty Quantification Skill

Analyze text for linguistic uncertainty markers and map them to quantified confidence scores per statement.

## Overview

This skill helps identify and quantify uncertainty in text by detecting linguistic hedging, qualifying language, and confidence markers. It transforms implicit uncertainty into explicit confidence scores and visualizations.

## What This Does

Uncertainty Quantification analyzes text through three stages:

1. **Marker Detection:** Identifies linguistic indicators of uncertainty
2. **Confidence Mapping:** Maps markers to numerical confidence scores (0-100%)
3. **Visualization:** Presents results as structured reports with uncertainty heatmaps

## When to Use

Use this skill when you need to:

- Evaluate the confidence level of claims or statements
- Identify hedging language in generated content
- Assess the reliability of information sources
- Compare certainty across multiple text generations
- Flag low-confidence statements for verification
- Analyze scientific, legal, or technical writing for qualifying language

## The Process

**Understanding the context:**
- Read the input text completely
- Identify individual statements or claims
- Note the domain/context (scientific, journalistic, conversational, etc.)

**Detecting uncertainty markers:**
- Scan for linguistic hedging patterns
- Identify epistemic modality markers
- Detect qualifying phrases and caveats
- Note absence of certainty (lack of definitive language)

**Mapping to confidence scores:**
- Assign base confidence (start at 100% = absolute certainty)
- Apply reductions based on detected markers
- Consider cumulative effect of multiple hedges
- Adjust for domain-specific conventions

**Presenting results:**
- Structure output with clear confidence scores
- Use visual indicators (color coding, symbols)
- Provide uncertainty heatmaps for longer texts
- Highlight highest and lowest confidence statements

## Uncertainty Markers

### High Uncertainty (Confidence: 0-40%)

- Speculation: "could be", "might be", "perhaps", "possibly"
- Doubt: "unclear", "uncertain", "questionable", "doubtful"
- Hypothesis: "we hypothesize", "it is conceivable that"
- Conditionals: "if X then maybe Y", "assuming that"
- Weak evidence: "some suggest", "there are claims that"

### Medium Uncertainty (Confidence: 40-70%)

- Probability: "likely", "probably", "tends to", "appears to"
- Hedging: "somewhat", "relatively", "fairly", "rather"
- Estimation: "approximately", "roughly", "around", "about"
- Qualified claims: "in most cases", "generally", "typically"
- Tentative: "seems to", "suggests that", "indicates"

### Low Uncertainty (Confidence: 70-95%)

- Strong probability: "very likely", "almost certainly", "highly probable"
- Evidence-based: "studies show", "research indicates", "data suggests"
- Consensus: "widely accepted", "generally agreed", "established"
- Observed patterns: "consistently", "regularly", "frequently"

### No Uncertainty (Confidence: 95-100%)

- Factual statements: "is", "are", "was", "were"
- Definitive: "always", "never", "all", "none", "every"
- Proven: "demonstrated", "proven", "confirmed", "verified"
- Mathematical: "exactly", "precisely", "equals"

## Confidence Scoring Guidelines

**Base Score:** Start with 100% confidence

**Apply Reductions:**
- Each high-uncertainty marker: -40 to -60 points
- Each medium-uncertainty marker: -20 to -30 points
- Each low-uncertainty marker: -5 to -15 points
- Lack of evidence cited: -10 to -20 points
- Vague quantifiers ("some", "many"): -10 to -15 points
- Passive voice without agent: -5 to -10 points

**Adjustments:**
- Multiple hedges compound (not additive)
- Domain conventions matter (scientific writing uses more hedging)
- Context can increase/decrease impact of markers
- Never below 0% or above 100%

**Special Cases:**
- Counterfactuals: Score the conditional, not the implication
- Opinions/recommendations: Mark as non-factual (N/A for confidence)
- Questions: Not statements, exclude from scoring
- Quotes: Attribute confidence to source, not quoter

## Output Format

### Statement-Level Analysis

```
📊 UNCERTAINTY ANALYSIS
━━━━━━━━━━━━━━━━━━━━

Statement 1: "Climate change is causing global temperatures to rise."
├─ Confidence: 95% ████████████████████░
├─ Markers: None (factual declarative)
└─ Classification: HIGH CERTAINTY

Statement 2: "This could lead to more extreme weather events."
├─ Confidence: 45% █████████░░░░░░░░░░░
├─ Markers: "could" (speculation)
└─ Classification: MEDIUM UNCERTAINTY

Statement 3: "Some scientists believe we might see impacts by 2030."
├─ Confidence: 25% █████░░░░░░░░░░░░░░░
├─ Markers: "some" (vague), "believe" (opinion), "might" (possibility)
└─ Classification: HIGH UNCERTAINTY
```

### Heatmap Visualization

For longer texts, provide a visual heatmap:

```
🌡️ CONFIDENCE HEATMAP
━━━━━━━━━━━━━━━━━━━

Paragraph 1: ████████████████████ (95%) ← High certainty
Paragraph 2: █████████░░░░░░░░░░░ (50%) ← Medium uncertainty
Paragraph 3: ████░░░░░░░░░░░░░░░░ (20%) ← High uncertainty
Paragraph 4: ████████████████░░░░ (85%) ← High certainty

Legend: █ = Confident | ░ = Uncertain
```

### Summary Statistics

```
📈 OVERALL METRICS
━━━━━━━━━━━━━━━━

Total Statements:        12
Average Confidence:      67%
Median Confidence:       72%
High Certainty (>80%):   5 statements (42%)
Medium Certainty (40-80%): 4 statements (33%)
Low Certainty (<40%):    3 statements (25%)

⚠️  FLAGGED FOR REVIEW
• Statement 3: Only 25% confidence
• Statement 7: Only 18% confidence
• Statement 9: Only 32% confidence
```

## Key Principles

- **Systematic Detection:** Use the marker taxonomy consistently
- **Context Matters:** Scientific hedging ≠ lack of confidence
- **Transparency:** Always show the markers that influenced scoring
- **Reproducibility:** Apply the same rubric across all statements
- **Actionability:** Flag low-confidence statements for verification
- **No Guessing:** When uncertain about classification, explain why

## Usage Example

**Input:**

```
The new treatment appears to be effective in reducing symptoms.
Studies suggest that approximately 70% of patients show improvement.
It might also have preventive benefits, though more research is needed.
```

**Expected Output:**

```
📊 UNCERTAINTY ANALYSIS
━━━━━━━━━━━━━━━━━━━━

Statement 1: "The new treatment appears to be effective in reducing symptoms."
├─ Confidence: 60% ████████████░░░░░░░░
├─ Markers: "appears to" (tentative)
└─ Notes: Medium certainty, needs evidence citation

Statement 2: "Studies suggest that approximately 70% of patients show improvement."
├─ Confidence: 75% ███████████████░░░░░
├─ Markers: "suggest" (tentative), "approximately" (estimation)
└─ Notes: Evidence-based but with hedging

Statement 3: "It might also have preventive benefits, though more research is needed."
├─ Confidence: 30% ██████░░░░░░░░░░░░░░
├─ Markers: "might" (speculation), "though more research is needed" (explicit uncertainty)
└─ Notes: Highly uncertain, speculative claim

📈 SUMMARY
━━━━━━━━━

Average Confidence: 55%
Recommendation: Verify claims with primary sources
Highest Uncertainty: Statement 3 (30%)
```

## Limitations

- Subjective interpretation of some markers
- Cultural and domain-specific language conventions vary
- Sarcasm and irony detection not included
- Cannot assess actual factual accuracy (only expressed confidence)
- Works best with formal, declarative text
- May need calibration for different domains

## Advanced Techniques

**Comparative Analysis:**
Compare uncertainty across multiple generations of the same content to identify:
- Consistency in confidence levels
- Where uncertainty increases/decreases
- Most stable vs. most variable claims

**Temporal Tracking:**
For iterative content generation:
- Track how confidence evolves across revisions
- Identify claims that remain uncertain
- Flag persistent hedging as needing verification

**Cross-Document Consensus:**
When analyzing multiple sources:
- Higher confidence when sources agree without hedging
- Flag contradictions (high confidence + opposite claims)
- Identify consensus claims vs. disputed claims

## Related Concepts

This skill complements other analytical approaches:

- **Claim Extraction:** Extract claims first, then quantify their uncertainty
- **Contradiction Detection:** Low-confidence claims are more likely contradictory
- **Scientific Rigor:** Helps identify overconfident or underspecified claims
- **Bias Detection:** Confidence patterns may reveal perspective issues

## Integration Examples

**With Claim Extraction:**
```
1. Extract claims using /extract-claims
2. Run uncertainty quantification on extracted claims
3. Flag low-confidence claims for fact-checking
4. Prioritize high-confidence claims for publication
```

**With Content Generation:**
```
1. Generate initial content
2. Analyze uncertainty levels
3. Identify low-confidence statements
4. Request evidence/citations for flagged statements
5. Re-analyze to confirm improved confidence
```

## Best Practices

1. **Always show your work:** List the markers you detected
2. **Be consistent:** Use the same scoring rubric throughout
3. **Adapt to domain:** Acknowledge when domain conventions affect scoring
4. **Flag extremes:** Highlight both very high and very low confidence
5. **Provide context:** Explain why a score was assigned
6. **Enable action:** Make it clear what should be done with the results

## Notes

This skill analyzes *expressed* uncertainty through linguistic markers. It does not:
- Verify factual accuracy
- Assess source credibility
- Perform fact-checking
- Make judgments about truth value

It measures confidence level as communicated by the text itself.

## Support

For questions about this skill or suggestions for improvement:
- GitHub: https://github.com/TwoDigits/claimification
- Issues: https://github.com/TwoDigits/claimification/issues
