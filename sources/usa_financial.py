# coding=utf-8

"""
USA Financial Market News Sources
Supports: Yahoo Finance, Finviz, MarketWatch, Seeking Alpha, Benzinga
"""

import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

import requests


class FinancialNewsFetcher:
    """Base class for financial news fetchers"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }

    def _get_proxies(self) -> Optional[Dict]:
        """Get proxy configuration"""
        if self.proxy_url:
            return {"http": self.proxy_url, "https": self.proxy_url}
        return None

    def _make_request(
        self, url: str, headers: Optional[Dict] = None, timeout: int = 10
    ) -> Optional[requests.Response]:
        """Make HTTP request with error handling"""
        try:
            request_headers = self.headers.copy()
            if headers:
                request_headers.update(headers)

            response = requests.get(
                url,
                headers=request_headers,
                proxies=self._get_proxies(),
                timeout=timeout,
            )
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Request failed for {url}: {e}")
            return None

    def _extract_ticker(self, text: str) -> Optional[str]:
        """Extract stock ticker from text (e.g., $AAPL, TSLA, (NASDAQ:TSLA))"""
        # Match $TICKER format
        match = re.search(r"\$([A-Z]{1,5})\b", text)
        if match:
            return match.group(1)

        # Match (EXCHANGE:TICKER) format
        match = re.search(r"\((?:NYSE|NASDAQ|AMEX):([A-Z]{1,5})\)", text)
        if match:
            return match.group(1)

        # Match standalone ticker (be conservative to avoid false positives)
        match = re.search(r"\b([A-Z]{2,5})\b", text)
        if match and len(match.group(1)) <= 5:
            return match.group(1)

        return None

    def _normalize_data(
        self,
        title: str,
        url: str,
        rank: int = 1,
        ticker: Optional[str] = None,
        source: str = "",
        category: str = "",
        timestamp: Optional[str] = None,
    ) -> Dict:
        """Normalize financial news data to standard format"""
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": title,
            "url": url,
            "mobileUrl": url,
            "rank": rank,
            "ticker": ticker or "",
            "company_name": "",
            "price_change": "",
            "timestamp": timestamp,
            "source": source,
            "category": category,
        }


class YahooFinanceFetcher(FinancialNewsFetcher):
    """Yahoo Finance - Trending Tickers and Market News"""

    def __init__(self, config: Dict, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.config = config
        self.enabled = config.get("enabled", True)
        self.data_types = config.get("config", {}).get(
            "data_type", ["trending", "gainers", "losers"]
        )

    def fetch(self) -> Tuple[Optional[str], str, str]:
        """Fetch Yahoo Finance trending data"""
        if not self.enabled:
            print("Yahoo Finance is disabled")
            return None, "yahoo-finance-trending", "Yahoo Finance Trending"

        try:
            # Use Yahoo Finance RSS feeds
            items = []

            # Trending stocks news
            if "trending" in self.data_types:
                trending_url = "https://finance.yahoo.com/rss/topfinstories"
                items.extend(self._fetch_rss(trending_url, "trending"))

            # Top gainers/losers news
            if "gainers" in self.data_types or "losers" in self.data_types:
                market_url = "https://finance.yahoo.com/rss/headline"
                items.extend(self._fetch_rss(market_url, "market"))

            if not items:
                print("No Yahoo Finance data fetched")
                return None, "yahoo-finance-trending", "Yahoo Finance Trending"

            # Convert to expected format
            result = {"status": "success", "items": items[:50]}  # Limit to 50 items
            return (
                json.dumps(result),
                "yahoo-finance-trending",
                "Yahoo Finance Trending",
            )

        except Exception as e:
            print(f"Yahoo Finance fetch error: {e}")
            return None, "yahoo-finance-trending", "Yahoo Finance Trending"

    def _fetch_rss(self, url: str, category: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        items = []
        try:
            response = self._make_request(url)
            if not response:
                return items

            root = ET.fromstring(response.content)
            for idx, item in enumerate(root.findall(".//item"), 1):
                title_elem = item.find("title")
                link_elem = item.find("link")
                pub_date_elem = item.find("pubDate")

                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    link = link_elem.text or ""
                    ticker = self._extract_ticker(title)

                    timestamp = ""
                    if pub_date_elem is not None and pub_date_elem.text:
                        timestamp = pub_date_elem.text

                    normalized = self._normalize_data(
                        title=title,
                        url=link,
                        rank=idx,
                        ticker=ticker,
                        source="Yahoo Finance",
                        category=category,
                        timestamp=timestamp,
                    )
                    items.append(normalized)

        except Exception as e:
            print(f"RSS parsing error for {url}: {e}")

        return items


class FinvizFetcher(FinancialNewsFetcher):
    """Finviz - Market News Aggregator"""

    def __init__(self, config: Dict, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.config = config
        self.enabled = config.get("enabled", True)
        self.filters = config.get("config", {}).get("filters", ["news"])

    def fetch(self) -> Tuple[Optional[str], str, str]:
        """Fetch Finviz market news"""
        if not self.enabled:
            print("Finviz is disabled")
            return None, "finviz-news", "Finviz Market News"

        try:
            # Finviz news RSS feed
            rss_url = "https://finviz.com/news.ashx?v=3"
            items = self._fetch_html_news(rss_url)

            if not items:
                print("No Finviz data fetched")
                return None, "finviz-news", "Finviz Market News"

            result = {"status": "success", "items": items[:50]}
            return json.dumps(result), "finviz-news", "Finviz Market News"

        except Exception as e:
            print(f"Finviz fetch error: {e}")
            return None, "finviz-news", "Finviz Market News"

    def _fetch_html_news(self, url: str) -> List[Dict]:
        """Fetch news from Finviz HTML page"""
        items = []
        try:
            response = self._make_request(url)
            if not response:
                return items

            # Parse HTML for news items
            # Finviz typically shows news in a simple format
            # This is a simplified parser - actual implementation may need adjustment
            text = response.text
            
            # Look for news links in the HTML
            # Pattern: <a href="..." class="nn-tab-link">Title</a>
            pattern = r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*nn-tab-link[^"]*"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, text)
            
            for idx, (link, title) in enumerate(matches[:50], 1):
                if not link.startswith("http"):
                    link = "https://finviz.com" + link
                
                ticker = self._extract_ticker(title)
                normalized = self._normalize_data(
                    title=title.strip(),
                    url=link,
                    rank=idx,
                    ticker=ticker,
                    source="Finviz",
                    category="news",
                )
                items.append(normalized)

        except Exception as e:
            print(f"Finviz HTML parsing error: {e}")

        return items


class MarketWatchFetcher(FinancialNewsFetcher):
    """MarketWatch - Breaking Market News"""

    def __init__(self, config: Dict, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.config = config
        self.enabled = config.get("enabled", True)
        self.sections = config.get("config", {}).get(
            "sections", ["breaking", "market_pulse"]
        )

    def fetch(self) -> Tuple[Optional[str], str, str]:
        """Fetch MarketWatch news"""
        if not self.enabled:
            print("MarketWatch is disabled")
            return None, "marketwatch", "MarketWatch Breaking News"

        try:
            items = []

            # MarketWatch RSS feeds
            if "breaking" in self.sections:
                breaking_url = "https://www.marketwatch.com/rss/topstories"
                items.extend(self._fetch_rss(breaking_url, "breaking"))

            if "market_pulse" in self.sections:
                market_url = "https://www.marketwatch.com/rss/marketpulse"
                items.extend(self._fetch_rss(market_url, "market_pulse"))

            if not items:
                print("No MarketWatch data fetched")
                return None, "marketwatch", "MarketWatch Breaking News"

            result = {"status": "success", "items": items[:50]}
            return json.dumps(result), "marketwatch", "MarketWatch Breaking News"

        except Exception as e:
            print(f"MarketWatch fetch error: {e}")
            return None, "marketwatch", "MarketWatch Breaking News"

    def _fetch_rss(self, url: str, category: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        items = []
        try:
            response = self._make_request(url)
            if not response:
                return items

            root = ET.fromstring(response.content)
            for idx, item in enumerate(root.findall(".//item"), 1):
                title_elem = item.find("title")
                link_elem = item.find("link")
                pub_date_elem = item.find("pubDate")

                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    link = link_elem.text or ""
                    ticker = self._extract_ticker(title)

                    timestamp = ""
                    if pub_date_elem is not None and pub_date_elem.text:
                        timestamp = pub_date_elem.text

                    normalized = self._normalize_data(
                        title=title,
                        url=link,
                        rank=idx,
                        ticker=ticker,
                        source="MarketWatch",
                        category=category,
                        timestamp=timestamp,
                    )
                    items.append(normalized)

        except Exception as e:
            print(f"MarketWatch RSS parsing error: {e}")

        return items


class SeekingAlphaFetcher(FinancialNewsFetcher):
    """Seeking Alpha - Market News and Analysis"""

    def __init__(self, config: Dict, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.config = config
        self.enabled = config.get("enabled", True)
        self.topics = config.get("config", {}).get("topics", ["market_news", "earnings"])

    def fetch(self) -> Tuple[Optional[str], str, str]:
        """Fetch Seeking Alpha news"""
        if not self.enabled:
            print("Seeking Alpha is disabled")
            return None, "seeking-alpha", "Seeking Alpha Market News"

        try:
            items = []

            # Seeking Alpha RSS feeds
            if "market_news" in self.topics:
                market_url = "https://seekingalpha.com/feed.xml"
                items.extend(self._fetch_rss(market_url, "market_news"))

            if "wall_street_breakfast" in self.topics:
                wsb_url = "https://seekingalpha.com/tag/wall-street-breakfast.xml"
                items.extend(self._fetch_rss(wsb_url, "wall_street_breakfast"))

            if not items:
                print("No Seeking Alpha data fetched")
                return None, "seeking-alpha", "Seeking Alpha Market News"

            result = {"status": "success", "items": items[:50]}
            return json.dumps(result), "seeking-alpha", "Seeking Alpha Market News"

        except Exception as e:
            print(f"Seeking Alpha fetch error: {e}")
            return None, "seeking-alpha", "Seeking Alpha Market News"

    def _fetch_rss(self, url: str, category: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        items = []
        try:
            response = self._make_request(url)
            if not response:
                return items

            root = ET.fromstring(response.content)
            
            # Handle Atom feeds
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall(".//atom:entry", ns)
            
            if not entries:
                # Try RSS format
                entries = root.findall(".//item")
                
                for idx, item in enumerate(entries, 1):
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_date_elem = item.find("pubDate")

                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text or ""
                        link = link_elem.text or ""
                        ticker = self._extract_ticker(title)

                        timestamp = ""
                        if pub_date_elem is not None and pub_date_elem.text:
                            timestamp = pub_date_elem.text

                        normalized = self._normalize_data(
                            title=title,
                            url=link,
                            rank=idx,
                            ticker=ticker,
                            source="Seeking Alpha",
                            category=category,
                            timestamp=timestamp,
                        )
                        items.append(normalized)
            else:
                # Parse Atom format
                for idx, entry in enumerate(entries, 1):
                    title_elem = entry.find("atom:title", ns)
                    link_elem = entry.find("atom:link[@rel='alternate']", ns)
                    updated_elem = entry.find("atom:updated", ns)

                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text or ""
                        link = link_elem.get("href", "")
                        ticker = self._extract_ticker(title)

                        timestamp = ""
                        if updated_elem is not None and updated_elem.text:
                            timestamp = updated_elem.text

                        normalized = self._normalize_data(
                            title=title,
                            url=link,
                            rank=idx,
                            ticker=ticker,
                            source="Seeking Alpha",
                            category=category,
                            timestamp=timestamp,
                        )
                        items.append(normalized)

        except Exception as e:
            print(f"Seeking Alpha RSS parsing error: {e}")

        return items


class BenzingaFetcher(FinancialNewsFetcher):
    """Benzinga - Real-time Financial News"""

    def __init__(self, config: Dict, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.config = config
        self.enabled = config.get("enabled", True)
        self.channels = config.get("config", {}).get(
            "channels", ["news", "analyst_ratings"]
        )

    def fetch(self) -> Tuple[Optional[str], str, str]:
        """Fetch Benzinga news"""
        if not self.enabled:
            print("Benzinga is disabled")
            return None, "benzinga", "Benzinga Real-time News"

        try:
            items = []

            # Benzinga RSS feed
            rss_url = "https://www.benzinga.com/feed"
            items.extend(self._fetch_rss(rss_url, "news"))

            if not items:
                print("No Benzinga data fetched")
                return None, "benzinga", "Benzinga Real-time News"

            result = {"status": "success", "items": items[:50]}
            return json.dumps(result), "benzinga", "Benzinga Real-time News"

        except Exception as e:
            print(f"Benzinga fetch error: {e}")
            return None, "benzinga", "Benzinga Real-time News"

    def _fetch_rss(self, url: str, category: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        items = []
        try:
            response = self._make_request(url)
            if not response:
                return items

            root = ET.fromstring(response.content)
            for idx, item in enumerate(root.findall(".//item"), 1):
                title_elem = item.find("title")
                link_elem = item.find("link")
                pub_date_elem = item.find("pubDate")

                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    link = link_elem.text or ""
                    ticker = self._extract_ticker(title)

                    timestamp = ""
                    if pub_date_elem is not None and pub_date_elem.text:
                        timestamp = pub_date_elem.text

                    normalized = self._normalize_data(
                        title=title,
                        url=link,
                        rank=idx,
                        ticker=ticker,
                        source="Benzinga",
                        category=category,
                        timestamp=timestamp,
                    )
                    items.append(normalized)

        except Exception as e:
            print(f"Benzinga RSS parsing error: {e}")

        return items


def create_financial_fetcher(
    platform_config: Dict, proxy_url: Optional[str] = None
) -> Optional[FinancialNewsFetcher]:
    """Factory function to create appropriate financial fetcher"""
    platform_id = platform_config.get("id", "")

    fetcher_map = {
        "yahoo-finance-trending": YahooFinanceFetcher,
        "finviz-news": FinvizFetcher,
        "marketwatch": MarketWatchFetcher,
        "seeking-alpha": SeekingAlphaFetcher,
        "benzinga": BenzingaFetcher,
    }

    fetcher_class = fetcher_map.get(platform_id)
    if fetcher_class:
        return fetcher_class(platform_config, proxy_url)

    return None


def is_financial_source(platform_id: str) -> bool:
    """Check if platform is a financial news source"""
    financial_sources = [
        "yahoo-finance-trending",
        "finviz-news",
        "marketwatch",
        "seeking-alpha",
        "benzinga",
    ]
    return platform_id in financial_sources
