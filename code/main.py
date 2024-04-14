import pygame
import sys
from game import Game

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()

    # Changing game window title and game window icon
    Icon = pygame.image.load("../resources/images/icon.png")
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(Icon)

    # Creating game class
    game = Game((SCREEN_WIDTH, SCREEN_HEIGHT))
    welcome_screen = True
    game.welcome_screen()

    while not game.Is_Game_Over:

        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_p]:
            welcome_screen = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game.Is_Game_Over = True
        if not welcome_screen:
            game.run()

        clock.tick(60)