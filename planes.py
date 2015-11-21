"""
"Planes" is a small game made with pygame and python 3.5
Authors: Henry Teigar & Miron Storozev
Tartu Ülikool 2015
"""

""" TODO """
# Bullet image degree calculation
""""""""""""

from init import *


def game_loop():
    pygame.event.clear()

    """ INITIATE ALL GAME SPECIFIC VARIABLES AND RESET OBJECTS (in case of restart)"""
    keyboard.reset()
    plane.reset()
    stopwatch.reset()
    """"""""""""""""""""""""""""""""""""""""""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    keyboard.down = True
                if event.key == pygame.K_UP:
                    keyboard.up = True
                if event.key == pygame.K_LEFT:
                    keyboard.left = True
                if event.key == pygame.K_RIGHT:
                    keyboard.right = True
                if event.key == pygame.K_SPACE:
                    keyboard.space = True
                    keyboard.fire = True
                if event.key == pygame.K_c:
                    plane.swap_weapon()
                    keyboard.c = True
            if event.type == pygame.KEYUP:
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

        # Render moving background
        background.blit()

        """ UPPER INFO PANEL """
        upperInfo.blit(plane, stopwatch)
        """"""""""""""""""""""""


        """ USER PLANE """
        plane.calc_degree(keyboard)
        plane.calc_pos(keyboard)
        plane.blit()
        """"""""""""""""""


        """ FIRE FROM USER WEAPON WHEN NECCESSAŖY """
        if keyboard.space:
            plane.fire(keyboard, stopwatch, bullets)
        """"""""""""""""""""""""""""""""""""""""""


        """ CALCULATE AND RENDER VISIBLE BULLETS"""
        bullets.calc_pos()
        bullets.remove_offscreen()
        bullets.blit()
        """"""""""""""""""""""""""""""


        """ ENEMIES """
        enemies.calc_pos(plane)
        enemies.addInfo(gameplay, stopwatch)
        enemies.check_bullet_col(bullets)
        enemies.remove_offscreen()
        enemies.blit()
        """"""""""""""


        """ GAMEPLAY """
        gameplay.addInfo(enemies)
        gameplay.spawn()
        """"""""""""""


        """ TIME """
        stopwatch.tick()
        clock.tick(60)
        pygame.display.update()
        """"""""""""

# Starts the main loop and resets all variables to default
game_loop()