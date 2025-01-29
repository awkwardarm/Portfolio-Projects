from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from itertools import zip_longest
import re


class PokemonCard:
    def __init__(self, html_content):
        self.html_content = html_content
        self.soup = BeautifulSoup(self.html_content, "html.parser")
        self.attributes_all = ["type", "rarity", "illustrator", "setId"]
        self.attributes_pokemon = ["color", "stage", "weakness", "retreat", "weakness"]
        self.stats = {}

        # Call methods on init
        self.ability_present, self.num_abilities = self._ability_present()
        self.extract_attributes(self.attributes_all)

        # Check if card has an ability, if so extract it
        if self.ability_present:
            self.extract_abilities()

        # Check if card is a pokemon
        if "type" in self.stats and self.stats["type"].lower() == "pokemon":
            self.extract_attributes(self.attributes_pokemon)
            self.extract_hp_value()
            self.energy_results_in_attack = self._find_img_followed_by_target_text(
                target_string="Energy"
            )
            self.extract_attacks()

            # Get evolution stages
            if "stage" in self.stats and self.stats["stage"].lower() != "basic":
                self.extract_evolve_from()

    def _get_soup_from_class(self, target_class):
        result = self.soup.findAll("div", class_=target_class)
        return result

    def _energy_icons_to_text(self, results):
        """Converts energy icons to text strings.

        Args:
            results (object): results from soup.find()

        Returns:
            str: energy as strings.
        """
        energy = []

        for item in results:
            # Find all elements with a src attribute
            elements_with_src = item.find_all(src=True)

            for element in elements_with_src:
                link = element["src"]
                split_link = link.split("/")
                color = split_link[-1].split(".")[0]
                energy.append(color)
        return energy

    def _extract_text_with_energy_labels(self, results):
        """Converts the energy image from a result and combines it with the result's text.

        Args:
            results (object): results from soup.find()

        Returns:
            str: Text string.
        """

        # Extract text into a list
        for item in results:
            # Check if result has text
            if item.get_text():
                # Use a regular expression to split the text on double spaces
                text = item.get_text()
                # Split on double spaces, using regex to account for punctuation
                split_text = re.split(r"\s{2,}", text)

        # get list of energy icons in text
        energy = self._energy_icons_to_text(results)

        # zip together in a list and fill extra incices with blank string
        zipped_longest = list(zip_longest(split_text, energy, fillvalue=""))

        # empty string
        final_text = ""
        for t, e in zipped_longest:
            final_text += t + " " + e + " "

        return final_text.strip()  # Remove whitespace at end

    def _find_img_followed_by_target_text(self, target_string):
        # Find all <img> elements with the specific src attribute
        base_address = "https://static.dotgg.gg/pokemon/icons/"
        extension = ".png"

        # List of energy types
        energy_types = [
            "colorless",
            "grass",
            "fire",
            "water",
            "lightning",
            "psychic",
            "fighting",
            "darkness",
            "metal",
            "fairy",
            "dragon",
        ]

        # Comprehension to get all energy_urls
        energy_urls = [
            f"{base_address}{energy_type}{extension}" for energy_type in energy_types
        ]

        # Find all image elements on page
        img_elements = self.soup.find_all("img")

        # Emtpy list of results
        results = []

        # Iterate through all images
        for img in img_elements:
            # get url
            energy_url = img.get("src")
            #
            if energy_url in energy_urls:
                # note index for later reference to energy_types
                energy_index = energy_urls.index(energy_url)

                # find the next element that is a string
                next_element = img.find_next(string=True)

                # Check if the next_element contains target_text
                if next_element and target_string in next_element:
                    # append energy type by using energy_index to result
                    results.append(energy_types[energy_index])

        return results  # use len(results) to count how many times an energy icon is in an attack

    def _extract_multi_digit_integers(self, target_class):
        results = self._get_soup_from_class(target_class)
        multi_digit_integers = []

        for result in results:
            text = result.get_text(strip=True)
            # Find all integers with more than one digit (including leading zeros)
            numbers = re.findall(r"\b\d{2,}\b", text)
            multi_digit_integers.extend(numbers)

        return multi_digit_integers

    def _ability_present(self):
        """
        Returns:
            bool: Boolean of ability present
        """
        ability_labels = self.soup.find_all(
            "div", class_="sc-lgJXFk jOaFFy", string="Ability"  # "sc-kAWYEp fwamfT"
        )

        if len(ability_labels) == 0:
            return False, 0
        else:
            return True, len(ability_labels)

    def extract_attributes(self, attributes_list):
        """Extracts pokemon card attributes linked to hrefs from a list of attributes

        Args:
            attributes_list (object): List of attributes to extract.
        """
        attributes_list
        result = self._get_soup_from_class(
            target_class="sc-hoZJAX dbGtTC"
        )  # "sc-ia-DHra dJiVFO"

        # find all hrefs in results
        hrefs = []
        for item in result:
            links = item.find_all("a", href=True)
            for link in links:
                href = link["href"]
                hrefs.append(href)

        # parse through the hrefs
        for href in hrefs:
            # print(href)
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)

            for item in attributes_list:
                if item in query_params:
                    self.stats[item] = query_params[item][0]

        # Get description if not a pokemon
        if "type" in self.stats and self.stats["type"].lower() != "pokemon":
            text = self._extract_text_with_energy_labels(result[0])
            self.stats["description"] = text

    def extract_hp_value(self):
        # Find the first <div> element with the specified class
        hp_label = self.soup.find(
            "div", class_="sc-lgJXFk jOaFFy", string="HP"
        )  # "sc-kAWYEp fwamfT"

        if hp_label:
            # Find the next sibling <div> element
            hp_value_div = hp_label.find_next_sibling(
                "div", class_="sc-hoZJAX dbGtTC"
            )  # "sc-ia-DHra dJiVFO"
            if hp_value_div:
                # Get the text content of the next sibling <div> element and convert it to an integer
                hp_value = int(hp_value_div.text.strip())
                self.stats["hp"] = hp_value

    def extract_attacks(self):
        """Extracts all attacks and their costs from a pokemon card."""

        # Create emtpy attack dictionary
        attacks_name = {}
        attacks_cost = {}
        attacks_description = {}
        attacks_damage = {}

        # Initialize attack number
        attack_number = 0

        # Get attacks from soup
        result = self._get_soup_from_class(
            target_class="sc-foEYJr hFLLWj"
        )  # "sc-ftHWs hDyyGk"

        # iterate through all attacks minus the number of abilities
        for item in result:
            # get list of energy for each attack
            energy = self._energy_icons_to_text(item)

            # add list of energy to dictionary of attack costs
            attacks_cost[attack_number] = energy

            # extract attack name
            span_elements = item.find_all("span")

            # get the attack damage from each attack
            for span in span_elements:
                # Get text
                text = span.next_sibling.strip()

                # Split on spaces
                text_split = text.split()

                # check if last index of text is a number (i.e. the damage amount from the attack)
                try:
                    last_element = text_split[-1]
                    last_int = int(last_element)  # Attempt to cast to an integer
                    attacks_damage[attack_number] = last_int

                    # Remove the damage integer and extract the attack description/name
                    beginning_elements = text_split[:-1]
                    attack_name = " ".join(beginning_elements)
                    attacks_name[attack_number] = attack_name

                except (ValueError, IndexError):
                    continue

                attack_number += 1

        # Extract attack strings
        result = self._get_soup_from_class(
            target_class="sc-hAOJoF ifwdyq"
        )  # "sc-haUpKT hWDDcE"

        # Reset attack number to 1
        attack_number = 0

        # iterate through all attacks
        if self.num_abilities > 0:
            for item in result[
                : -self.num_abilities
            ]:  # remove duplicate descriptions with slicing if abilities are present
                # get text
                div_text = item.text.strip()

                # add text to dictionary of attack descriptions
                attacks_description[attack_number] = div_text
                attack_number += 1
        else:
            for item in result:
                # get text
                div_text = item.text.strip()

                # add text to dictionary of attack descriptions
                attacks_description[attack_number] = div_text
                attack_number += 1

        self.stats["attacks_name"] = attacks_name
        self.stats["attacks_cost"] = attacks_cost
        self.stats["attacks_description"] = attacks_description
        self.stats["attacks_damage"] = attacks_damage

        # see if there is any energy effects in attack
        num_energy_in_attack = len(self.energy_results_in_attack)
        if num_energy_in_attack > 0:

            # Remove extra attack name
            value_to_remove = "Energy from this Pokémon."
            keys_to_remove = [
                key
                for key, value in self.stats["attacks_name"].items()
                if value == value_to_remove
            ]

            for key in keys_to_remove:
                del self.stats["attacks_name"][key]

            # * move energy from attacks_cost to description
            # find keys of attacks_description that have " Energy" in value
            keys_with_energy_in_value = []
            counter = num_energy_in_attack
            while counter > 0:
                for key, value in self.stats["attacks_description"].items():
                    if " Energy" in value:
                        keys_with_energy_in_value.append(key)
                counter -= 1

            # Move energy's to description
            energy_to_description = []
            for key in keys_with_energy_in_value:
                energy_to_description.append(
                    self.stats["attacks_cost"][key][-1]
                )  # index last energy in list
                self.stats["attacks_cost"][key].pop(-1)

                # Split description string on "  " and store in temp_list
                temp_list = self.stats["attacks_description"][key].split("  ")

                counter -= 1

                new_description = (
                    f"{temp_list[0]} {energy_to_description[0]} {temp_list[1]}"
                )

                # Replace description
                self.stats["attacks_description"][key] = new_description

        # remove entries in self.stats["attacks_cost"] that are from abilities
        if self.num_abilities > 0:
            keys = list(self.stats["attacks_cost"].keys())
            keys_to_remove = keys[-self.num_abilities :]
            for key in keys_to_remove:
                del self.stats["attacks_cost"][key]

    def extract_abilities(self):
        abilities_name = {}
        abilities_description = {}

        # Extract ability name
        ability_number = 0
        ability_result = self._get_soup_from_class(
            target_class="sc-ejqGWM eTSXYb"
        )  # "sc-dWHSxa iCTYfN"

        for item in ability_result:  # [: -self.num_abilities]:
            # filter out first attack that contains a span
            if not item.find("span"):
                abilities_name[ability_number] = item.get_text(strip=True)
                ability_number += 1

        # Extract ability description text
        ability_number = 0
        ability_result = self._get_soup_from_class(
            target_class="sc-hAOJoF ifwdyq"
        )  # "sc-haUpKT hWDDcE"

        for item in ability_result[
            : -self.num_abilities
        ]:  # remove duplicate descriptions with slicing
            text = self._extract_text_with_energy_labels(ability_result)
            abilities_description[ability_number] = text
            ability_number += 1

        # Append to dictionary
        self.stats["abilities_name"] = abilities_name
        self.stats["abilities_description"] = abilities_description
        # self.stats["ability_description"] = text

    def extract_evolve_from(self):
        target_class = "sc-fafqur kGiwSM"  # "sc-bzAlbP hkCTME"
        results = self._get_soup_from_class(target_class)
        evolves_from_text = None

        for result in results:
            # Find the <div> element containing "Evolves from:"
            evolves_from_div = result.find(
                "div", string=lambda text: text and "Evolves from:" in text
            )
            if evolves_from_div:
                # Extract the following text
                evolves_from_text = (
                    evolves_from_div.get_text(strip=True)
                    .replace("Evolves from:", "")
                    .strip()
                )
                break

        self.stats["evolves_from"] = evolves_from_text
