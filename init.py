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
upperInfo = UpperInfo(screen)
gameplay = Gameplay()

# Nuppude asendid
down_arrow = False
up_arrow = False
left_arrow = False
right_arrow = False
space = False
c_but = False