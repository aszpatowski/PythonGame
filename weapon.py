import pygame
import math


class Weapon:
    x = None
    y = None
    vx = 0.0
    vy = 0.0
    MINV = 0.05
    place = True  # place = True broń jest na podłodze, False broń trzyma jakis gracz,
    IMAGE = None
    IMAGEOLD = None
    TILE_SIZE = None
    AIR_RESISTANCE = 0.98
    TYPE = None  # 1 = ak47, 2 = pistol, 3 = knife, 4 = baseball
    throw_player_id = None
    def __init__(self, X, Y, TILE_SIZE):
        self.x = X
        self.y = Y
        self.TILE_SIZE = TILE_SIZE

    def back_xy(self):
        return (self.x, self.y)

    def movement(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.AIR_RESISTANCE if abs(
            self.vx) >= self.MINV else 0  # predkosc zmniejsza sie przez opor powietrza,
        self.vy *= self.AIR_RESISTANCE if abs(self.vy) >= self.MINV else 0  # dopoki nie osiagnie predkosci minimalnej,
        # wtedy =


class Guns(Weapon):
    MAX_BULLETS = None
    bullets = None
    cooldown = None

    def __init__(self, X, Y, TILE_SIZE):
        Weapon.__init__(self, X, Y, TILE_SIZE)

    def draw_and_check(self, screen):  # po skonczeniu nabojow usuwamy bron
        if self.bullets > 0:
            if self.place:  # if self.place == True
                self.movement()
                self.IMAGE = self.IMAGEOLD
                if abs(self.vx + self.vy) > 0:
                    self.IMAGE = pygame.transform.rotate(self.IMAGEOLD,
                                                         math.degrees(math.atan2(self.vx, self.vy)) + 135)
                screen.blit(self.IMAGE, (self.x, self.y))
        else:
            del self


class Cold_Weapon(Weapon):
    def __init__(self, X, Y, TILE_SIZE):
        Weapon.__init__(self, X, Y, TILE_SIZE)

    def draw_and_check(self, screen):  # po skonczeniu nabojow usuwamy bron
        if self.place == True:
            self.movement()
            self.IMAGE = self.IMAGEOLD
            if abs(self.vx + self.vy) > 0:
                if abs(self.vx + self.vy) > 0:
                    self.IMAGE = pygame.transform.rotate(self.IMAGEOLD,
                                                         math.degrees(math.atan2(self.vx, self.vy)) + 135)
            screen.blit(self.IMAGE, (self.x, self.y))


class AK47(Guns):
    def __init__(self, X, Y, TILE_SIZE):
        Guns.__init__(self, X, Y, TILE_SIZE)
        self.cooldown = 15  # mozna strzelac 4 razy na sekunde
        self.bullets = self.MAX_BULLETS = 30
        self.IMAGE = pygame.transform.scale(pygame.image.load("textures/guns/ak47.png").convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))
        self.IMAGEOLD = self.IMAGE
        self.TYPE = 1

class Pistol(Guns):
    def __init__(self, X, Y, TILE_SIZE):
        Guns.__init__(self, X, Y, TILE_SIZE)
        self.cooldown = 60  # mozna strzelac 1 razy na sekunde
        self.bullets = self.MAX_BULLETS = 15
        self.IMAGE = pygame.transform.scale(pygame.image.load("textures/guns/pistol.png").convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))
        self.IMAGEOLD = self.IMAGE
        self.TYPE = 2

class Knife(Cold_Weapon):
    def __init__(self, X, Y, TILE_SIZE):
        Cold_Weapon.__init__(self, X, Y, TILE_SIZE)
        self.IMAGE = pygame.transform.scale(pygame.image.load("textures/white_weapon/knife.png").convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))
        self.IMAGEOLD = self.IMAGE
        self.TYPE = 3

class Baseball(Cold_Weapon):
    def __init__(self, X, Y, TILE_SIZE):
        Cold_Weapon.__init__(self, X, Y, TILE_SIZE)
        self.IMAGE = pygame.transform.scale(pygame.image.load("textures/white_weapon/baseball.png").convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))
        self.IMAGEOLD = self.IMAGE
        self.TYPE = 4