#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from urllib2 import quote, Request, build_opener
from pygame import mixer

class Voice:
    def __init__(self, fileFormat, api_key):
        self.api_key = api_key
        self.fileFormat = fileFormat
        self.lang = 'ru-RU'
        self.speaker = 'omazh'
        self.setting = {'robot':'true', 'normal':'false'}
        self.robot = self.setting['normal']
        self.speed = 1


    def say(self, emotion, text, play=1):
        text = quote(text.encode('utf-8'))
        url = 'http://tts.voicetech.yandex.net/generate?text='+ text +'&format=' + self.fileFormat +\
              '&robot=' +self.robot+ '&lang=' +self.lang+ '&emotion=' \
              +emotion+ '&speaker=' +self.speaker+ '&key=' + self.api_key
        request = Request(url)
        opener = build_opener()
        f = open("voiceSynthFile/say.mp3", "wb")
        f.write(opener.open(request).read())
        f.close()
        if play:
            mixer.init(16000, -16, self.speed, 2048)
            mixer.music.load("voiceSynthFile/say.mp3")
            mixer.music.play()
            while mixer.music.get_busy() == True:
                continue

    def voiceConfig(self, lang, speaker, option, speed):
        #self.lang = lang
        self.speaker = speaker
        self.robot = self.setting[option]
        self.speed = speed


    def playVoice(self):
        mixer.init(16000, -16, 1, 2048)
        mixer.music.load("voiceSynthFile/say.mp3")
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue
