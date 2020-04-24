import pygame, math
class Player(object):
    playerX = 0.0
    playerY = 0.0
    playerVX = 0.0
    playerVY = 0.0
    playerAngle = 0.0
    joystickID = 0
    rect = 0
    def __init__(self,joystickID,XY):
        self.playerimage = pygame.image.load("textures/players/player1/sprite_0.png")
        self.playerold = self.playerimage
        pygame.joystick.init()
        self.joystickID = joystickID
        self.player = pygame.joystick.Joystick(self.joystickID)
        self.playerX = XY[0]
        self.playerY = XY[1]
        self.player.init()
    def movement(self):
        self.playerVX = round(self.player.get_axis(0), 1)
        self.playerVY = round(self.player.get_axis(1), 1)

        self.playerX = self.playerX + self.playerVX
        self.playerY = self.playerY + self.playerVY

        if(self.player.get_name()=='Controller (XBOX 360 For Windows)'):
            if (round(self.player.get_axis(3),2)!=0  or round(self.player.get_axis(4),2)!=0):
                self.playerAngle = math.degrees(math.atan2(round(self.player.get_axis(4),2),round(self.player.get_axis(3),2)))

        elif(self.player.get_name()=='PC/PS3/Android'):
            if (round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0):
                self.playerAngle = math.degrees(
                    math.atan2(round(self.player.get_axis(2), 2), round(self.player.get_axis(3), 2)))
        else:
            if (round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0):
                self.playerAngle = math.degrees(math.atan2(round(self.player.get_axis(3), 2), round(self.player.get_axis(2), 2)))


    def draw(self,screen):
        self.rect = self.playerimage.get_rect(center=(self.playerX, self.playerY))
       # print(type(self.rect))
        self.playerimage = pygame.transform.rotate(self.playerold, self.playerAngle)
        return screen.blit(self.playerimage,self.rect)

