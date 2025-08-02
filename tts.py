#! /usr/bin/env python3
import edge_tts
import subprocess
import time
import threading
import sys

###########
# globals #
###########

VOICE = "en-US-AvaNeural"
PITCH = "+20Hz"
RATE  = "+10%"
# RATE  = "+100%"

###############
# mpv process #
###############

mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--", "fd://0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        )

def close_tts():
    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()


def read_text(text):
    communicator = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE)

    for chunk in communicator.stream_sync():
        if chunk["type"] == "audio" and chunk["data"]:
            mpv_process.stdin.write(chunk["data"])
            mpv_process.stdin.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Argument provided, read it
        read_text(sys.argv[1])
    else:
        # No argument, read from stdin
        read_text(sys.stdin.read().strip())

    close_tts()
