# Deep Dive w/Scott

![Deep Dive w/Scott](images/deepdive.jpg)

## Schedule
Deep Dive happens every week. Normally Fridays at 2pm Pacific but occasionally shifted to Thursday at 2pm. Typically goes for two hours or more. Questions are welcome. Next week will be on Friday as well.

## Formatting Episodes notes with `add_yt_links.py`

The current scripts will look for the following patterns:
`* #:##:##` or `* ##:##` or `* #:##` to and turn them into links and add
Direct YT links to Timestamped Markdown Files.
Example YT URL: `https://www.youtube.com/watch?v=VIDEO_ID&t=seconds`

Examples:
`python add_yt_links VIDEO_ID`
>VIDEO_ID is the YT video parameter from the watch url v=VIDEO_ID
If episode_data is not supplied, today's date is used.

`python add_yt_links VIDEO_ID YYYY-MM-DD`
> VIDEO_ID is the YT video parameter from the watch url v=VIDEO_ID
Specify an EPISODE_DATE to process files for other dates.
