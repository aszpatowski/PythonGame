import pygame
import math


class Bullet:
    x = None
    y = None
    vx = 0.0
    vy = 0.0
    playerID = None

    def __init__(self, x, y, vx, vy, playerID):
        self.IMAGE = pygame.transform.scale(pygame.image.load("textures/guns/bullet.png").convert_alpha(),
                                            (10, 18))
        self.IMAGEOLD = self.IMAGE
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.playerID = playerID

    def movement(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        self.IMAGE = pygame.transform.rotate(self.IMAGEOLD, math.degrees(math.atan2(-self.vx, -self.vy)))
        screen.blit(self.IMAGE, (self.x, self.y))
