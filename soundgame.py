
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(r"C:\Users\BaoPhuc\Downloads\sound.mp3")

    def play_background_music(self, loops=-1):
        self.background_music.play(loops=loops)

    def stop_background_music(self):
        self.background_music.stop()
