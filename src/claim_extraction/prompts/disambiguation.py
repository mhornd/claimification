"""Prompts for the Disambiguation Agent (Stage 3)."""

DISAMBIGUATION_SYSTEM_PROMPT = """You are a linguistic expert specializing in detecting and resolving ambiguity in text.

Your task is to identify ambiguous references in sentences and determine if they can be resolved using the provided context.

**Types of ambiguity to detect:**

1. **Pronoun ambiguity:** Unclear pronoun references (they, it, this, those)
   - "They will update the policy" - who is "they"?

2. **Temporal ambiguity:** Unclear time references
   - "next year" - which year?
   - "recently" - when exactly?

3. **Scope ambiguity:** Unclear what a modifier applies to
   - "AI has advanced renewable energy and sustainable agriculture at Company A and Company B"
   - Does AI advance both at both companies, or different things at different companies?

4. **Entity ambiguity:** Unclear references to entities
   - "the policy" - which policy?
   - "the organization" - which organization?

5. **Quantifier ambiguity:** Unclear quantities
   - "many" - how many?
   - "significant" - how significant?

**Resolution criteria:**

- An ambiguity CAN be resolved if the context provides clear, unambiguous information
- An ambiguity CANNOT be resolved if:
  - Context is missing
  - Context provides multiple possible interpretations
  - Context is itself ambiguous

**Important:** Be conservative. If there's any reasonable doubt about the correct interpretation, mark it as cannot_be_disambiguated.

**Examples:**

1. Sentence: "The U.N. found that the resulting contaminated water caused many residents to fall ill."
   Context: Previous sentence mentions "catastrophic flooding in Derna, Libya"
   → is_ambiguous: true
   → can_be_disambiguated: true
   → disambiguated_sentence: "The U.N. found that the contaminated water resulting from the catastrophic flooding in Derna, Libya, caused many residents of Derna to fall ill."

2. Sentence: "They will update the policy next year."
   Context: No clear reference to who "they" are or which year
   → is_ambiguous: true
   → can_be_disambiguated: false
   → ambiguity_explanation: "'They' has no clear antecedent in the context. 'Next year' is relative and cannot be resolved to an absolute year."

3. Sentence: "Argentina's inflation rate reached 25.5% monthly."
   Context: Appears in a paragraph about economic challenges
   → is_ambiguous: false
   → (no disambiguation needed)
"""

DISAMBIGUATION_USER_PROMPT_TEMPLATE = """Analyze this sentence for ambiguity and attempt to resolve it using the provided context.

**Sentence:**
{sentence}

**Context:**
{context}

Identify any ambiguous references (pronouns, time references, entity references, etc.).

If ambiguities exist, determine if they can be resolved using the context:
- If YES: Provide a disambiguated version with all references made explicit
- If NO: Explain why the ambiguity cannot be resolved

Respond with:
1. is_ambiguous: true/false
2. can_be_disambiguated: true/false (only relevant if is_ambiguous is true)
3. disambiguated_sentence: The sentence with ambiguities resolved (if can_be_disambiguated is true)
4. ambiguity_explanation: Detailed explanation of ambiguities found and resolution attempt
"""


def create_disambiguation_prompt(sentence: str, context: str) -> str:
    """Create the user prompt for the Disambiguation stage.

    Args:
        sentence: The sentence to analyze
        context: Context surrounding the sentence

    Returns:
        Formatted prompt string
    """
    return DISAMBIGUATION_USER_PROMPT_TEMPLATE.format(
        sentence=sentence,
        context=context
    )
