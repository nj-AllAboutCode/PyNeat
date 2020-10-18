import pygame
from pygame.locals import *


class Bird(pygame.sprite.Sprite):
    def __init__(self, master):
        self.master = master
        pygame.sprite.Sprite.__init__(self)
        self.s = 20
        self.col = (255, 60, 50)
        self.pos = pygame.math.Vector2(100, self.master.size[1]/2)
        self.vel = pygame.math.Vector2(0, 0)
        self.gravity = pygame.math.Vector2(0, 0.98)
        self.velLimit = self.gravity.y*2
        self.jumpMag = 9
        self.image = pygame.surface.Surface((self.s, self.s))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def jump(self):
        if self.vel.y > -self.velLimit:
            self.vel += pygame.math.Vector2(0, -self.jumpMag)

    def update(self):
        self.pos += self.vel
        self.vel += self.gravity
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.master.pipes):
            self.kill()
        if self.pos.y > self.master.size[1] or self.pos.y < 0:
            self.kill()
