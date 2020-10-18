import pygame
from pygame.locals import *
import random
from population import *
from agent import *
from bird import *
from genome import Genome
from visualize_net import visualize

pygame.init()
pygame.font.init()


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
        self.extra = 400
        self.frameCount = 0
        self.screen = pygame.display.set_mode(
            (self.size[0]+self.extra, self.size[1]))
        self.running = True
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.pop = Population(self)
        self.new()

    def addPipe(self):
        diff = random.uniform(
            self.size[1] / 10 + 20, (self.size[1] / 10) * 2)
        Uheight = random.uniform(100, self.size[1]-100-diff)
        LHeight = self.size[1] - Uheight - diff

        self.pipes.add(Pipe(self, Uheight, True))
        self.pipes.add(Pipe(self, LHeight, False))

    def new(self):
        self.pipes = pygame.sprite.Group()
        self.addPipe()
        self.frameCount = 0

    def quit_(self):
        pygame.quit()
        quit()

    def draw_text(self, text, x, y):
        font = pygame.font.SysFont('monospace', 20)
        textS = font.render(text, True, (255, 255, 255))
        self.screen.blit(textS, (x, y))

    def blit_status(self):
        offsetx = self.size[0]+20

        # show data
        self.draw_text("--Info--", offsetx+20, 20)
        self.draw_text("Population Size: " +
                       str(self.pop.popSize), offsetx+20, 50)

        self.draw_text(
            "Generation: "+str(self.pop.generations), offsetx+20, 80)
        self.draw_text(
            "Best Score: "+str(self.pop.bestScore), offsetx+20, 110)
        self.draw_text("Last gen best score: " +
                       str(self.pop.lastBestScore), offsetx+20, 140)

    def blit_frames(self):
        # draw sepatations
        pygame.draw.line(self.screen, (150, 150, 255),
                         (self.size[0]+20, 0), (self.size[0]+20, self.size[1]), 4)
        pygame.draw.line(self.screen, (150, 150, 255),
                         (self.size[0]+20, self.size[1]/2-2), (self.size[0]+self.extra, self.size[1]/2-2), 4)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.frameCount += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_()

            # update
            self.pipes.update()
            self.pop.update()

            # render
            self.screen.fill((0, 0, 0))
            self.pop.render()
            self.pipes.draw(self.screen)
            self.blit_frames()
            self.blit_status()
            visualize(self.screen, self.pop.lastBestBrain,
                      self.size[0], self.size[1]/2, self.extra, self.size[1]/2)
            pygame.display.flip()


g = Main()
g.run()
