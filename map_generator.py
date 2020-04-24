import pygame, numpy as np,os
from array import *
class Map():
    TILE_SIZE = 64 #ROZMIAR KAFELKI W PIKSELACH
    GRASS_LOADED = []
    def __init__(self,HEIGHT,WIDTH):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH

        self.TILES_H_A = self.HEIGHT // self.TILE_SIZE # ILOŚC KAFELEK 32X32 KTORE SIE ZMIESZCZA NA#
                                                        # EKRANIE O WYKOSOSCI HEIGHT
        self.TILES_W_A = self.WIDTH // self.TILE_SIZE # ANALOGICZNE TYLKO DO SZEROKOSCI WIDTH
        print(self.TILES_W_A)
        print(self.TILES_H_A)
        self.MAP_ARRAY = [[0] * self.WIDTH] * self.HEIGHT
        RANDOM_ARRAY = np.random.randint(5, size=(self.HEIGHT, self.WIDTH))
        print(RANDOM_ARRAY)
        for i in range(5):
            self.GRASS_LOADED.append(pygame.transform.scale(pygame.image.load(f"textures/grass/grass{i}.png"),(self.TILE_SIZE,self.TILE_SIZE)))
        for i in range(self.TILES_H_A):
            for n in range(self.TILES_W_A):
                self.MAP_ARRAY[i][n] = self.GRASS_LOADED[RANDOM_ARRAY[i][n]]
    def draw(self,screen):
        for i in range(self.TILES_H_A):
            for n in range(self.TILES_W_A):
                #self.rect = self.GRASS_LOADED[2].get_rect(center=(i * 32, n * 32))
                #screen.blit(self.MAP_ARRAY[i][n], (i * 32, n * 32)) TYMCZASOWO WYLACZONE
                screen.blit(self.GRASS_LOADED[2],(i * self.TILE_SIZE, n * self.TILE_SIZE))


#ZWIEKSZONE DO 64X64 ZEBY ZWIEKSZYC WYDAJNOSC


