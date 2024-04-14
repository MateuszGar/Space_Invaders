import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, screen_height, shooter):
        """
        1: It sets bullet's sprite attributes.
        2: It sets bullet's attributes.
        """
        super().__init__()
        self.Screen_Height = screen_height
        # 1
        self.image = pygame.Surface((4, 20))
        self.rect = self.image.get_rect(center=position)
        if shooter == "Player":
            self.image.fill("#B7FDFE")
        else:
            self.image.fill('white')
        # 2
        self.Speed = 8
        self.__Shooter = shooter

    def __annihilate(self):
        """It destroys bullet object."""
        if self.__Shooter == "Player":
            if self.rect.midbottom[1] < 0:
                self.kill()
        else:
            if self.rect.midtop[1] > self.Screen_Height:
                self.kill()

    def __move(self):
        """It moves bullet object."""
        if self.__Shooter == "Player":
            self.rect.y -= self.Speed
        else:
            self.rect.y += self.Speed

    def update(self):
        """It updates bullet object."""
        self.__move()
        self.__annihilate()