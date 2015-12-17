from settings import *
from plot import *
from math import *
from random import *
import mat
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
        self.primary_ammo = 1000
        self.secondary_ammo = 0
        self.active_weapon = "bullet_1"
        self.time = None
        self.single = False
        self.effectsdict = {}

    def addInfo(self, stopwatch):
        self.time = stopwatch.sec

    def swap_weapon(self):
        if self.active_weapon == self.primary_weapon:
            self.active_weapon = self.secondary_weapon
        else:
            self.active_weapon = self.primary_weapon

    def effects(self):
        if 'shake' in self.effectsdict:
            if self.time - self.effectsdict['shake'] < 1:
                dt = round(self.time - self.effectsdict['shake'], 1) * 10
                if dt % 2 == 0:
                    self.y += 2
                else:
                    self.y -= 2
            else:
                del self.effectsdict['shake']

    def shake(self):
        if 'shake' not in self.effectsdict:
            self.effectsdict['shake'] = self.time

    def swap_single(self):
        if self.active_weapon == self.primary_weapon:
            if self.single == True:
                self.single = False
                Info.primary_img_active = pygame.image.load(ammo[self.primary_weapon]['bullet_icon_active'])
                Info.primary_img_unactive = pygame.image.load(ammo[self.primary_weapon]['bullet_icon_unactive'])
            else:
                self.single = True
                Info.primary_img_active = pygame.image.load(ammo[self.primary_weapon]['bullet_icon_active_single'])
                Info.primary_img_unactive = pygame.image.load(ammo[self.primary_weapon]['bullet_icon_unactive_single'])

    def change_primary_weapon(self, name):
        self.primary_weapon = name
        Info.primary_img_active = pygame.image.load(ammo[name]['bullet_icon_active'])
        Info.primary_img_unactive = pygame.image.load(ammo[name]['bullet_icon_unactive'])
        self.single = Bullets.info(name, 'single')

    def change_secondary_weapon(self, name):
        self.secondary_weapon = name
        Info.secondary_img_active = pygame.image.load(ammo[name]['bullet_icon_active'])
        Info.secondary_img_unactive = pygame.image.load(ammo[name]['bullet_icon_unactive'])

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
            if self.single is False or kb.fire is True:
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
        self.plane = None
        self.bullets = None

    def add(self, x, y, type, style):
        self.enemies.append(Enemy(x, y, type, style))


    def addInfo(self, gameplay, stopwatch, plane, bullets):
        self.gameplay = gameplay
        self.stopwatch = stopwatch
        self.plane = plane
        self.bullets = bullets

        # Provide additional info for enemies
        for enemy in self.enemies:
            enemy.plane = self.plane
            enemy.bullets = self.bullets
            enemy.stopwatch = self.stopwatch

    def blit(self):
        self.update_status()
        for enemy in self.enemies:
            x_off = enemy.x_off
            y_off = enemy.y_off
            self.screen.blit(enemy.image, (enemy.x - x_off, enemy.y - y_off))
            self.blit_lives(enemy)

    def fire(self):
        for enemy in self.enemies:
            if enemy.ammo != None:
                enemy.fire_control(self.stopwatch)

    def check_bullet_col(self, bullets):
        for enemy in self.enemies:
            for bullet in bullets.active_bullets:
                if bullet.x >= enemy.x and bullet.y <= (enemy.y + enemy.height/2) and bullet.y >= (enemy.y - enemy.height/2) and enemy.status != 'wrecked' and bullet.origin.type == 'user':
                    enemy.lives -= bullet.damage
                    bullets.remove(bullet)

    def check_user_col(self, plane):
        for enemy in self.enemies:
            if enemy.x <= plane.x + 100 and enemy.x >= plane.x and enemy.y >= plane.y - 20 and enemy.y <= plane.y + 70 and enemy.status == 'flying':
                plane.lives -= 50
                plane.shake()
                enemy.lives = 0

    def remove_offscreen(self):
        for enemy in self.enemies:
            if enemy.x < -100:
                self.enemies.remove(enemy)
                self.gameplay.remaining_enemies -= 1

    def update_status(self):
        for enemy in self.enemies:
            if enemy.status != 'wrecked' and enemy.lives <= 0:
                enemy.status = 'dead'

    def slow_to_stop(self, x1, x2, cur, v0):
        dist = abs(x2-x1)
        travelled = abs(x1-cur)
        if (dist - travelled) > 1:
            return v0 * (1 - (travelled / dist)) - 0.5
        else:
            return -0.5

    def calc_delta(self):

        active_following_enemies = 0

        for enemy in self.enemies:

            # IF ENEMY IS DEAD
            if enemy.status == 'dead':
                if not enemy.y > (display_height - randint(55,80)):
                    enemy.dy = 8
                else:
                    enemy.destroy(self.gameplay)
                    enemy.dx = -bg_speed
                    enemy.dy = 0
            elif enemy.status != 'wrecked':

                # SIN_PASSING_SLOW
                if enemy.style == 'sin_passing_slow':
                    enemy.y += 1 * sin(enemy.x * 0.01)
                    enemy.dx = -2

                # MOVING STRAIGHT
                elif enemy.style == 'moving_straight':
                    enemy.dx = -2
                    enemy.dy = 0

                # HOVERING LARGE CIRC
                elif enemy.style == 'hovering_large_circ':
                    if enemy.x > display_width - 200 and enemy.movePhase == 0:
                        if enemy.x < display_width - 50:
                            enemy.dx = self.slow_to_stop(display_width-50, display_width-200, enemy.x, -4)
                        else:
                            enemy.dx = -4
                    else:
                        enemy.movePhase = 1
                        enemy.dx = cos(self.stopwatch.sec * 0.5)
                        enemy.dy = sin(self.stopwatch.sec * 0.5)

                # HOVERING MOVING
                elif enemy.style == 'hovering_moving':
                    if enemy.x > display_width - 400 and enemy.movePhase == 0:
                        if enemy.x < display_width - 50:
                            enemy.dx = self.slow_to_stop(display_width-50, display_width-200, enemy.x, -4)
                        else:
                            enemy.dx = -4
                    else:
                        enemy.movePhase = 1
                        enemy.x += cos(enemy.y * 0.05)
                        enemy.dy = sin(self.stopwatch.sec * 0.5)

                # APPROACHING_FOLLOWING
                elif enemy.style == 'approaching_following':

                    # Simulate dx = 1.5
                    if enemy.dx == -2:
                        enemy.dx = -1
                    else:
                        enemy.dx = -2

                    # Follow plane y coordinate
                    if abs(enemy.y - self.plane.y - 25 - 130*active_following_enemies * -1) > enemy.lag:
                        if enemy.y - (self.plane.y + 25 + 130*active_following_enemies * -1) < 0:
                            enemy.dy = 1
                        else:
                            enemy.dy = -1
                    else:
                        enemy.dy = 0

                    active_following_enemies += 1

                else:
                    print("No such moving style: ", enemy.style)
                    self.gameplay.gameover = True

    def calc_pos(self):
        self.calc_delta()

        for enemy in self.enemies:
            enemy.x += enemy.dx
            enemy.y += enemy.dy

    def blit_lives(self, enemy):
        if enemy.lives > 0:
            x = enemy.x - enemy.x_off + enemy.lives_x_off
            y = enemy.y - enemy.y_off + enemy.lives_y_off
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
        self.degree = 0
        self.x_off = Enemies.info(type, 'x_off')
        self.y_off = Enemies.info(type, 'y_off')
        self.lives_y_off = Enemies.info(type, 'lives_y_off')
        self.lives_x_off = Enemies.info(type, 'lives_x_off')
        self.weapon_pos_x = Enemies.info(type, 'weapon_pos_x')
        self.weapon_pos_y = Enemies.info(type, 'weapon_pos_y')
        self.ammo = Enemies.info(type, 'ammo')
        self.height = Enemies.info(type, 'height')
        self.status = 'flying'
        self.style = style
        self.bullets = None
        self.lag = randint(5,30)
        self.type = type
        self.value = Enemies.info(type, 'value')
        self.max_lives = Enemies.info(type, 'max_lives')
        self.lives = self.max_lives
        self.image = pygame.image.load(Enemies.info(type, 'image'))
        self.movePhase = 0
        self.stopwatch = None
        self.plane = None
        self.shooting_start_time = 0
        self.last_shot = 0

    def fire_control(self, stopwatch):
        if abs(self.shooting_start_time - stopwatch.sec) < Enemies.info(self.type, 'shooting_duration'):
            if self.style == "approaching_following":
                self.fire_if_alligned()
            else:
                self.fire()
        else:
            if abs(self.shooting_start_time - stopwatch.sec) > Enemies.info(self.type, 'shooting_duration') + Enemies.info(self.type, 'shooting_resttime'):
                self.shooting_start_time = stopwatch.sec


    def fire_if_alligned(self):
        if abs(self.plane.y - self.y + 25) < 30:
            self.fire()

    def weapon_pos(self):
        return self.x + self.weapon_pos_x, self.y + self.weapon_pos_y

    def fire(self):
        if self.ammo != None:
            time_since_shot = self.stopwatch.mill - self.last_shot

            if time_since_shot >= Bullets.info(self.ammo, 'lag'):
                bullet = Bullet(self, self.ammo)
                self.bullets.add(bullet)
                self.last_shot = self.stopwatch.mill


    def destroy(self, gameplay):
        self.status = 'wrecked'
        gameplay.score += self.value
        self.image = pygame.image.load(Enemies.info(self.type, 'wrecked_image'))

class Bullets:
    def __init__(self, screen):
        self.total_count = 0
        self.active_count = 0
        self.active_user_bullets = 0
        self.screen = screen
        self.active_bullets = []

    def add(self, bullet):
        self.active_bullets.append(bullet)
        self.total_count += 1
        self.active_count += 1
        if bullet.origin.type == "user":
            self.active_user_bullets += 1

    def remove(self, bullet):
        self.active_bullets.remove(bullet)
        self.active_count -= 1
        if bullet.origin.type == "user":
            self.active_user_bullets -= 1

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

class BonusBoxes:
    def __init__(self, screen):
        self.bonusBoxes = []
        self.screen = screen

    def add(self, name, x, y):
        self.bonusBoxes.append(BonusBox(name, x, y))

    def blit(self):
        for box in self.bonusBoxes:
            self.screen.blit(box.image, (box.x, box.y))

    def calc_pos(self):
        for box in self.bonusBoxes:
            box.x -= 2

    @staticmethod
    def info(name, property):
        return bonus_boxes_info[name][property]

class BonusBox:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.type = BonusBoxes.info(name, 'type')
        self.reference = BonusBoxes.info(name, 'reference')
        self.addition = BonusBoxes.info(name, 'addition')
        self.image = pygame.image.load(BonusBoxes.info(name, 'image'))
        self.x_off = BonusBoxes.info(name, 'x_off')
        self.y_off = BonusBoxes.info(name, 'y_off')

class Keyboard:
    def __init__(self):
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        self.c = False
        self.space = False
        self.fire = False
        self.x = False

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

# All visible info. Like active weapon, score etc
class Info:

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
        self.pause = False

    def blit_bullet_icons(self, plane, stopwatch):

        # Primary weapon info
        primary_lag = ammo[plane.primary_weapon]['lag']
        time_since_primary = stopwatch.mill - plane.last_shot_primary
        primary_img_active = Info.primary_img_active
        primary_img_unactive = Info.primary_img_unactive

        # Secondary weapon info
        secondary_lag = ammo[plane.secondary_weapon]['lag']
        time_since_secondary = stopwatch.mill - plane.last_shot_secondary
        secondary_img_active = Info.secondary_img_active
        secondary_img_unactive = Info.secondary_img_unactive

        # Show weapon images accordingly to active weapon status
        if plane.active_weapon == plane.primary_weapon:
            self.screen.blit(primary_img_active, (self.primary_x, self.primary_y))
            self.screen.blit(secondary_img_unactive, (self.secondary_x, self.secondary_y))
        else:
            self.screen.blit(primary_img_unactive, (self.primary_x, self.primary_y))
            self.screen.blit(secondary_img_active, (self.secondary_x, self.secondary_y))

        # Calculate and blit loading bars
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

    def blit_pause(self):
        textSurface = self.font.render(('PAUSED'), True, d_blue)
        textRect = textSurface.get_rect()
        textRect.center = (display_width/2,display_height/3)
        self.screen.blit(textSurface, textRect)

    def blit_score(self, score):
        textSurface = self.font.render("Score: " + str(score), True, white)
        textRect = textSurface.get_rect()
        textRect.center = (self.primary_x + 900 + textRect.width/2, self.heart_y + 55)
        self.screen.blit(textSurface, textRect)

    def blit_wave_nr(self, wave_nr):
        textSurface = self.font.render("Wave: " + str(wave_nr+1), True, white)
        textRect = textSurface.get_rect()
        textRect.center = (self.primary_x + 700 + textRect.width/2, self.heart_y + 55)
        self.screen.blit(textSurface, textRect)

    def blit(self, plane, stopwatch, gameplay):
        self.blit_bullet_icons(plane, stopwatch)
        self.blit_heart()
        self.blit_score(gameplay.score)
        self.blit_wave_nr(gameplay.wave_nr)
        self.blit_lives(plane)
        self.blit_ammo(plane)
        if self.pause == True:
            self.blit_pause()

class Gameplay:
    def __init__(self):
        self.plot = plot
        self.wave_nr = 0
        self.wave = self.plot[0]
        self.total_waves = len(self.plot)
        self.remaining_enemies = 0
        self.keyboard = ''
        self.score = 0
        self.spawned = False
        self.gameover = False
        self.gameover_reason = ''
        self.info = ''

    def next_wave(self):
        self.wave_nr += 1
        self.wave = plot[self.wave_nr]
        self.spawned = False

    def checkAmmo(self, plane, bullets):
        if plane.primary_ammo + plane.secondary_ammo == 0 and bullets.active_user_bullets == 0:
            return
            # plane.primary_ammo += mat.arva()


    def addInfo(self, enemies, plane, bonusBoxes, keyboard, info):
        self.enemies = enemies
        self.plane = plane
        self.bonusBoxes = bonusBoxes
        self.keyboard = keyboard
        self.info = info

    def check_if_game_over(self):
        if self.plane.lives <= 0:
            self.gameover_reason = "You got destroyed!"
            self.gameover = True

        return self.gameover


    def pause(self, keyboard, info):
        info.pause = True
        info.blit_pause()
        pygame.display.update()
        p_down = 2
        while p_down > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        p_down -= 1
                        info.pause = False
                    if event.key == pygame.K_DOWN:
                        keyboard.down = False
                    if event.key == pygame.K_UP:
                        keyboard.up = False
                    if event.key == pygame.K_LEFT:
                        keyboard.left = False
                    if event.key == pygame.K_RIGHT:
                        keyboard.right = False
                    if event.key == pygame.K_SPACE:
                        keyboard.space = False
                    if event.key == pygame.K_c:
                        keyboard.c = False
                    if event.key == pygame.K_x:
                        keyboard.x = False

    def spawn(self):
        if self.spawned == False:
            for col_nr, col in enumerate(self.wave):
                for object_nr, object in enumerate(col):
                    # OBJECT IN COLUMN


                    # If enemy
                    if len(object) == 3:
                        x = 1400 + col_nr * 200
                        y = object[2]
                        self.enemies.add(x, y, object[0], object[1])
                        self.remaining_enemies += 1

                    # If bonuspack or new weapon etc
                    else:
                        # If bonus pack
                        if object[0] in bonus_boxes_info:
                            x = 1400 + col_nr * 200
                            self.bonusBoxes.add(object[0], x, object[1])


            self.spawned = True

        if self.remaining_enemies == 0:
            if self.wave_nr != self.total_waves - 1:
                self.next_wave()
            else:
                print("You have completed the game!")
                self.gameover = True


