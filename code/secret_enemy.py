from random import randint
import pygame
from object import Object


class Secret_Enemy(Object):
    def __init__(self, screen_size, speed):
        """It sets secret enemy's sprite attributes and points value."""
        self.__SECRET_ENEMY_COOLDOWN = pygame.USEREVENT + 1
        self.Points_Value = 100
        if speed > 0:
            super().__init__((-40, 104), speed, screen_size)
        else:
            super().__init__((screen_size[0], 104), speed, screen_size)
        self.image = pygame.image.load("../resources/images/100.png")
        self.rect = self.image.get_rect(bottomleft=self._Coordinates)

    def annihilate(self):
        """It annihilates a secret enemy."""
        random_time = randint(20 * 1000, 30 * 1000)
        pygame.time.set_timer(self.__SECRET_ENEMY_COOLDOWN, random_time)
        self.kill()

    def __move(self):
        """It moves a secret enemy."""
        if self.rect.right < 0 or self.rect.left > self._Screen_Size[0]:
            self.annihilate()
        else:
            self.rect.x += self._Speed

    def update(self):
        """It updates a secret enemy."""
        self.__move()