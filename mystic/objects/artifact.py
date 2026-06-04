"""Scraper and parser for Lord of the Mysteries Sealed Artifacts"""

import os
import re
import requests
import bs4
from mystic.helpers.exceptions import NotFoundError
import mystic.helpers as helpers

API_URL = "https://lordofthemysteries.fandom.com/api.php"
REQUEST_TIMEOUT = 10


class SealedArtifact:
    """Represents a Sealed Artifact in Lord of the Mysteries."""

    def __init__(self, name: str):
        """
        Initializes a SealedArtifact object.

        Parameters:
        - name (str): The name of the artifact.

        Raises:
        - NotFoundError: If the artifact is not found.
        """
        # Clean and format the artifact name
        self.url_name = helpers.misc.format_name(name)
        self.url = "https://lordofthemysteries.fandom.com/wiki/" + self.url_name

        # Handle persistent caching
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cache_dir = os.path.join(project_dir, ".cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{self.url_name}.html")

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
                raise NotFoundError(f"Network error while looking up '{name}': {e}")

            if response.status_code != 200:
                raise NotFoundError(f"Artifact '{name}' not found (HTTP {response.status_code}).")

            try:
                res_data = response.json()
            except ValueError:
                raise NotFoundError(f"Invalid API response format for '{name}'.")

            if "error" in res_data:
                raise NotFoundError(f"Artifact '{name}' not found on the wiki.")

            html_content = res_data["parse"]["text"]["*"]

            # Save to local cache
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
            except Exception as e:
                print(f"Warning: Failed to write cache for {self.url_name}: {e}")

        self.parsed = bs4.BeautifulSoup(html_content, "html.parser")

        # Parse Name
        title_element = self.parsed.find("h2", class_="pi-title")
        self.name = title_element.text.strip() if title_element else self.url_name.replace("_", " ")

        # Parse Infobox Key-Value pairs
        self.infobox_data = {}
        infobox = self.parsed.find("aside", class_="portable-infobox")
        if infobox:
            for item in infobox.find_all("div", class_="pi-item"):
                label = item.find("h3", class_="pi-data-label")
                value = item.find("div", class_="pi-data-value")
                if label and value:
                    val_text = value.text.strip().replace("[Click the toggle]", "").strip()
                    val_text = re.sub(r'\[\d+\]', '', val_text)  # Strip references
                    self.infobox_data[label.text.strip()] = val_text

        # Extract specific infobox properties
        self.chinese_name = self.infobox_data.get("Chinese", "Unknown")
        self.type = self.infobox_data.get("Type", "Sealed Artifact")
        self.appearance = self.infobox_data.get("Appearance", "Unknown")
        self.status = self.infobox_data.get("Status", "Unknown")
        self.latest_possessor = self.infobox_data.get("Latest Possessor(s)", "Unknown")
        self.former_possessors = self.infobox_data.get("Former Possessor(s)", "Unknown")
        self.corresponding_pathway = self.infobox_data.get("Corresponding Pathway(s)", "Unknown")
        self.power = self.infobox_data.get("Power", "Unknown")
        self.downside = self.infobox_data.get("Downside", "Unknown")

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
            text = p.text.strip()
            # Clean and filter paragraphs
            if text and len(text) > 30 and not text.startswith("Sealed Artifact"):
                cleaned_text = re.sub(r'\[\d+\]', '', text)
                overview_list.append(cleaned_text)
            if len(overview_list) >= 2:
                break
        self.overview = "\n\n".join(overview_list)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
