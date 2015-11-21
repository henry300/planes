"""
"Planes" is a small game made with pygame and python 3.5
Authors: Henry Teigar & Miron Storozev
Tartu Ülikool 2015
"""
from init import *
pygame.init()


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
        upperInfo.blit_bullet_icons(plane, stopwatch)
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



        # """ ENEMIES """
        # # Add new enemies based on stopwatch
        # enemies.add_new_enemies(stopwatch)
        #
        # # Calculate enemy positions and collisions with user bullets/missles
        # enemies.calc_pos(plane)
        # enemies.check_col(bullets.active_bullets)
        #
        # # Render enemies
        # enemies.blit()
        # """"""""""""""


        # Advance time and update
        stopwatch.tick()
        clock.tick(60)
        pygame.display.update()

# Starts the main loop and resets all variables to default
game_loop()