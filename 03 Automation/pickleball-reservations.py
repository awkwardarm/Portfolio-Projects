"""
Automated court and event registration for pickleball. 
"""

from playwright.sync_api import Playwright, sync_playwright, expect
import os
import sys
import numpy as np
import time
import datetime
from tryba_auto_functions import (
    add_ics_to_ical,
    get_next_sunday_from_tomorrow,
    get_weekday_tomorrow,
)


def main(reservation_type: str):
    """
    Input reservation_type as "Open Play" or "Private Court".
    """

    def run(playwright: Playwright, player, reso_day, reso_hour) -> None:

        # Set up chromium
        browser = playwright.chromium.launch(
            headless=False, slow_mo=500, downloads_path="/Users/matthewtryba/Downloads"
        )

        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://my.website.life/login.html")
        page.wait_for_load_state()
        page.get_by_placeholder("Username, Email, or Member ID").fill(player.username)
        page.get_by_placeholder("Password").fill(player.password)
        page.get_by_role("button", name=" Log In").click()
        page.wait_for_load_state()

        if reservation_type.lower() == "open play":

            # Get next sunday date as string
            next_sunday_from_tomorrow = get_next_sunday_from_tomorrow()

            # Get next sunday
            next_sunday_date = next_sunday_from_tomorrow.strftime("%Y-%m-%d")

            # Go to next week's pickle schedule
            pickle_schedule = (
                "https://my.website.life/clubs/co/centennial/classes.html?teamMemberView=true&mode=week&selectedDate="
                + next_sunday_date
                + "&interest=Pickleball+Open+Play&location=Centennial"
            )
            page.goto(pickle_schedule)
            page.wait_for_load_state()

            if reso_day != "Saturday":
                # Sleep script randomly to prevent detection
                random_integer = np.random.randint(0, 10)
                time.sleep(random_integer)

            # Get desired reservation from dictionary
            selector = open_play_schedule[reso_day][reso_hour]

            # Add try/except here to account for added events on saturdays. I need to wait for them to add the youth event again.

            page.wait_for_selector(selector)
            page.locator(selector).click()
            page.wait_for_load_state()

            # Click Reserve
            selector = ".transition-wrapper > div:nth-child(1) > p:nth-child(5) > button:nth-child(1)"
            page.wait_for_selector(selector)
            page.locator(selector).click()
            page.wait_for_load_state()

            # Click Accept Waiver
            page.get_by_test_id("acceptWaiver").locator("span").click()
            page.get_by_test_id("finishBtn").click()
            page.wait_for_load_state()

            if player == "matthew":

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
                add_ics_to_ical(new_file_path, calendar="Pickleball Auto")

        elif reservation_type.lower() == "private court":

            # Reservation details
            desired_court = private_court_reservations[reso_day][0]["court"]
            start_time = private_court_reservations[reso_day][0]["time"]
            duration = str(private_court_reservations[reso_day][0]["duration"])

            # Concat into URL
            private_court_url = (
                "https:/my.website.life/account/reservations.html?resourceId=ZXhlcnA6MTk0YnI"
                + desired_court
                + "OjcwMTU5MTE0MTUwOA==&start="
                + str(reservation_day)
                + "T"
                + start_time
                + "-06:00&duration="
                + duration
                + "&cancelUrl=aHR0cHM6Ly9teS5saWZldGltZS5saWZlL2NsdWJzL2NvL2NlbnRlbm5pYWwvcmVzb3VyY2UtYm9va2luZy5odG1sP3Nwb3J0PVBpY2tsZWJhbGwlM0ErSW5kb29yJmNsdWJJZD0xOTQmZGF0ZT0yMDI0LTA0LTExJnN0YXJ0VGltZT0tMSZkdXJhdGlvbj02MCZoaWRlTW9kYWw9dHJ1ZQ=="
            )

            page.goto(private_court_url)
            page.wait_for_load_state()

            # Click Accept Waiver
            page.get_by_test_id("acceptWaiver").locator("span").click()
            page.get_by_test_id("finishBtn").click()
            page.wait_for_load_state()

        # ---------------------

        context.close()
        browser.close()

    # Loop through players and determine if they have a reservation request at time of sript trigger. If so, execute request.
    for player in players:

        if reservation_type.lower() == "open play" and validate_reso(
            reso_day=reso_day, reso_hour=reso_hour, player=player
        ):
            with sync_playwright() as playwright:
                run(playwright, player=player, reso_day=reso_day, reso_hour=reso_hour)

        # Private court reservations only for "Matthew Tryba"
        elif reservation_type.lower() == "private court" and player == matthew:
            with sync_playwright() as playwright:
                run(playwright, player=player, reso_day=reso_day, reso_hour=reso_hour)


def validate_reso(reso_day, reso_hour, player):
    """
    True if the reservation day and time are in the player's desired schedule.
    """

    for key, values in player.reservations_open.items():
        if key == reso_day:
            return reso_hour in values


class Player:
    def __init__(self, name, username, password, reservations_open) -> None:
        self.name = name
        self.username = username
        self.password = password
        self.reservations_open = reservations_open


matthew = Player(
    name="Matthew Tryba",
    username=os.getenv("my_website_life_username"),
    password=os.getenv("my_website_life_password"),
    reservations_open={
        "Tuesday": [16],
        "Wednesday": [18],
        "Friday": [18],
        "Saturday": [10],
        "Sunday": [10],
    },
)

vincent = Player(
    name="Vinny Nguyen",
    username=os.getenv("my_website_life_vincent_username"),
    password=os.getenv("my_website_life_vincent_password"),
    reservations_open={
        "Wednesday": [18],
        "Friday": [18],
        "Saturday": [8, 10],
        "Sunday": [8, 10],
    },
)


""" INPUTS """
open_play_schedule = {
    "Tuesday": {
        16: "div.day:nth-child(3) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)"
    },
    "Wednesday": {
        18: "div.day:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)"
    },
    "Friday": {
        18: "div.day:nth-child(6) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)"
    },
    "Saturday": {
        8: "div.day:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)",
        10: "div.day:nth-child(7) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span:nth-child(1)",
    },
    "Sunday": {
        8: "div.day:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(2) > a:nth-child(1) > span:nth-child(1)",
        10: "div.day:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > p:nth-child(2) > a:nth-child(1) > span:nth-child(1)",
    },
}

# Court identifiers
court_4_id = "2NDAx"
court_9_id = "3NDAy"
court_3_id = "2MjAx"

# Dictionary of desired private court reservations
private_court_reservations = {
    # Add more reservations for the same day as needed
    "Monday": [{"time": "16:00:00", "court": court_4_id, "duration": 90}],
    "Tuesday": [{"time": "11:00:00", "court": court_3_id, "duration": 90}],
    "Wednesday": [{"time": "15:00:00", "court": court_4_id, "duration": 90}],
    "Thursday": [{"time": "17:00:00", "court": court_3_id, "duration": 60}],
    "Friday": [{"time": "16:00:00", "court": court_9_id, "duration": 90}],
    "Saturday": [{"time": "12:00:00", "court": court_4_id, "duration": 90}],
    "Sunday": [{"time": "12:00:00", "court": court_9_id, "duration": 90}],
}

# Get date for next week
today = datetime.date.today()
reservation_day = today + datetime.timedelta(days=8)

# Get target hour for open play reservation. Reservations are made 7 days and 22 hours in advance
reso_hour = datetime.datetime.now().hour - 2

# Get number of weekday and convert it to string for that day
reso_day = get_weekday_tomorrow()

players = [matthew, vincent]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print(
            "Please provide a reservation type as an argument: 'Open Play' or 'Private Court'."
        )
