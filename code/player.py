import pygame
from object import Object


class Player(Object):
    def __init__(self, screen_size):
        """
        1: It sets player's sprite attributes.
        2: It sets player's bullets attributes.
        """
        super().__init__((screen_size[0] // 2, screen_size[1]), 5, screen_size)
        # 1
        self.image = pygame.image.load("../resources/images/player.png")
        self.rect = self.image.get_rect(midbottom=self._Coordinates)
        self.__Health = 3
        # 2
        self.__Ready_To_Fire = True
        self.__Bullet_Cooldown = 600
        self.__Bullet_Lifetime = 0

    def update(self, screen):
        """It updates enemy position, recharges enemy's bullet. Also updates Bullets group and draws it."""
        self.__move()
        self.__recharge_bullet()
        self.Bullets.update()
        self.Bullets.draw(screen)

    def __move(self):
        """
        It checks if player can be moved to the right or left.
        Also checks if player want to fire a bullet.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.right < self._Screen_Size[0]:
                self.rect.x += self._Speed
        elif keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self._Speed
        if keys[pygame.K_SPACE] and self.__Ready_To_Fire:
            self.fire_bullet("Player")
            self._Bullet_Sound.play()
            self.__Bullet_Lifetime = pygame.time.get_ticks()
            self.__Ready_To_Fire = False

    def __recharge_bullet(self):
        """Checks if enemy can shoot another bullet."""
        if not self.__Ready_To_Fire:
            Current_Time = pygame.time.get_ticks()
            if Current_Time - self.__Bullet_Lifetime >= self.__Bullet_Cooldown:
                self.__Ready_To_Fire = True
                self.__Bullet_Lifetime = 0

    def get_health(self):
        """It returns number of health."""
        return self.__Health

    def damage(self, kind_of_damage):
        """It damages a player."""
        if kind_of_damage == "normal":
            self.__Health -= 1
        elif kind_of_damage == "enemy_touch":
            self.__Health = 0

    def increase_health(self):
        """It increases a player's health."""
        if self.__Health != 3:
            self.__Health += 1