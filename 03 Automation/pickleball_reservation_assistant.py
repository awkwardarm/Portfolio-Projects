from playwright.sync_api import Playwright, sync_playwright, expect
import os
import sys
import numpy as np
import time
import datetime
from tryba_auto_functions import get_weekday, get_next_sunday, add_ics_to_ical, get_next_sunday_from_tomorrow, get_weekday_tomorrow

def main(reservation_type: str):

    '''
    Input reservation_type as "Open Play" or "Private Court".
    '''

    def run(playwright: Playwright) -> None:

        # Set up chromium
        browser = playwright.chromium.launch(headless=False, slow_mo=500, downloads_path='/Users/matthewtryba/Downloads')
        context = browser.new_context()
        page = context.new_page()

        # Login
        username = os.getenv('my_lifetime_life_username')
        password = os.getenv('my_lifetime_life_password')
        page.goto('https://my.lifetime.life/login.html')
        page.get_by_placeholder("Username, Email, or Member ID").fill(username)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name=" Log In").click()
        page.wait_for_load_state()

        # Get number of weekday and convert it to string for that day
        weekday_name = get_weekday_tomorrow()
        
        if reservation_type.lower() == 'open play':

            # Get next sunday date as string
            next_sunday = get_next_sunday()
            next_sunday_from_tomorrow = get_next_sunday_from_tomorrow()

            # Get next sunday
            #next_sunday_date = next_sunday.strftime("%Y-%m-%d") # Format as YYYY-MM-DD
            next_sunday_date = next_sunday_from_tomorrow.strftime("%Y-%m-%d")

            # Go to next week's pickle schedule
            pickle_schedule = (
                'https://my.lifetime.life/clubs/co/centennial/classes.html?teamMemberView=true&mode=week&selectedDate=' 
                + next_sunday_date 
                + '&interest=Pickleball+Open+Play&location=Centennial'
            )
            page.goto(pickle_schedule)
            page.wait_for_load_state()

            if weekday_name != 'Saturday':
                # Sleep script randomly to prevent detection
                random_integer = np.random.randint(0,10)
                time.sleep(random_integer)

            # Note: use firefox to copy CSS Selector to paste into dictionary
            pickle_events = {
            'Tuesday':'div.day:nth-child(3) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)',
            'Wednesday':'div.day:nth-child(4) > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > p:nth-child(5) > a:nth-child(1)',
            'Friday':'div.day:nth-child(6) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > p:nth-child(5) > a:nth-child(1)',
            'Saturday':'div.day:nth-child(7) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > p:nth-child(5) > a:nth-child(1)',
            'Sunday':'div.day:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > p:nth-child(5) > a:nth-child(1)'
            }

            # Get desired reservation from dictionary
            selector = pickle_events[weekday_name]
            page.wait_for_selector(selector)
            page.locator(selector).click()
            page.wait_for_load_state()

            # Click Reserve
            page.get_by_role("button", name="Reserve").click()
            page.wait_for_load_state()
        
        elif reservation_type.lower() == 'private court':

            # Court identifiers
            court_4_id = '2NDAx'
            court_9_id = '3NDAy'

            # Get date for next week
            today = datetime.date.today()
            #reservation_day = today + datetime.timedelta(days=7)
            reservation_day = today + datetime.timedelta(days=8)

            print(reservation_day)
            
            private_court_reservations = {
                'Monday': [
                    # Add more reservations for the same day as needed
                    {'time': '16:00:00', 'court': court_9_id, 'duration': 120}
                ],
                'Tuesday': [
                    {'time': '11:00:00', 'court': court_4_id, 'duration': 90}
                ],
                'Wednesday': [
                    {'time': '15:00:00', 'court': court_4_id, 'duration': 120}
                ],
                'Friday': [
                    {'time': '16:00:00', 'court': court_9_id, 'duration': 120}
                ],
                'Saturday': [
                    {'time': '12:00:00', 'court': court_4_id, 'duration': 120}
                ],
                'Sunday': [
                    {'time': '12:00:00', 'court': court_9_id, 'duration': 120}
                ]}
            
            # Reservation details
            #desired_court = court_4_id
            desired_court = private_court_reservations[weekday_name][0]['court']
            #start_time = '11:00:00' # formatted 00:00:00 in 24 hour time
            start_time = private_court_reservations[weekday_name][0]['time']
            #duration = '90'
            duration = str(private_court_reservations[weekday_name][0]['duration'])

            # Concat into URL
            private_court_url = (
                'https://my.lifetime.life/account/reservations.html?resourceId=ZXhlcnA6MTk0YnI' 
                + desired_court 
                + 'OjcwMTU5MTE0MTUwOA==&start=' 
                + str(reservation_day) 
                + 'T' 
                + start_time 
                + '-07:00&duration=' 
                + duration 
                + '&cancelUrl=aHR0cHM6Ly9teS5saWZldGltZS5saWZlL2NsdWJzL2NvL2NlbnRlbm5pYWwvcmVzb3VyY2UtYm9va2luZy5odG1sP3Nwb3J0PVBpY2tsZWJhbGwlM0ErSW5kb29yJmNsdWJJZD0xOTQmZGF0ZT0yMDI0LTAyLTI3JnN0YXJ0VGltZT0tMSZkdXJhdGlvbj02MCZoaWRlTW9kYWw9dHJ1ZQ=='
            )

            page.goto(private_court_url)
            page.wait_for_load_state()
        
        # Click Accept Waiver
        page.get_by_test_id("acceptWaiver").locator("span").click()
        page.get_by_test_id("finishBtn").click()
        page.wait_for_load_state()

        if reservation_type.lower() == 'open play':

            # Add to calendar
            page.get_by_role("button", name="Add to Calendar").click()
            page.wait_for_load_state()

            # Download .ics file to add to calendar
            with page.expect_download() as download_info:
                page.get_by_test_id("modalAddToCalendarBtn").click()
            download = download_info.value

            # Define the new filename with the .ics extension
            downloaded_file_path = download.path()
            new_file_path = str(downloaded_file_path) + ".ics"

            # Rename the file
            os.rename(downloaded_file_path, new_file_path)

            # Add to iCalendar
            add_ics_to_ical(new_file_path, calendar='Pickleball Auto')

        # ---------------------
        
        context.close()
        browser.close()

    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    #main(reservation_type="Private Court")

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a reservation type as an argument: 'Open Play' or 'Private Court'.")

