import pygame


class Scoreboard:
    def __init__(self, screen, screen_size):
        """
        1: It sets value of a scoreboard and its coordinates. It sets a screen on which scoreboard will be updated.
        2: It sets font and sizes of normal scoreboard and game over font.
        3: It opens a highscore.txt file and sends its content to variable.
        """
        # 1
        self.__Value = 0
        self.__Coordinates = [10, 15]
        self.__Screen_Size = screen_size
        self.__Screen = screen
        # 2
        FONT = '../resources/font/RenogareSoft-Regular.ttf'
        self.__FONT_COLOR = 'white'
        self.__FONT_SIZE = 22
        self.__Score_Font = pygame.font.Font(FONT, self.__FONT_SIZE)
        self.__Game_Over_Font = pygame.font.Font(FONT, 64)
        # 3
        with open("../save/highscore.txt", "r") as highscore:
            self.__High_Score = int(highscore.read())

    def draw(self):
        """It updates a score text on a screen."""
        Score = self.__Score_Font.render(f"Score: {self.__Value}", True, self.__FONT_COLOR)
        High_Score = self.__Score_Font.render(f"High Score: {self.__High_Score}", True, self.__FONT_COLOR)

        S_Coordinates = (self.__Coordinates[0], self.__Coordinates[1])
        HS_Coordinates = (self.__Coordinates[0], self.__Coordinates[1] + self.__FONT_SIZE)

        self.__Screen.blit(Score, Score.get_rect(topleft=S_Coordinates))
        self.__Screen.blit(High_Score, High_Score.get_rect(topleft=HS_Coordinates))

    def game_over(self):
        """It initializes game over text and places it on a screen."""
        Game_Over_Caption = self.__Game_Over_Font.render(f"GAME OVER", True, self.__FONT_COLOR)
        Restart_Caption = self.__Score_Font.render(f"To play again, press R key.", True, self.__FONT_COLOR)
        Quit_Caption = self.__Score_Font.render(f"To quit game, press ESC key.", True, self.__FONT_COLOR)

        GO_Coordinates = (self.__Screen_Size[0] // 2, self.__Screen_Size[1] // 2)
        R_Coordinates = (self.__Screen_Size[0] // 2, (self.__Screen_Size[1] // 2) + 64)
        Q_Coordinates = (self.__Screen_Size[0] // 2, (self.__Screen_Size[1] // 2) + 88)

        self.__Screen.blit(Game_Over_Caption, Game_Over_Caption.get_rect(center=GO_Coordinates))
        self.__Screen.blit(Restart_Caption, Restart_Caption.get_rect(center=R_Coordinates))
        self.__Screen.blit(Quit_Caption, Quit_Caption.get_rect(center=Q_Coordinates))

    def reset_value(self):
        """It resets value after game is over and player wants to play again."""
        self.__Value = 0

    def __overwrite_high_score(self):
        """It overwrites a high score."""
        with open("../save/highscore.txt", "w") as highscore:
            highscore.write(f"{self.__High_Score}")

    def increase_score(self, value):
        """It increases a score."""
        self.__Value += value
        if self.__Value > self.__High_Score:
            self.__High_Score = self.__Value
            self.__overwrite_high_score()
        self.draw()