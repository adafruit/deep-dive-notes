# Deep Dive w/Scott

![Deep Dive w/Scott](images/deepdive.jpg)

## Schedule
Deep Dive happens every week. Normally Fridays at 2pm Pacific but occasionally
shifted to Thursday at 2pm. Typically goes for two hours or more. Questions are
welcome.

## Show Notes GitHub Action
The GitHub Action uses a Google API Key stored as a GitHub Secret.

With this api key, and the playlist ID in the action, the GitHub Action runs on
a schedule, checks for a new episode in the playlist and if there are no show
notes that episode it scrapes them out of the API response, formats them into
markdown and creates a PR with the new show notes.
