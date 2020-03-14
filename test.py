import pygame

pygame.init()

screen = pygame.display.set_mode((1920,1080),0,32)

while True:
    for event in pygame.event.get():
        print(event)