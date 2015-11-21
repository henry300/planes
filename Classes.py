from settings import *
from math import *
import pygame

class Plane:
    def __init__(self, screen):
        self.image_surf = pygame.image.load("images/plane.png")
        self.screen = screen
        self.x = 50
        self.y = display_height / 2 - 100
        self.degree = 0
        self.lives = 100
        self.last_shot_primary = 0
        self.last_shot_secondary = 0
        self.type = "user"
        self.fired_primary = 0
        self.fired_secondary = 0
        self.primary_weapon = "bullet_1"
        self.secondary_weapon = "missile_1"
        self.active_weapon = "bullet_1"

    def swap_weapon(self):
        if self.active_weapon == self.primary_weapon:
            self.active_weapon = self.secondary_weapon
        else:
            self.active_weapon = self.primary_weapon

    def calc_degree(self, kb):
        degree = self.degree
        up = kb.up
        down = kb.down

        if down:
            if degree > -20:
                degree -= 1
            else:
                degree = -20
        if up:
            if degree < 20:
               degree += 1
            else:
               degree = 20
        if (not up and not down) or (up and down):
            if degree >= 2:
                degree -= 2
            elif degree <= -2:
                degree += 2
            else:
                degree = 0
        self.degree = degree

    def calc_pos(self, kb):
        up = kb.up
        down = kb.down
        left = kb.left
        right = kb.right

        if up:
            self.y -= up_speed
        if down:
            self.y += down_speed
        if left:
            self.x -= left_speed
        if right:
            self.x += right_speed

    def calc_weapon_pos(self):
        x_offset = cos(self.degree*pi/180) * 50
        y_offset = -sin(self.degree*pi/180) * 50
        return (40 + x_offset + self.x), (46 + y_offset + self.y)

    def blit(self):
        def rot_center(image, angle):
            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotozoom(image, angle, 1)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            return rot_image
        self.image_surf_rotated = rot_center(self.image_surf, self.degree)
        self.screen.blit(self.image_surf_rotated, (self.x, self.y))

    def fire(self, kb, stopwatch, bullets):
        last_shot_primary = self.last_shot_primary
        last_shot_secondary = self.last_shot_secondary
        time_since_primary = stopwatch.mill - last_shot_primary
        time_since_secondary = stopwatch.mill - last_shot_secondary
        active_weapon = self.active_weapon

        # Assign correct lag to active weapon
        if self.active_weapon == self.primary_weapon:
            if last_shot_primary != 0:
                time_since_active = time_since_primary
            else:
                time_since_active = 999999999
        else:
            if last_shot_secondary != 0:
                time_since_active = time_since_secondary
            else:
                time_since_active = 999999999

        # Fire from main weapon
        if kb.space and (time_since_active) >= Bullets.info(active_weapon, 'lag'):
            if ammo[active_weapon]['single'] is False or kb.fire is True:
                bullet = Bullet(self, active_weapon)
                bullets.add(bullet)
                self.fired_primary += 1
                if active_weapon == self.primary_weapon:
                    self.last_shot_primary = stopwatch.mill
                else:
                    self.last_shot_secondary = stopwatch.mill
                kb.fire = False

    def reset(self):
        self.__init__(self.screen)

class Enemies:
    def __init__(self):
        self.enemies = []
        self.attacking_count = len(self.enemies)

class Bullets:
    def __init__(self, screen):
        self.total_count = 0
        self.active_count = 0
        self.screen = screen
        self.active_bullets = []

    def add(self, bullet):
        self.active_bullets.append(bullet)
        self.total_count += 1
        self.active_count += 1

    def remove(self, bullet):
        self.active_bullets.remove(bullet)
        self.active_count -= 1

    def remove_offscreen(self):
        for bullet in self.active_bullets:
            if bullet.x > display_width or bullet.x < 0:
                self.remove(bullet)

    def calc_pos(self):
        for bullet in self.active_bullets:
            dx = cos(bullet.degree*pi/180) * bullet.speed
            dy = -sin(bullet.degree*pi/180) * bullet.speed
            if bullet.origin.type == "user":
                direction = 1
            else:
                direction = -1
            bullet.x += direction * dx
            bullet.y += direction * dy

    def blit(self):
        for bullet in self.active_bullets:
            x_off = Bullets.info(bullet.type, 'x_off')
            y_off = Bullets.info(bullet.type, 'y_off')
            self.screen.blit(bullet.image, (bullet.x + x_off, bullet.y - y_off))

    @staticmethod
    def info(type, property):
        return ammo[type][property]

class Bullet:
    def __init__(self, origin, type):
        self.x = origin.calc_weapon_pos()[0]
        self.y = origin.calc_weapon_pos()[1]
        self.degree = origin.degree
        self.damage = Bullets.info(type, 'damage')
        self.type = type
        self.origin = origin
        self.image = pygame.image.load(Bullets.info(type, 'bullet_image'))
        self.speed = Bullets.info(type, 'speed')

class Keyboard:
    def __init__(self):
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        self.c = False
        self.space = False
        self.fire = False

    def reset(self):
        self.__init__()

class Background:
    def __init__(self, screen):
        self.image_surf = pygame.image.load("images/background.png")
        self.screen = screen
        self.x1 = 0
        self.x2 = display_width
        self.speed = bg_speed

    def blit(self):
        if self.x1 < -display_width:
            self.x1 = display_width
        if self.x2 < -display_width:
            self.x2 = display_width
        self.screen.blit(self.image_surf, (self.x1, 0))
        self.screen.blit(self.image_surf, (self.x2, 0))
        self.x1 -= self.speed
        self.x2 -= self.speed

class Stopwatch:
    def __init__(self):
        self.mill = 0
        self.sec = 0

    def tick(self):
        self.mill += 1
        self.sec += 1/60

    def reset(self):
        self.__init__()

class UpperInfo:
    def __init__(self, screen):
        self.screen = screen

    def blit_primary_weapon_img(self, plane):
        primary_active_img = pygame.image.load(ammo[plane.primary_weapon]['bullet_icon_active'])
        primary_unactive_img = pygame.image.load(ammo[plane.primary_weapon]['bullet_icon_unactive'])

        if plane.active_weapon == plane.primary_weapon:
            self.screen.blit(primary_active_img, (500,200))
        else:
            self.screen.blit(primary_unactive_img, (500,200))


