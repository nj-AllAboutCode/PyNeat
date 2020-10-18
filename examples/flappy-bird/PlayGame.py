import pygame
from pygame.locals import *
import random
from genome import Genome


class Bird(pygame.sprite.Sprite):
    def __init__(self, master, id):
        self.master = master
        pygame.sprite.Sprite.__init__(self, self.master.birds)
        self.s = 20
        self.id = id
        self.col = (255, 60, 50)
        self.pos = pygame.math.Vector2(100, self.master.size[1]/2)
        self.vel = pygame.math.Vector2(0, 0)
        self.gravity = pygame.math.Vector2(0, 1.0)
        self.velLimit = self.gravity.y*2
        self.jumpMag = 10
        self.inair = False
        self.brain = Genome(3, 1, self.id)
        self.image = pygame.surface.Surface((self.s, self.s))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def jump(self):
        if self.vel.y > -self.velLimit:
            self.vel += pygame.math.Vector2(0, -self.jumpMag)
            self.inair = True

    def update(self):
        if self.vel.y < 0:
            self.inair = False
        self.pos += self.vel
        self.vel += self.gravity
        self.rect.center = self.pos

        if pygame.sprite.spritecollideany(self, self.master.pipes):
            self.kill()

        if self.pos.y > self.master.size[1] or self.pos.y < 0:
            self.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, master, h, up=True):
        self.master = master
        pygame.sprite.Sprite.__init__(
            self, [self.master.pipes, self.master.all_sprites])
        self.w = 15
        self.col = (200, 200, 200)
        self.up = up
        self.h = h
        self.vel = pygame.math.Vector2(-4, 0)
        if self.up:
            self.pos = pygame.math.Vector2(self.master.size[0], 0)
        else:
            self.pos = pygame.math.Vector2(
                self.master.size[0], self.master.size[1]-self.h)

        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.image.fill(self.col)
        self.rect.topleft = self.pos

    def update(self):
        self.pos += self.vel
        self.rect.topleft = self.pos
        if self.pos.x + self.w < 0:
            self.kill()


class Main:
    def __init__(self):
        self.size = (500, 600)
        self.fps = 30
        self.screen = pygame.display.set_mode(self.size)
        self.running = True
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.new()

    def addPipe(self):
        diff = random.uniform(
            self.size[1] / 10, (self.size[1] / 10) * 2)
        Uheight = random.uniform(100, self.size[1]-100-diff)
        LHeight = self.size[1] - Uheight - diff

        self.pipes.add(Pipe(self, Uheight, True))
        self.pipes.add(Pipe(self, LHeight, False))

    def new(self):
        self.birds = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.birds.add(Bird(self, 0))
        self.addPipe()
        self.all_sprites.add(self.pipes)
        self.all_sprites.add(self.birds)

    def quit_(self):
        pygame.quit()
        quit()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_()
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        for i in self.birds:
                            i.jump()

            # update
            self.all_sprites.update()
            if len(self.pipes) == 0:
                self.addPipe()
            if len(self.birds) == 0:
                self.pipes.empty()
                self.birds.empty()
                self.all_sprites.empty()
                self.new()

            # render
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()


g = Main()
g.run()
