#!/usr/bin/env python

"""
Name: simpletts.py
Description: This program will read what ever is selected on the screen
Author: Michael Forde
"""

# Standard library imports
import subprocess
import threading
import tempfile
import argparse
import typing
import socket
import base64
import queue
import json
import sys
import os

# Third party imports
import gtts

__version__ = "0.0.1"

# PyAudio data buffer size
CHUNK = 1024

# Text queue to store selected
# text for later playback
text_queue = queue.Queue()

# Server Unix socket
server_soc = os.path.join(tempfile.gettempdir(), "simpletts.socket")

# Flag that triggers termination of the player
STOP = False


def send_request(soc: socket.socket, request: typing.Dict[str, str]):
    """Convert a string of text to base64 encoded json object."""
    json_data = json.dumps(request)
    raw_req = base64.b64encode(json_data.encode("utf8"))
    soc.sendall(raw_req)


def receive_request(conn: socket.socket) -> typing.Dict[str, str]:
    """Takes a socket connection and retrieve all incoming data and return json object."""
    chucks = []
    while True:
        # Retrieve data chuck
        datagram = conn.recv(1024)
        if datagram:
            chucks.append(datagram)
        else:
            # No more data left to read
            break

    # Reconstruct base64 data
    data = b"".join(chucks)
    raw_data = base64.b64decode(data)
    return json.loads(raw_data.decode("utf8"))


def unix_server():
    """Start a UDS server to listen for requests."""
    # Remove left over socket file if one exists
    if os.path.exists(server_soc):
        os.unlink(server_soc)

    # Create a UDS(Unix Domain Socket)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_soc)
    sock.listen(1)

    try:
        while True:
            # Wait for a connection
            connection, _ = sock.accept()

            try:
                # Handle request from client
                request = receive_request(connection)

                # Text to be converted to speech
                if request["command"] == "text":
                    text_queue.put(request["data"])

                # Stop Speeking
                elif request["command"] == "stop":
                    global STOP
                    STOP = True
                    break

            finally:
                # Make sure that the connection is always closed
                connection.close()

    finally:
        # Make sure that the server connection is closed
        os.unlink(server_soc)
        sock.close()


def communicate() -> typing.Union[bool, socket.socket]:
    """Check if this script is already running, and return connection to that script."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(server_soc)
    except (FileNotFoundError, ConnectionRefusedError):
        return False
    else:
        return sock


def speek(text: str):
    # Start the comunication server
    t1 = threading.Thread(target=unix_server, daemon=True)
    t1.start()

    text_queue.put(text)
    # Loop until text queue is empty
    while STOP is False and not text_queue.empty():
        text = text_queue.get()

        # Send text to google's text to speech service
        tts = gtts.gTTS(text, lang="en")

        # Start a mpv process and send output from gtts to stdin of the mpv process
        # This saves from having to download the whole file before playing,
        # as mpv will start playing as soon as the first bytes are received
        mpv_process = subprocess.Popen(["mpv", "-"], stdin=subprocess.PIPE)
        tts.write_to_fp(mpv_process.stdin)
        mpv_process.stdin.close()

        # Wait for the mpv process to finish playing before continuing
        # Or terminate the mpv process if the stop request was received
        while mpv_process.poll() is None:
            if STOP:
                mpv_process.terminate()
                break

        text_queue.task_done()


def parse_args() -> argparse.Namespace:
    """Parse program arguments."""
    parser = argparse.ArgumentParser(description="Simple text to speech with google TTS.")
    parser.add_argument("-t", "--text", action="store",
                        help="Text to send to google TTS.")
    parser.add_argument("-s", "--stop", action="store_true",
                        help="Stop playback of TTS if already running")
    parser.add_argument("-x", "--xsel", action="store_true",
                        help="Fetch selected text using 'xsel', and send it to google TTS.")
    parser.add_argument("--version", action="store_true",
                        help="The version number for this script.")
    return parser.parse_args(sys.argv[1:] if sys.argv[1:] else ["-h"])


def main():
    # Parse program arguments
    cli_args = parse_args()

    # Check if script is already running
    running_soc = communicate()

    if cli_args.text or cli_args.xsel:
        if cli_args.text:
            text = cli_args.text
            if text == "-":
                text = sys.stdin.read()
        else:
            text = subprocess.run("xsel", stdout=subprocess.PIPE, check=True, encoding="utf8").stdout

        if text:
            if running_soc:
                request = {"command": "text", "data": text}
                send_request(running_soc, request)
            else:
                speek(text)

    elif cli_args.stop and running_soc:
        request = {"command": "stop"}
        send_request(running_soc, request)

    elif cli_args.version:
        print("Simple TTS {}".format(__version__))


if __name__ == "__main__":
    main()
