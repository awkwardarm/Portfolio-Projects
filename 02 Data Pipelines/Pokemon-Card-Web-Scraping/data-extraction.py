from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def main():

    # Import collection.csv
    csv_file = "/Users/matthewtryba/Documents/GitHub/pokemon-tcg-pocket/collection.csv"
    collection = pd.read_csv(csv_file)
    # make column name_url and remove all white space and lower
    collection["name_url"] = collection["name"].apply(
        lambda x: x.replace(" ", "").lower()
    )

    # iterate through collection and save html files
    for index, row in collection.iterrows():
        # Get card name info
        card_set = row["set"].lower()
        card_number = row["number"]
        card_name = row["name_url"]

        # append to url
        url = f"https://ptcgpocket.gg/cards/{card_set}-{card_number}-{card_name}/"

        # Save html file from url
        soup = url_to_soup(url)

        # Save Soup to HTML file
        folder_path = (
            "/Users/matthewtryba/Documents/GitHub/pokemon-tcg-pocket/card-html-files"
        )
        file_name = f"{card_set} - {card_number} - {row['name']}.html"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))


def url_to_soup(url, max_retries=3):
    with sync_playwright() as p:
        # Set initial attempt
        retries = 0

        while retries < max_retries:
            # Launch the browser
            browser = p.firefox.launch(headless=True)
            context = browser.new_context(
                java_script_enabled=True,
                bypass_csp=True,
                ignore_https_errors=True,
                permissions=["geolocation"],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                storage_state={"cookies": [], "origins": []},  # Block cookies
            )
            # context = browser.new_context()
            page = browser.new_page()
            try:
                page.goto(url, timeout=120000)  # Increase the timeout duration
                page.wait_for_load_state(
                    "domcontentloaded", timeout=120000
                )  # wait for domcontentloaded

                # Manual wait to ensure all dynamic content is loaded
                time.sleep(15)

                # Get the rendered HTML
                content = page.content()
                soup = BeautifulSoup(content, features="html.parser")

                # Close the browser
                browser.close()

                return soup

            except Exception as e:
                print(f"An error occurred: {e}")
                retries += 1
                if retries >= max_retries:
                    print(f"Failed to load the page afet {max_retries} attempts.")
                else:
                    print(f"Retrying... ({retries}/{max_retries})")
                time.sleep(5)
        browser.close()


if __name__ == "__main__":
    main()
