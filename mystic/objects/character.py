"""Character class that represents a character in the Lord of the Mysteries."""

from typing import Optional
from mystic import objectStructures
import mystic.helpers as helpers


class Character(objectStructures.CharacterStructure):
    """
    A class that represents a character in the Lord of the Mysteries.
    Inherits from the CharacterStructure class in the objectStructures module.

    Attributes:
    name (str): The name of the character.
    chinese_name (list[tuple]): The Chinese names of the character as a list of tuple ~ (Chinese Name, English Translation).
    birth: The birth details of the character.
    gender: The gender of the character.
    species: The species of the character.
    height: The height of the character.
    eye_colour: The eye colour of the character.
    hair_colour: The hair colour of the character.
    aliases: The aliases of the character.
    titles: The titles of the character.
    pathways: The pathways of the character.
    authorities: The authorities of the character.
    relatives: The relatives of the character.
    masters: The masters of the character.
    enemies: The enemies of the character.
    allies: The allies of the character.
    image: The image of the character.
    affiliation: The affiliation of the character.
    occupation: The occupation of the character.
    religion: The religion of the character.
    residence: The residence of the character.
    origin: The origin of the character.
    intro: The introduction of the character.
    honorific_name: The honorific name of the character.
    symbol: The symbol of the character.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the Character class.

        Parameters:
        name (str): The name of the character.
        """
        
        super().__init__(name)

        self.chinese_name = self.get_chinese_name()
        self.birth = self.get_birth()
        self.gender = self.get_gender()
        self.species = self.get_species()
        self.height = self.get_height()
        self.eye_colour = self.get_eye_colour()
        self.hair_colour = self.get_hair_colour()
        self.aliases = self.get_aliases()
        self.titles = self.get_titles()
        self.pathways = self.get_pathways()
        self.authorities = self.get_authorities()
        self.relatives = self.get_relatives()
        self.masters = self.get_masters()
        self.enemies = self.get_enemies()
        self.allies = self.get_allies()
        self.image = self.get_image()
        self.affiliation = self.get_affiliation()
        self.occupation = self.get_occupation()
        self.religion = self.get_religion()
        self.residence = self.get_residence()
        self.origin = self.get_origin()
        self.intro = self.get_intro()
        self.honorific_name = self.get_honorific_name()
        self.symbol = self.get_symbol()

    def get_name(self) -> Optional[str]:
        """
        Returns the name of the character.

        Returns:
        str: The name of the character.
        """
        try:
            return self.parsed.find("h2", class_="pi-title").text
        except AttributeError:
            return None

    def get_chinese_name(self) -> list:
        """
        Returns the Chinese names of the character as a list of tuple ~ (Chinese Name, English Translation).

        Returns:
        list[tuple]: The Chinese names of the character.
        """
        try:
            names = []
            head = self.parsed.find("h3", string="Chinese")
            div = head.parent.find("div", class_="pi-data-value pi-font")

            children = div.findChildren("span")

            if len(children) == 0:
                names.append(div.text)

            for child in children:
                children2 = child.findChildren("i")
                if len(children2) != 0:
                    continue
                names.append(child.text)

            ching = list(zip(names[0::2], names[1::2]))
            return ching
        except AttributeError:
            return []

    def get_birth(self) -> Optional[str]:
        """
        Retrieves the birth information of the character.

        Returns:
            str: The birth information of the character, or None if not found.
        """
        head = self.parsed.find("h3", string="Birth")
        try:
            return helpers.misc.clean_text(head.parent.find("div").text)
        except AttributeError:
            return None

    def get_gender(self) -> Optional[str]:
        """
        Retrieves the gender/sex of the character.

        Returns:
            str: The gender/sex of the character, or None if not found.
        """
        head = self.parsed.find("h3", string="Gender") or self.parsed.find("h3", string="Sex")
        try:
            a_tag = head.parent.find("a")
            val = a_tag.text if a_tag else head.parent.find("div").text
            return helpers.misc.clean_text(val)
        except AttributeError:
            return None

    def get_species(self) -> Optional[list]:
        """
        Retrieves the species of the character.

        Returns:
            list: A list of species of the character.
        """
        species = []
        head = self.parsed.find("h3", string="Species")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    species.append(text)
                return species if species else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    species.append(text)
            return species if species else None
        except AttributeError:
            return None

    def get_height(self) -> Optional[list]:
        """
        Retrieves the height of the character.

        Returns:
            Optional[list]: A list of heights, or None if not found.
        """
        heights = []
        head = self.parsed.find("h3", string="Height")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    heights.append(text)
                return heights if heights else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    heights.append(text)
            return heights if heights else None
        except AttributeError:
            return None

    def get_eye_colour(self) -> Optional[list]:
        """
        Retrieves the eye color(s) of the character.

        Returns:
            list: A list of eye color(s) of the character.
        """
        eyes = []
        head = self.parsed.find("h3", string="Eye")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    eyes.append(text)
                return eyes if eyes else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    eyes.append(text)
            return eyes if eyes else None
        except AttributeError:
            return None

    def get_hair_colour(self) -> Optional[list]:
        """
        Retrieves the hair color(s) of the character.

        Returns:
            list: A list of hair color(s) of the character.
        """
        hairs = []
        head = self.parsed.find("h3", string="Hair")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    hairs.append(text)
                return hairs if hairs else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    hairs.append(text)
            return hairs if hairs else None
        except AttributeError:
            return None

    def get_aliases(self) -> Optional[list]:
        """
        Retrieves the aliases of the character.

        Returns:
            Optional[list]: A list of aliases, or None if not found.
        """
        aliases = []
        head = self.parsed.find("h3", string="Aliases")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    aliases.append(text)
                return aliases if aliases else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    aliases.append(text)
            return aliases if aliases else None
        except AttributeError:
            return None

    def get_titles(self) -> Optional[list]:
        """
        Retrieves the titles associated with the character.

        Returns:
            Optional[list]: A list of titles, or None if not found.
        """
        titles = []
        head = self.parsed.find("h3", string="Titles")
        try:
            head.parent
        except AttributeError:
            return None

        lists = head.parent.find_all("li")
        if len(lists) == 0:
            text = helpers.misc.clean_text(head.parent.find("div").text)
            if text:
                titles.append(text)
            return titles if titles else None

        import copy
        for li in lists:
            li_copy = copy.copy(li)
            desc_spans = []
            for span in li_copy.find_all("span"):
                if getattr(span, "attrs", None) is None:
                    continue
                if span.get("style"):
                    desc_text = helpers.misc.clean_text(span.text)
                    if desc_text:
                        desc_spans.append(desc_text)
                    span.decompose()
            main_text = helpers.misc.clean_text(li_copy.text)
            desc_str = ", ".join(desc_spans)
            if desc_str:
                titles.append(f"{main_text} ({desc_str})")
            elif main_text:
                titles.append(main_text)
        return titles if titles else None

    def get_pathways(self) -> Optional[list]:
        """
        Retrieves the pathways associated with the character.

        Returns:
            Optional[list]: A list of pathway names, or None if not found.
        """
        pathways = []
        head = self.parsed.find("h3", string="Pathway(s)")
        if not head:
            # Fallback to checking the Authorities label
            head = self.parsed.find("h3", string="Authorities")
        
        if not head:
            return None
            
        try:
            # If it has links, extract text from links
            for a in head.parent.find_all("a"):
                if a.text.strip():
                    text = helpers.misc.clean_text(a.text)
                    if text and text not in pathways:
                        pathways.append(text)
            # If no links, try to split plain text
            if not pathways:
                div_text = head.parent.find("div").text
                for word in div_text.split():
                    cleaned_word = helpers.misc.clean_text(word)
                    if cleaned_word and cleaned_word not in pathways:
                        pathways.append(cleaned_word)
            return pathways if pathways else None
        except AttributeError:
            return None

    def get_authorities(self) -> Optional[list]:
        """
        Retrieves the list of authorities associated with the character.

        Returns:
            Optional[list]: The list of authorities, or None if not found.
        """
        authorities = []
        head = self.parsed.find("h3", string="Authorities")
        try:
            head.parent
        except AttributeError:
            return None

        for a in head.parent.find_all("a"):
            if a.text.strip():
                if not a.get("title"):
                    continue
                text = helpers.misc.clean_text(a.text)
                if text:
                    authorities.append(text)
        return authorities if authorities else None

    def get_relatives(self) -> Optional[list]:
        """
        Retrieves the list of relatives for the character.

        Returns:
            Optional[list]: A list of relatives, or None if not found.
        """
        relatives = []
        head = self.parsed.find("h3", string="Relative(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    relatives.append(text)
                return relatives if relatives else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    relatives.append(text)
            return relatives if relatives else None
        except AttributeError:
            return None

    def get_masters(self) -> Optional[list]:
        """
        Retrieves the list of masters associated with the character.

        Returns:
            Optional[list]: A list of masters, or None if not found.
        """
        masters = []
        head = self.parsed.find("h3", string="Master(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    masters.append(text)
                return masters if masters else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    masters.append(text)
            return masters if masters else None
        except AttributeError:
            return None

    def get_enemies(self) -> Optional[list]:
        """
        Retrieves a list of enemies associated with the character.

        Returns:
            Optional[list]: A list of enemies, or None if not found.
        """
        enemies = []
        head = self.parsed.find("h3", string="Enemie(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    enemies.append(text)
                return enemies if enemies else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    enemies.append(text)
            return enemies if enemies else None
        except AttributeError:
            return None

    def get_allies(self) -> Optional[list]:
        """
        Retrieves a list of allies associated with the character.

        Returns:
            Optional[list]: A list of allies, or None if not found.
        """
        allies = []
        head = self.parsed.find("h3", string="Allies")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    allies.append(text)
                return allies if allies else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    allies.append(text)
            return allies if allies else None
        except AttributeError:
            return None

    def get_image(self) -> str:
        """
        Retrieves the image URL of the character.

        Returns:
            str: The URL of the character's image.
        """
        try:
            figure_header = self.parsed.find("figure", class_="pi-item pi-image")
            return figure_header.find("img")["src"]
        except (AttributeError, TypeError, KeyError):
            return "No Image exists yet."

    def get_affiliation(self) -> Optional[list]:
        """
        Retrieves the affiliations of the character.

        Returns:
            Optional[list]: A list of affiliations, or None if not found.
        """
        affiliations = []
        head = self.parsed.find("h3", string="Affiliation(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    affiliations.append(text)
                return affiliations if affiliations else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    affiliations.append(text)
            return affiliations if affiliations else None
        except AttributeError:
            return None

    def get_occupation(self) -> Optional[list]:
        """
        Retrieves the occupation(s) of the character.

        Returns:
            Optional[list]: A list of occupations, or None if not found.
        """
        occupations = []
        head = self.parsed.find("h3", string="Occupation(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    occupations.append(text)
                return occupations if occupations else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    occupations.append(text)
            return occupations if occupations else None
        except AttributeError:
            return None

    def get_religion(self) -> Optional[list]:
        """
        Retrieves the religion(s) of the character.

        Returns:
            Optional[list]: A list of religions, or None if not found.
        """
        religions = []
        head = self.parsed.find("h3", string="Religion(s)")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    religions.append(text)
                return religions if religions else None
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    religions.append(text)
            return religions if religions else None
        except AttributeError:
            return None

    def get_origin(self) -> list:
        """
        Retrieves the origin of the Character.

        Returns:
            list: A list of origins. Empty list if not found.
        """
        origins = []
        head = self.parsed.find("h3", string="Origin")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    origins.append(text)
                return origins
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    origins.append(text)
            return origins
        except AttributeError:
            return []

    def get_residence(self) -> list:
        """
        Retrieves the residence of the Character.

        Returns:
            list: A list of residences. Empty list if not found.
        """
        residences = []
        head = self.parsed.find("h3", string="Residence")
        try:
            data = head.parent.find("div")
            children = data.findAll("li")
            if len(children) == 0:
                text = helpers.misc.clean_text(data.text)
                if text:
                    residences.append(text)
                return residences
            for child in children:
                text = helpers.misc.clean_text(child.text)
                if text:
                    residences.append(text)
            return residences
        except AttributeError:
            return []

    def get_intro(self) -> list:
        """
        Retrieves the intro of the Character.

        Returns:
            list: A list of intro paragraph strings.
        """
        intros = self.parsed.find_all("p")[7:12]
        poem_divs = self.parsed.find_all("div", class_="poem")
        poem_ps = [p for div in poem_divs for p in div.find_all("p")]

        intros = [intro for intro in intros if intro not in poem_ps]
        intro_texts = [helpers.misc.clean_text(p.text) for p in intros if p.text.strip()]

        return [t for t in intro_texts if t]

    def get_honorific_name(self) -> list[str]:
        """
        Retrieves the honorific name of the character.

        Returns:
            list: A list of honorific name strings.
        """
        honorific = self.parsed.find_all("div", class_="poem")
        for div in honorific:
            for span in div.find_all("span", class_="refpopups-custom-content mobile-hidden", style="display:none"):
                span.decompose()
       
        honorific_text = [helpers.misc.clean_text(p.text) for p in honorific[1:2]]

        if not honorific_text or honorific_text == [""]:
            honorific_text = [helpers.misc.clean_text(p.text) for p in honorific[0:1]]

        return [t for t in honorific_text if t]
    
    def get_symbol(self) -> str:
        """
        Retrieves the symbol of the character.
        
        Returns:
            An image representing the symbol of mysticism of the character.
        """
        try:
            symbol = self.parsed.find("h2", string="Mysticism")
            symbols = symbol.parent.find("figure", class_="pi-item pi-image")
            symbols = symbols.find("img")["src"]
            return symbols
        except (AttributeError, TypeError, KeyError):
            return "The Character does not have a Mysticism Symbol."

        
    
   
