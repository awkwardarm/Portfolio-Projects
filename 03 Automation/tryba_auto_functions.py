import datetime
from icalendar import Calendar
import send2trash
import os


def get_next_sunday():
    '''
    Takes no input. 

    Returns:
        datetime: The date of next Sunday. 
    '''

    today = datetime.date.today()
    days_ahead = 6 - today.weekday()  # Sunday is 6

    if days_ahead <= 0:  # If today is Sunday, get the next Sunday
        days_ahead += 7

def get_next_sunday_from_tomorrow():
    '''
    Takes no input. 

    Returns:
        datetime: The date of next Sunday. 
    '''

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    days_ahead = 6 - tomorrow.weekday()  # Sunday is 6

    if days_ahead <= 0:  # If today is Sunday, get the next Sunday
        days_ahead += 7
    
    return tomorrow + datetime.timedelta(days=days_ahead)

def get_weekday() -> str:
    '''
    Takes no input.

    Returns:
        str: The name of the current weekday.
    '''

    weekday_num = datetime.date.today().weekday()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekdays[weekday_num]

def get_weekday_tomorrow() -> str:
    '''
    Takes no input.

    Returns:
        str: The name of the current weekday.
    '''
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    weekday_num = tomorrow.weekday()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekdays[weekday_num]

def add_ics_to_ical(ics_file_path: str, calendar: str):
    '''
    Adds event to iCalender on MacOS from .ics file. \n
    Sends .ics file to trash when executed.

    Returns:
        None.
    '''

    # function to read ics file
    def read_ics(file_path):
            with open(file_path, 'rb') as f:
                cal = Calendar.from_ical(f.read())
                for event in cal.walk('vevent'):
                    return event
    
    event = read_ics(ics_file_path)
    summary = str(event.get('summary'))

    # get start and end times
    start = event.get('dtstart').dt.strftime("%B %d, %Y at %I:%M:%S %p")
    end = event.get('dtend').dt.strftime("%B %d, %Y at %I:%M:%S %p")

    # format Apple script 
    command = f"""
    tell application "Calendar"
        tell calendar "{calendar}"
            make new event with properties {{summary: "{summary}", start date: date "{start}", end date: date "{end}"}}
        end tell
    end tell
    """

    # Execute Apple script
    os.system(f"osascript -e '{command}'")
    
    # send .ics file to trash
    send2trash.send2trash(ics_file_path)

