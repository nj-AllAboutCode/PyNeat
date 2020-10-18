from genome import Genome
import random
from bird import Bird
import pygame


class Agent():
    def __init__(self, master, id):
        self.id = id
        self.master = master
        self.brain = Genome(4, 1, self.id)
        self.score = 0
        self.span = 0
        self.bird = Bird(self.master)
        self.birdSprite = pygame.sprite.RenderPlain(self.bird)

    def cacfitness(self):
        if self.score == 0:
            self.fitness = self.span
        else:
            self.fitness = self.score*10 + self.span

    def clone(self):
        clone = Agent(self.master, None)
        clone.brain = self.brain.clone()
        return clone

    def crossover(self, parent, best=False):
        child = Agent(self.master, None)
        if best:
            child.brain = self.brain.crossover(parent.brain)

        else:
            if parent.fitness < self.fitness:
                child.brain = self.brain.crossover(parent.brain)
            else:
                child.brain = parent.brain.crossover(self.brain)
        child.brain.mutate()
        return child

    def update(self):
        self.bird.update()
        # action
        if len(self.master.pipes) != 0:
            inputs = self.get_inputs()
            prediction = self.brain.feedForward(inputs)
            if prediction[0] >= 0.5:
                self.bird.jump()

    def get_inputs(self):
        # distance from upper pipe
        # distance from lower pipe
        # distance from top
        # distaned from bottom
        inputs = []
        pipes = self.master.pipes

        for i in pipes:
            if i.up:
                inputs.append(self.bird.pos.y-i.pos.y)
            else:
                inputs.append(i.pos.y-self.bird.pos.y)

        inputs.append(self.bird.pos.y)
        inputs.append(self.master.size[1]-self.bird.pos.y)

        maxEl = abs(max(inputs, key=abs))
        ret = []
        for i in inputs:
            ret.append(round(i/maxEl, 2))

        return ret
