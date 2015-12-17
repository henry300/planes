from settings import *
from Classes import *
from math import *
from random import *


# Create main frame and caption for it
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(caption)

# Enable mouse setting
pygame.mouse.set_visible(mouse)

# Create clock for the game
clock = pygame.time.Clock()

# Create necessary objects
background = Background(screen)
plane = Plane(screen)
keyboard = Keyboard()
enemies = Enemies(screen)
bullets = Bullets(screen)
stopwatch = Stopwatch()
info = Info(screen)
bonusBoxes = BonusBoxes(screen)
gameplay = Gameplay()

# Nuppude asendid
down_arrow = False
up_arrow = False
left_arrow = False
right_arrow = False
space = False
c_but = False

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("calibri",26)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
