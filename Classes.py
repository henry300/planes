from settings import *
import pygame

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

