import logging
from typing import List, Dict
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import (
    RatelimitException,
    TimeoutException,
    DuckDuckGoSearchException
)

logger = logging.getLogger(__name__)

class DuckDuckGoAPI:
    def __init__(self):
        self.ddgs = DDGS()
    
    async def search(self, query: str) -> List[Dict]:
        logger.debug(f"Searching for: {query}")
        try:
            results = self.ddgs.text(
                f"top 10 {query}",
                region='wt-wt',
                safesearch='moderate',
                max_results=10
            )
            return self._format_results(results)
        except (RatelimitException, TimeoutException) as e:
            logger.error(f"Search error: {str(e)}")
            raise SearchError(f"Search API error: {str(e)}")
        except DuckDuckGoSearchException as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def _format_results(self, data: list) -> List[Dict]:
        return [{
            "title": result.get("title", ""),
            "snippet": result.get("body", ""),
            "link": result.get("href", ""),
            "source": self._extract_domain(result.get("href", "")),
            "category": ""  # Not available in basic text search
        } for result in data]

    def _extract_domain(self, url: str) -> str:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")

class SearchError(Exception):
    """Exception raised for search-related errors."""
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

async def web_search(query: str) -> List[Dict[str, str]]:
    """Perform search using duckduckgo-search library"""
    api = DuckDuckGoAPI()
    return await api.search(query) 