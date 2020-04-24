import pygame, sys,math
from player import Player
from map_generator import Map

class Game(object):
    TPS_DELTA = 0.0
    TPS_MAX = 60
    width = 1344
    height = 704
    def __init__(self):
        # Config
        # Intitialization
        pygame.init()
        self.screen = pygame.display.set_mode([self.width,self.height])
        self.tps_clock = pygame.time.Clock()
        self.Spawnplayers(pygame.joystick.get_count()) # spawnowanie graczy zaleznie od ilosc padow
        self.Map = Map(self.width,self.height)

        while True:
            # Handle events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit(0)

            # Ticking
            self.TPS_DELTA += self.tps_clock.tick() / 1000.0
            while self.TPS_DELTA > (1 / self.TPS_MAX):
                self.TPS_DELTA -= 1 / self.TPS_MAX

            # Drawing
            self.screen.fill((100,0,0))
            self.check_collision_between_players(pygame.joystick.get_count())
            self.draw(pygame.joystick.get_count())
            pygame.display.flip()
    def Spawnplayers(self,number_of_players):
        self.players = [Player(n,(32+300*n,32+100*n)) for n in range(0,number_of_players)]
        #pozniej miejsce spawnu bedzie zalezne od mapy
    def draw(self,number_of_players):
        self.Map.draw(self.screen)
        for n in range(0,number_of_players):
            self.players[n].movement()
            self.players[n].draw(self.screen)
    def check_collision_between_players(self,number_of_players): # w czasie tworzenia
        for n in range(number_of_players):
            for i in range(number_of_players):
                if i != n:
                   if (math.sqrt((self.players[n].playerX - self.players[i].playerX)**2+\
                    (self.players[n].playerY - self.players[i].playerY)**2)<=64):
                       self.players[n].playerX -= self.players[n].playerVX
                       self.players[n].playerY -= self.players[n].playerVY
                       self.players[i].playerX -= self.players[i].playerVX
                       self.players[i].playerY -= self.players[i].playerVY
                       self.players[n].playerVX = 0
                       self.players[i].playerVX = 0
                       self.players[n].playerVY = 0
                       self.players[i].playerVY = 0
                   else:
                       continue
                else:
                    continue



if __name__=="__main__":
    Game()