"""Scraper and parser for general Lord of the Mysteries Wiki pages"""

import os
import re
import requests
import bs4
from mystic.helpers.exceptions import NotFoundError
import mystic.helpers as helpers

API_URL = "https://lordofthemysteries.fandom.com/api.php"
REQUEST_TIMEOUT = 10


class WikiPage:
    """Represents a general page on the Lord of the Mysteries Wiki."""

    def __init__(self, title: str):
        """
        Initializes a WikiPage object.

        Parameters:
        - title (str): The title of the page to lookup.

        Raises:
        - NotFoundError: If the page is not found.
        """
        self.url_name = helpers.misc.format_name(title)
        self.url = "https://lordofthemysteries.fandom.com/wiki/" + self.url_name

        # Handle persistent caching
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cache_dir = os.path.join(project_dir, ".cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{self.url_name}.html")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        html_content = None
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        else:
            params = {
                "action": "parse",
                "format": "json",
                "page": self.url_name,
                "prop": "text",
                "redirects": "true",
                "disableeditsection": "true"
            }
            headers = {
                "User-Agent": "ArrodesBot/1.0 (Discord Bot; contact: owner)"
            }
            try:
                response = requests.get(API_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
            except requests.exceptions.RequestException as e:
                raise NotFoundError(f"Network error while looking up '{title}': {e}")

            if response.status_code != 200:
                raise NotFoundError(f"Page '{title}' not found (HTTP {response.status_code}).")

            try:
                res_data = response.json()
            except ValueError:
                raise NotFoundError(f"Invalid API response format for '{title}'.")

            if "error" in res_data:
                raise NotFoundError(f"Page '{title}' not found on the wiki.")

            html_content = res_data["parse"]["text"]["*"]

            # Save to local cache
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
            except Exception as e:
                print(f"Warning: Failed to write cache for {self.url_name}: {e}")

        self.parsed = bs4.BeautifulSoup(html_content, "html.parser")

        # Parse Name/Title
        title_element = self.parsed.find("h2", class_="pi-title")
        if not title_element:
            title_element = self.parsed.find("h1", id="firstHeading")
        self.name = title_element.text.strip() if title_element else self.url_name.replace("_", " ")

        # Parse Infobox Key-Value pairs
        self.infobox_data = {}
        infobox = self.parsed.find("aside", class_="portable-infobox")
        if infobox:
            for item in infobox.find_all("div", class_="pi-item"):
                label = item.find("h3", class_="pi-data-label")
                value = item.find("div", class_="pi-data-value")
                if label and value:
                    val_text = helpers.misc.clean_text(value.text)
                    self.infobox_data[label.text.strip()] = val_text

        # Parse Official Image
        self.image = "No image found."
        try:
            collection = self.parsed.find("figure", class_="pi-item pi-image")
            if collection and collection.find("img"):
                self.image = collection.find("img")["src"]
        except Exception:
            pass

        # Parse Overview paragraphs
        paragraphs = self.parsed.find_all("p")
        overview_list = []
        for p in paragraphs:
            # Check if this paragraph is inside a table, poem, or infobox to avoid duplication
            if p.find_parent(class_="portable-infobox") or p.find_parent(class_="poem") or p.find_parent("table"):
                continue
            text = helpers.misc.clean_text(p.text)
            if text and len(text) > 30:
                overview_list.append(text)
            if len(overview_list) >= 2:
                break
        self.overview = "\n\n".join(overview_list)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
