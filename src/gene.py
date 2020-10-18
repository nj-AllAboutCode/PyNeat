import random
import math


class NodeGene:
    def __init__(self, inum, lay, isOut=False):
        self.inum = inum
        self.lay = lay
        self.isOut = isOut
        self.bias = random.uniform(-1, 1)
        self.input_sum = 0
        self.output_val = 0
        self.output_connections = []
        self.x, self.y = None, None

    def activation(self, x):
        # sigmoid activation
        return 1/(1 + math.exp(-x))

    def mutateBias(self):
        # 5% chance of being changed to a new value
        if random.random() < 0.05:
            self.bias = random.uniform(-1, 1)
        # 95% chance of random change
        else:
            self.bias += random.gauss(0, 1)/50

    def clone(self):
        # generate a clone
        node = NodeGene(self.inum, self.lay, self.isOut)
        node.bias = self.bias
        return node

    def connected_to(self, n):
        # check connection between two nodes
        if n.lay == self.lay:
            return False
        elif n.lay > self.lay:
            for i in self.output_connections:
                if i.toNode == n:
                    return True
        else:
            for i in self.output_connections:
                if i.toNode == self:
                    return True

    def engage(self):
        # no activation for input layer
        if self.lay != 0:
            self.output_val = self.activation(self.input_sum + self.bias)

        for i in self.output_connections:
            if i.enabled:
                i.to_node.input_sum += i.weight * self.output_val


class ConnectionGene:
    def __init__(self, frm, to, weight):
        self.from_node = frm
        self.to_node = to
        self.weight = weight
        self.enabled = True

    def mutateWeight(self):
        # 5% chance of being changed to a new value
        if random.random() < 0.05:
            self.weight = random.uniform(-1, 1)
        # 95% chance of random change
        else:
            self.weight += random.gauss(0, 1)/50

    def clone(self):
        clone = ConnectionGene(self.from_node, self.to_node, self.weight)
        clone.enabled = self.enabled
        return clone

    def getInnovationNum(self):
        # return the innovation number for this connection gene
        return (1/2)*(self.from_node.inum + self.to_node.inum)*(self.from_node.inum + self.to_node.inum + 1) + self.to_node.inum
