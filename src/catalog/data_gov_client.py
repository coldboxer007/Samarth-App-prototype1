"""Client for interacting with data.gov.in API."""

import requests
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

from src.config import DATA_GOV_API_KEY, DATA_GOV_BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataGovClient:
    """Client for fetching datasets from data.gov.in."""

    def __init__(self, api_key: str = DATA_GOV_API_KEY):
        self.api_key = api_key
        self.base_url = DATA_GOV_BASE_URL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_resource(self, resource_id: str, limit: int = 10000, offset: int = 0) -> Dict:
        """
        Fetch data from a specific resource.

        Args:
            resource_id: The resource ID from data.gov.in
            limit: Number of records to fetch
            offset: Offset for pagination

        Returns:
            Dictionary containing the API response
        """
        url = f"{self.base_url}/{resource_id}"
        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": limit,
            "offset": offset
        }

        logger.info(f"Fetching resource {resource_id} (limit={limit}, offset={offset})")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        return response.json()

    def fetch_all_pages(self, resource_id: str, limit_per_page: int = 10000) -> List[Dict]:
        """
        Fetch all pages of data from a resource.

        Args:
            resource_id: The resource ID from data.gov.in
            limit_per_page: Number of records per page

        Returns:
            List of all records
        """
        all_records = []
        offset = 0

        while True:
            response = self.fetch_resource(resource_id, limit=limit_per_page, offset=offset)

            if "records" in response:
                records = response["records"]
                if not records:
                    break

                all_records.extend(records)
                logger.info(f"Fetched {len(records)} records (total: {len(all_records)})")

                # Check if we've fetched all records
                if len(records) < limit_per_page:
                    break

                offset += limit_per_page
            else:
                logger.warning(f"No 'records' key in response for resource {resource_id}")
                break

        logger.info(f"Total records fetched for {resource_id}: {len(all_records)}")
        return all_records
