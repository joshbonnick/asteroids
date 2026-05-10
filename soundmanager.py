import pygame
from singleton import singleton

@singleton
class SoundManager:
    def __init__(self):
        self.sounds = {
            "shoot": "assets/sfx/laser.ogg",
            "hit": "assets/sfx/hit.ogg",
            "game_over": "assets/sfx/lose.ogg",
        }

    def shoot(self):
        self.__play(self.sounds["shoot"])

    def hit(self):
        self.__play(self.sounds["hit"], 0.1)

    def game_over(self):
        self.__stop()
        self.__play(self.sounds["game_over"])

    def __stop(self):
        pygame.mixer.stop()

    def __play(self, sound, volume=1.0):
        sound = pygame.mixer.Sound(sound)
        sound.set_volume(volume)
        sound.play()