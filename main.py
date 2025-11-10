import events
import stream
from urls import *
import time
import os
from datetime import datetime
import re
from config import *
from log import log

def main():
    log("Running...")
    while True:
        date_today = datetime.today().strftime('%Y-%m-%d')
        
        event = events.get_next_event()
        event_title = event["title"]
        event_dates = event["dates"]

        if is_now_in_timeslot(dates_list=event_dates, start_time_str=TRY_START_REC, end_time_str=TRY_END_REC):
            log(f"Ready to record next event: {event_title}")

            dir_name = f"{date_today} - {event_title}"
            dir_name = clean_filename(dir_name)

            try:
                os.makedirs(f"{OUTPUT_DIR}/{dir_name}", exist_ok=True)
                log(f"Directory '{dir_name}' created successfully.")
            except Exception as e:
                log(message=f"{e}", msg_type="ERROR")

            events.save_next_event_file(event=event, event_dir=dir_name)

            temp_file_name = datetime.now().strftime("%Y%m%d%H%M%S")

            if SKIP_RECORDING:
                pass
            else:
                stream.record_audio_stream(STREAM_URL, output_dir=f"{OUTPUT_DIR}/{dir_name}/{temp_file_name}.mp3")

                try:
                    temp_file_size = os.path.getsize(f"{OUTPUT_DIR}/{dir_name}/{temp_file_name}.mp3")

                    if temp_file_size > MIN_FILE_SIZE:
                        # succeed. rename.
                        pass
                    else:
                        # not succeeded
                        pass
                except:
                    log(message="file not found", msg_type="ERROR")


                # Create txt file with info?
                log("Waiting...")
                time.sleep(REC_DELAY)
                
        else:
            log(message=f"No events soon. Next event: {event_title} on {event_dates}")
            time.sleep(CHECK_EVENT_DELAY)


def clean_filename(name, replacement="_") -> str:
    return re.sub(r'[<>:"/\\|?*]', replacement, name)

def is_now_in_timeslot(dates_list: list[str], start_time_str: str, end_time_str: str) -> bool:
    """
    Parameters:
        dates_list (list[str]): List of dates in 'YYYY-MM-DD' format
            e.g. ['2025-10-26', '2025-10-27']
        start_time_str (str): Start time in 'HH:MM' 24-hour format
            e.g. '14:00'
        end_time_str (str): End time in 'HH:MM' 24-hour format
            e.g. '18:30'
    """
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    
    # Return False if today is not in the provided list
    if today_str not in dates_list:
        return False
    
    # Parse times
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    
    # Check if current time is within range
    return start_time <= now.time() <= end_time


if __name__ == '__main__':
    main()