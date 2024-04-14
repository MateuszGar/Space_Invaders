import pygame
from block import Block


class Obstacles:
    def __init__(self, screen_width, number_of_obstacles, block_size):
        """
        1: It sets shape of single obstacle and its size.
        1.2: It sets number of obstacles in a row and size of blocks which obstacles are build.
        2.1. It calculates coordinates on which obstacles will be placed.
        2.2: It initializes block group and adds blocks at certain coordinates.
        """
        # 1.1
        self.__Shape = ['   XXXXXXXX   ',
                        '  XXXXXXXXXX  ',
                        '  XXXXXXXXXX  ',
                        ' XXXXXXXXXXXX ',
                        ' XXXXXXXXXXXX ',
                        'XXXXXX  XXXXXX',
                        'XXXXX    XXXXX',
                        'XXXX      XXXX',
                        'XXXX      XXXX',
                        'XXX        XXX']
        self.__Shape_Size = (len(self.__Shape[0]), len(self.__Shape))
        # 1.2
        self.__Number_Of_Obstacles = number_of_obstacles
        self.__Block_Size = block_size
        # 2.1
        # Helpful variables to help position the obstacles at even intervals on the screen.
        Temporary_Interval = (screen_width -
                              self.__Number_Of_Obstacles * self.__Shape_Size[0] * self.__Block_Size) //\
                             (self.__Number_Of_Obstacles + 1)
        Shape_Size_Width_In_Pixels = self.__Shape_Size[0] * self.__Block_Size
        Interval = Temporary_Interval + Shape_Size_Width_In_Pixels
        self.__Coordinates_Of_Obstacles = [Temporary_Interval + (Shape_Size_Width_In_Pixels // 2) + i * Interval
                                           for i in range(self.__Number_Of_Obstacles)]
        # 2.2
        self.Blocks = pygame.sprite.Group()
        self.obstacles_initialize()

    def obstacles_initialize(self):
        """It initializes obstacles at certain coordinates."""
        Shape_reversed = list(reversed(self.__Shape))
        for balanced_x in self.__Coordinates_Of_Obstacles:
            for row_index in range(self.__Shape_Size[1]):
                for column_index in range(self.__Shape_Size[0]):
                    if Shape_reversed[row_index][column_index] == "X":
                        x = balanced_x + column_index * self.__Block_Size - ((self.__Shape_Size[0] // 2) * self.__Block_Size)
                        y = 520 - row_index * self.__Block_Size
                        block = Block((x, y), self.__Block_Size)
                        self.Blocks.add(block)

    def update(self):
        """It updates blocks group."""
        self.Blocks.update()

    def draw(self, screen):
        """It draws blocks group."""
        self.Blocks.draw(screen)