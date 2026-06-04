"""Scraper and parser for Lord of the Mysteries Beyonder Pathways"""

import os
import re
import requests
import bs4
from mystic.helpers.exceptions import NotFoundError

API_URL = "https://lordofthemysteries.fandom.com/api.php"
REQUEST_TIMEOUT = 10

# 22 standard pathways and their common aliases
PATHWAY_ALIASES = {
    "fool": "Fool_Pathway",
    "seer": "Fool_Pathway",
    "door": "Door_Pathway",
    "apprentice": "Door_Pathway",
    "error": "Error_Pathway",
    "marauder": "Error_Pathway",
    "spectator": "Visionary_Pathway",
    "visionary": "Visionary_Pathway",
    "hanged": "Hanged_Man_Pathway",
    "hanged man": "Hanged_Man_Pathway",
    "secrets suppliant": "Hanged_Man_Pathway",
    "sun": "Sun_Pathway",
    "bard": "Sun_Pathway",
    "tyrant": "Tyrant_Pathway",
    "sailor": "Tyrant_Pathway",
    "white tower": "White_Tower_Pathway",
    "reader": "White_Tower_Pathway",
    "red priest": "Red_Priest_Pathway",
    "hunter": "Red_Priest_Pathway",
    "demoness": "Demoness_Pathway",
    "assassin": "Demoness_Pathway",
    "black emperor": "Black_Emperor_Pathway",
    "lawyer": "Black_Emperor_Pathway",
    "justiciar": "Justiciar_Pathway",
    "arbiter": "Justiciar_Pathway",
    "hermit": "Hermit_Pathway",
    "mystery pryer": "Hermit_Pathway",
    "paragon": "Paragon_Pathway",
    "savant": "Paragon_Pathway",
    "wheel of fortune": "Wheel_of_Fortune_Pathway",
    "wheel": "Wheel_of_Fortune_Pathway",
    "monster": "Wheel_of_Fortune_Pathway",
    "death": "Death_Pathway",
    "corpse collector": "Death_Pathway",
    "twilight giant": "Twilight_Giant_Pathway",
    "giant": "Twilight_Giant_Pathway",
    "warrior": "Twilight_Giant_Pathway",
    "darkness": "Darkness_Pathway",
    "sleepless": "Darkness_Pathway",
    "moon": "Moon_Pathway",
    "apothecary": "Moon_Pathway",
    "mother": "Mother_Pathway",
    "planter": "Mother_Pathway",
    "chained": "Chained_Pathway",
    "prisoner": "Chained_Pathway",
    "abyss": "Abyss_Pathway",
    "devil": "Abyss_Pathway",
    "criminal": "Abyss_Pathway",
}


class Pathway:
    """Represents a Beyonder Pathway in Lord of the Mysteries."""

    def __init__(self, name: str):
        """
        Initializes a Pathway object.

        Parameters:
        - name (str): The name/alias of the pathway.

        Raises:
        - NotFoundError: If the pathway is not found.
        """
        cleaned_name = name.strip().lower()
        if cleaned_name in PATHWAY_ALIASES:
            self.url_name = PATHWAY_ALIASES[cleaned_name]
        else:
            # Fallback to formatting
            words = [w.capitalize() for w in cleaned_name.replace("pathway", "").strip().split()]
            self.url_name = "_".join(words) + "_Pathway"

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
                raise NotFoundError(f"Pathway '{name}' not found (HTTP {response.status_code}).")

            try:
                res_data = response.json()
            except ValueError:
                raise NotFoundError(f"Invalid API response format for '{name}'.")

            if "error" in res_data:
                raise NotFoundError(f"Pathway '{name}' not found on the wiki.")

            html_content = res_data["parse"]["text"]["*"]

            # Save to local cache
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
            except Exception as e:
                print(f"Warning: Failed to write cache for {self.url_name}: {e}")

        self.parsed = bs4.BeautifulSoup(html_content, "html.parser")
        
        # Parse Title
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
                    val_text = re.sub(r'\[\d+\]', '', val_text)  # Strip reference brackets
                    self.infobox_data[label.text.strip()] = val_text

        # Extract specific infobox properties
        self.god = self.infobox_data.get("God", "Unknown")
        self.mythical_form = self.infobox_data.get("Mythical Form", "Unknown")
        self.sefirah = self.infobox_data.get("Sefirah", "Unknown")
        self.above_the_sequence = self.infobox_data.get("Above the Sequence", "Unknown")
        self.organizations = self.infobox_data.get("Related Organization(s)", "Unknown")

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
            if text and len(text) > 30 and not text.startswith("Mysteries Pathway"):
                cleaned_text = re.sub(r'\[\d+\]', '', text)
                overview_list.append(cleaned_text)
            if len(overview_list) >= 2:
                break
        self.overview = "\n\n".join(overview_list)

        # Parse Sequence Table
        self.sequences = []
        table = self.parsed.find("table")
        if table:
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    seq_num_text = tds[0].text.strip()
                    if seq_num_text.isdigit():
                        seq_name_raw = tds[1].text.strip()
                        # Clean up name: Split by '-' or ':' and take the first portion
                        seq_name = seq_name_raw.split(" - ")[0].split("-")[0].strip()
                        seq_name = re.sub(r'\[\d+\]', '', seq_name)
                        self.sequences.append((int(seq_num_text), seq_name))
            # Sort sequence from 9 to 0
            self.sequences.sort(key=lambda x: x[0], reverse=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
