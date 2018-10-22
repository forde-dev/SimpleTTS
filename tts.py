"""
Name: tts.py
Description: This program will read what ever is selected on the screen
Author: Michael Forde
"""

# Imports
from gtts import gTTS
from pydub import AudioSegment, playback
import os
import eyed3
import yaml
import time

# Configs
"""
In the _settings.yml file I have assigned 4 settings
    lang: -  this is for the language you want it to play - e.g en for english
    mp3name: - this if for the name of the file you want it to save - e.g temptts for temptts.mp3
    playspeed: - this is the play speed of the file - e.g 1 for normal speed
    version: - this is the version of this program - e.g 0.0.1 for first version
"""
with open("_settings.yml", 'r') as yml:
    cfg = yaml.load(yml)


class Text:
    """
    for the Text class there is one attribute
    _text - string - this uses a feature called xsel to capture the current highlighted text
    """
    def __init__(self):
        self._text = os.popen('xsel').read()

    # when called this returns _text
    def getText(self):
        return self._text

class GttsCall:
    """
    for the GttsCall class there is 3 attributes
    _text - string - this requests the text from the Text class
    _lang - string - this collects the lang config from the _settings.yml
    _gtts - audio object - this sends text and receives the audio object from googles api
    """
    def __init__(self):
        self._text = Text().getText()
        self._lang = cfg['lang']
        self._gtts = None

    # this gets the language used
    def getLang(self):
        return self._lang

    # this sets the languages
    # TODO: make this edit the _settings.yml file
    def setLang(self, lang):
        self._lang = lang
        return self._lang

    # this sends text to googles tts api
    def gTTS(self):
        self._gtts = gTTS(text=self._text, lang=self._lang)
        return self._gtts

class Mp3:
    """
    for the Mp3 class there is 4 attributes
    _gtts - audio object- this request from the GttsCall class
    _filename - string - this is set by the config file and assigns it
    _length - float - this is used to store the duration of the mp3 thats playing
    _playspeed - float - this is used to determine how fast the mp3 file will be played, also set from _settings.yml
    """
    def __init__(self):
        self._gtts = GttsCall().gTTS()
        self._filename = cfg['mp3name']
        self._length = 0.0
        self._playspeed = float(cfg['playspeed'])

    # this function saves the mp3 file made from the google tts lib, it send shifts the playback speed of the file based
    # on the playspeed setting in the _settings.yml
    def saveMp3(self):
        self._gtts.save('%s.mp3' % self._filename)

        def speed_swifter(sound, speed=1.0):
            sound_out = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
            return sound_out

        sound = AudioSegment.from_mp3('%s.mp3' % self._filename)
        sound_playspeed = speed_swifter(sound, self._playspeed)

        sound_playspeed.export(os.path.join('%s.mp3' % self._filename), format="mp3")

    # this returns the duration of the mp3 file
    def getLength(self):
        self._length = eyed3.load('%s.mp3' % self._filename).info.time_secs
        return self._length

    # TODO: fix the following 3 functions

    # this speeds up the playback speed
    def speedUp(self):
        """
        with open("_settings.yml", 'w') as cyml:
            change = yaml.load(cyml)
        update = self._playspeed + 0.1
        self._playspeed = update
        change['playspeed'] = str(update)
        cyml.close()
        return self._playspeed
        """
        pass

    # this slows down the playback speed
    def speedDown(self):
        """
        with open("_settings.yml", 'w') as cyml:
            change = yaml.load(cyml)
        update = self._playspeed - 0.1
        self._playspeed = update
        change['playspeed'] = str(update)
        cyml.close()
        return self._playspeed
        """
        pass

    # this sets the playback speed to a certain value
    def setSpeed(self, speed):
        """
        with open("_settings.yml", 'w') as cyml:
            change = yaml.load(cyml)
        update = speed
        self._playspeed = update
        change['playspeed'] = str(update)
        cyml.close()
        return self._playspeed
        """
        pass

    # this plays the text highlighted
    def playText(self):
        self.saveMp3()
        sound = AudioSegment.from_mp3('%s.mp3' % self._filename)
        playback.play(sound)
        time.sleep(self._length + 1)

    # this repeats the playText, or the last mp3 file
    def repeatPlay(self):
        sound = AudioSegment.from_mp3('%s.mp3' % self._filename)
        playback.play(sound)
        time.sleep(self._length + 1)

    # TODO: add a stop playing function

# this closes the config file
yml.close()

# this is only ran if the sript is ran directly
if __name__ == '__main__':
    s = Text()
    g = GttsCall()
    m = Mp3()


    #text = 'string'

    #s.setText(text)
    print(s.getText())
    m.playText()



