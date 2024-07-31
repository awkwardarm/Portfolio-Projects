'''
This script autoreplies to project quote requests when potential clients reach out on an online marketplace. 
'''

from playwright.sync_api import Playwright, sync_playwright, expect
import time
import logging
import os

from tryba_auto_functions import (
    save_playwright_context_storage,
    load_playwright_context_storage,
    is_chromium_running
    )

# Set up logging
logging.basicConfig(level=logging.INFO)

def main(inputs):

    # Set cookie storage path
    storage_state_path = "storage_state.json"
    
    with sync_playwright() as p:
        # Initiate Browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        
        # Main loop, restarts if Chromium quits
        while True:
            # Browser launch, login, and save cookies
            try:
                # Load saved storage state if available
                try:
                    context = load_playwright_context_storage(browser, storage_state_path)
                except FileNotFoundError:
                    context = browser.new_context()

                page = context.new_page()

                # If no cookies, initiate login sequence and save cookies
                if not context.cookies():
                    # Initiate login sequence of no cookies found
                    login(page)
                    # Save cookies for next browser bootup
                    save_playwright_context_storage(context, storage_state_path)

                while True:
                    # Loop if chromium is running
                    is_chromium_running(page)
                    # Check messages
                    check_messages(page, inputs)

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                save_playwright_context_storage(context, storage_state_path)
                context.close()  # Close the current context
                time.sleep(5)  # Wait before retrying
                continue # retry login with cookies if failure
            
                #ERROR:root:An error occurred: Timeout 30000ms exceeded.

def login(page):
    page.goto("https://soundbetter.com/users/sign_in")
    page.wait_for_load_state()
    page.get_by_placeholder("Email").fill(username)
    page.get_by_placeholder("Password").fill(password)
    logging.info("Please log in manually and then press Enter to continue...")
    input()


def check_messages(page, inputs):
    # Go to "messages" page
    page.goto('https://soundbetter.com/messages')
    page.wait_for_load_state()
    time.sleep(60)

    # Check for "Awaiting Response"
    awaiting_response = page.query_selector('.label > span:nth-child(1)')

    if awaiting_response:
        awaiting_response.click()

        # Click "Send A Proposal"
        selector = ".fancybox > div:nth-child(1)"
        page.wait_for_selector(selector)
        page.locator(selector).click()

        # Wait for "Send proposal" button to be visible
        proposal_button_selector = 'input.btn:nth-child(10)'  # Adjust if needed
        page.wait_for_selector(proposal_button_selector)

        # Fill form
        for key, value in inputs.items():
            selector, text = value
            page.locator(selector).click()
            page.locator(selector).fill("") # Clear any pre-filled text
            page.keyboard.type(str(text))  # Convert to string if necessary
            time.sleep(1)  # Adjust delay if needed

        # Select the second option from dropdown for 50/50 payment terms
        page.select_option('#proposal_payment_agreement', value='half')
        time.sleep(1)

        # Click "Send proposal"
        page.locator(proposal_button_selector).click()
        page.wait_for_load_state()

        page.goto('https://soundbetter.com/messages')


# ------------------ INPUTS -----------------------#

inputs = {
    'rate':['#proposal_price', 0000], 
    'project_type':['#proposal_description', 'Full Production (per song)'], 
    'message':['#proposal_message', "Sample Message"]
}


password = os.getenv("soundbetter_password")
username = os.getenv("soundbetter_username")


if __name__ == "__main__":
    main(inputs)
