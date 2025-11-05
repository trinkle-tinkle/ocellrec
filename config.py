# General
OUTPUT_DIR = 'recordings'
SKIP_RECORDING = False # The recording will be skipped but the event file and info will be created.

# Minimum file size in bytes to check if the recording succeeded.
MIN_FILE_SIZE = 50000

# Time range to check for the stream
TRY_START_REC = "20:20" # May start late depending on CHECK_EVENT_DELAY
TRY_END_REC = "23:59"

# Delay between attempts to record in seconds.
REC_DELAY = 60
CHECK_EVENT_DELAY = 600