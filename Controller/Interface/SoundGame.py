import pygame

sound_folder = "Resource/Chess_Sound/"

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(sound_folder + "sound.mp3")
        self.move_sound = pygame.mixer.Sound(sound_folder + "chessmove.mp3")
        self.capture_sound = pygame.mixer.Sound(sound_folder +  "chess_capture.mp3")
        self.check_sound = pygame.mixer.Sound(sound_folder + "check.mp3")
    def playBackGroundMusic(self, loops=-1):
        self.background_music.play(loops=loops)
    def playMoveSound(self):
        self.move_sound.play()

    def stopBackgroundMusic(self):
        self.background_music.stop()
