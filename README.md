# SimpleTTS
This is a simple tts that i have quickly pulled together for use on my main linux computer.

This script is designed to be called from a keyboard shortcut. You can bind 'simpletts -x' to
the shortcut key 'F8', and when pressed all selected text will be processed and sent to google's 
Text to Speech service. If 'F8' is pressed again, then the selected text will be queued up to be played after the
current request is finished. You can also map 'simpletts -s' to a key to stop it speeking.

# How to use
To use this program, you must first have the below modules installed.

  --> gTTS
  
  --> mpv

# Install
pip install git+https://github.com/willforde/SimpleTTS

# Command-line arguments::

    usage: simpletts [-h] [-t TEXT] [-s] [-x] [--version]
    
    Simple text to speech with google TTS.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TEXT, --text TEXT  Text to send to google TTS.
      -s, --stop            Stop playback of TTS if already running
      -x, --xsel            Fetch selected text using 'xsel', and send it to
                            google TTS.
      --version             The version number for this script.
