from settings import *
import pygame


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

class Plane:
    def __init__(self, screen):
        self.image_surf = pygame.image.load("images/plane.png")
        self.screen = screen
        self.x = 50
        self.y = display_height / 2 - 100
        self.degree = 0
        self.lives = 100
        self.last_shot = 0
        self.type = "user"
        self.fired_main = 0
        self.fired_secondary = 0
        self.main_weapon = "bullet_1"
        self.secondary_weapon = "missle_1"

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
        if not up and not down:
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
        last_shot = self.last_shot
        time_since = stopwatch.mill - last_shot
        main_weapon = self.main_weapon
        secondary_weapon = self.secondary_weapon

        # Fire from main weapon
        if kb.space and (time_since) >= Bullets.lag(main_weapon):
            bullet = Bullet(self, main_weapon, Bullets.damage(main_weapon), kb)
            bullets.add(bullet)
            self.fired_main += 1
            self.last_shot = stopwatch.mill

    def reset(self):
        self.__init__(self.screen)

class Bullets:
    def __init__(self):
        self.total_count = 0
        self.active_count = 0
        self.active_bullets = []

    def add(self, bullet):
        self.active_bullets.append(bullet)
        self.total_count += 1
        self.active_count += 1

    def remove(self, bullet):
        self.active_bullets.remove(bullet)
        self.active_count -= 1

    @staticmethod
    def lag(type):
        if type == "bullet_1":
            return bullet_1_lag

    @staticmethod
    def damage(type):
        if type == "bullet_1":
            return bullet_1_damage

class Bullet:
    def __init__(self, plane, type, damage, kb):
        self.x = plane.x
        self.y = plane.y
        self.degree = plane.degree
        self.damage = damage
        self.type = type

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