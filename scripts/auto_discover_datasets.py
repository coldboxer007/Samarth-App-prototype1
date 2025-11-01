"""Script to automatically discover and ingest datasets from data.gov.in."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.catalog.dataset_discovery import DatasetDiscovery
from src.app import SamarthApp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Discover and ingest datasets automatically."""
    logger.info("=" * 60)
    logger.info("Automatic Dataset Discovery")
    logger.info("=" * 60)

    # Initialize discovery
    discovery = DatasetDiscovery()

    # Discover datasets
    logger.info("\nStep 1: Discovering datasets from data.gov.in...")
    discovered = discovery.discover_all_datasets()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Discovery Summary")
    logger.info("=" * 60)
    logger.info(f"Climate datasets found: {len(discovered['climate'])}")
    logger.info(f"Agriculture datasets found: {len(discovered['agriculture'])}")

    # Display discovered datasets
    logger.info("\n📊 Climate Datasets:")
    for ds in discovered['climate']:
        logger.info(f"  - {ds.name}")
        logger.info(f"    Resource ID: {ds.resource_id}")
        logger.info(f"    Publisher: {ds.publisher}")

    logger.info("\n🌾 Agriculture Datasets:")
    for ds in discovered['agriculture']:
        logger.info(f"  - {ds.name}")
        logger.info(f"    Resource ID: {ds.resource_id}")
        logger.info(f"    Publisher: {ds.publisher}")

    logger.info("\n" + "=" * 60)
    logger.info("Dataset discovery complete!")
    logger.info("Datasets have been added to the catalog.")
    logger.info("\nTo load data, use:")
    logger.info("  python scripts/ingest_sample_data.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
