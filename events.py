import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from config import *

import urls

def get_next_event() -> dict:
    """
        Returns a dict with data of the NEXT event
    """
    event_data = {
        'title': '',
        'lineup': '',
        'dates': [], # some events may have more than one date
        'time': '',
        'desc1': '',
        'desc2': ''
    }
    try:
        response = requests.get(urls.WEBSITE_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        first_concert_div = soup.find('div', id='desktop-div')


        # left div
        event_side_l_div = first_concert_div.find('div', class_='event-side-l').find('p', class_='lineup').get_text(strip=True)

        event_data['lineup'] = event_side_l_div

        # middle div
        event_side_desc_div = first_concert_div.find('div', class_='event-desc')

        event_title = event_side_desc_div.find('h2', class_='event-desc').get_text(strip=True)
        event_data['title'] = event_title
        event_desc1 = event_side_desc_div.find_all('p', class_='eventdesc')[0].get_text(strip=True)
        event_data['desc1'] = event_desc1
        event_desc2 = event_side_desc_div.find_all('p', class_='eventdesc')[1].get_text(strip=True)
        event_data['desc2'] = event_desc2

        # right div
        event_side_r_div = first_concert_div.find('div', class_='event-side-r')

        event_date = event_side_r_div.find('h1', class_='event-date').get_text(strip=True)
        event_data['dates'] = convert_date(event_date)
        event_time = event_side_r_div.find('ul', class_='eventtime').get_text(strip=True)
        event_data['time'] = convert_time(event_time)

        return event_data
            
    except requests.exceptions.RequestException as e:
        print(e)

def convert_date(date_string: str) -> list[str]:
    date_string = date_string.replace("❘", "|").replace(" ", "").strip()
    
    if "|" in date_string:
        days_part, month_part = date_string.split("|")
        days = [int(day.strip()) for day in days_part.split("+")]
        month = int(month_part.strip())
    else:
        raise ValueError("invalid format")
    
    current_year = datetime.now().year # this is bad
    
    formatted_dates = []
    for day in days:
        date = datetime(current_year, month, day)
        if date < datetime.now():
            date = datetime(current_year, month, day) # current_year + 1?
        formatted_dates.append(date.strftime("%Y-%m-%d"))
    
    return formatted_dates


def convert_time(time_string: str) -> str:
    match = re.search(r'\b\d{1,2}:\d{2}\b', time_string)
    if match:
        return match.group(0)
    return None

def save_event(event, path):

    pass

def save_next_event_file(event, event_dir="", save_separately=False):
    event_title = event["title"]
    event_dates = ", ".join(event["dates"])
    event_current_date = datetime.today().strftime('%Y-%m-%d')
    event_time = event["time"]
    event_desc1 = event["desc1"]
    event_desc2 = event["desc2"]
    event_lineup = event["lineup"]

    if not event_dir:
        event_dir = f"{event_dates} - {event_title}"

    filename = clean_filename(f"{event_dates} - {event_title}")

    if save_separately:
        file_dir = f"{filename}.txt"
    else:    
        file_dir = f"{OUTPUT_DIR}/{event_dir}/{filename}.txt"

    with open(file_dir, "w") as f:
        f.write(f"Event: {event_title}\n")
        f.write(f"------------------\n")
        f.write(f"Lineup: {event_lineup}\n")
        f.write(f"Dates: {event_dates}\n")
        f.write(f"Current date: {event_current_date}\n")
        f.write(f"Time: {event_time}\n")
        f.write(f"Description 1: {event_desc1}\n")
        f.write(f"Description 2: {event_desc2}\n")

def clean_filename(name, replacement="_"):
    return re.sub(r'[<>:"/\\|?*]', replacement, name)

if __name__ == '__main__':

    save_next_event_file(get_next_event(), save_separately=True)