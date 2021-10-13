"""
    Add Direct YT links to Timestamped Markdown Files
    Example YT URL "https://www.youtube.com/watch?v=video_id&t=seconds"

    Example:
        python create_episode_notes video_id
            video_id is the YT video parameter from the watch url v=video_id
"""


import datetime
from pathlib import Path
import re
import sys
import time

import requests

# pylint: disable=anomalous-backslash-in-string
# Matches * #:##:## or * ##:## or * #:##
TIMESTAMP_PATTERN = re.compile("\d:\d\d:\d\d|\d\d:\d\d|\d:\d\d")
YT_BASE_URL = "https://www.youtube.com/watch?v="


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


def get_episode_from_yt(video_id):
    """Get the episode metadata from YT
    params:
    video_id (str): The ID of the YT Video

    return:
    episode (dict): Episode object wirh title, description and date
    """
    response = requests.get(f"{YT_BASE_URL}{video_id}")
    description_regex = r'"shortDescription":"(.*?)"'
    date_regex = r'"uploadDate":"(.*?)"'
    title_regex = r'"title":"(.*?)"'
    description_matches = re.search(description_regex, response.text)
    date_matches = re.search(date_regex, response.text)
    title_matches = re.search(title_regex, response.text)
    return {
        "date": date_matches.group(1),
        "description": description_matches.group(1).replace("\\n", "\n"),
        "title": title_matches.group(1).replace("#adafruit", ""),
    }


def process_episode_description(episode_notes):
    """
    params:
    episode_notes (Path): File to be processed and re-written
    """
    with episode_notes.open() as file:
        file_contents = file.read()
        file_contents = re.sub(TIMESTAMP_PATTERN, yt_timestamp_url_repl, file_contents)
        episode_notes.write_text(file_contents)


def yt_timestamp_url_repl(match):
    """Regex REPL to go with sub command
    Params:
    match (regex match object)
    Return:
    new string (str)
    """
    print(match.group)
    elapsed_time = match.group(0)
    if len(elapsed_time.split(":")) == 2:
        elapsed_time = f"0:{elapsed_time}"
    seconds = convert_elapsed_time_to_seconds(elapsed_time)
    episode_url_ts = f"{YT_BASE_URL}{YT_VIDEO_ID}&t={seconds}"
    print(episode_url_ts)
    return f"- [{match.group(0)}]({episode_url_ts})"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("You must supply a YT video ID.")
    YT_VIDEO_ID = sys.argv[1]
    episode = get_episode_from_yt(YT_VIDEO_ID)
    episode_path = Path(f"{episode['date'].split('-')[0]}/{episode['date']}.md")
    if episode_path.exists() is not True:
        with open(episode_path, "w", encoding="utf-8") as episode_file:
            episode_file.write(f"# {episode['title'].strip()}\n\n")
            episode_file.write(episode["description"])
        process_episode_description(episode_file)
    else:
        print(f"{episode_path} already exists.")
