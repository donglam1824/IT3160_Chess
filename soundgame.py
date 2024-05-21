import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(r"Chess_Image/sound.mp3")
        self.move_sound = pygame.mixer.Sound(r"Chess_Image/chessmove.mp3")
    def play_background_music(self, loops=-1):
        self.background_music.play(loops=loops)
    def play_move_sound(self):
        self.move_sound.play()

    def stop_background_music(self):
        self.background_music.stop()
