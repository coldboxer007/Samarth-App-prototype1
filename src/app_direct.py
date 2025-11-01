"""Direct interpretation app - LLM works with raw datasets."""

import pandas as pd
from typing import Dict, List
import logging

from src.catalog import DataGovClient, DatasetCatalog
from src.catalog.dataset_discovery import DatasetDiscovery
from src.adapters import AdapterFactory
from src.llm.data_interpreter import DataInterpreter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SamarthDirectApp:
    """
    Simplified Samarth app that gives raw datasets directly to LLM.

    Flow:
    1. User asks question
    2. Discover relevant datasets
    3. Fetch raw data (no transformation!)
    4. Send raw data + question to LLM
    5. LLM interprets and answers
    """

    def __init__(self):
        """Initialize components."""
        self.catalog = DatasetCatalog()
        self.discovery = DatasetDiscovery()
        self.data_client = DataGovClient()
        self.interpreter = DataInterpreter()

    def answer_question(
        self,
        question: str,
        auto_discover: bool = True,
        max_datasets: int = 5,
        max_rows_per_dataset: int = 1000
    ) -> Dict:
        """
        Answer a question using direct LLM interpretation of raw datasets.

        Args:
            question: User's natural language question
            auto_discover: Whether to discover new datasets
            max_datasets: Maximum number of datasets to send to LLM
            max_rows_per_dataset: Maximum rows per dataset to send to LLM

        Returns:
            Dict with 'question', 'answer', 'datasets_used', 'sources', 'discovered_new'
        """
        logger.info(f"Answering question with direct interpretation: {question}")

        try:
            # Step 1: Discover relevant datasets
            discovered_new = False
            relevant_dataset_ids = []

            if auto_discover:
                logger.info("Step 1: Discovering datasets...")
                relevant_dataset_ids = self.discovery.discover_and_add_datasets_for_question(question)

                if relevant_dataset_ids:
                    logger.info(f"Found {len(relevant_dataset_ids)} relevant datasets")
                    discovered_new = True
                else:
                    logger.warning("No datasets discovered, using existing catalog")

            # Step 2: Get all available datasets from catalog
            all_datasets = self.catalog.list_datasets()

            # Filter to relevant ones (prioritize discovered, then use others)
            if relevant_dataset_ids:
                dataset_list = [self.catalog.get_dataset(ds_id) for ds_id in relevant_dataset_ids[:max_datasets]]
            else:
                # Use first N from catalog
                dataset_list = all_datasets[:max_datasets]

            # Remove None values
            dataset_list = [ds for ds in dataset_list if ds is not None]

            if not dataset_list:
                return {
                    "question": question,
                    "answer": "No datasets available. Please add datasets to the catalog first.",
                    "datasets_used": [],
                    "sources": [],
                    "discovered_new": discovered_new
                }

            logger.info(f"Using {len(dataset_list)} datasets for interpretation")

            # Step 3: Fetch raw data for each dataset
            datasets_with_data = []
            for dataset in dataset_list:
                try:
                    raw_data = self._fetch_raw_data(dataset)
                    if raw_data is not None and not raw_data.empty:
                        datasets_with_data.append({
                            "name": dataset.get("name", "Unknown"),
                            "data": raw_data,
                            "metadata": dataset
                        })
                        logger.info(f"Loaded {len(raw_data)} rows from {dataset['name']}")
                except Exception as e:
                    logger.error(f"Failed to fetch data for {dataset.get('name')}: {e}")
                    continue

            if not datasets_with_data:
                return {
                    "question": question,
                    "answer": "Failed to fetch data from any dataset. Please check dataset availability.",
                    "datasets_used": [],
                    "sources": [],
                    "discovered_new": discovered_new
                }

            logger.info(f"Successfully loaded {len(datasets_with_data)} datasets with data")

            # Step 4: Send to LLM for direct interpretation
            logger.info("Step 4: Sending raw data to LLM for interpretation...")
            result = self.interpreter.interpret_and_answer(
                user_question=question,
                datasets=datasets_with_data,
                max_rows_per_dataset=max_rows_per_dataset,
                auto_filter=True  # Enable intelligent filtering
            )

            return {
                "question": question,
                "answer": result["answer"],
                "datasets_used": result["datasets_used"],
                "sources": result["sources"],
                "discovered_new": discovered_new
            }

        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise

    def _fetch_raw_data(self, dataset: Dict) -> pd.DataFrame:
        """
        Fetch raw data from data.gov.in without any transformation.

        Args:
            dataset: Dataset metadata dict

        Returns:
            Raw DataFrame as-is from the API
        """
        resource_id = dataset.get("resource_id")
        format_type = dataset.get("format", "json")

        if not resource_id:
            logger.warning(f"No resource_id for dataset {dataset.get('name')}")
            return None

        try:
            # Fetch data
            adapter = AdapterFactory.get_adapter(format_type)

            if format_type == "json":
                # Fetch all pages (with reasonable per-page limit)
                records = self.data_client.fetch_all_pages(resource_id, limit_per_page=1000)

                if not records:
                    logger.warning(f"No records fetched for {resource_id}")
                    return None

                # Convert to DataFrame - NO TRANSFORMATION
                df = adapter.read_and_cache(resource_id, records, format_type)

                return df
            else:
                logger.warning(f"Unsupported format: {format_type}")
                return None

        except Exception as e:
            logger.error(f"Error fetching raw data: {e}")
            return None

    def get_catalog_stats(self) -> Dict:
        """Get statistics about the dataset catalog."""
        datasets = self.catalog.list_datasets()

        stats = {
            "total_datasets": len(datasets),
            "climate_datasets": len([d for d in datasets if d.get("category") == "climate"]),
            "agriculture_datasets": len([d for d in datasets if d.get("category") == "agriculture"])
        }

        return stats
