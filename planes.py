"""
"Planes" is a small game made with pygame and python 3.5
Authors: Henry Teigar & Miron Storozev
Tartu Ülikool 2015
"""
from init import *
pygame.init()


def game_loop():
    pygame.event.clear()


    """ INITIATE ALL GAME SPECIFIC VARIABLES AND OBJECTS """
    # Nuppude asendid
    down_arrow = False
    up_arrow = False
    left_arrow = False
    right_arrow = False
    space = False
    c_but = False

    # Create necessary objects
    background = Background(screen)
    # print(Background.speeds)
    # plane = Plane()
    # enemies = Enemies()
    # bullets = Bullets()
    # missles = Missles()
    stopwatch = Stopwatch()
    """"""""""""""""""""""""""""""""""""""""""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    down_arrow = True
                if event.key == pygame.K_UP:
                    up_arrow = True
                if event.key == pygame.K_LEFT:
                    left_arrow = True
                if event.key == pygame.K_RIGHT:
                    right_arrow = True
                if event.key == pygame.K_SPACE:
                    space = True
                if event.key == pygame.K_c:
                    c_but = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_arrow = False
                if event.key == pygame.K_UP:
                    up_arrow = False
                if event.key == pygame.K_LEFT:
                    left_arrow = False
                if event.key == pygame.K_RIGHT:
                    right_arrow = False
                if event.key == pygame.K_SPACE:
                    space = False
                if event.key == pygame.K_c:
                    c_but = False

        # Render moving background
        background.blit()





        # Advance time and update
        stopwatch.tick()
        clock.tick(60)
        pygame.display.update()


# Starts the main loop and resets all variables to default
game_loop()