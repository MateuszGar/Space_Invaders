import pygame
from object import Object


class Enemy(Object):
    def __init__(self, coordinates, model, speed, screen_size):
        """It sets enemy's sprite attributes and points value."""
        self.Points_Value = int(model)
        super().__init__(coordinates, speed, screen_size)
        # 1
        file_path = "../resources/images/" + model + ".png"
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect(bottomleft=self._Coordinates)

    def move(self, moving_down):
        """It moves an enemy in certain direction."""
        if not moving_down:
            if self._Speed > 0:
                if self.rect.right < self._Screen_Size[0]:
                    self.rect.x += self._Speed
            elif self._Speed < 0:
                if self.rect.left > 0:
                    self.rect.x += self._Speed
        else:
            self.rect.y += 2
            self._Speed *= -1

    def update(self, screen):
        """It updates enemy position, recharges enemy's bullet. Also updates Bullets group and draws it."""
        self.Bullets.update()
        self.Bullets.draw(screen)