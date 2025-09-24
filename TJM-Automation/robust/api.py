from typing import List, Dict, Optional
import time
import requests
import logging


class ApiClient:
    def __init__(self, base_url: str, timeout: int, logger: logging.Logger):
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logger

    def _request_with_retries(self, method: str, url: str, retries: int = 3, backoff: float = 0.75) -> Optional[requests.Response]:
        last_exc: Optional[Exception] = None
        for attempt in range(1, retries + 1):
            try:
                resp = requests.request(method, url, timeout=self.timeout)
                resp.raise_for_status()
                return resp
            except requests.exceptions.RequestException as exc:
                last_exc = exc
                self.logger.warning(f"API {method} {url} attempt {attempt}/{retries} failed: {exc}")
                time.sleep(backoff * attempt)
        self.logger.error(f"API {method} {url} failed after {retries} attempts: {last_exc}")
        return None

    def fetch_posts(self, limit: int) -> List[Dict]:
        response = self._request_with_retries('GET', self.base_url)
        if not response:
            return []
        try:
            data = response.json()
            if not isinstance(data, list):
                self.logger.error("API returned non-list payload; aborting.")
                return []
        except Exception as exc:
            self.logger.error(f"Failed to parse JSON: {exc}")
            return []

        validated: List[Dict] = []
        for item in data[:limit]:
            if isinstance(item, dict) and 'title' in item and 'body' in item:
                validated.append(item)
            else:
                self.logger.warning(f"Skipping malformed item: {str(item)[:120]}")
        return validated


