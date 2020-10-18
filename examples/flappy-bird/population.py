import random
from agent import *


class Population:
    def __init__(self, master):
        self.master = master
        self.generations = 1
        self.bestAgent = None
        self.lastBestScore = 0
        self.lastBestBrain = None
        self.bestScore = 0
        self.bestFitness = 0
        self.population = []
        self.matingPool = []
        self.bestFitness = 0
        self.popSize = 50
        for i in range(self.popSize):
            self.population.append(Agent(self.master, i))

    def render(self):
        # display population
        for i in self.population:
            i.birdSprite.draw(self.master.screen)
        if self.bestAgent:
            self.bestAgent.birdSprite.draw(self.master.screen)

    def calculateFitness(self):
        cmax = 0
        cbest = None
        for i in self.population:
            i.cacfitness()
            # if fitness is greater than best fitness update best agent and brain
            if i.fitness > self.bestFitness:
                self.bestFitness = i.fitness
                self.bestScore = i.score
                self.Bestbrain = i.brain
                # draw the best brain

            if i.fitness > cmax:
                cbest = i
                cmax = i.fitness
        self.lastBestScore = cbest.score
        self.lastBestBrain = cbest.brain
        print(self.lastBestBrain.fullyConnected())
        # normalize fitness
        for i in self.population:
            i.fitness /= cmax

    def fillMatingPool(self):
        self.matingPool = []
        for i in self.population:
            n = i.fitness * 100
            for j in range(round(n)):
                self.matingPool.append(i)

    def naturalSelection(self):
        # generate new population
        self.calculateFitness()
        self.fillMatingPool()
        self.population = []

        for i in range(self.popSize):
            p1 = self.getPlayer()
            p2 = self.getPlayer()
            if random.random() < 0.99 or not self.bestAgent:  # 99% chance of random parent
                if(p1.fitness > p2.fitness):
                    self.population.append(p1.crossover(p2))
                else:

                    self.population.append(p2.crossover(p1))

            else:  # 1  % chance of best parent
                self.population.append(self.bestAgent.crossover(p1, True))

        self.generations += 1

    def getPlayer(self):
        return random.choice(self.matingPool)

    def update(self):
        for i in self.population:
            if i.birdSprite:
                i.update()
        if self.bestAgent:
            self.bestAgent.update()

        if len(self.master.pipes) == 0:
            # pipe destroyed therefore update score of all alive agents
            for i in self.population:
                if i.bird:
                    i.score += 1
            self.master.addPipe()

        # increment lifespan of bird persecond
        if self.master.frameCount % self.master.fps == 0:
            for i in self.population:
                if i.birdSprite:
                    i.span += 1

        # all genetic stuff
        if self.done():
            self.new()
            self.master.new()

    def new(self):
        self.naturalSelection()
        self.bestAgent = Agent(self.master, "best")
        self.bestAgent.brain = self.Bestbrain
        self.bestAgent.bird.col = (60, 200, 50)
        self.bestAgent.bird.image.fill(self.bestAgent.bird.col)

    def done(self):
        c = 0
        for i in self.population:
            if not i.birdSprite:
                c += 1
        if self.bestAgent:
            return c == self.popSize and not self.bestAgent.birdSprite
        else:
            return c == self.popSize
