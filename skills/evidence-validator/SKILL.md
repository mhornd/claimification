---
name: evidence-validator
description: Validate claims with rigorous evidence from reputable sources - requires double verification and internet research for every factual statement
---

# Evidence Validator

Verify every claim. Accept nothing without proof.

## Overview

Every document, report, and article contains claims. "Studies show X." "Experts agree Y." "Research proves Z."

Most claims are unsupported, poorly sourced, or based on weak evidence. This skill validates them through rigorous internet research.

You're an evidence hunter, not a fact-checker. Find proof for every claim, verify from multiple independent sources, assess evidence strength. Accept nothing on faith.

**CRITICAL:** This is a research task. You MUST search the internet for evidence. You MUST verify every fact from TWO independent reputable sources minimum. No shortcuts.

## When to Use

Use before publishing or trusting any content with factual claims:
- Research papers or white papers
- Reports with statistics or data
- Articles making scientific claims
- Marketing content with product claims
- Journalism or investigative pieces
- Policy documents with evidence
- Any content where accuracy matters

Don't use for:
- Opinion pieces (subjective, not factual)
- Creative fiction (facts don't matter)
- Internal brainstorming (exploratory)
- Already peer-reviewed content

## The Process

**IMPORTANT: This is active research, not passive extraction.**

**Step 1: Extract claims from the text**
Identify every factual statement that needs evidence:
- Statistics: "70% of users prefer X"
- Scientific claims: "Vitamin D prevents COVID"
- Historical facts: "Founded in 2015"
- Expert consensus: "Doctors recommend Y"
- Causal claims: "A causes B"

**Step 2: Research each claim (MANDATORY)**
For EVERY claim, you MUST:
1. Search the internet for evidence
2. Prioritize reputable sources (see criteria below)
3. Find AT LEAST TWO independent sources
4. Verify facts match the claim exactly
5. Check publication dates (recent = better)

**DO NOT skip research. DO NOT assume. DO NOT accept single sources.**

**Step 3: Assess evidence strength**
For each claim, categorize evidence:
- **STRONG:** Multiple reputable sources, primary research, peer-reviewed
- **MODERATE:** Credible sources, but limited or secondary research
- **WEAK:** Single source, outdated, or questionable credibility
- **NONE:** No evidence found despite thorough search

**Step 4: Flag unsupported claims**
Any claim with WEAK or NONE evidence is flagged as:
- ⚠️ UNSUPPORTED (no evidence found)
- ⚠️ WEAKLY SUPPORTED (insufficient or questionable evidence)
- ⚠️ CONTRADICTED (evidence shows opposite)

**Step 5: Compile evidence summary**
Brief but complete:
- List each claim
- Show evidence found (or lack thereof)
- Cite all sources with URLs
- Note evidence strength

## Source Quality Criteria

**TIER 1 - Highest Quality (Prefer these):**
- Peer-reviewed scientific journals (Nature, Science, JAMA, etc.)
- Government statistical agencies (Census, CDC, FDA, etc.)
- University research institutions (.edu domains)
- Established scientific organizations (WHO, NIH, etc.)
- Primary research papers with methodology

**TIER 2 - Reputable (Acceptable):**
- Established newspapers with fact-checking (NYT, WSJ, The Guardian)
- Industry research firms (Gartner, McKinsey, Pew Research)
- Professional organizations in relevant field
- Well-documented company reports (10-K filings, annual reports)
- Technical documentation from established companies

**TIER 3 - Use with Caution:**
- General news sites (CNN, BBC, Reuters)
- Wikipedia (only for directional research, verify claims elsewhere)
- Trade publications
- Company blogs or PR
- Expert interviews without citation

**TIER 4 - Reject:**
- Social media posts
- Personal blogs without credentials
- Marketing content without data
- Anonymous sources
- "Trust me bro" statements
- Circular citations (A cites B, B cites A)

**Double Verification Rule:**
You need TWO independent Tier 1 or Tier 2 sources, OR
THREE independent sources if one is Tier 3.

Never accept a claim based on a single source, no matter how reputable.

## Evidence Strength Guidelines

**STRONG Evidence:**
- Multiple peer-reviewed studies confirm claim
- Government statistics directly support claim
- Primary research with clear methodology
- Recent publications (within 2-3 years for fast-moving fields)
- Independent replication of findings
- Example: "70% success rate" backed by randomized controlled trial + meta-analysis

**MODERATE Evidence:**
- Credible secondary sources report claim
- Industry research from reputable firm
- Expert consensus without primary research
- Older but still relevant data (3-5 years)
- Single strong source + corroborating weak source
- Example: "Market size $10B" from Gartner report + company filings

**WEAK Evidence:**
- Single source only
- Questionable source credibility
- Outdated information (>5 years in fast fields)
- Circular citations
- Vague claims without specific data
- Example: "Most users prefer X" from company marketing page

**NO Evidence:**
- No sources found after thorough search
- Only promotional or biased sources
- Contradictory evidence found
- Example: "Proven to cure disease" with zero scientific backing

## Output Format

Keep it brief but complete. Show every claim, evidence status, and sources.

```
🔬 EVIDENCE VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Document: [Title]
Claims Analyzed: 8
Evidence Found: 5 strong, 2 moderate, 0 weak, 1 unsupported

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ STRONG EVIDENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claim #1: "70% of developers use Git for version control"
Evidence:
  ✓ Stack Overflow Developer Survey 2025: 74% use Git
    Source: https://stackoverflow.com/survey/2025
  ✓ GitHub's State of Software 2025: 71% Git adoption
    Source: https://github.com/reports/state-of-software-2025
Status: ✅ VERIFIED (Strong)
Note: Multiple independent sources confirm ~70% range

Claim #2: "Vitamin D deficiency linked to increased COVID-19 severity"
Evidence:
  ✓ Meta-analysis in Nature Medicine (2024): Significant correlation
    Source: https://nature.com/articles/nm-2024-12345
  ✓ NIH systematic review (2024): Confirmed association
    Source: https://nih.gov/studies/vitamin-d-covid
  ✓ Peer-reviewed study in JAMA (2023): 40% higher severity in deficient patients
    Source: https://jamanetwork.com/journals/jama/article/2023-67890
Status: ✅ VERIFIED (Strong)
Note: Peer-reviewed, recent, multiple independent studies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ MODERATE EVIDENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claim #3: "Global AI market to reach $500B by 2028"
Evidence:
  ✓ Gartner market research report (2024): Projected $497B by 2028
    Source: https://gartner.com/ai-market-forecast-2024
  ✓ McKinsey analysis (2024): Estimates $450-550B range
    Source: https://mckinsey.com/ai-economic-impact
Status: ⚡ SUPPORTED (Moderate)
Note: Reputable sources but projections, not confirmed data

Claim #4: "Company founded in 2015"
Evidence:
  ✓ Company's About page: Founded 2015
    Source: https://company.com/about
  ✓ LinkedIn company profile: Founded 2015
    Source: https://linkedin.com/company/example
  ✓ Crunchbase: Founded Jan 2015
    Source: https://crunchbase.com/organization/example
Status: ⚡ SUPPORTED (Moderate)
Note: Multiple sources confirm, but all potentially sourced from company

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  UNSUPPORTED / WEAK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claim #5: "Our product is 10x faster than competitors"
Evidence:
  ✗ Only found claim on company's marketing page
  ✗ No independent benchmarks found
  ✗ No peer comparisons or reviews
Status: ❌ UNSUPPORTED
Recommendation: Remove claim or conduct independent benchmark
Sources Checked: TechCrunch, industry review sites, academic databases

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Claims: 8
✅ Strong Evidence: 5 claims (62.5%)
⚡ Moderate Evidence: 2 claims (25%)
⚠️  Weak Evidence: 0 claims
❌ Unsupported: 1 claim (12.5%)

Credibility Score: 87.5% (strong + moderate claims)

Action Required:
- Remove or substantiate Claim #5 (unsupported)
- Consider updating Claim #3 with disclaimer (projection)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ALL SOURCES CITED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Stack Overflow Developer Survey 2025
   https://stackoverflow.com/survey/2025

2. GitHub's State of Software 2025
   https://github.com/reports/state-of-software-2025

3. Meta-analysis in Nature Medicine (2024)
   https://nature.com/articles/nm-2024-12345

4. NIH systematic review (2024)
   https://nih.gov/studies/vitamin-d-covid

5. Peer-reviewed study in JAMA (2023)
   https://jamanetwork.com/journals/jama/article/2023-67890

6. Gartner market research report (2024)
   https://gartner.com/ai-market-forecast-2024

7. McKinsey analysis (2024)
   https://mckinsey.com/ai-economic-impact

8. Company About page
   https://company.com/about

9. LinkedIn company profile
   https://linkedin.com/company/example

10. Crunchbase company data
    https://crunchbase.com/organization/example
```

## Research Methodology

**How to search effectively:**

1. **Start with claim extraction**
   Use /extract-claims if needed to get atomic claims first

2. **Search for each claim systematically**
   - Start with academic databases (Google Scholar, PubMed)
   - Move to government/institutional sources
   - Check reputable news and industry research
   - Verify dates and recency

3. **Verify independence of sources**
   - Two sources citing the same original = one source
   - Look for primary research, not secondary citations
   - Check if sources are independent entities

4. **Cross-check contradictions**
   - If sources conflict, flag it
   - Look for more recent data
   - Assess methodology quality

5. **Document everything**
   - Save URLs for all sources
   - Note publication dates
   - Record exact figures/quotes

## Common Claim Types

**Statistical Claims:**
"70% of users...", "50% increase in...", "Average of..."
→ Need: Primary data source or reputable research
→ Look for: Sample size, methodology, date

**Scientific Claims:**
"X causes Y", "Studies show...", "Research proves..."
→ Need: Peer-reviewed papers or systematic reviews
→ Look for: RCT, meta-analysis, replication studies

**Historical Facts:**
"Founded in...", "First launched...", "Invented by..."
→ Need: Multiple independent sources
→ Look for: Primary documents, authoritative records

**Expert Consensus:**
"Doctors recommend...", "Experts agree..."
→ Need: Professional organization statements or surveys
→ Look for: Official guidelines, position papers

**Market Data:**
"Market size of...", "Industry growth...", "Projected to reach..."
→ Need: Research firm reports or industry analysis
→ Look for: Methodology, data sources, confidence intervals

## Do's and Don'ts

**DO:**
- Search the internet for EVERY factual claim
- Require TWO independent reputable sources minimum
- Prioritize peer-reviewed and government sources
- Check publication dates (recent = better)
- Verify exact numbers match the claim
- Flag unsupported claims clearly
- Cite all sources with full URLs
- Note evidence strength explicitly
- Cross-check contradictory evidence

**DON'T:**
- Accept single sources (even if reputable)
- Trust company marketing without verification
- Use social media as evidence
- Skip research because claim "seems true"
- Cite Wikipedia as final evidence (use it to find primary sources)
- Accept circular citations
- Ignore publication dates
- Confuse correlation with causation
- Accept vague claims without specifics

## Watch Out For

**Circular Citations:**
Article A cites Article B, Article B cites Article A
→ Only counts as ONE source (or zero if no primary data)

**Outdated Information:**
"Market size $10B" from 2018 report in 2026
→ Flag as outdated, search for recent data

**Promotional Bias:**
Only source is company's own marketing
→ Insufficient evidence, need independent verification

**Misrepresented Studies:**
Claim: "Coffee cures cancer"
Study: "Coffee may reduce certain cancer risks in mice"
→ Claim not supported by evidence

**Cherry-Picked Data:**
Claim cites only favorable studies, ignores contradictory evidence
→ Flag bias, search for systematic reviews or meta-analyses

**Sample Size Issues:**
"90% success rate" from study with 10 participants
→ Flag as weak evidence due to small sample

## Integration Workflows

**For research papers:**
1. Extract all factual claims
2. Research and verify each claim
3. Flag unsupported statements
4. Add citations for strong claims
5. Recommend removal of weak claims

**For marketing content:**
1. Identify product claims requiring evidence
2. Search for independent verification
3. Flag marketing-only claims
4. Suggest substantiation or removal
5. Ensure compliance with advertising standards

**For journalism:**
1. Extract all factual statements
2. Verify from primary sources
3. Check for contradictory evidence
4. Flag claims needing attribution
5. Ensure source diversity

**For reports:**
1. Validate all statistics and data
2. Verify study citations are accurate
3. Check for misrepresentation
4. Update outdated information
5. Strengthen evidence base

## Verification Tiers

**Tier 1: Publication in peer-reviewed journal**
- Highest evidence standard
- Requires two independent studies minimum
- Check for replication and meta-analyses

**Tier 2: Government or institutional data**
- Authoritative for statistics and official data
- Cross-check with independent sources when possible
- Verify dates and relevance

**Tier 3: Reputable research firms**
- Good for market data and industry trends
- Check methodology and sample size
- Verify with second independent firm

**Tier 4: Established journalism**
- Acceptable for general facts
- Must verify sources are cited in article
- Check for fact-checking process

**Tier 5: Company/promotional**
- Insufficient alone
- Must verify with independent sources
- Treat as claim, not evidence

## Key Principles

- **Every fact needs TWO independent sources:** No exceptions
- **Research is mandatory:** This is not passive extraction, it's active verification
- **Source quality matters:** Tier 1 beats Tier 3, always
- **Recent beats old:** In fast-moving fields, prioritize recent evidence
- **Primary beats secondary:** Original research > someone citing research
- **Independence is critical:** Same source cited twice = one source
- **Flag, don't fix:** Show what's unsupported, don't make up evidence
- **Cite everything:** URLs for all sources in summary

## Your Checklist

For every claim you validate:
- [ ] Claim extracted and made specific
- [ ] Internet search performed (academic, government, reputable sources)
- [ ] At least TWO independent sources found
- [ ] Sources are reputable (Tier 1-2 preferred)
- [ ] Evidence directly supports the claim
- [ ] Publication dates noted and recent
- [ ] Sources are independent (not circular)
- [ ] Evidence strength assessed (strong/moderate/weak/none)
- [ ] All sources cited with URLs
- [ ] Contradictory evidence checked

## Works Well With

Combine with these other skills:
- **/extract-claims** - Get clean atomic claims before validation
- **/contradiction-detector** - Check if evidence contradicts claims
- Fact-checking tools - Complement with automated checks
- Citation management - Export sources to reference managers

## Remember

Evidence validation is rigorous research work. You MUST search the internet. You MUST find TWO independent reputable sources. You MUST assess evidence strength. You MUST cite everything.

No shortcuts. No assumptions. No single sources. No promotional content as evidence.

Your job is to separate substantiated facts from unsupported claims. When in doubt, research more. When evidence is weak, flag it. When claims are unsupported, say so clearly.

The difference between credible content and misinformation is often just doing the research to verify every single claim.
