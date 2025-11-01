"""Adapters for reading different data formats from data.gov.in."""

import pandas as pd
import requests
from pathlib import Path
from typing import Optional
import logging
import hashlib
import json

from src.config import PARQUET_CACHE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FormatAdapter:
    """Base class for format adapters."""

    def __init__(self):
        self.cache_dir = PARQUET_CACHE_DIR

    def _get_cache_path(self, resource_id: str) -> Path:
        """Get the cache file path for a resource."""
        return self.cache_dir / f"{resource_id}.parquet"

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to lowercase with underscores."""
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
        return df

    def read_and_cache(self, resource_id: str, data: any, source_format: str) -> pd.DataFrame:
        """Read data and cache as parquet."""
        raise NotImplementedError


class JSONAdapter(FormatAdapter):
    """Adapter for JSON format data."""

    def read_and_cache(self, resource_id: str, data: list, source_format: str = "json") -> pd.DataFrame:
        """
        Convert JSON records to DataFrame and cache.

        Args:
            resource_id: The resource ID
            data: List of records from API
            source_format: Format type

        Returns:
            Normalized DataFrame
        """
        cache_path = self._get_cache_path(resource_id)

        # Check if cache exists
        if cache_path.exists():
            logger.info(f"Loading from cache: {cache_path}")
            return pd.read_parquet(cache_path)

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Normalize columns
        df = self._normalize_columns(df)

        # Parse tab-separated values if detected
        df = self._parse_tab_separated_columns(df)

        # Add source tracking
        df['source_id'] = resource_id

        # Cache as parquet
        df.to_parquet(cache_path, index=False)
        logger.info(f"Cached {len(df)} records to {cache_path}")

        return df

    def _parse_tab_separated_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect and parse tab-separated values in columns.

        Some data.gov.in datasets have tab-separated values stored in single columns.
        This method detects such columns and expands them into proper columns.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with tab-separated values properly parsed
        """
        # Check each column for tab-separated values
        for col in df.columns:
            if col == 'source_id':
                continue

            # Check if column contains string values with tabs
            if df[col].dtype == 'object':
                # Sample first non-null value
                sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else None

                if sample_val and isinstance(sample_val, str) and '\t' in sample_val:
                    logger.info(f"Detected tab-separated values in column: {col}")

                    # Split the column name on underscores to get individual column names
                    # The column name often contains the actual column names separated by underscores
                    potential_col_names = col.split('_')

                    # Split each row on tabs
                    split_data = df[col].str.split('\t', expand=True)

                    # Assign column names - handle duplicates intelligently
                    if len(potential_col_names) == split_data.shape[1]:
                        # Remove empty strings and handle duplicates
                        cleaned_names = []
                        seen = {}
                        for i, name in enumerate(potential_col_names):
                            if not name or name in ['', ' ']:
                                name = f'col_{i}'
                            # Handle duplicates by appending suffix
                            if name in seen:
                                seen[name] += 1
                                name = f'{name}_{seen[name]}'
                            else:
                                seen[name] = 0
                            cleaned_names.append(name)
                        split_data.columns = cleaned_names
                    else:
                        # Use numbered columns
                        split_data.columns = [potential_col_names[i] if i < len(potential_col_names)
                                             else f'col_{i}' for i in range(split_data.shape[1])]

                    # Remove the original column and add the split columns
                    df = df.drop(columns=[col])
                    df = pd.concat([split_data, df], axis=1)

                    logger.info(f"Expanded into {split_data.shape[1]} columns")
                    break  # Only process one tab-separated column per dataset

        return df


class CSVAdapter(FormatAdapter):
    """Adapter for CSV format data."""

    def read_and_cache(self, resource_id: str, url: str, source_format: str = "csv") -> pd.DataFrame:
        """
        Download CSV and cache.

        Args:
            resource_id: The resource ID
            url: URL to CSV file
            source_format: Format type

        Returns:
            Normalized DataFrame
        """
        cache_path = self._get_cache_path(resource_id)

        # Check if cache exists
        if cache_path.exists():
            logger.info(f"Loading from cache: {cache_path}")
            return pd.read_parquet(cache_path)

        # Download and read CSV
        logger.info(f"Downloading CSV from {url}")
        df = pd.read_csv(url)

        # Normalize columns
        df = self._normalize_columns(df)

        # Add source tracking
        df['source_id'] = resource_id

        # Cache as parquet
        df.to_parquet(cache_path, index=False)
        logger.info(f"Cached {len(df)} records to {cache_path}")

        return df


class ExcelAdapter(FormatAdapter):
    """Adapter for Excel/XLSX format data."""

    def read_and_cache(self, resource_id: str, url: str, source_format: str = "xlsx") -> pd.DataFrame:
        """
        Download Excel file and cache.

        Args:
            resource_id: The resource ID
            url: URL to Excel file
            source_format: Format type

        Returns:
            Normalized DataFrame
        """
        cache_path = self._get_cache_path(resource_id)

        # Check if cache exists
        if cache_path.exists():
            logger.info(f"Loading from cache: {cache_path}")
            return pd.read_parquet(cache_path)

        # Download and read Excel
        logger.info(f"Downloading Excel from {url}")
        df = pd.read_excel(url)

        # Normalize columns
        df = self._normalize_columns(df)

        # Add source tracking
        df['source_id'] = resource_id

        # Cache as parquet
        df.to_parquet(cache_path, index=False)
        logger.info(f"Cached {len(df)} records to {cache_path}")

        return df


class AdapterFactory:
    """Factory for creating appropriate adapters."""

    @staticmethod
    def get_adapter(format_type: str) -> FormatAdapter:
        """Get the appropriate adapter for a format type."""
        format_type = format_type.lower()

        if format_type in ["json", "api"]:
            return JSONAdapter()
        elif format_type == "csv":
            return CSVAdapter()
        elif format_type in ["xlsx", "xls", "excel"]:
            return ExcelAdapter()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
