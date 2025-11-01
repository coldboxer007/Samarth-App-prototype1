"""Script to test the Samarth system with sample data."""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import SamarthApp
from src.database import CanonicalDatabase
from src.catalog import DatasetMetadata, DatasetCatalog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_climate_data():
    """Create sample climate data for testing."""
    data = {
        'year': [2018, 2019, 2020, 2021, 2022] * 3,
        'state_name': ['Maharashtra'] * 5 + ['Karnataka'] * 5 + ['Punjab'] * 5,
        'state_code': ['MH'] * 5 + ['KA'] * 5 + ['PB'] * 5,
        'rainfall_mm': [800, 850, 820, 890, 910, 900, 920, 880, 950, 960, 600, 620, 590, 650, 640],
        'temperature_celsius': [28, 29, 28.5, 29.2, 29.5, 26, 26.5, 26.2, 27, 27.5, 24, 24.5, 24.2, 25, 25.5],
        'month': [None] * 15,
        'district_code': [None] * 15,
        'district_name': [None] * 15,
        'source_id': ['sample_climate_001'] * 15
    }
    return pd.DataFrame(data)


def create_sample_agriculture_data():
    """Create sample agriculture data for testing."""
    data = {
        'year': [2018, 2019, 2020, 2021, 2022] * 6,
        'state_name': ['Maharashtra'] * 10 + ['Karnataka'] * 10 + ['Punjab'] * 10,
        'state_code': ['MH'] * 10 + ['KA'] * 10 + ['PB'] * 10,
        'crop_name': ['Rice', 'Wheat', 'Rice', 'Wheat', 'Rice'] * 2 +
                     ['Rice', 'Cotton', 'Rice', 'Cotton', 'Rice'] * 2 +
                     ['Wheat', 'Rice', 'Wheat', 'Rice', 'Wheat'] * 2,
        'production_tonnes': [
            # Maharashtra
            12000, 8000, 12500, 8200, 13000, 12200, 8100, 12800, 8300, 13200,
            # Karnataka
            10000, 5000, 10200, 5100, 10500, 10100, 5050, 10400, 5200, 10800,
            # Punjab
            15000, 9000, 15500, 9200, 16000, 15200, 9100, 15800, 9300, 16200
        ],
        'area_hectares': [
            # Maharashtra
            2000, 1600, 2050, 1620, 2100, 2020, 1610, 2080, 1630, 2120,
            # Karnataka
            1800, 1000, 1820, 1020, 1850, 1810, 1010, 1840, 1030, 1880,
            # Punjab
            2200, 1500, 2250, 1520, 2300, 2220, 1510, 2280, 1530, 2320
        ],
        'yield_kg_per_hectare': [None] * 30,
        'season': [None] * 30,
        'district_code': [None] * 30,
        'district_name': [None] * 30,
        'source_id': ['sample_agri_001'] * 30
    }
    df = pd.DataFrame(data)
    # Calculate yield
    df['yield_kg_per_hectare'] = (df['production_tonnes'] * 1000) / df['area_hectares']
    return df


def test_system():
    """Test the system with sample data."""
    logger.info("=" * 60)
    logger.info("Testing Samarth System")
    logger.info("=" * 60)

    # Initialize database
    db = CanonicalDatabase()
    catalog = DatasetCatalog()

    # Clear existing data
    logger.info("\n[1/5] Clearing existing data...")
    db.clear_all_data()

    # Create sample data
    logger.info("\n[2/5] Creating sample data...")
    climate_df = create_sample_climate_data()
    agri_df = create_sample_agriculture_data()
    logger.info(f"  - Created {len(climate_df)} climate records")
    logger.info(f"  - Created {len(agri_df)} agriculture records")

    # Load data into database
    logger.info("\n[3/5] Loading data into database...")
    db.insert_climate_data(climate_df)
    db.insert_agriculture_data(agri_df)

    # Add to catalog
    logger.info("\n[4/5] Adding to catalog...")
    catalog.add_dataset(DatasetMetadata(
        dataset_id="sample_climate_001",
        resource_id="sample_climate_001",
        name="Sample Climate Data",
        publisher="Test",
        format="json",
        category="climate",
        sample_columns="year,state_name,rainfall_mm,temperature_celsius"
    ))
    catalog.add_dataset(DatasetMetadata(
        dataset_id="sample_agri_001",
        resource_id="sample_agri_001",
        name="Sample Agriculture Data",
        publisher="Test",
        format="json",
        category="agriculture",
        sample_columns="year,state_name,crop_name,production_tonnes,area_hectares"
    ))

    # Test queries
    logger.info("\n[5/5] Testing queries...")
    app = SamarthApp()

    test_questions = [
        "What are the top crops in Maharashtra?",
        "Show me rainfall trends in Punjab",
        "How has rainfall affected rice production in Karnataka?"
    ]

    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n--- Test Question {i} ---")
        logger.info(f"Q: {question}")

        try:
            result = app.answer_question(question)
            logger.info(f"✓ Query successful!")
            logger.info(f"  Rows returned: {len(result['result_table'])}")
            logger.info(f"  Sources used: {len(result['sources'])}")
            logger.info(f"\nNarrative Preview:")
            logger.info(result['narrative'][:200] + "...")

        except Exception as e:
            logger.error(f"✗ Query failed: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("Testing Complete!")
    logger.info("=" * 60)
    logger.info("\nYou can now run: streamlit run streamlit_app.py")


if __name__ == "__main__":
    test_system()
