# pylint: disable=anomalous-backslash-in-string
"""
    Using the YouTube API, get the lastest episode from a given playlist ID,
    generate show notes in a markdown file named YYYY\YYYY-MM-DD.md an submit
    them in a PR.
"""
from datetime import datetime, timedelta
from logging import error
import os
from pathlib import Path
import re
import time

import googleapiclient.discovery

# pylint: disable=anomalous-backslash-in-string
# Matches * #:##:## or * ##:## or * #:##
TIMESTAMP_PATTERN = re.compile("\d:\d\d:\d\d|\d\d:\d\d|\d:\d\d")
YT_BASE_URL = "https://www.youtube.com/watch?v="


def convert_elapsed_time_to_seconds(elapsed_time):
    """Converts a  string of elapsed time to seconds.

    params:
    self (Episode)
    elapsed_time (str)

    return:
    seconds (int)
    """
    _elapsed_time = time.strptime(elapsed_time, "%H:%M:%S")
    return int(
        timedelta(
            hours=_elapsed_time.tm_hour,
            minutes=_elapsed_time.tm_min,
            seconds=_elapsed_time.tm_sec,
        ).total_seconds()
    )


class Episode:
    """An Episode object."""

    def yt_ts_url_format(self, match):
        """Regex Replace (REPL) to go with substitute command

        params:
        self (Episode)
        match (regex match object)

        return:
        markdown bullet with timestamped YT url (str)
        """
        elapsed_time = match.group(0)
        if len(elapsed_time.split(":")) == 2:
            elapsed_time = f"0:{elapsed_time}"
        seconds = convert_elapsed_time_to_seconds(elapsed_time)
        episode_url_ts = f"{YT_BASE_URL}{self.episode_id}&t={seconds}"
        return f"- [{match.group(0)}]({episode_url_ts})"

    def format_thumbnail(self, resolution):
        """Create a markdown IMG from the available YT Thumbnails."""
        thumbnail = self.thumbnails[resolution]
        return f"![{self.title}]({thumbnail['url']} '{self.title}')"

    def __init__(self, episode_snippet):
        self.raw = episode_snippet
        self.episode_id = episode_snippet["resourceId"]["videoId"]
        self.date = datetime.fromisoformat(episode_snippet["publishedAt"][:-1])
        self.description = episode_snippet["description"]
        self.thumbnails = episode_snippet["thumbnails"]
        self.title = episode_snippet["title"].replace("#adafruit", "").strip()

        self.show_notes = re.sub(
            TIMESTAMP_PATTERN, self.yt_ts_url_format, self.description
        )
        self.path = Path(f"{self.date.year}/{self.date.date()}.md")
        self.thumbnail_markdown = self.format_thumbnail("standard")


def get_episode_from_playlist(yt_client, playlist_id):
    """Return an Episode Object for specified plauylist id"""
    request = yt_client.playlistItems().list(part="snippet", playlistId=playlist_id)
    response = request.execute()
    return Episode(response["items"][0]["snippet"])


def get_latest_playlist_episode(api_key, playlist_id):
    """Check for the latest episode in the provided playlist , and if the show
    notes do not already exist generate the show notes.
    """
    api_service_name = "youtube"
    api_version = "v3"

    yt_client = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    episode = get_episode_from_playlist(yt_client, playlist_id)

    if episode.path.exists() is not True:
        # Create folders if needed
        # pylint: disable-msg=E1101
        episode.path.parents[0].mkdir(parents=True, exist_ok=True)
        print(f"New show notes: {episode.path}")
        print(f"YouTube Video ID: {episode.episode_id}")
        with open(episode.path, "w", encoding="utf-8") as episode_file:
            episode_file.write(f"# {episode.title}\n\n")
            episode_file.write(f"{episode.thumbnail_markdown}\n\n")
            episode_file.write(episode.show_notes)
        return episode.path.as_posix()
    print(f"{episode.path} already exists.")
    return False


if __name__ == "__main__":
    try:
        API_KEY = os.getenv("YOUTUBE_API_KEY")
    except Exception as error:
        raise RuntimeError("YouTube API Key is required.") from error

    try:
        YOUTUBE_PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID")
    except Exception as error:
        raise RuntimeError("YouTube Playlist ID is required.") from error

    episode_notes = get_latest_playlist_episode(API_KEY, YOUTUBE_PLAYLIST_ID)
    if episode_notes:
        github_env = os.getenv("GITHUB_ENV")
        with open(github_env, "a", encoding="utf-8") as github_env_file:
            github_env_file.write(f"NEWFILE_PATH={episode_notes}")
