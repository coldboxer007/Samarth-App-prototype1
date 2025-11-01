"""Test script for real-time dataset discovery."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.catalog.dataset_discovery import DatasetDiscovery
from src.catalog.dataset_catalog import DatasetCatalog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_keyword_extraction():
    """Test keyword extraction from questions."""
    logger.info("=" * 60)
    logger.info("Test 1: Keyword Extraction")
    logger.info("=" * 60)

    discovery = DatasetDiscovery()

    test_questions = [
        "What is the average rainfall in Maharashtra?",
        "Show me crop production data for rice in Punjab",
        "How does temperature affect wheat yield?",
    ]

    for question in test_questions:
        logger.info(f"\nQuestion: {question}")
        keywords = discovery._extract_search_keywords(question)
        logger.info(f"Extracted keywords: {keywords}")


def test_realtime_discovery():
    """Test real-time discovery for a question."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 2: Real-time Dataset Discovery")
    logger.info("=" * 60)

    # Clear catalog first
    catalog = DatasetCatalog()
    logger.info(f"Datasets in catalog before: {len(catalog.list_datasets())}")

    # Test discovery for a question
    discovery = DatasetDiscovery()
    question = "What is the average rainfall in Maharashtra during monsoon season?"

    logger.info(f"\nQuestion: {question}")
    logger.info("Discovering datasets...")

    relevant_ids = discovery.discover_and_add_datasets_for_question(question)

    logger.info(f"\nRelevant dataset IDs: {relevant_ids}")
    logger.info(f"Datasets in catalog after: {len(catalog.list_datasets())}")

    # Show what was added
    logger.info("\nDatasets in catalog:")
    for ds in catalog.list_datasets():
        logger.info(f"  - {ds['name']} ({ds['dataset_id']}) - {ds['category']}")


def test_incremental_discovery():
    """Test that discovery doesn't re-add existing datasets."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 3: Incremental Discovery (No Duplicates)")
    logger.info("=" * 60)

    discovery = DatasetDiscovery()
    catalog = DatasetCatalog()

    initial_count = len(catalog.list_datasets())
    logger.info(f"Initial dataset count: {initial_count}")

    # Ask the same question again
    question = "What is the rainfall data for India?"
    logger.info(f"\nAsking same type of question again: {question}")

    relevant_ids = discovery.discover_and_add_datasets_for_question(question)

    final_count = len(catalog.list_datasets())
    logger.info(f"Final dataset count: {final_count}")
    logger.info(f"New datasets added: {final_count - initial_count}")


if __name__ == "__main__":
    try:
        test_keyword_extraction()
        test_realtime_discovery()
        test_incremental_discovery()

        logger.info("\n" + "=" * 60)
        logger.info("All tests completed!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
