"""
Name: tts.py
Description: This program will read what ever is selected on the screen
Author: Michael Forde
"""
from gtts import gTTS
import os
import vlc
import time
import eyed3

# this captures the 'xsel'(what i have selected on the screen) and reads it and assigns it to ttstext
ttstext = os.popen('xsel').read()

#print(ttstext)

# this uses the gTTS module to take the ttstext and send it to google API
tts = gTTS(text=ttstext, lang='en')

# this takes the google API translation as a mp3 file and saves it as tts
tts.save('tts.mp3')

# this uses eyed3 to inspect the tts file to gather the lenght of it
duration = eyed3.load("tts.mp3").info.time_secs

# this plays the mp3 file
sound_file = vlc.MediaPlayer("tts.mp3")
sound_file.play()

# this uses the duration from above and keeps the py script running for the lenght of time the mp3 plays
time.sleep(duration + 1)



