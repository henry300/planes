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
    # Nuppude asendid
    k_down = False
    k_up = False
    k_left = False
    k_right = False
    k_space = False
    k_c = False

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
                    k_down = True
                if event.key == pygame.K_UP:
                    k_up = True
                if event.key == pygame.K_LEFT:
                    k_left = True
                if event.key == pygame.K_RIGHT:
                    k_right = True
                if event.key == pygame.K_SPACE:
                    k_space = True
                if event.key == pygame.K_c:
                    k_c = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    k_down = False
                if event.key == pygame.K_UP:
                    k_up = False
                if event.key == pygame.K_LEFT:
                    k_left = False
                if event.key == pygame.K_RIGHT:
                    k_right = False
                if event.key == pygame.K_SPACE:
                    k_space = False
                if event.key == pygame.K_c:
                    k_c = False

        # Render moving background
        background.blit()

        """ USER PLANE """
        plane.calc_degree(k_up, k_down)
        plane.calc_pos(k_up, k_down, k_left, k_right)
        plane.blit()
        """"""""""""""""""



        # Advance time and update
        stopwatch.tick()
        clock.tick(60)
        pygame.display.update()


# Starts the main loop and resets all variables to default
game_loop()