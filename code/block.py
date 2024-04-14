import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, position, block_size):
        """It sets image, rect class, coordinates and size of a block."""
        super().__init__()
        self.__Coordinates = position
        self.__Block_Size = block_size
        self.image = pygame.Surface((self.__Block_Size, self.__Block_Size))
        self.image.fill("#5EF38C")
        self.rect = self.image.get_rect(bottomleft=self.__Coordinates)