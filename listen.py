#!/usr/bin/env python

"""
ListenBrainz listening for Pianobar, the command-line Pandora client.
Modified very gratefully from scrobble.py by Jon Pierce <jon@jonpierce.com> (Copyright (c) 2011)

Copyright (c) 2022
montdor <https://github.com/montdor/>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Dependencies:
1) https://github.com/PromyLOPh/pianobar/
2) https://python.org/
3) https://github.com/paramsingh/pylistenbrainz
4) https://listenbrainz.org/profile/ (User token)

Installation:
# 1) Copy this script to the Pianobar config directory, ~/.config/pianobar/,
#    and make sure this script is executable.
# 2) Supply your own ListenBrainz user token below.
# 3) Update Pianobar's config file to use this script as its event_command, or
#    as part of a multi.sh
"""

import sys
import time

AUTH_TOKEN = "#####################################"

THRESHOLD = 50  # the percentage of the song that must have been played to scrobble
PLAYED_ENOUGH = 240  # or if it has played for this many seconds
MIN_DURATION = 30  # minimum duration for a song to be "scrobblable"


def main():
    event = sys.argv[1]
    lines = sys.stdin.readlines()
    fields = dict([line.strip().split("=", 1) for line in lines])

    artist_name = fields["artist"]
    track_name = fields["title"]
    release_name = fields["album"]
    song_duration = int(fields["songDuration"])
    song_played = int(fields["songPlayed"])
    # rating = int(fields["rating"]) # This currently is unsupported by the
    # pylistenbrainz API

    import pylistenbrainz

    if (
        event == "songfinish"
        and song_duration > MIN_DURATION
        and (
            100.0 * song_played / song_duration > THRESHOLD
            or song_played > PLAYED_ENOUGH
        )
    ):
        song_started = int(time.time() - song_played)
        client = pylistenbrainz.ListenBrainz()
        listen = pylistenbrainz.Listen(
            track_name=track_name,
            artist_name=artist_name,
            release_name=release_name,
            listened_at=song_started,
        )
        client = pylistenbrainz.ListenBrainz()
        client.set_auth_token(AUTH_TOKEN)
        response = client.submit_single_listen(listen)


if __name__ in "__main__":
    main()
