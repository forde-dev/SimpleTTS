"""
Name: tts.py
Description: This program will read what ever is selected on the screen
Author: Michael Forde
"""

# Imports
from gtts import gTTS
from pydub import AudioSegment
import os
import eyed3
import yaml
import time

#import vlc



# Configs
with open("_settings.yml", 'r') as yml:
    cfg = yaml.load(yml)

class Text:

    def __init__(self):
        self._text = os.popen('xsel').read()

    def getText(self):
        return self._text

class GttsCall:

    def __init__(self):
        self._text = Text().getText()
        self._lang = cfg['lang']
        self._gtts = None

    def getLang(self):
        return self._lang

    def setLang(self, lang):
        self._lang = lang
        return self._lang

    def gTTS(self):
        self._gtts = gTTS(text=self._text, lang=self._lang)
        return self._gtts

class Mp3:

    def __init__(self):
        self._gtts = GttsCall().gTTS()
        self._filename = cfg['mp3name']
        self._length = None
        self._playspeed = cfg['playspeed']

    def saveMp3(self):
        self._gtts.save('%s.mp3' % self._filename)


    def getLength(self):
        self._length = eyed3.load("tts.mp3").info.time_secs
        return self._length






if __name__ == '__main__':
    s = Text()
    g = GttsCall()
    m = Mp3()


    #text = 'string'

    #s.setText(text)
    print(s.getText())
    m.saveMp3()

