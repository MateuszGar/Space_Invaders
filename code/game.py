import pygame
from scoreboard import Scoreboard
from player import Player
from obstacles import Obstacles
from army import Army
from sounds import Sounds


class Game:
    def __init__(self, screen_size):
        """
        1: It creates game screen.
        2: It creates player class and initializing it with sprite.GroupSingle.
        3: It creates obstacles class.
        4: It creates army class.
        5: It creates scoreboard class.
        6: It flags that give information if game is over.
        7: It creates sounds class.
        """
        # 1
        self.__Screen_Size = screen_size
        self.__Screen = pygame.display.set_mode((self.__Screen_Size[0], self.__Screen_Size[1]))
        # 2
        self.__Player_Sprite = Player(self.__Screen_Size)
        self.__Player = pygame.sprite.GroupSingle(self.__Player_Sprite)
        # 3
        self.__Obstacles = Obstacles(self.__Screen_Size[1], 4, 6)
        # 4
        self.__Army = Army(self.__Screen_Size, 70, 8)
        # 5
        self.__Scoreboard = Scoreboard(self.__Screen, self.__Screen_Size)
        # 6
        self.Is_Game_Over = False
        # 7
        self.__Sounds = Sounds()

    def run(self):
        """This function is main game engine. Here everything is getting updated and drawn."""
        self.__Sounds.Background_Music.set_volume(0.04)
        self.__update()
        self.__draw()
        self.__collisions()
        pygame.display.flip()

    def __update(self):
        """It updates objects in a whole game."""
        self.__Screen.fill((30, 30, 30))
        self.__Player.update(self.__Screen)
        if len(self.__Army.Enemies) == 0:
            self.__Obstacles.Blocks.empty()
            self.__Obstacles.obstacles_initialize()
            self.__Player_Sprite.increase_health()
        self.__Obstacles.update()
        self.__Army.update(self.__Screen)

    def __draw(self):
        """It draws objects on screen."""
        self.__Player.draw(self.__Screen)
        self.__Army.draw(self.__Screen)
        self.__Obstacles.draw(self.__Screen)
        self.__health_board_draw()
        self.__Scoreboard.draw()

    def __collisions(self):
        """It checks if objects get shot down."""
        # Player's bullets vs Army, Secret Enemy and Obstacles
        for bullet in iter(self.__Player_Sprite.Bullets):
            shoot_down_enemies = pygame.sprite.spritecollide(bullet, self.__Army.Enemies, True)
            if shoot_down_enemies:
                for enemy in iter(pygame.sprite.Group(shoot_down_enemies)):
                    enemy_value = enemy.Points_Value
                    self.__Sounds.Enemy_Death_Sound.play()
                    self.__Scoreboard.increase_score(enemy_value)
                bullet.kill()
            shoot_down_secret_enemy = pygame.sprite.spritecollide(bullet, self.__Army.Secret_Enemy, True)
            if shoot_down_secret_enemy:
                for secret_enemy in iter(pygame.sprite.Group(shoot_down_secret_enemy)):
                    secret_enemy_value = secret_enemy.Points_Value
                    self.__Sounds.Enemy_Death_Sound.play()
                    self.__Scoreboard.increase_score(secret_enemy_value)
                bullet.kill()
            if pygame.sprite.spritecollide(bullet, self.__Obstacles.Blocks, True):
                self.__Sounds.Obstacles_Explosion_Sound.play()
                bullet.kill()
        # Army's bullets vs Player and Obstacles
        for enemy in iter(self.__Army.Enemies):
            if enemy.rect.bottom > 536:
                self.__Sounds.Player_Death_Sound.play()
                self.__game_over_screen()
            for bullet in iter(enemy.Bullets):
                if pygame.sprite.spritecollide(bullet, self.__Player, False):
                    self.__Player_Sprite.damage("normal")
                    self.__Sounds.Player_Explosion_Sound.play()
                    if self.__Player_Sprite.get_health() == 0:
                        self.__Sounds.Player_Death_Sound.play()
                        self.__game_over_screen()
                    bullet.kill()
                if pygame.sprite.spritecollide(bullet, self.__Obstacles.Blocks, True):
                    self.__Sounds.Obstacles_Explosion_Sound.play()
                    bullet.kill()
        # Army vs Player and Obstacles
        for enemy in iter(self.__Army.Enemies):
            if pygame.sprite.spritecollide(enemy, self.__Player, False):
                self.__Player_Sprite.damage("enemy touch")
                self.__Sounds.Player_Death_Sound.play()
                self.__game_over_screen()
            if pygame.sprite.spritecollide(enemy, self.__Obstacles.Blocks, True):
                self.__Sounds.Obstacles_Explosion_Sound.play()

    def __health_board_draw(self):
        """It draws health board."""
        Interval = self.__Player_Sprite.image.get_size()[0] + 10
        Starting_Coordinates = [self.__Screen_Size[0] - Interval * self.__Player_Sprite.get_health(), 10]
        Health_Font = pygame.font.Font('../resources/font/RenogareSoft-Regular.ttf', 24)
        self.__Screen.blit(Health_Font.render("Lives: ", True, 'white'),
                           (Starting_Coordinates[0] - 80, Starting_Coordinates[1] + 20))
        for live in range(self.__Player_Sprite.get_health()):
            x = Starting_Coordinates[0] + live * Interval
            self.__Screen.blit(self.__Player_Sprite.image, (x, Starting_Coordinates[1]))

    def welcome_screen(self):
        """It shows welcome screen with enemy points and instructions."""
        Welcome_Font = pygame.font.Font('../resources/font/RenogareSoft-Regular.ttf', 24)
        Start_x_Coordinate = self.__Screen_Size[0] // 2
        Start_y_Coordinate = self.__Screen_Size[1] // 6
        Interval = (90, 40)
        Helpful_Height = 210

        Enemy_100 = pygame.image.load("../resources/images/100.png")
        Enemy_30 = pygame.image.load("../resources/images/30.png")
        Enemy_20 = pygame.image.load("../resources/images/20.png")
        Enemy_10 = pygame.image.load("../resources/images/10.png")

        Play_Caption = Welcome_Font.render("PLAY", True, 'white')
        Space_Invaders_Caption = Welcome_Font.render("SPACE INVADERS", True, 'white')
        Points_Caption = Welcome_Font.render("POINTS:", True, 'white')
        Points_Enemy_100 = Welcome_Font.render("= ??? POINTS", True, 'white')
        Points_Enemy_30 = Welcome_Font.render("= 30 POINTS", True, 'white')
        Points_Enemy_20 = Welcome_Font.render("= 20 POINTS", True, 'white')
        Points_Enemy_10 = Welcome_Font.render("= 10 POINTS", True, 'white')
        Instruction_1_Caption = Welcome_Font.render("To play, press P key.", True, 'white')
        Instruction_2_Caption = Welcome_Font.render("To quit game, press ESC key.", True, 'white')
        Instruction_3_Caption = Welcome_Font.render("To move player, press arrows keys.", True, 'white')
        Instruction_4_Caption = Welcome_Font.render("To shoot a bullet, press Space key.", True, 'white')

        P_Coordinates = (Start_x_Coordinate, Start_y_Coordinate - 60)
        SI_Coordinates = (Start_x_Coordinate, Start_y_Coordinate)
        Enemy_100_Coordinates = (Start_x_Coordinate - Interval[0], Helpful_Height)
        Enemy_30_Coordinates = (Start_x_Coordinate - Interval[0], Helpful_Height + Interval[1])
        Enemy_20_Coordinates = (Start_x_Coordinate - Interval[0], Helpful_Height + 2 * Interval[1])
        Enemy_10_Coordinates = (Start_x_Coordinate - Interval[0], Helpful_Height + 3 * Interval[1])
        I1_Coordinates = (Start_x_Coordinate, self.__Screen_Size[1] - 200)
        I2_Coordinates = (Start_x_Coordinate, self.__Screen_Size[1] - 200 + 48)
        I3_Coordinates = (Start_x_Coordinate, self.__Screen_Size[1] - 200 + 48 * 2)
        I4_Coordinates = (Start_x_Coordinate, self.__Screen_Size[1] - 200 + 48 * 3)

        self.__Screen.blit(Play_Caption, Play_Caption.get_rect(center=P_Coordinates))
        self.__Screen.blit(Space_Invaders_Caption, Space_Invaders_Caption.get_rect(center=SI_Coordinates))
        self.__Screen.blit(Points_Caption, Points_Caption.get_rect(center=(Start_x_Coordinate, Helpful_Height - 40)))
        self.__Screen.blit(Points_Enemy_100,
                           Points_Enemy_100.get_rect(center=(Start_x_Coordinate + 20, Enemy_100_Coordinates[1])))
        self.__Screen.blit(Points_Enemy_30,
                           Points_Enemy_30.get_rect(center=(Start_x_Coordinate + 20, Enemy_30_Coordinates[1])))
        self.__Screen.blit(Points_Enemy_20,
                           Points_Enemy_20.get_rect(center=(Start_x_Coordinate + 20, Enemy_20_Coordinates[1])))
        self.__Screen.blit(Points_Enemy_10,
                           Points_Enemy_10.get_rect(center=(Start_x_Coordinate + 20, Enemy_10_Coordinates[1])))
        self.__Screen.blit(Enemy_100, Enemy_100.get_rect(center=Enemy_100_Coordinates))
        self.__Screen.blit(Enemy_30, Enemy_30.get_rect(center=Enemy_30_Coordinates))
        self.__Screen.blit(Enemy_20, Enemy_20.get_rect(center=Enemy_20_Coordinates))
        self.__Screen.blit(Enemy_10, Enemy_10.get_rect(center=Enemy_10_Coordinates))
        self.__Screen.blit(Instruction_1_Caption, Instruction_1_Caption.get_rect(center=I1_Coordinates))
        self.__Screen.blit(Instruction_2_Caption, Instruction_2_Caption.get_rect(center=I2_Coordinates))
        self.__Screen.blit(Instruction_3_Caption, Instruction_3_Caption.get_rect(center=I3_Coordinates))
        self.__Screen.blit(Instruction_4_Caption, Instruction_4_Caption.get_rect(center=I4_Coordinates))
        pygame.display.update()

    def __game_over_screen(self):
        """It shows game over screen after player's death."""
        self.__Screen.fill((30, 30, 30))
        self.__Scoreboard.game_over()
        self.__Scoreboard.draw()
        self.__Sounds.Background_Music.stop()
        pygame.display.update()
        while True:
            if pygame.key.get_pressed()[pygame.K_r]:
                for i in range(3 - self.__Player_Sprite.get_health()):
                    self.__Player_Sprite.increase_health()
                self.__Obstacles.Blocks.empty()
                self.__Obstacles.obstacles_initialize()
                self.__Army.Enemies.empty()
                self.__Army.army_initialize()
                self.__Sounds.Background_Music.play(-1)
                self.__Scoreboard.reset_value()
                break
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.Is_Game_Over = True
                break