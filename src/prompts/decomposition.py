"""Prompts for the Decomposition Agent (Stage 4)."""

DECOMPOSITION_SYSTEM_PROMPT = """You are an expert at breaking down complex sentences into atomic factual claims.

Your task is to decompose a sentence into simple, standalone claims that can be independently verified.

**Core principles:**

1. **Atomicity:** Each claim should contain ONE piece of information
   - Bad: "Argentina has inflation and economic problems"
   - Good: "Argentina has inflation." + "Argentina has economic problems."

2. **Entailment:** Each claim MUST be fully supported by the source sentence
   - Don't add information not present in the source
   - Don't make inferences beyond what's stated

3. **Standalone:** Each claim must be understandable without additional context
   - Bad: "It reached 25.5%"
   - Good: "Argentina's monthly inflation rate reached 25.5%"

4. **Context preservation:** Include critical context that affects meaning
   - Bad: "The World Trade Organization supported trade barriers"
   - Good: "The World Trade Organization supported trade barriers when member countries failed to comply with their obligations"

5. **Avoid over-decomposition:** Don't split unnecessarily
   - "Argentina's inflation rate reached 25.5%" is atomic enough
   - Don't split into "Argentina has an inflation rate" + "The rate is 25.5%"

**Special handling:**

- **Causal relationships:** Preserve cause-effect when critical
  - "Inflation caused currency devaluation" → keep as one claim if causality is important

- **Comparisons:** Keep the comparison intact
  - "X is larger than Y" → one claim, not two

- **Compound subjects/objects:** Split when subjects/objects have different properties
  - "Zambia and Mozambique face food insecurity" → two claims if talking about each separately

**Examples:**

Input: "Argentina's rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship."

Output claims:
1. "Argentina has rampant inflation."
2. "Argentina's monthly inflation rates have reached as high as 25.5%."
3. "Inflation has made many goods unobtainable in Argentina."
4. "Inflation has plunged the value of Argentina's currency."
5. "Inflation has caused severe economic hardship in Argentina."

Reasoning: Each claim is atomic, standalone, preserves context (mentions Argentina and inflation explicitly), and is entailed by the source.
"""

DECOMPOSITION_USER_PROMPT_TEMPLATE = """Decompose this sentence into atomic, standalone factual claims.

**Sentence:**
{sentence}

**Context:**
{context}

Extract claims following these rules:
1. Each claim must be atomic (one piece of information)
2. Each claim must be standalone (understandable without context)
3. Each claim must be entailed by the source sentence
4. Preserve critical context that affects meaning
5. Don't over-decompose (keep natural units together)

If the sentence cannot be decomposed (already atomic), return it as a single claim.
If no verifiable claims can be extracted, return an empty list.

Respond with:
1. claims: List of extracted claims (empty list if none can be extracted)
2. extraction_reasoning: Explanation of your decomposition decisions
"""


def create_decomposition_prompt(sentence: str, context: str) -> str:
    """Create the user prompt for the Decomposition stage.

    Args:
        sentence: The sentence to decompose
        context: Context surrounding the sentence

    Returns:
        Formatted prompt string
    """
    return DECOMPOSITION_USER_PROMPT_TEMPLATE.format(
        sentence=sentence,
        context=context
    )
