import pygame, sys
from player import Player

class Game(object):
    tps_delta = 0.0
    tps_max = 60
    width = 1200
    height = 720
    def __init__(self):
        # Config
        # Intitialization
        pygame.init()
        self.screen = pygame.display.set_mode([self.width,self.height])
        self.tps_clock = pygame.time.Clock()
        self.Spawnplayers(pygame.joystick.get_count()) # spawnowanie graczy zaleznie od ilosc padow

        while True:
            # Handle events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit(0)

            # Ticking
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > (1 / self.tps_max):
                self.tps_delta -=1 /self.tps_max

            # Drawing
            self.screen.fill((100,0,0))
            self.draw(pygame.joystick.get_count())
            #self.check_collision(pygame.joystick.get_count())
            pygame.display.flip()
    def Spawnplayers(self,number_of_players):
        self.players = [Player(n,(100+300*n,100+150*n)) for n in range(0,number_of_players)]
        #pozniej miejsce spawnu bedzie zalezne od mapy
    def draw(self,number_of_players):
        for n in range(0,number_of_players):
            self.players[n].movement()
            self.players[n].draw(self.screen)
    def check_collision(self,number_of_players): # w czasie tworzenia
        for n in range(number_of_players):
            for i in range(number_of_players):
                print(pygame.sprite.collide_rect(self.players[n].draw(self.screen),self.players[n].draw(self.screen)))
if __name__=="__main__":
    Game()