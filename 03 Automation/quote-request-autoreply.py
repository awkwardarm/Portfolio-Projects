"""
This script autoreplies to project quote requests when potential clients reach out on an online marketplace. 
"""

from playwright.sync_api import Playwright, sync_playwright
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import numpy as np
from datetime import datetime, timedelta

from tryba_auto_functions import (
    save_playwright_context_storage,
    load_playwright_context_storage,
    is_chromium_running,
)

# Set up logging
logging.basicConfig(level=logging.INFO)


def main(inputs):

    # Set cookie storage path
    storage_state_path = "storage_state.json"
    time_delta = timedelta(hours=12)
    # time_delta = timedelta(seconds=15) # override for testing

    with sync_playwright() as p:
        while True:
            browser = None
            context = None
            try:
                start_time = datetime.now()  # set start time
                browser = p.chromium.launch(
                    headless=False, slow_mo=500
                )  # launch browser

                # Create or load a context
                context = create_or_load_content(browser, storage_state_path)

                while context:  # Make sure context exists
                    # Check if time_delta has passed, adds stability
                    if datetime.now() - start_time > time_delta:
                        logging.info(
                            f"Time delta {time_delta} reached, restarting browser"
                        )
                        break

                    try:
                        page = context.new_page()

                        # Check if we need to login
                        check_login_state(context, storage_state_path, page)

                        # Main message checking loop. Refreshes the page and checks for new quote requests
                        while True:
                            if not is_chromium_running(page):
                                logging.warning(
                                    "Chromium is not running, breaking loop"
                                )
                                break

                            # Check messages
                            check_messages(page, inputs)

                            # Check if time_delta has passed to restart the browser
                            if datetime.now() - start_time > time_delta:
                                break

                            time.sleep(5)  # Wait before retrying\

                    except Exception as e:
                        logging.error(f"Error in page operations: {e}")
                        break  # Break inner loop to recreate page
            except Exception as e:
                logging.error(f"Critical error in main loop: {e}")
                break  # break inner loop to recreate page
            finally:
                # Clean up
                try:
                    if context:
                        save_playwright_context_storage(context, storage_state_path)
                        context.close()  # Close the current context
                    if browser:
                        browser.close()
                except Exception as e:
                    logging.error(f"Error during cleanup: {e}")
            time.sleep(5)


def login(page):
    page.goto("https://soundbetter.com/users/sign_in")
    page.wait_for_load_state()
    page.get_by_placeholder("Email").fill(username)
    page.get_by_placeholder("Password").fill(password)
    logging.info(" Please log in manually and then press Enter to continue...")
    input()


def create_or_load_content(browser, storage_state_path):
    # Create or load a context
    try:
        context = load_playwright_context_storage(browser, storage_state_path)
        logging.info("Loaded existing context from storage")
    except FileNotFoundError:
        context = browser.new_context()
        logging.info("Created new context")
    except Exception as e:
        logging.error(f"Error loading context: {e}")
        context = browser.new_context()
        logging.info(f"Falling back to new context due to error {e}")
    return context


def check_login_state(context, storage_state_path, page):
    # Check if we need to login
    try:
        cookies = context.cookies()
        if not cookies:
            logging.info("No cookies found, initiating login")
            login(page)
            save_playwright_context_storage(context, storage_state_path)
    except Exception as e:
        logging.error(f"Error checking cookies: {e}")
        login(page)
        save_playwright_context_storage(context, storage_state_path)


def check_messages(page, inputs):
    # Go to "messages" page
    page.goto("https://soundbetter.com/messages")
    page.wait_for_load_state()

    # Sleep randomly between 60 and 180 seconds
    random_sleep = np.random.randint(60, 181)
    # time.sleep(5) # override for testing
    time.sleep(random_sleep)

    # Check for "Awaiting Response"
    awaiting_response = page.query_selector(".label > span:nth-child(1)")

    if awaiting_response:
        awaiting_response.click()

        # Click "Send A Proposal"
        selector = ".fancybox > div:nth-child(1)"
        page.wait_for_selector(selector)
        page.locator(selector).click()

        # Wait for "Send proposal" button to be visible
        proposal_button_selector = "input.btn:nth-child(10)"  # Adjust if needed
        page.wait_for_selector(proposal_button_selector)

        # Fill form
        for key, value in inputs.items():
            selector, text = value
            page.locator(selector).click()
            page.locator(selector).fill("")  # Clear any pre-filled text
            page.keyboard.type(str(text))  # Convert to string if necessary
            time.sleep(1)  # Adjust delay if needed

        # Select the second option from dropdown for 50/50 payment terms
        page.select_option("#proposal_payment_agreement", value="half")
        time.sleep(1)

        # Click "Send proposal"
        page.locator(proposal_button_selector).click()
        page.wait_for_load_state()

        page.goto("https://soundbetter.com/messages")


# ------------------ INPUTS -----------------------#


inputs = {
    "rate": ["#proposal_price", 3500],
    "project_type": [
        "#proposal_description",
        "Includes: track production, vocal production, vocal arranging, mixing, and mastering. (Per Song)",
    ],
    "message": [
        "#proposal_message",
        """Thank you for reaching out. I'm away from my studio at the moment and I will personally respond as soon as I return.
               
Your best songs in my hands will reach their full potential. Together we can craft them into professionally polished records that resonate with your audience. Every step of the entire process (pre-production, track production, vocal production, mixing, and mastering) is under my umbrella. From demo to master there's no need to hire additional engineers, session players, or producers. I'm a master of the craft and I find no greater joy than evoking emotion out of the speakers.
               
If you don't need full production, I'll review and edit the quote.
               
Lastly, please send me a link to your most effective songs, I'd love to hear your best work.
               
I look forward to listening and connecting,
               
-Matthew Tryba""",
    ],
}


password = os.getenv("soundbetter_password")
username = os.getenv("soundbetter_username")


if __name__ == "__main__":
    main(inputs)
