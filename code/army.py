from enemy import Enemy
from secret_enemy import Secret_Enemy
from random import randint, choice
import pygame


class Army:
    def __init__(self, screen_size, border, number_of_enemies_in_a_row):
        """
        1: It sets number of enemies in a row and screen size.
        2.1: It calculates coordinates on which enemies will be placed.
        2.2: It sets enemies speed and initializes enemies group.
        3: It sets bullet attributes.
        4: It sets secret enemy class and cooldown variable for respawning.
        5: It adds enemies at certain coordinates.
        """
        # 1
        self.__Number_of_Enemies_In_A_Row = number_of_enemies_in_a_row
        self.__Screen_Size = screen_size
        # 2.1
        Interval = (self.__Screen_Size[0] - 2 * border - self.__Number_of_Enemies_In_A_Row * 40) // \
                   (self.__Number_of_Enemies_In_A_Row - 1)
        self.__Coordinates_Of_Enemies = [border + i * (Interval + 40) for i in range(self.__Number_of_Enemies_In_A_Row)]
        # 2.2
        self.__Base_Speed = 2
        self.__Speed = self.__Base_Speed
        self.Enemies = pygame.sprite.Group()
        # 3
        self.__Ready_To_Fire = True
        self.__Bullet_Lifetime = 0
        self.__Bullet_Cooldown = 800
        # 4
        self.__SECRET_ENEMY_COOLDOWN = pygame.USEREVENT + 1
        self.Secret_Enemy = pygame.sprite.GroupSingle()
        # 5
        self.army_initialize()

    def army_initialize(self):
        """It initializes an army."""
        random_time = randint(15 * 1000, 25 * 1000)
        pygame.time.set_timer(self.__SECRET_ENEMY_COOLDOWN, random_time)
        for a in range(5, -1, -1):
            if a <= 1:
                model = "30"
            elif a <= 3:
                model = "20"
            else:
                model = "10"
            for b in self.__Coordinates_Of_Enemies:
                x = b
                y = 154 + a * 40
                enemy = Enemy((x, y), model, self.__Speed, self.__Screen_Size)
                self.Enemies.add(enemy)

    def __move(self):
        """It moves an army."""
        is_normal_move = True
        if self.__Speed != 0:
            for enemy in iter(self.Enemies):
                if self.__Speed > 0:
                    if enemy.rect.right + self.__Speed > self.__Screen_Size[0]:
                        self.__Speed *= -1
                        is_normal_move = False
                        break
                elif self.__Speed < 0:
                    if enemy.rect.left + self.__Speed < 0:
                        self.__Speed *= -1
                        is_normal_move = False
                        break
            for enemy in iter(self.Enemies):
                if is_normal_move:
                    enemy.move(False)
                else:
                    enemy.move(True)

    def __recharge_bullet(self):
        """It recharges bullet fired by enemy."""
        if not self.__Ready_To_Fire:
            Current_Time = pygame.time.get_ticks()
            if Current_Time - self.__Bullet_Lifetime >= self.__Bullet_Cooldown:
                self.__Ready_To_Fire = True

    def __fire_bullet(self):
        """It fires bullet by random enemy in an army."""
        if self.__Ready_To_Fire:
            random_number = randint(0, len(self.Enemies))
            for random_enemy in iter(self.Enemies):
                if random_number == 0:
                    random_enemy.fire_bullet("Enemy")
                    break
                random_number -= 1
            self.__Bullet_Lifetime = pygame.time.get_ticks()
            self.__Ready_To_Fire = False

    def __secret_enemy(self, screen):
        """It summons a secret enemy."""
        is_summoned = bool(self.Secret_Enemy)
        if not is_summoned:
            if pygame.event.get(self.__SECRET_ENEMY_COOLDOWN):
                speed = choice([(-1) * self.__Base_Speed, self.__Base_Speed])
                self.Secret_Enemy.add(Secret_Enemy(self.__Screen_Size, speed))
                random_number = randint(25 * 1000, 35 * 1000)
                pygame.time.set_timer(self.__SECRET_ENEMY_COOLDOWN, random_number)
        else:
            self.Secret_Enemy.update()
            self.Secret_Enemy.draw(screen)

    def __speed_update(self):
        """It updates army speed when number of enemies is decreasing."""
        speed = (self.__Number_of_Enemies_In_A_Row * 6 - len(self.Enemies)) // (self.__Number_of_Enemies_In_A_Row * 2.5)
        if self.__Speed > 0:
            self.__Speed = self.__Base_Speed + speed
        else:
            self.__Speed = -self.__Base_Speed - speed
        for enemy in iter(self.Enemies):
            enemy._Speed = self.__Speed

    def update(self, screen):
        """It updates an army."""
        self.__speed_update()
        self.__move()
        self.__recharge_bullet()
        self.__fire_bullet()
        if len(self.Enemies) == 0:
            self.__Speed = self.__Base_Speed
            self.army_initialize()
        self.Enemies.update(screen)
        self.__secret_enemy(screen)

    def draw(self, screen):
        """It draws an army."""
        self.Enemies.draw(screen)
