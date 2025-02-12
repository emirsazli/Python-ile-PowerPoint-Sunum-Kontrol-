import random
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import pyaudio
import os
from selenium import webdriver


r=sr.Recognizer()

class SesliAsistan():
    def seslendirme(self,metin):
        xtts = gTTS(text = metin, lang="tr")
        dosya = "dosya"+str(random.randint(0,1234123412)) + ".mp3"
        xtts.save(dosya)
        playsound(dosya)
        os.remove(dosya)

asistan = SesliAsistan()
asistan.seslendirme("10.02.2025 Tarihinden Herkese Selamlar...")