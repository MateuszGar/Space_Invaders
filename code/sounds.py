import pygame


class Sounds:
    def __init__(self):
        """It sets background music and explosion sounds."""
        self.Background_Music = pygame.mixer.Sound("../resources/sounds/background_music.wav")
        self.Background_Music.play(-1)
        self.Background_Music.set_volume(0)
        self.Obstacles_Explosion_Sound = pygame.mixer.Sound("../resources/sounds/obstacles_explosion_sound.wav")
        self.Obstacles_Explosion_Sound.set_volume(0.1)
        self.Player_Explosion_Sound = pygame.mixer.Sound("../resources/sounds/player_explosion_sound.wav")
        self.Player_Explosion_Sound.set_volume(0.3)
        self.Enemy_Death_Sound = pygame.mixer.Sound("../resources/sounds/enemy_death_sound.wav")
        self.Enemy_Death_Sound.set_volume(0.1)
        self.Player_Death_Sound = pygame.mixer.Sound("../resources/sounds/player_death_sound.wav")
        self.Player_Death_Sound.set_volume(0.3)