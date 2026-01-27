"""Basic usage example for Claimification."""

import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import ClaimificationPipeline, SentenceStatus


def main():
    """Run a basic claim extraction example."""

    # Example from the explanation.md file
    question = "What are challenges in emerging markets?"

    answer = """Several emerging markets are grappling with severe economic instability. For instance, Argentina's rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship. Some experts estimate that the annual inflation rate could potentially double to 300%, while others predict even higher rates.

Nigeria, for example, is striving to become self-sufficient in wheat production but is hindered by climate change and violence, exacerbated by high grain prices due to the suspension of the Black Sea Grain Initiative.

Climate change has played a pivotal role in creating food insecurity and economic instability in farming-dependent economies, such as Zambia and Mozambique."""

    # Initialize pipeline
    # Make sure OPENAI_API_KEY or ANTHROPIC_API_KEY is set in environment
    pipeline = ClaimificationPipeline(
        model=os.getenv("CLAIMIFICATION_MODEL", "gpt-4o"),
        temperature=0.0,
        context_sentences=2,
        verbose=True
    )

    # Extract claims
    result = pipeline.extract_claims(question, answer)

    # Print results in detail
    print("\n" + "="*80)
    print("DETAILED RESULTS")
    print("="*80 + "\n")

    for i, sentence_result in enumerate(result.sentence_results):
        letter = chr(65 + i)  # A, B, C, ...

        print(f"{letter}. {sentence_result.source_sentence}\n")

        if sentence_result.status == SentenceStatus.EXTRACTED:
            for j, claim in enumerate(sentence_result.claims, 1):
                print(f"   {j}. {claim.text}")
            print()
        elif sentence_result.status == SentenceStatus.NO_VERIFIABLE_CLAIMS:
            reason = sentence_result.metadata.get('reason', 'Unknown')
            print(f"   ❌ No verifiable claims: {reason}\n")
        elif sentence_result.status == SentenceStatus.CANNOT_DISAMBIGUATE:
            explanation = sentence_result.metadata.get('ambiguity_explanation', 'Unknown')
            print(f"   ⚠️  Cannot disambiguate: {explanation}\n")
        else:
            error = sentence_result.metadata.get('error', 'Unknown')
            print(f"   🔴 Error: {error}\n")

    # Print summary statistics
    stats = result.get_statistics_summary()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total sentences: {stats['total_sentences']}")
    print(f"Total claims extracted: {stats['total_claims']}")
    print(f"Success rate: {stats['extracted']}/{stats['total_sentences']} sentences")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY=sk-...")
        sys.exit(1)

    main()
