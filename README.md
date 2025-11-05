# birds-rec

# How to use this
Some extra variables are required. Create a ```urls.py``` file and add them:
- ```STREAM_URL``` (URL of the audio stream)
- ```WEB_URL``` (main website URL)

I intentionally gitignored this file.

## Dependencies
- ffmpeg
- BeautifulSoup

## Running the program
```
python main.py
```

# Issues
- There's the possibility of two different concerts in each of the two sets in one day. Right now both sets would be recorded but would be filed under the first concert, loosing the information of the second.
- It may fail if there's any concerts on January 1st 2026. Check ```convert_date()``` in ```events.py```.
