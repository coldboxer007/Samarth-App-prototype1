"""Dataset catalog management for tracking available datasets."""

import duckdb
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from src.config import DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DatasetMetadata:
    """Metadata for a dataset resource."""
    dataset_id: str
    resource_id: str
    name: str
    publisher: str
    format: str
    category: str  # 'climate' or 'agriculture'
    sample_columns: str  # JSON string of column names
    last_updated: Optional[str] = None


class DatasetCatalog:
    """Manages the catalog of available datasets."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._initialize_catalog_table()

    def _initialize_catalog_table(self):
        """Create the catalog table if it doesn't exist."""
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dataset_catalog (
                    dataset_id VARCHAR PRIMARY KEY,
                    resource_id VARCHAR,
                    name VARCHAR,
                    publisher VARCHAR,
                    format VARCHAR,
                    category VARCHAR,
                    sample_columns VARCHAR,
                    last_updated TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("Dataset catalog table initialized")

    def add_dataset(self, metadata: DatasetMetadata):
        """Add or update a dataset in the catalog."""
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO dataset_catalog
                (dataset_id, resource_id, name, publisher, format, category, sample_columns, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (dataset_id)
                DO UPDATE SET
                    resource_id = EXCLUDED.resource_id,
                    name = EXCLUDED.name,
                    publisher = EXCLUDED.publisher,
                    format = EXCLUDED.format,
                    category = EXCLUDED.category,
                    sample_columns = EXCLUDED.sample_columns,
                    last_updated = EXCLUDED.last_updated
            """, [
                metadata.dataset_id,
                metadata.resource_id,
                metadata.name,
                metadata.publisher,
                metadata.format,
                metadata.category,
                metadata.sample_columns,
                metadata.last_updated
            ])
            logger.info(f"Added/updated dataset: {metadata.dataset_id}")

    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """Retrieve a dataset from the catalog."""
        with duckdb.connect(self.db_path) as conn:
            result = conn.execute(
                "SELECT * FROM dataset_catalog WHERE dataset_id = ?",
                [dataset_id]
            ).fetchone()

            if result:
                columns = [desc[0] for desc in conn.description]
                return dict(zip(columns, result))
            return None

    def list_datasets(self, category: Optional[str] = None) -> List[Dict]:
        """List all datasets in the catalog."""
        with duckdb.connect(self.db_path) as conn:
            if category:
                result = conn.execute(
                    "SELECT * FROM dataset_catalog WHERE category = ?",
                    [category]
                ).fetchall()
            else:
                result = conn.execute(
                    "SELECT * FROM dataset_catalog"
                ).fetchall()

            columns = [desc[0] for desc in conn.description]
            return [dict(zip(columns, row)) for row in result]

    def get_resource_id(self, dataset_id: str) -> Optional[str]:
        """Get the resource ID for a dataset."""
        dataset = self.get_dataset(dataset_id)
        return dataset["resource_id"] if dataset else None
