import math

import pygame


class Player(object):
    playerX = 0.0
    playerY = 0.0
    playerVX = 0.0
    playerVY = 0.0
    playerAngle = 0.0
    joystickID = None
    rect = 0
    cooldown = 0
    alive = 1
    stun_time = None

    def __init__(self, joystickID, X, Y):
        self.joystickID = joystickID
        self.playernormal = pygame.image.load(
            "textures/players/player{}/sprite_0.png".format(self.joystickID))
        self.playerstun = pygame.image.load(
            "textures/players/player{}/stunplayer.png".format(self.joystickID))
        self.playerdead = pygame.image.load(
            "textures/players/player{}/deadplayer.png".format(self.joystickID))
        self.playerak47 = pygame.image.load(
            "textures/players/player{}/ak47player.png".format(self.joystickID))
        self.playerpistol = pygame.image.load(
            "textures/players/player{}/pistolplayer.png".format(self.joystickID))
        self.playerknife = pygame.image.load(
            "textures/players/player{}/knifeplayer.png".format(self.joystickID))
        self.playerbaseball = pygame.image.load(
            "textures/players/player{}/baseballplayer.png".format(self.joystickID))
        self.playerimage = self.playernormal
        self.playerold = self.playerimage
        pygame.joystick.init()
        self.player = pygame.joystick.Joystick(self.joystickID)
        self.playerX = X
        self.playerY = Y
        self.sound_shot = pygame.mixer.Sound('sounds/colt.wav')
        self.sound_throw = pygame.mixer.Sound('sounds/throw.wav')
        self.sound_no_ammo = pygame.mixer.Sound('sounds/no_ammo.wav')
        self.font_type = pygame.font.Font('fonts/basic/basic.ttf', 20)
        self.player.init()
        self.weapon = []
        self.stun_time = 0

    def movement(self):
        self.playerVX = 2 * round(self.player.get_axis(0), 2)
        self.playerVY = 2 * round(self.player.get_axis(1), 2)
        self.cooldown = self.cooldown - 1 if self.cooldown > 0 else 0  # cooldown broni
        self.playerX += self.playerVX
        self.playerY += self.playerVY
        # print(self.player.get_button(0))

        if self.player.get_name() == 'Controller (XBOX 360 For Windows)':
            if round(self.player.get_axis(3), 2) != 0 or round(self.player.get_axis(4), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(4), 2), \
                                              round(self.player.get_axis(3), 2))

        elif self.player.get_name() == 'PC/PS3/Android':
            if round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(2), 2), \
                                              round(self.player.get_axis(3), 2))
        else:
            if round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(3), 2), \
                                              round(self.player.get_axis(2), 2))

    def interreaction(self, bullets_in_game, bullet):
        if len(self.weapon) != 0:
            if self.player.get_button(4) == 1:
                self.sound_throw.play()
                self.pop_weapon(0)
            elif self.weapon[0].TYPE in (1, 2) and self.player.get_button(5) == 1 \
                    and self.cooldown == 0:
                if self.weapon[0].bullets >0:
                    self.sound_shot.play()
                    self.fire(bullets_in_game, bullet)
                else:
                    self.sound_no_ammo.play()
                    self.cooldown = self.weapon[0].cooldown
    def draw(self, screen):
        self.rect = self.playerimage.get_rect(center=(self.playerX, self.playerY))
        # print(type(self.rect))
        self.playerimage = pygame.transform.rotate(self.playerold, math.degrees(self.playerAngle))
        if self.stun_time > 0 and self.alive == 1:
            self.stun_time -= 1
            if self.stun_time == 0:
                self.change_outfit()
        if len(self.weapon) != 0 and self.weapon[0].TYPE in (1, 2) and self.alive == 1:
            self.ammo_text = self.font_type.render(
                f"{self.joystickID} {self.weapon[0].bullets}/{self.weapon[0].MAX_BULLETS}", True,
                (0, 0, 0))
        else:
            self.ammo_text = self.font_type.render(
                f"{self.joystickID}", True,
                (0, 0, 0))
        screen.blit(self.ammo_text, (self.playerX - 32, self.playerY - 50))
        return screen.blit(self.playerimage, self.rect)

    def pop_weapon(self, type):
        if type:
            self.weapon[0].x = self.playerX - 32
            self.weapon[0].y = self.playerY - 32
            self.weapon[0].vx = 1 * self.playerVX + 3 * math.sin(self.playerAngle)
            self.weapon[0].vy = 1 * self.playerVY + 3 * math.cos(self.playerAngle)
            self.weapon[0].place = True
            self.weapon[0].throw_player_id = self.joystickID
            self.weapon.pop()
        else:
            self.weapon[0].x = self.playerX - 32
            self.weapon[0].y = self.playerY - 32
            self.weapon[0].vx = 2 * self.playerVX + 10 * math.sin(self.playerAngle)
            self.weapon[0].vy = 2 * self.playerVY + 10 * math.cos(self.playerAngle)
            self.weapon[0].place = True
            self.weapon[0].throw_player_id = self.joystickID
            self.weapon.pop()
            self.change_outfit()

    def fire(self, bullets_in_game, Bullet):
        self.cooldown = self.weapon[0].cooldown
        bullets_in_game.append(Bullet(self.playerX,
                                      self.playerY,
                                    1 * self.playerVX + 10 * math.sin(self.playerAngle),
                                    1 * self.playerVY + 10 * math.cos(self.playerAngle),
                                      self.joystickID))
        self.weapon[0].bullets -= 1

    def change_outfit(self):
        if (len(self.weapon) == 0):
            self.playerimage = self.playernormal
            self.playerold = self.playerimage
        else:
            if (self.weapon[0].TYPE == 1):
                self.playerimage = self.playerak47
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 2):
                self.playerimage = self.playerpistol
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 3):
                self.playerimage = self.playerknife
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 4):
                self.playerimage = self.playerbaseball
                self.playerold = self.playerimage

    def agony(self, vx_bullet, vy_bullet):
        if (len(self.weapon)) != 0:
            self.pop_weapon(1)
        self.alive = 0
        self.playerVX += vx_bullet
        self.playerVY += vy_bullet
        self.playerAngle = math.degrees(math.atan2(vx_bullet, vy_bullet))
        self.playerimage = self.playerdead
        self.playerold = self.playerimage

    def stun(self, vx_bullet, vy_bullet,stun_time):
        if (len(self.weapon)) != 0:
            self.pop_weapon(1)
        self.stun_time = stun_time
        self.playerVX += vx_bullet
        self.playerVY += vy_bullet
        self.playerAngle = math.degrees(math.atan2(vx_bullet, vy_bullet))
        self.playerimage = self.playerstun
        self.playerold = self.playerimage
