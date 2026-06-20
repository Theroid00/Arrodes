"""Structure for Characters class of the API."""

import requests
import bs4
import mystic.helpers as helpers

API_URL = "https://lordofthemysteries.fandom.com/api.php"
REQUEST_TIMEOUT = 10  # seconds


class CharacterStructure:
    """Represents a character in the Lord of the Mysteries universe."""

    def __init__(self, name: str):
        """
        Initializes a CharacterStructure object.

        Parameters:
        - name (str): The name of the character.

        Raises:
        - NotFoundError: If the character is not found on the website.
        """
        self.url_name = helpers.misc.format_name(name)
        # Keep self.url pointing to the user-friendly wiki page for backward compatibility
        self.url = "https://lordofthemysteries.fandom.com/wiki/" + self.url_name
        
        import os
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
                "disableeditsection": "true"
            }
            headers = {
                "User-Agent": "ArrodesBot/1.0 (Discord Bot; contact: owner)"
            }
            try:
                self.response = requests.get(API_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
            except requests.exceptions.Timeout:
                raise helpers.exceptions.NotFoundError(
                    f"Request timed out while looking up '{name}'."
                )
            except requests.exceptions.RequestException as e:
                raise helpers.exceptions.NotFoundError(
                    f"Network error while looking up '{name}': {e}"
                )
            if self.response.status_code != 200:
                raise helpers.exceptions.NotFoundError(
                    f"Character '{name}' not found (HTTP {self.response.status_code})."
                )

            try:
                res_data = self.response.json()
            except ValueError:
                raise helpers.exceptions.NotFoundError(
                    f"Invalid response format while looking up '{name}'."
                )

            if "error" in res_data:
                err_code = res_data["error"].get("code", "unknown")
                if err_code == "missingtitle":
                    raise helpers.exceptions.NotFoundError(
                        f"Character '{name}' not found on the wiki."
                    )
                else:
                    raise helpers.exceptions.NotFoundError(
                        f"Fandom API error while looking up '{name}': {res_data['error'].get('info', 'No details')}"
                    )

            html_content = res_data["parse"]["text"]["*"]
            
            # Save to local persistent cache
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
            except Exception as e:
                print(f"Warning: Failed to write cache for {self.url_name}: {e}")

        self.parsed = bs4.BeautifulSoup(html_content, "html.parser")
        self.name = self.get_name()


    def get_name(self):
        """
        Retrieves the name of the character.
        Intended to be overridden by subclasses.

        Returns:
        - str: The name of the character.
        """
        return None

    def get_data(self) -> dict:
        """
        Retrieves the data of the character.

        Returns:
        - dict: The data of the character.
        """
        data = dict(self.__dict__)
        data.pop("response", None)
        data.pop("parsed", None)
        data.pop("url_name", None)

        return data

    def __str__(self) -> str:
        return self.name or ""

    def __repr__(self) -> str:
        return self.name or ""

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value
