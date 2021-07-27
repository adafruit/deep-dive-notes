"""
    Add Direct YT links to Timestamped Markdown Files
    Example YT URL "https://www.youtube.com/watch?v=VIDEO_ID?t=seconds"

    Example:
        python add_yt_links VIDEO_ID
            VIDEO_ID is the YT video parameter from the watch url v=VIDEO_ID
            If episode_data is not supplied, today's date is used.

        python add_yt_links VIDEO_ID EPISODE_DATE(YYYY-MM-DD)
            VIDEO_ID is the YT video parameter from the watch url v=VIDEO_ID
            Specify an episode date to process files for other dates.
"""


import datetime
from pathlib import Path
import re
import sys
import time

# pylint: disable=anomalous-backslash-in-string
# Matches * #:##:## or * ##:## or * #:##
TIMESTAMP_PATTERN = re.compile("\*\s\d:\d\d:\d\d|\*\s\d\d:\d\d|\*\s\d:\d\d")


def convert_elapsed_time_to_seconds(elapsed_time):
    """Converts a  string of elapsed time to seconds

    params:
    elapsed_time (str)

    return:
    seconds (int)
    """
    print(f"convert_elapsed_time_to_seconds: {elapsed_time}")
    _elapsed_time = time.strptime(elapsed_time, "%H:%M:%S")
    return int(
        datetime.timedelta(
            hours=_elapsed_time.tm_hour,
            minutes=_elapsed_time.tm_min,
            seconds=_elapsed_time.tm_sec,
        ).total_seconds()
    )


def process_episode(episode_notes):
    """
    params:
    episode_notes (Path): File to be processed and re-written
    """
    with episode_notes.open() as file:
        file_contents = file.read()
        file_contents = re.sub(TIMESTAMP_PATTERN, yt_timestamp_url_repl, file_contents)
        print(file_contents)
        episode_notes.write_text(file_contents)


def yt_timestamp_url_repl(match):
    """
    Regex REPL to go with sub command

    Params:
    match (regex match object)

    Return:
    new string (str)
    """
    elapsed_time = match.group(0).split(" ")[1]
    if len(elapsed_time.split(":")) == 2:
        elapsed_time = f"0:{elapsed_time}"
    seconds = convert_elapsed_time_to_seconds(elapsed_time)
    episode_url_ts = f"https://www.youtube.com/watch?v={VIDEO_ID}?t={seconds}"
    print(episode_url_ts)
    return f"* [{match.group(0).split(' ')[1]}]({episode_url_ts})"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("You must supply a YT video ID.")
    VIDEO_ID = sys.argv[1]

    if len(sys.argv) > 2:
        EPISODE_DATE = sys.argv[2]
    else:
        EPISODE_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

    episode_file = Path(f"{EPISODE_DATE.split('-')[0]}/{EPISODE_DATE}.md")
    if episode_file.exists() is not True:
        raise ValueError(f"{episode_file} is not found.")
    process_episode(episode_file)
