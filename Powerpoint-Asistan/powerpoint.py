import random
import time
from gtts import gTTS
import pygame
import speech_recognition as sr
import os
import pyautogui  # Klavye simülasyonu için pyautogui kütüphanesini ekliyoruz
import tkinter as tk
from tkinter import messagebox

# Speech Recognition (Ses Tanıma) için 'r' nesnesini tanımlıyoruz
r = sr.Recognizer()  # Burada 'r' tanımlandı, böylece 'r.listen()' kullanılabilir.

# pygame'in mixer modülünü başlatıyoruz
pygame.mixer.init()

class SesliAsistan:
    def __init__(self, window):
        self.window = window
        self.sesli_asistan_acik = False  # Başlangıçta sesli asistan kapalı
        self.seslendirme("PowerPoint kontrolüne hoş geldiniz. Komutları bekliyorum.")

        # GUI Elemanları
        self.start_button = tk.Button(window, text="Sesli Asistanı Başlat", command=self.toggle_asistan, width=20, height=2)
        self.start_button.pack(pady=20)

        self.quit_button = tk.Button(window, text="Çıkış", command=window.quit, width=20, height=2)
        self.quit_button.pack(pady=20)

        self.ses_label = tk.Label(window, text="Sesli Komut Bekleniyor...", width=40)
        self.ses_label.pack(pady=10)

    def seslendirme(self, metin):
        # Sesli yanıt üretme fonksiyonu
        xtts = gTTS(text=metin, lang="tr")  # gTTS kullanarak metni sesli yanıt olarak oluşturuyoruz
        dosya = "dosya" + str(random.randint(0, 1234123412)) + ".mp3"
        xtts.save(dosya)

        # pygame ile ses dosyasını çalıyoruz
        pygame.mixer.music.load(dosya)
        pygame.mixer.music.play()

        # Ses çalmayı bitene kadar bekliyoruz
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Dosya çalmayı bitirdiği zaman, dosyayı silmek için biraz zaman ekliyoruz
        pygame.mixer.music.stop()

        # Ses dosyasını silmeden önce pygame'in bitmesini bekliyoruz
        try:
            os.remove(dosya)  # Ses dosyasını sildik
        except PermissionError:
            print(f"{dosya} dosyasını silerken hata oluştu. Dosya hala kullanılmakta.")

    def ses_kayit(self):
        # Mikrofonu dinleyip komut alıyoruz
        with sr.Microphone() as kaynak:
            print("Sizi dinliyorum..")
            try:
                # Dinleme süresi ve komut süresi
                listen = r.listen(kaynak, timeout=10, phrase_time_limit=5)  # Timeout değerini arttırdık
                voice = r.recognize_google(listen, language="tr-TR").lower()
                print(f"Algılanan ses: {voice}")
                return voice
            except sr.UnknownValueError:
                print("Ses algılanamadı.")
                return ""  # Sessiz mod: Yanıt vermeyecek
            except sr.WaitTimeoutError:
                print("Dinleme süresi aşıldı. Lütfen tekrar deneyin.")
                return ""  # Zaman aşımı hatası
            except sr.RequestError as e:
                print(f"Google API hatası: {e}")
                return ""  # Bağlantı hatasında da sessiz kalacak

    def ses_karsilik(self, gelen_ses):
        # PowerPoint komutlarına karşılık veren kısımlar:
        if "geç" in gelen_ses or "ileri git" in gelen_ses or "sonraki sayfaya git" in gelen_ses:
            self.seslendirme("Bir sonraki sayfaya geçiyorum...")
            pyautogui.press('right')  # Sağ ok tuşuna basarak bir sonraki sayfaya geçiş yapıyoruz
            self.ses_label.config(text="Bir sonraki sayfaya geçildi.")

        elif "geri gel" in gelen_ses or "önceki sayfaya git" in gelen_ses:
            self.seslendirme("Bir önceki sayfaya geri dönüyorum...")
            pyautogui.press('left')  # Sol ok tuşuna basarak bir önceki sayfaya geri dönüyoruz
            self.ses_label.config(text="Bir önceki sayfaya geri dönüldü.")

        elif "durdur" in gelen_ses or "slayt gösterisini durdur" in gelen_ses:
            self.seslendirme("Slayt gösterisini durduruyorum...")
            pyautogui.press('esc')  # Escape tuşu ile slayt gösterisini durduruyoruz
            self.ses_label.config(text="Slayt gösterisi durduruldu.")

        elif "başlat" in gelen_ses or "slayt gösterisini başlat" in gelen_ses:
            self.seslendirme("Slayt gösterisini başlatıyorum...")
            pyautogui.press('f5')  # F5 tuşuna basarak slayt gösterisini başlatıyoruz
            self.ses_label.config(text="Slayt gösterisi başlatıldı.")

        elif "kapat" in gelen_ses:
            self.seslendirme("Sesli asistanı kapatıyorum...")
            self.ses_label.config(text="Sesli asistan kapatılıyor...")
            exit()  # Asistanı kapatıyor

    def toggle_asistan(self):
        # Asistanı başlatma/durdurma fonksiyonu
        if not self.sesli_asistan_acik:
            self.sesli_asistan_acik = True
            self.start_button.config(text="Sesli Asistanı Durdur")
            self.seslendirme("Sesli asistan başlatıldı. Komutları bekliyorum.")
            while self.sesli_asistan_acik:
                ses = self.ses_kayit()
                if ses:  # Ses boş değilse
                    self.ses_karsilik(ses)
        else:
            self.sesli_asistan_acik = False
            self.start_button.config(text="Sesli Asistanı Başlat")
            self.seslendirme("Sesli asistan kapatıldı.")
            self.ses_label.config(text="Sesli Komut Bekleniyor...")


# GUI'yi başlatıyoruz
def main():
    window = tk.Tk()
    window.title("Sesli Asistan - PowerPoint Kontrolü")
    window.geometry("400x300")

    # Asistanı başlatıyoruz
    asistan = SesliAsistan(window)

    # GUI çalıştırılıyor
    window.mainloop()

if __name__ == "__main__":
    main()
