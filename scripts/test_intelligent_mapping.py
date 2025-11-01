"""Test intelligent schema mapping with real datasets."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import SamarthApp
from src.catalog.dataset_catalog import DatasetCatalog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_intelligent_mapping():
    """Test intelligent mapping with actual datasets."""
    logger.info("=" * 60)
    logger.info("Testing Intelligent Schema Mapping")
    logger.info("=" * 60)

    app = SamarthApp()
    catalog = DatasetCatalog()

    # Check what datasets we have
    datasets = catalog.list_datasets()
    logger.info(f"\nFound {len(datasets)} datasets in catalog")

    # Filter for climate datasets
    climate_datasets = [d for d in datasets if d['category'] == 'climate']
    logger.info(f"Climate datasets: {len(climate_datasets)}")

    if climate_datasets:
        # Test with first climate dataset
        test_dataset = climate_datasets[0]
        logger.info(f"\nTesting with: {test_dataset['name']}")
        logger.info(f"Resource ID: {test_dataset['dataset_id']}")

        # Check if already loaded
        if app._is_dataset_loaded(test_dataset['dataset_id']):
            logger.info("Dataset already loaded, checking database...")

            # Query the database to see what data is there
            query = f"SELECT * FROM climate_data WHERE source_id = '{test_dataset['dataset_id']}' LIMIT 5"
            try:
                result = app.db.conn.execute(query).fetchdf()
                logger.info(f"\nSample data in database ({len(result)} rows):")
                logger.info(result.to_string())
            except Exception as e:
                logger.error(f"Error querying database: {e}")
        else:
            logger.info("Dataset not yet loaded, loading now...")
            try:
                app._auto_load_dataset(test_dataset)
                logger.info("✅ Dataset loaded successfully!")

                # Check what was inserted
                query = f"SELECT * FROM climate_data WHERE source_id = '{test_dataset['dataset_id']}' LIMIT 5"
                result = app.db.conn.execute(query).fetchdf()
                logger.info(f"\nInserted data ({len(result)} rows):")
                logger.info(result.to_string())
            except Exception as e:
                logger.error(f"Error loading dataset: {e}")

    # Test with agriculture dataset
    agri_datasets = [d for d in datasets if d['category'] == 'agriculture']
    logger.info(f"\nAgriculture datasets: {len(agri_datasets)}")

    if agri_datasets:
        test_dataset = agri_datasets[0]
        logger.info(f"\nTesting with: {test_dataset['name']}")
        logger.info(f"Resource ID: {test_dataset['dataset_id']}")

        if not app._is_dataset_loaded(test_dataset['dataset_id']):
            logger.info("Dataset not yet loaded, loading now...")
            try:
                app._auto_load_dataset(test_dataset)
                logger.info("✅ Dataset loaded successfully!")

                # Check what was inserted
                query = f"SELECT * FROM agriculture_data WHERE source_id = '{test_dataset['dataset_id']}' LIMIT 5"
                result = app.db.conn.execute(query).fetchdf()
                logger.info(f"\nInserted data ({len(result)} rows):")
                logger.info(result.to_string())
            except Exception as e:
                logger.error(f"Error loading dataset: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("Testing Complete!")
    logger.info("=" * 60)


def test_question_flow():
    """Test the full question answering flow."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Full Question Flow")
    logger.info("=" * 60)

    app = SamarthApp()

    # Test question
    question = "What is the average rainfall in Maharashtra during monsoon season?"
    logger.info(f"\nQuestion: {question}")

    try:
        result = app.answer_question(question, auto_discover=True)

        logger.info(f"\n{'='*60}")
        logger.info("Results:")
        logger.info(f"{'='*60}")
        logger.info(f"\nDiscovered new datasets: {result.get('discovered_new', False)}")
        logger.info(f"\nData rows returned: {len(result['result_table'])}")

        if len(result['result_table']) > 0:
            logger.info("\nSample data:")
            logger.info(result['result_table'].head().to_string())

        logger.info(f"\nNarrative:")
        logger.info(result['narrative'])

        logger.info(f"\nSources used:")
        for source in result['sources']:
            logger.info(f"  - {source['name']} ({source['category']})")

    except Exception as e:
        logger.error(f"Error answering question: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        test_intelligent_mapping()
        test_question_flow()
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
