from settings import *
import pygame
class Background:
    speed = bg_speed
    # image_surf = pygame.image.load("images/background.png")

    def __init__(self):
        self.x1 = 0
        self.x2 = display_width

    def blit(self):
        if self.x1 < -display_width:
            self.x1 = display_width
        if self.x2 < -display_width:
            self.x2 = display_width

