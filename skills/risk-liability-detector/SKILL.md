---
name: risk-liability-detector
description: Identify overpromises, missing disclaimers, and liability risks in marketing copy, contracts, or customer communications
---

# Risk & Liability Detector

Catch legal problems before they catch you.

## Overview

Every piece of customer-facing content carries legal risk. "Guarantees 100%." "Never fails." "Your data is completely safe." One overpromise can cost millions.

Most teams review for grammar and brand voice. Few systematically scan for legal landmines.

You're a risk radar, not a lawyer. Find statements that create liability exposure, flag missing disclaimers, identify overpromises. Make content safer without killing the message.

## When to Use

Use before publishing any customer-facing content:

- Marketing copy and ad campaigns
- Product descriptions and landing pages
- Customer emails and announcements
- Social media posts and press releases
- Sales materials and pitch decks
- Terms of service or SLA documents
- Support responses with commitments

Don't use for:

- Internal documentation (no customer exposure)
- Content already reviewed by legal counsel
- Historical analysis without publishing intent
- Pure informational content with no claims

## The Process

**First, scan for danger words:**
Look for absolute language:

- "Guarantee", "guaranteed", "ensures", "promises"
- "100%", "always", "never", "zero", "complete"
- "Completely", "totally", "absolutely", "perfectly"
- "Risk-free", "safe", "secure", "protected"
- "Best", "fastest", "only", "ultimate" (superlatives)

**Then, identify risk types:**
For each problematic statement, categorize:

1. **Legal Risk** - Creates contractual liability or warranty claims
2. **Regulatory Risk** - Violates industry regulations (FTC, FDA, CAN-SPAM, etc.)
3. **Reputational Risk** - Damages credibility when proven false
4. **Professional Liability** - Unauthorized practice of law/medicine/other licensed profession

**Assess severity:**

- **HIGH:** Immediate legal exposure, regulatory violations, false claims
- **MEDIUM:** Overpromises that could become lawsuits, missing disclaimers
- **LOW:** Marketing puffery that borders on problematic, vague claims

**Finally, provide fixes:**

- Specific rewrite suggestions
- Required disclaimers
- Qualifying language to add
- Claims to substantiate or remove

## Risk Categories

### Legal Risk (Contractual Liability)

**Absolute performance guarantees:**

- "We guarantee 100% uptime" → Creates SLA obligation
- "You'll never lose data" → Strict liability claim
- "Always works perfectly" → Warranty claim

**Outcome promises:**

- "You will save $10,000" → Measurable outcome claim
- "Guaranteed results" → Performance warranty
- "Your problems will be solved" → Success guarantee

**Time commitments without conditions:**

- "24/7 support" → Must deliver or breach
- "Instant response" → Measurable commitment
- "Same-day delivery" → Hard timeline

**Fix approach:** Add qualifiers ("up to", "typically", "designed to"), conditions ("under normal use"), or remove absolute language.

### Regulatory Risk

**FTC - Deceptive advertising:**

- Unsubstantiated claims ("clinically proven" without studies)
- False comparisons ("better than competitors" without evidence)
- Hidden fees or conditions

**CAN-SPAM Act (Email marketing):**

- Missing unsubscribe link
- Missing physical address
- Deceptive subject lines
- No identification of sender

**FDA (Healthcare/Medical):**

- Medical claims without approval ("cures cancer")
- Disease treatment claims for supplements
- Diagnostic claims for non-approved devices

**GDPR/Privacy:**

- Claims about data security without basis
- Missing privacy disclosures
- Unauthorized data use claims

**Unauthorized Practice of Law/Medicine:**

- "Your personal lawyer" for non-legal service
- "Medical advice" from non-doctors
- "Legal review" without licensed attorneys

**Fix approach:** Add required disclosures, remove prohibited claims, ensure regulatory compliance for industry.

### Reputational Risk

**Exaggerations that can be fact-checked:**

- "Used by millions" when you have 1,000 users
- "Industry leader" when you're not
- "Award-winning" without actual awards

**Impossible absolutes:**

- "Zero bugs" (every software has bugs)
- "Perfect security" (nothing is perfect)
- "Never goes down" (everything goes down)

**Competitive claims without evidence:**

- "Better than [competitor]" without data
- "Only solution that..." when others exist
- "#1 in [category]" without ranking source

**Fix approach:** Use accurate numbers, qualify claims ("one of the leading"), remove unprovable statements.

## Output Format

Keep it actionable. Show what's risky, why it matters, how to fix it.

```
⚠️  RISK & LIABILITY DETECTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Content: [Title/Type of content being reviewed]
Review Date: [Date]
Total Risks Found: 5 (2 HIGH, 2 MEDIUM, 1 LOW)

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 HIGH RISK
━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 - Absolute Performance Guarantee
Location: Headline
Problematic Text: "We guarantee 100% accuracy in all diagnoses"
Risk Type: Legal + Regulatory
Why Risky: Creates express warranty; medical claims require FDA approval
Potential Impact: Product liability lawsuits, FDA enforcement, class action
Fix: Remove "100%" → "Our AI assists with diagnostic accuracy" + Add disclaimer: "Not a substitute for professional medical advice"

#2 - False User Claims
Location: Social proof section
Problematic Text: "Used by 50,000+ businesses worldwide"
Risk Type: Legal (Fraud/Misrepresentation)
Why Risky: Actual user count is 487 - this is false advertising
Potential Impact: FTC enforcement, loss of trust, securities fraud if fundraising
Fix: Use accurate number: "Join 500+ businesses using our platform" OR remove claim entirely

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ MEDIUM RISK
━━━━━━━━━━━━━━━━━━━━━━━━━━━

#3 - Unsubstantiated Security Claim
Location: Product description
Problematic Text: "Your data is completely safe and secure"
Risk Type: Legal + Reputational
Why Risky: Absolute security claim impossible to guarantee; liability if breach occurs
Potential Impact: Lawsuits after data breach, credibility damage
Fix: Qualify: "We use industry-standard encryption and security practices" + Link to security documentation

#4 - Missing CAN-SPAM Requirements
Location: Email footer
Problematic Text: [Missing unsubscribe link and physical address]
Risk Type: Regulatory
Why Risky: CAN-SPAM Act violations carry penalties up to $50,120 per email
Potential Impact: FTC fines, deliverability issues
Fix: Add unsubscribe link + Add physical mailing address + Ensure sender identification

━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  LOW RISK
━━━━━━━━━━━━━━━━━━━━━━━━━━━

#5 - Borderline Superlative
Location: Call-to-action
Problematic Text: "The ultimate solution for your business"
Risk Type: Reputational
Why Risky: Vague superlative that could disappoint; hard to substantiate
Potential Impact: Customer disappointment, minor credibility hit
Fix: Make specific: "A comprehensive solution for [specific use case]" OR remove "ultimate"

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ RECOMMENDED ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMMEDIATE (Before publishing):
1. Remove false user count claim (#2) - CRITICAL
2. Rewrite medical guarantee (#1) + add disclaimer
3. Add CAN-SPAM compliance elements (#4)

SHORT-TERM (This week):
4. Revise security claim (#3) with qualifiers
5. Replace superlative (#5) with specific value prop

ONGOING:
- Have legal counsel review all marketing claims
- Maintain substantiation files for any performance claims
- Create approved disclaimer library

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: DO NOT PUBLISH (2 high-risk issues require fixes)
Overall Risk Level: HIGH
Legal Review Needed: YES

Safe to publish after: All HIGH risks addressed + legal counsel review
```

## Detection Examples

**From Marketing Copy:**

```
Input: "Our software never crashes and saves you thousands in IT costs.
Join 10,000+ happy customers who love our risk-free guarantee!"

Risks Found:
#1 - HIGH: "Never crashes" = Absolute performance claim (Legal risk)
Fix: "Built for reliability with 99.9% uptime"

#2 - MEDIUM: "Saves you thousands" = Unsubstantiated outcome promise (Legal + Reputational)
Fix: "Can reduce IT costs" or provide case study data

#3 - MEDIUM: "Risk-free guarantee" = Missing terms (Legal)
Fix: Define guarantee terms or link to refund policy

#4 - LOW: "10,000+ happy customers" = Verify number is accurate
Fix: Use exact number if under 10K, or ensure claim is substantiated
```

**From Email Campaign:**

```
Input: "URGENT: Your account needs immediate action! Click here now to
secure your data. We've made your information completely protected."

Risks Found:
#1 - HIGH: Missing CAN-SPAM requirements (Regulatory)
Fix: Add unsubscribe + physical address

#2 - MEDIUM: "URGENT" + "immediate action" = Potentially deceptive urgency (FTC)
Fix: Only use if genuinely urgent, otherwise misleading

#3 - MEDIUM: "Completely protected" = Absolute security claim (Legal)
Fix: "We've enhanced security features" with specifics

#4 - LOW: Vague call-to-action could be phishing-like (Reputational)
Fix: Be specific about what action is needed
```

**From Product Description:**

```
Input: "SmartContract AI - Your personal lawyer in your pocket. Saves
thousands in legal fees. Used by businesses worldwide."

Risks Found:
#1 - HIGH: "Your personal lawyer" = Unauthorized practice of law (Regulatory + Legal)
Fix: "Legal contract analysis tool" + "Not a substitute for licensed legal counsel"

#2 - MEDIUM: "Saves thousands in legal fees" = Replacement of legal services claim (Legal)
Fix: "Helps you understand contracts before consulting an attorney"

#3 - LOW: "Used by businesses worldwide" = Vague claim (Reputational)
Fix: Specific number or remove if not substantiated
```

## Risk Severity Guidelines

**HIGH Risk - Stop and fix before publishing:**

- False or fraudulent claims (wrong user numbers, fake awards)
- Absolute guarantees that create strict liability (100%, never, always)
- Regulatory violations (missing CAN-SPAM, unauthorized practice of profession)
- Medical/health claims without FDA approval
- Measurable outcome promises without substantiation
- Claims that create express warranties you can't honor

**MEDIUM Risk - Fix before or shortly after publishing:**

- Overpromises that could lead to lawsuits (vague guarantees)
- Missing disclaimers for important claims
- Unsubstantiated comparative claims ("better than")
- Security/safety claims without basis
- Borderline regulatory issues (unclear if violates rules)
- Exaggerations that can be easily fact-checked

**LOW Risk - Consider fixing, monitor:**

- Marketing puffery (subjective claims like "great", "amazing")
- Vague superlatives without specific claims ("ultimate", "best")
- Aspirational language ("we strive to", "we aim for")
- Minor inaccuracies that don't affect core claims
- Dated information that should be updated

## Common Patterns

**The "Impossible Absolute" Pattern:**
Any claim with 100%, always, never, zero, complete, perfect in a measurable context.
→ Always flag as HIGH risk
→ Either remove or add realistic qualifier

**The "Regulatory Trap" Pattern:**
Language that triggers industry-specific regulations (medical, legal, financial).
→ Flag as HIGH if unlicensed practice claims
→ Require disclaimers or remove claims

**The "Hidden Promise" Pattern:**
Statements that imply outcomes without explicitly promising them.
"Most users see results" = Implied success rate claim
→ Flag as MEDIUM, require substantiation or qualification

**The "Social Proof Inflation" Pattern:**
User counts, testimonials, awards that can't be verified.
→ Verify accuracy
→ Flag as HIGH if false, LOW if just rounded

## Do's and Don'ts

**DO:**

- Flag every absolute claim (100%, never, always, guarantee)
- Check for industry-specific regulations (healthcare, finance, legal)
- Verify any numbers or statistics can be substantiated
- Provide specific rewrite suggestions, not just "fix this"
- Categorize by risk type (Legal/Regulatory/Reputational)
- Prioritize by severity (HIGH/MEDIUM/LOW)
- Include required disclaimers in fix suggestions
- Note missing compliance elements (CAN-SPAM, privacy policies)

**DON'T:**

- Miss security claims ("safe", "secure", "protected")
- Ignore outcome promises ("you will save", "you'll achieve")
- Skip over professional service claims ("lawyer", "doctor", "advisor")
- Treat all risks equally (prioritize HIGH risks)
- Only identify problems without suggesting fixes
- Confuse marketing puffery with actual claims ("great product" is usually fine)
- Flag aspirational language as high risk ("we strive to" is okay)
- Forget to check for required disclosures

## Watch Out For

**Qualified vs. Absolute Claims:**
"Designed to provide 99.9% uptime" (qualified) ≠ "Guarantees 100% uptime" (absolute)
Absolute = HIGH risk, Qualified = Usually okay

**Industry-Specific Triggers:**
"Medical advice", "legal counsel", "financial advisor", "diagnose", "treat", "cure"
→ Immediate regulatory red flags if not licensed service

**Hidden Comparisons:**
"Better solution" (better than what?), "More efficient" (than what?), "#1 platform" (ranked by whom?)
→ Require substantiation or qualification

**Outcome vs. Feature:**
"Fast processing" (feature) vs. "You'll save 5 hours per week" (outcome promise)
Outcomes require substantiation, features usually okay

**Temporal Claims:**
"24/7", "instant", "immediate", "same-day", "real-time"
→ These create measurable obligations; verify you can deliver

## Integration Workflows

**Pre-publish review:**

1. Run risk detector on final content
2. Fix all HIGH risks before publishing
3. Document rationale for any MEDIUM risks kept
4. Have legal review if any HIGH risks identified

**Marketing campaign launch:**

1. Review all copy (ads, emails, landing pages)
2. Check for CAN-SPAM compliance in emails
3. Verify all claims can be substantiated
4. Prepare disclosure/disclaimer library

**Social media posts:**

1. Quick scan before posting (especially CEO/founder posts)
2. Flag guarantees or absolute claims
3. Verify any statistics or user numbers
4. Check for compliance with platform policies

**Customer communications:**

1. Review email templates for overpromises
2. Ensure support responses don't create warranties
3. Check for missing disclaimers
4. Audit commitment language (use commitment-tracker)

## Key Principles

- **Absolute language = Legal liability:** "Guarantee", "always", "never" create strict obligations
- **Claims need proof:** Any measurable claim should have substantiation
- **Disclaimers matter:** Missing disclaimers increase liability even for true claims
- **Regulatory > Brand:** Compliance violations trump marketing impact
- **High risk stops publishing:** Don't negotiate on HIGH risks - fix them
- **Context changes risk:** Same word in different contexts has different risk (healthcare vs. SaaS)
- **Fix suggestions are required:** Don't just flag problems, provide solutions

## Your Checklist

For every piece of content you review:

- [ ] Scan for absolute language (100%, always, never, guarantee)
- [ ] Check for outcome promises (you will save, you'll achieve)
- [ ] Identify professional service claims (lawyer, doctor, medical or else)
- [ ] Verify numbers and statistics are accurate
- [ ] Look for missing disclaimers or disclosures
- [ ] Check regulatory compliance (CAN-SPAM for emails, FDA for health, etc.)
- [ ] Assess security/safety claims
- [ ] Evaluate competitive/superlative claims
- [ ] Categorize each risk by type (Legal/Regulatory/Reputational)
- [ ] Assign severity (HIGH/MEDIUM/LOW)
- [ ] Provide specific fix for each risk
- [ ] Give clear publish/don't-publish verdict

## Remember

Legal risk isn't about being conservative - it's about being accurate. "We guarantee 99.9% uptime" is a strong claim that's legally defensible if true. "We guarantee 100% uptime" is impossible and creates liability.

Your job is to separate defensible claims from legal landmines, provide concrete fixes, and give teams confidence to publish safely. When in doubt, flag it and explain why - better to be cautious than to defend a lawsuit.

The difference between effective marketing and legal disaster is often just one word: "guarantee".
