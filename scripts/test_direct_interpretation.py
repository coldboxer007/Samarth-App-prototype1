"""Test script for direct LLM interpretation approach."""

import sys
sys.path.append('.')

from src.app_direct import SamarthDirectApp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_simple_question():
    """Test with a simple question."""
    app = SamarthDirectApp()

    question = "What is the average rainfall in Maharashtra?"

    print("\n" + "="*80)
    print("TEST: Simple Question - Direct Interpretation")
    print("="*80)
    print(f"Question: {question}\n")

    result = app.answer_question(question, auto_discover=True)

    print("-"*80)
    print("ANSWER:")
    print("-"*80)
    print(result['answer'])

    print("\n" + "-"*80)
    print("DATASETS USED:")
    print("-"*80)
    for ds in result['datasets_used']:
        print(f"  - {ds}")

    print("\n" + "-"*80)
    print(f"Discovered new datasets: {result['discovered_new']}")
    print("="*80)

    return result


def test_multi_state_comparison():
    """Test Question 1: Multi-state comparison."""
    app = SamarthDirectApp()

    question = ("Compare the average annual rainfall in Maharashtra and Punjab for the last 5 years. "
                "In parallel, list the top 3 most produced crops (by volume) in each state during "
                "the same period, citing all data sources.")

    print("\n" + "="*80)
    print("TEST: Multi-State Rainfall + Top Crops - Direct Interpretation")
    print("="*80)
    print(f"Question: {question}\n")

    result = app.answer_question(
        question,
        auto_discover=True,
        max_datasets=10,  # Use more datasets for complex question
        max_rows_per_dataset=500  # Limit rows per dataset
    )

    print("-"*80)
    print("ANSWER:")
    print("-"*80)
    print(result['answer'])

    print("\n" + "-"*80)
    print("DATASETS USED:")
    print("-"*80)
    for ds in result['datasets_used']:
        print(f"  - {ds}")

    print("\n" + "-"*80)
    print(f"Discovered new datasets: {result['discovered_new']}")
    print("="*80)

    return result


def test_district_extremes():
    """Test Question 2: District extremes."""
    app = SamarthDirectApp()

    question = ("Identify the district in Maharashtra with the highest production of Rice in the "
                "most recent year and compare with the district with the lowest production of Rice "
                "in Punjab.")

    print("\n" + "="*80)
    print("TEST: District Extremes - Direct Interpretation")
    print("="*80)
    print(f"Question: {question}\n")

    result = app.answer_question(question, auto_discover=True)

    print("-"*80)
    print("ANSWER:")
    print("-"*80)
    print(result['answer'])

    print("\n" + "-"*80)
    print("DATASETS USED:")
    print("-"*80)
    for ds in result['datasets_used']:
        print(f"  - {ds}")

    print("\n" + "-"*80)
    print(f"Discovered new datasets: {result['discovered_new']}")
    print("="*80)

    return result


def test_correlation_analysis():
    """Test Question 3: Correlation analysis."""
    app = SamarthDirectApp()

    question = ("Analyze the production trend of Rice in Western India over the last decade. "
                "Correlate this trend with the corresponding climate data and provide a summary "
                "of the apparent impact.")

    print("\n" + "="*80)
    print("TEST: Decade-Long Trend + Correlation - Direct Interpretation")
    print("="*80)
    print(f"Question: {question}\n")

    result = app.answer_question(
        question,
        auto_discover=True,
        max_datasets=10,
        max_rows_per_dataset=1000
    )

    print("-"*80)
    print("ANSWER:")
    print("-"*80)
    print(result['answer'])

    print("\n" + "-"*80)
    print("DATASETS USED:")
    print("-"*80)
    for ds in result['datasets_used']:
        print(f"  - {ds}")

    print("\n" + "-"*80)
    print(f"Discovered new datasets: {result['discovered_new']}")
    print("="*80)

    return result


def test_catalog_stats():
    """Show catalog statistics."""
    app = SamarthDirectApp()
    stats = app.get_catalog_stats()

    print("\n" + "="*80)
    print("CATALOG STATISTICS")
    print("="*80)
    print(f"Total datasets: {stats['total_datasets']}")
    print(f"Climate datasets: {stats['climate_datasets']}")
    print(f"Agriculture datasets: {stats['agriculture_datasets']}")
    print("="*80)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTING DIRECT LLM INTERPRETATION APPROACH")
    print("="*80)
    print("\nThis approach:")
    print("  1. Discovers datasets based on question")
    print("  2. Fetches RAW data (no transformation)")
    print("  3. Sends raw data + question directly to LLM")
    print("  4. LLM interprets and answers")
    print("\nBenefits:")
    print("  - No transformation failures (100% dataset loading)")
    print("  - LLM handles messy data intelligently")
    print("  - More flexible than rigid schema mapping")
    print("="*80)

    # Show current catalog
    test_catalog_stats()

    # Run tests
    print("\n\n### TEST 1: Simple Question ###")
    try:
        test_simple_question()
        print("\n✅ Test 1 PASSED")
    except Exception as e:
        print(f"\n❌ Test 1 FAILED: {e}")

    print("\n\n### TEST 2: Multi-State Comparison ###")
    try:
        test_multi_state_comparison()
        print("\n✅ Test 2 PASSED")
    except Exception as e:
        print(f"\n❌ Test 2 FAILED: {e}")

    print("\n\n### TEST 3: District Extremes ###")
    try:
        test_district_extremes()
        print("\n✅ Test 3 PASSED")
    except Exception as e:
        print(f"\n❌ Test 3 FAILED: {e}")

    print("\n\n### TEST 4: Correlation Analysis ###")
    try:
        test_correlation_analysis()
        print("\n✅ Test 4 PASSED")
    except Exception as e:
        print(f"\n❌ Test 4 FAILED: {e}")

    print("\n\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
