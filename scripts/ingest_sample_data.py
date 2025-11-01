"""Script to ingest sample datasets from data.gov.in."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import SamarthApp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sample dataset configurations
# These are example resource IDs - you'll need to replace with actual ones from data.gov.in

SAMPLE_DATASETS = {
    "climate": [
        {
            "dataset_id": "imd_rainfall_2020",
            "resource_id": "YOUR_RESOURCE_ID_HERE",  # Replace with actual IMD resource ID
            "name": "IMD Rainfall Data 2020",
            "category": "climate",
            "format": "json"
        },
        # Add more climate datasets here
    ],
    "agriculture": [
        {
            "dataset_id": "crop_production_2020",
            "resource_id": "YOUR_RESOURCE_ID_HERE",  # Replace with actual crop production resource ID
            "name": "Crop Production Statistics 2020",
            "category": "agriculture",
            "format": "json"
        },
        # Add more agriculture datasets here
    ]
}


def main():
    """Ingest sample datasets."""
    app = SamarthApp()

    logger.info("Starting data ingestion...")

    # Ingest climate datasets
    logger.info("Ingesting climate datasets...")
    for dataset in SAMPLE_DATASETS["climate"]:
        try:
            logger.info(f"Loading: {dataset['name']}")
            app.load_dataset(
                dataset_id=dataset["dataset_id"],
                resource_id=dataset["resource_id"],
                name=dataset["name"],
                category=dataset["category"],
                format_type=dataset["format"]
            )
            logger.info(f"✓ Successfully loaded: {dataset['name']}")
        except Exception as e:
            logger.error(f"✗ Failed to load {dataset['name']}: {e}")

    # Ingest agriculture datasets
    logger.info("Ingesting agriculture datasets...")
    for dataset in SAMPLE_DATASETS["agriculture"]:
        try:
            logger.info(f"Loading: {dataset['name']}")
            app.load_dataset(
                dataset_id=dataset["dataset_id"],
                resource_id=dataset["resource_id"],
                name=dataset["name"],
                category=dataset["category"],
                format_type=dataset["format"]
            )
            logger.info(f"✓ Successfully loaded: {dataset['name']}")
        except Exception as e:
            logger.error(f"✗ Failed to load {dataset['name']}: {e}")

    logger.info("Data ingestion completed!")


if __name__ == "__main__":
    main()
