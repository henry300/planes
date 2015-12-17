"""
"Planes" is a small game made with pygame and python 3.5
Authors: Henry Teigar & Miron Storozev
Tartu Ülikool 2015
"""

""" TODO """
# Bonus boxes
# New weapon boxes
# Much more moving styles
# Start screen
# Possibility to start over
# Bullet image degree calculation
# Proper gameplay
# Menus
# Highscore
# Make exe or atleast mac file from the project



# KNOWN BUGS AND NEEDED FIXES

#1  User and enemy collision - x coordinate is fixed and so collision point is wrong
#2  Ammo variable name is not consistent

""""""""""""

from init import *

def game_loop():
    pygame.event.clear()

    """ INITIATE ALL GAME SPECIFIC VARIABLES AND RESET OBJECTS (in case of restart)"""
    keyboard.reset()
    plane.reset()
    stopwatch.reset()
    gameplay.reset()
    enemies.reset(screen)
    bullets.reset(screen)
    """"""""""""""""""""""""""""""""""""""""""
    gameover = False


    while not gameover:
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
                if event.key == pygame.K_x:
                    plane.swap_single()
                    keyboard.x = True
                if event.key == pygame.K_p:
                    gameplay.pause(keyboard, info)
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
                if event.key == pygame.K_x:
                    keyboard.x = False

        # Render moving background
        background.blit()

        """ INFO PANEL AND OTHER INFORMATION"""
        info.blit(plane, stopwatch, gameplay)
        """"""""""""""""""""""""

        """ CALCULATE AND RENDER VISIBLE BULLETS"""
        bullets.calc_pos()
        bullets.remove_offscreen()
        bullets.blit()
        """"""""""""""""""""""""""""""

        """ USER PLANE """
        plane.calc_degree(keyboard)
        plane.calc_pos(keyboard)
        plane.addInfo(stopwatch, gameplay)
        plane.check_bullet_col(bullets)
        plane.effects()
        plane.blit()
        """"""""""""""""""


        """ FIRE FROM USER WEAPON WHEN NECCESSAŖY c"""
        if keyboard.space:
            plane.fire(keyboard, stopwatch, bullets)
        """"""""""""""""""""""""""""""""""""""""""


        """ ENEMIES """
        enemies.calc_pos()
        enemies.addInfo(gameplay, stopwatch, plane, bullets)
        enemies.check_bullet_col(bullets)
        enemies.check_user_col(plane)
        enemies.fire()
        enemies.remove_offscreen()
        enemies.blit()
        """"""""""""""


        """ BONUSBOXES """
        bonusBoxes.calc_pos()
        bonusBoxes.blit()
        """"""""""""""""""


        """ GAMEPLAY """
        gameplay.addInfo(enemies, plane, bonusBoxes, keyboard, info)
        gameplay.checkAmmo(plane, bullets)
        gameplay.spawn()
        gameover = gameplay.check_if_game_over()
        """"""""""""""


        """ TIME """
        stopwatch.tick()
        clock.tick(60)
        pygame.display.update()
        """"""""""""

    ending_screen(gameplay.score)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(pygame.image.load("images/background.png"), (0,0))
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Planes", largeText)
        TextRect.center = ((display_width/2),(100))
        screen.blit(TextSurf, TextRect)

        button("Play",display_width/2 - 125,190,250,50,(8,81,127),(16,110,170),game_loop)
        button("Highscores",display_width/2 - 125,250,250,50,(8,81,127),(16,110,170),highscores)
        button("Quit",display_width/2 - 125,310,250,50,(153,37,37),(185,48,48),exit)
        pygame.display.update()
        clock.tick(15)

def ending_screen(score):

    ending_screen = True

    f = open("highscores.txt", "a")
    f.write(str(score)+"\n")
    f.close()

    while ending_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(pygame.image.load("images/background.png"), (0,0))
        largeText = pygame.font.SysFont("comicsansms",115)
        largeText2 = pygame.font.SysFont("comicsansms",80)

        TextSurf, TextRect = text_objects("Game over!", largeText, (8,81,127))
        TextSurf2, TextRect2 = text_objects("Score: " + str(score), largeText2, (16,110,170))

        TextRect.center = ((display_width/2),(240))
        TextRect2.center = ((display_width/2),(300))
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf2, TextRect2)

        button("OK!",display_width/2 -75,360,150,50,(8,81,127),(16,110,170),game_intro)
        pygame.display.update()
        clock.tick(15)

def highscores():

    highscores = True

    lines = open("highscores.txt", "r", encoding="utf-8").read().splitlines()
    print(lines)
    scores = []
    for line in lines:
        scores.append(int(line))
    scores = sorted(scores)[:-6:-1]

    print(scores)

    while highscores:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(pygame.image.load("images/background.png"), (0,0))
        largeText = pygame.font.SysFont("comicsansms",115)
        largeText2 = pygame.font.SysFont("comicsansms",60)

        TextSurf, TextRect = text_objects("Highscores", largeText)

        for nr, score in enumerate(scores):
            TextSurf3, TextRect3 = text_objects("#"+str(nr+1), largeText2, (8,90,130))
            TextRect3.center = ((540),(160 + int(nr)*45))
            screen.blit(TextSurf3, TextRect3)

            TextSurf2, TextRect2 = text_objects(str(score), largeText2, (8,90,130))
            TextRect2.center = ((display_width/2),(160 + int(nr)*45))
            screen.blit(TextSurf2, TextRect2)


        TextRect.center = ((display_width/2),(70))
        screen.blit(TextSurf, TextRect)

        button("Back",display_width/2 -75,380,150,50,(8,81,127),(16,110,170),game_intro)
        pygame.display.update()
        clock.tick(15)

def exit():
    pygame.quit()
    quit()


# Starts the main loop and resets all variables to default
game_intro()


print(gameplay.gameover_reason)