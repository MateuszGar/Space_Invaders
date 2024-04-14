import pygame
from bullet import Bullet


class Object(pygame.sprite.Sprite):
    def __init__(self, coordinates, speed, screen_size):
        """
        1: It initializes image and rect class.
        2: It sets object's attributes like coordinates, speed and health.
        3: It sets bullet's sound.
        4: It sets object's bullet group.
        """
        self._Screen_Size = screen_size
        # 1
        super().__init__()
        # 2
        self._Coordinates = coordinates
        self._Speed = speed
        # 3
        self._Bullet_Sound = pygame.mixer.Sound("../resources/sounds/bullet_sound.wav")
        self._Bullet_Sound.set_volume(0.03)
        # 4
        self.Bullets = pygame.sprite.Group()

    def fire_bullet(self, shooter):
        """It fires a bullet. It adds bullet class to Bullets group."""
        if shooter == "Player":
            bullet = Bullet(self.rect.midtop, self._Coordinates[1], "Player")
        else:
            bullet = Bullet(self.rect.midbottom, self._Screen_Size[1], "Enemy")
        self._Bullet_Sound.play()
        self.Bullets.add(bullet)