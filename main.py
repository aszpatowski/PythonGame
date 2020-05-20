import math
import sys
import random
import pygame
from PythonGame.map_generator import Map
from PythonGame.player import Player
from PythonGame.maps import maps
from PythonGame.weapon import *
from PythonGame.bullet import *


class Game(object):
    TPS_MAX = 120.0
    width = 1344
    height = 768
    #width = 1920
    #height = 1080
    WEAPONS_AVAILABLE = [AK47, Pistol, Knife, Baseball]
    weapons_in_game = []
    bullets_in_game = []
    frames = 0
    PLAYERS_COORDINATE = [(64, 64), (1270, 700), (1270, 64), (64, 700)]

    def __init__(self):
        # Config
        # Intitialization
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init(22100, -16, 2, 64)
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Super Cruel Arena")
        pygame.display.set_icon(pygame.image.load("logos/icon.png"))
        self.tps_clock = pygame.time.Clock()
        self.Map = Map(self.width, self.height)
        self.Spawnplayers(pygame.joystick.get_count())  # spawnowanie graczy zaleznie od ilosc padow

        self.sound_collision_weapon = pygame.mixer.Sound('sounds/collision_weapon.wav')
        self.sound_ricochet = pygame.mixer.Sound('sounds/ricochet.wav')
        self.sound_punch_weapon = pygame.mixer.Sound('sounds/punch_weapon.wav')
        self.sound_shot_body = pygame.mixer.Sound('sounds/shot_body.wav')
        while True:
            # Handle events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit(0)
            self.tps_clock.tick(self.TPS_MAX)
            pygame.display.set_caption("Super Cruel Arena FPS:{}".format(self.tps_clock.get_fps()))
            print(len(self.weapons_in_game))
            self.frames += 1
            if self.frames == 2 * self.TPS_MAX:
                self.frames = 0
                self.Spawnweapons()
            self.check_collision_between_players(pygame.joystick.get_count())
            self.check_collision_environment(pygame.joystick.get_count())
            self.weapon_interreaction()
            self.bullets_interreaction()
            self.draw(pygame.joystick.get_count())
            pygame.display.flip()

    def Spawnplayers(self, number_of_players):
        self.players = [Player(n, self.PLAYERS_COORDINATE[n][0], self.PLAYERS_COORDINATE[n][1]) for n in
                        range(0, number_of_players)]
        # pozniej miejsce spawnu bedzie zalezne od mapy

    def Spawnweapons(self):
        if random.randint(0, 1) == 1 and len(self.weapons_in_game) <= 6:
            while True:
                randomX = random.randint(0, len(maps.game_map1[0]) - 1)  # random.randint ma przedział zamknięty
                randomY = random.randint(0, len(maps.game_map1) - 1)
                # Sprawdza czy nie ma przeszkody
                if maps.game_map1[randomY][randomX] == 0:
                    x = Map.TILE_SIZE * randomX
                    y = Map.TILE_SIZE * randomY
                    # Sprawdza czy nie ma innej broni
                    if (x, y) not in [weapon.back_xy() for weapon in self.weapons_in_game]:
                        self.weapons_in_game.append(random.choice(self.WEAPONS_AVAILABLE)(x, y, Map.TILE_SIZE))
                        break

    def draw(self, number_of_players):
        self.Map.draw(self.screen)
        for weapon in self.weapons_in_game:
            weapon.draw_and_check(self.screen)
        for player in self.players:
            if player.alive == 1 and player.stun_time == 0:
                player.movement()
                player.interreaction(self.bullets_in_game, Bullet)
            player.draw(self.screen)
        for bullet in self.bullets_in_game:
            bullet.movement()
            bullet.draw(self.screen)

    def check_collision_between_players(self, number_of_players):
        for player1 in self.players:
            for player2 in self.players:
                if id(player1) != id(player2):
                    if math.sqrt((player1.playerX - player2.playerX) ** 2 + \
                                 (player1.playerY - player2.playerY) ** 2) <= 64:

                        player1.playerX -= player1.playerVX
                        player1.playerY -= player1.playerVY
                        player2.playerX -= player2.playerVX
                        player2.playerY -= player2.playerVY

                        player1.playerVX = player2.playerVX = player1.playerVY = player2.playerVY = 0
                    else:
                        continue
                else:
                    continue

    def check_collision_environment(self, number_of_players):
        for player in self.players:
            if player.alive != 0:
                for i in range(len(maps.game_map1)):
                    for n in range(len(maps.game_map1[0])):
                        if maps.game_map1[i][n] == 1:
                            deltaX = player.playerX - Map.TILE_SIZE * n - 32
                            deltaY = player.playerY - Map.TILE_SIZE * i - 32
                            if math.sqrt((deltaX) ** 2 + \
                                         (deltaY) ** 2) < 48:
                                player.playerX -= player.playerVX
                                player.playerY -= player.playerVY
                                player.playerVX *= -abs(math.sin(math.atan2(deltaX, deltaY)))
                                player.playerVY *= -abs(math.cos(math.atan2(deltaX, deltaY)))

                            else:
                                continue
                        else:
                            if 32 <= player.playerX <= self.width - 32 and \
                                    32 <= player.playerY <= self.height - 32:
                                continue
                            else:
                                player.playerX -= player.playerVX
                                player.playerY -= player.playerVY
                                player.playerVX = player.playerVY = 0

    def weapon_interreaction(self):
        weapons_to_delete = []
        for weapon in self.weapons_in_game:
            for player in self.players:
                # nastepny if sprawdza kolejno:
                # czy gracz nie ma broni,
                # czy bron nie jest podniesiona,
                # czy gracz ma wcisniety klawisz od podnieszenia,
                # czy styka się z bronią
                if weapon.place == True and \
                        math.sqrt((player.playerX - weapon.x - 32) ** 2 + \
                                  (player.playerY - weapon.y - 32) ** 2) < 64:
                    if (abs(weapon.vx) + abs(weapon.vy)) > 4 and player.joystickID != weapon.throw_player_id \
                            and player.alive == 1:
                        self.sound_punch_weapon.play()
                        if weapon.TYPE == 3:
                            player.agony(10 * weapon.vx, 10 * weapon.vy)
                            weapon.vx = weapon.vy = 0.0
                        else:
                            player.stun(10 * weapon.vx, 10 * weapon.vy,weapon.STUN)
                            weapon.vx = weapon.vy = 0.0
                    if len(player.weapon) == 0 and \
                            player.player.get_button(1):
                        weapon.place = False
                        weapon.vx = weapon.vy = 0.0  # zerowanie predkosci
                        player.weapon.append(weapon)
                        player.change_outfit()

            for i in range(len(maps.game_map1)):
                for n in range(len(maps.game_map1[0])):
                    if maps.game_map1[i][n] == 1:
                        deltaX = weapon.x - Map.TILE_SIZE * n
                        deltaY = weapon.y - Map.TILE_SIZE * i
                        if math.sqrt((deltaX) ** 2 + \
                                     (deltaY) ** 2) < 50:
                            # głośność jest zależna od predkosci przedmiotu
                            volume = (abs(weapon.vx) + abs(weapon.vy)) / 14 if ((abs(weapon.vx) + abs(
                                weapon.vy)) / 14) <= 1 else 1
                            self.sound_collision_weapon.set_volume(volume)
                            self.sound_collision_weapon.play()
                            weapon.vx *= -abs(math.sin(math.atan2(deltaX, deltaY)))
                            weapon.vy *= -abs(math.cos(math.atan2(deltaX, deltaY)))
                            weapon.x += weapon.vx
                            weapon.y += weapon.vy
                        else:
                            pass
                        # Usuwanie broni z mapy, po jej wyleceniu poza mape.
            if 0 <= weapon.x <= self.width - 32 and 0 <= weapon.y <= self.height - 32 or \
                    self.weapons_in_game.index(weapon) in weapons_to_delete:
                continue
            else:
                weapons_to_delete.append(self.weapons_in_game.index(weapon))
        weapons_to_delete.sort(reverse=True)
        for i in range(0, len(weapons_to_delete)):
            self.weapons_in_game.pop(weapons_to_delete[i])

    # Funkcja bullets_interreaction jest dosyć skompilkowana
    # Prawdopodobnie ulegnie przebudowie
    # Zeby nie raziłą w oczy swoją potęgą
    def bullets_interreaction(self):
        bullets_to_delete = []

        # Najpierw sprawdam czy nabój trafił gracza
        for bullet in self.bullets_in_game:
            for player in self.players:
                if math.sqrt((player.playerX - bullet.x - 32) ** 2 + \
                             (player.playerY - bullet.y - 32) ** 2) < 36 and \
                        bullet.playerID != player.joystickID:
                    self.sound_shot_body.play()
                    player.agony(bullet.vx, bullet.vy)
                    bullets_to_delete.append(self.bullets_in_game.index(bullet))

            # Potem sprawdzam czy naboj trafil w sciane, jesli tak to go niszcze
            for i in range(len(maps.game_map1)):
                for n in range(len(maps.game_map1[0])):
                    if maps.game_map1[i][n] == 1:
                        if math.sqrt((bullet.x - Map.TILE_SIZE * n - 32) ** 2 + \
                                     (bullet.y - Map.TILE_SIZE * i - 32) ** 2) < 32:
                            if self.bullets_in_game.index(bullet) not in bullets_to_delete:
                                self.sound_ricochet.play()
                                bullets_to_delete.append(self.bullets_in_game.index(bullet))
                            else:
                                pass
            # Sprawdzanie czy naboj nie wyleciał poza mape
            if 0 <= bullet.x <= self.width - 32 and 0 <= bullet.y <= self.height - 32:
                pass
            else:
                if self.bullets_in_game.index(bullet) not in bullets_to_delete:
                    bullets_to_delete.append(self.bullets_in_game.index(bullet))
                else:
                    pass
        bullets_to_delete.sort(reverse=True)
        for i in range(0, len(bullets_to_delete)):
            self.bullets_in_game.pop(bullets_to_delete[i])


if __name__ == "__main__":
    Game()
