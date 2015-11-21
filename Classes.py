from settings import *
from plot import *
from math import *
from random import *
import pygame
pygame.init()

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
        self.primary_ammo = 100000
        self.secondary_ammo = 10
        self.active_weapon = "bullet_1"

    def swap_weapon(self):
        if self.active_weapon == self.primary_weapon:
            self.active_weapon = self.secondary_weapon
        else:
            self.active_weapon = self.primary_weapon

    def change_primary_weapon(self, name):
        self.primary_weapon = name
        UpperInfo.primary_img_active = pygame.image.load(ammo[name]['bullet_icon_active'])
        UpperInfo.primary_img_unactive = pygame.image.load(ammo[name]['bullet_icon_unactive'])

    def change_secondary_weapon(self, name):
        self.secondary_weapon = name
        UpperInfo.secondary_img_active = pygame.image.load(ammo[name]['bullet_icon_active'])
        UpperInfo.secondary_img_unactive = pygame.image.load(ammo[name]['bullet_icon_unactive'])

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

    def weapon_pos(self):
        x_offset = cos(self.degree*pi/180) * 50
        y_offset = -sin(self.degree*pi/180) * 50
        return (56 + x_offset + self.x), (46 + y_offset + self.y)

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
            active_ammo = self.primary_ammo
            if last_shot_primary != 0:
                time_since_active = time_since_primary
            else:
                time_since_active = 999999999
        else:
            active_ammo = self.secondary_ammo
            if last_shot_secondary != 0:
                time_since_active = time_since_secondary
            else:
                time_since_active = 999999999

        # Fire from main weapon
        if kb.space and (time_since_active) >= Bullets.info(active_weapon, 'lag') and active_ammo > 0:
            if ammo[active_weapon]['single'] is False or kb.fire is True:
                bullet = Bullet(self, active_weapon)
                bullets.add(bullet)
                if active_weapon == self.primary_weapon:
                    self.last_shot_primary = stopwatch.mill
                else:
                    self.last_shot_secondary = stopwatch.mill

                # Reduce ammo
                if active_weapon == self.primary_weapon:
                    self.primary_ammo -= 1
                else:
                    self.secondary_ammo -= 1

                kb.fire = False

    def reset(self):
        self.__init__(self.screen)

class Enemies:
    def __init__(self, screen):
        self.enemies = []
        self.attacking_count = len(self.enemies)
        self.screen = screen

    def add(self, x, y, type, style):
        self.enemies.append(Enemy(x, y, type, style))

    def blit(self):
        self.update_status()
        for enemy in self.enemies:
            x_off = enemy.x_off
            y_off = enemy.y_off
            self.screen.blit(enemy.image, (enemy.x - x_off, enemy.y - y_off))
            self.blit_lives(enemy)

    def check_bullet_col(self, bullets):
        for enemy in self.enemies:
            for bullet in bullets.active_bullets:
                if bullet.x >= enemy.x and bullet.y <= (enemy.y + enemy.height/2) and bullet.y >= (enemy.y - enemy.height/2):
                    enemy.lives -= bullet.damage
                    bullets.active_bullets.remove(bullet)

    def remove_offscreen(self):
        for enemy in self.enemies:
            if enemy.x < -100:
                self.enemies.remove(enemy)

    def update_status(self):
        for enemy in self.enemies:
            if enemy.status != 'wrecked' and enemy.lives <= 0:
                enemy.status = 'dead'

    def calc_delta(self, plane):
        for enemy in self.enemies:

            # IF ENEMY IS DEAD
            if enemy.status == 'dead':
                if not enemy.y > (display_height - randint(70,90)):
                    enemy.dy = 8
                else:
                    enemy.destroy()
                    enemy.dx = -bg_speed
                    enemy.dy = 0
            elif enemy.status != 'wrecked':
                if enemy.style == 'sin_passing':
                    enemy.dx = -4

    def calc_pos(self, plane):
        self.calc_delta(plane)

        for enemy in self.enemies:
            enemy.x += enemy.dx
            enemy.y += enemy.dy

    def blit_lives(self, enemy):
        if enemy.lives > 0:
            x = enemy.x - enemy.x_off
            y = enemy.y - enemy.y_off + 130
            pygame.draw.rect(self.screen, red, (x,y,100*1.5,5))
            pygame.draw.rect(self.screen, green, (x,y,(enemy.lives / enemy.max_lives * 100)*1.5,5))


    @staticmethod
    def info(type, property):
        return enemy_info[type][property]

class Enemy:
    def __init__(self, x, y, type, style):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.x_off = Enemies.info(type, 'x_off')
        self.y_off = Enemies.info(type, 'y_off')
        self.height = Enemies.info(type, 'height')
        self.status = 'flying'
        self.style = style
        self.type = type
        self.max_lives = Enemies.info(type, 'max_lives')
        self.lives = self.max_lives
        self.image = pygame.image.load(Enemies.info(type, 'image'))

    def destroy(self):
        self.status = 'wrecked'
        self.image = pygame.image.load(Enemies.info(self.type, 'wrecked_image'))

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
            self.screen.blit(bullet.image, (bullet.x - x_off, bullet.y - y_off))

    @staticmethod
    def info(type, property):
        return ammo[type][property]

class Bullet:
    def __init__(self, origin, type):
        self.x = origin.weapon_pos()[0]
        self.y = origin.weapon_pos()[1]
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

    primary_img_active = pygame.image.load(ammo['bullet_1']['bullet_icon_active'])
    primary_img_unactive = pygame.image.load(ammo['bullet_1']['bullet_icon_unactive'])
    secondary_img_active = pygame.image.load(ammo['missile_1']['bullet_icon_active'])
    secondary_img_unactive = pygame.image.load(ammo['missile_1']['bullet_icon_unactive'])

    def __init__(self, screen):
        self.screen = screen
        self.primary_x = 170
        self.primary_y = 0
        self.secondary_x = 350
        self.secondary_y = 0
        self.heart_x = -10
        self.heart_y = -10
        self.heart = pygame.image.load("images/heart.png")
        self.font = pygame.font.Font("/Library/Fonts/MyriadPro-Bold.otf", 40)

    def blit_bullet_icons(self, plane, stopwatch):

        # Primary weapon info
        primary_lag = ammo[plane.primary_weapon]['lag']
        time_since_primary = stopwatch.mill - plane.last_shot_primary
        primary_img_active = UpperInfo.primary_img_active
        primary_img_unactive = UpperInfo.primary_img_unactive

        # Secondary weapon info
        secondary_lag = ammo[plane.secondary_weapon]['lag']
        time_since_secondary = stopwatch.mill - plane.last_shot_secondary
        secondary_img_active = UpperInfo.secondary_img_active
        secondary_img_unactive = UpperInfo.secondary_img_unactive

        if plane.active_weapon == plane.primary_weapon:
            self.screen.blit(primary_img_active, (self.primary_x, self.primary_y))
            self.screen.blit(secondary_img_unactive, (self.secondary_x, self.secondary_y))
        else:
            self.screen.blit(primary_img_unactive, (self.primary_x, self.primary_y))
            self.screen.blit(secondary_img_active, (self.secondary_x, self.secondary_y))

        if time_since_primary >= primary_lag or plane.last_shot_primary == 0:
            load_percent_primary = 1
        else:
            load_percent_primary = (time_since_primary / primary_lag) % 1

        if time_since_secondary >= secondary_lag or plane.last_shot_secondary == 0:
            load_percent_secondary = 1
        else:
            load_percent_secondary = (time_since_secondary / secondary_lag) % 1

        pygame.draw.rect(self.screen, d_blue, (self.primary_x + 34, self.primary_y + 66,42 * load_percent_primary,4))
        pygame.draw.rect(self.screen, d_blue, (self.secondary_x + 34, self.secondary_y + 66,42 * load_percent_secondary,4))

    def blit_heart(self):
        self.screen.blit(self.heart, (self.heart_x, self.heart_y))

    def blit_lives(self, plane):
        textSurface = self.font.render(str(plane.lives), True, white)
        textRect = textSurface.get_rect()
        textRect.center = (self.heart_x + 100 + textRect.width/2, self.heart_y + 55)
        self.screen.blit(textSurface, textRect)

    def blit_ammo(self, plane):
        textSurface = self.font.render(str(plane.primary_ammo), True, white)
        textRect = textSurface.get_rect()
        textRect.center = (self.primary_x + 90 + textRect.width/2, self.heart_y + 55)

        textSurface2 = self.font.render(str(plane.secondary_ammo), True, white)
        textRect2 = textSurface2.get_rect()
        textRect2.center = (self.secondary_x + 90 + textRect2.width/2, self.heart_y + 55)

        self.screen.blit(textSurface, textRect)
        self.screen.blit(textSurface2, textRect2)

    def blit(self, plane, stopwatch):
        self.blit_bullet_icons(plane, stopwatch)
        self.blit_heart()
        self.blit_lives(plane)
        self.blit_ammo(plane)

class Gameplay:
    def __init__(self):
        self.plot = plot
        self.wave_nr = 0
        self.wave = self.plot[0]
        self.cols = len(self.plot[self.wave_nr])
        self.score = 0
        self.remaining_enemies = 0
        self.spawned = False

    def next_wave(self):
        self.wave_nr += self.wave_nr

    def spawn(self, enemies):
        if self.spawned == False:

            for col_nr, col in enumerate(self.wave):
                objects_in_col = len(col)
                for object_nr, object in enumerate(col):
                    if object_nr == 2:
                        continue

                    x = 1400 + col_nr * 200
                    y = object[2]

                    # If enemy
                    if len(object) == 3:

                        enemies.add(x, y, object[0], object[1])

                    # If bonuspack
                    else:
                        pass

            self.spawned = True

    # FOR RANDOM SPAWN LOCATION - NOT USED AT THIS POINT OF TIME
    def calc_spawn_coord(self, col_nr, object_nr, objects_in_col):
        x = 200 + col_nr * 200

        if objects_in_col == 1:
            y = randint(90, display_height - 90)
        elif objects_in_col == 2:
            if object_nr == 0:
                y = randint(90, display_height // 2 - 90)
            else:
                y = randint(display_height // 2 + 90, display_height - 90)
        elif objects_in_col == 3:
            if object_nr == 0:
                y = randint(90, display_height // 3 - 50)
            elif object_nr == 1:
                y = randint(display_height // 3 + 50, 2*display_height//3 - 50)
            else:
                y = randint(2*display_height//3 + 50, display_height - 90)

        return x, y
