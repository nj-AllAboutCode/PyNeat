import random
from gene import *


class Genome:
    def __init__(self, num_in, num_out, id, offspring=False):
        self.num_in = num_in
        self.num_out = num_out
        self.id = id
        self.offspring = offspring
        self.layers = 2
        self.nextNode = 0
        self.nodes = []
        self.connections = []
        self.generateFull()

    def generateFull(self):
        if not self.offspring:
            # add input nodes
            for _ in range(self.num_in):
                self.nodes.append(NodeGene(self.nextNode, 0))
                self.nextNode += 1

            for _ in range(self.num_out):
                self.nodes.append(NodeGene(self.nextNode, 1, True))
                self.nextNode += 1

            for i in range(self.num_in):
                for j in range(self.num_out):
                    weight = random.uniform(-1, 1)
                    out = ConnectionGene(
                        self.nodes[i], self.nodes[j+self.num_in], weight)
                    self.connections.append(out)
                    self.nodes[i].output_connections.append(out)

    def generateNew(self):
        # remove all output connections
        for i in self.nodes:
            i.output_connections = []

        # add connections to nodes
        for i in self.connections:
            i.from_node.output_connections.append(i)

        # sort nodes by layer
        self.nodes.sort(key=lambda x: x.lay)

    def feedForward(self, inputValues):

        # prepare network
        self.generateNew()

        # clear old inputs
        for i in self.nodes:
            i.input_sum = 0

        # asign to input nodes
        for i in range(self.num_in):
            self.nodes[i].output_val = inputValues[i]

        # engage all nodes and get result
        result = []
        for i in self.nodes:
            i.engage()
            if i.isOut:
                result.append(i.output_val)
        return result

    def commonConnection(self, innN, connections):
        # find a common connection
        for conn in connections:
            if innN == conn.getInnovationNum():
                return connections.index(conn)
        return -1

    def add_node(self):
        # pick a random connection and remove it
        conn = random.choice(self.connections)
        conn.enabled = False
        self.connections.remove(conn)

        # create a new node and shift nodes to match the layer value
        node = NodeGene(self.nextNode, conn.from_node.lay + 1)
        for n in self.nodes:
            if n.lay > conn.from_node.lay:
                n.lay += 1

        # make new connections
        conn1 = ConnectionGene(conn.from_node, node,
                               random.uniform(-1, 1))
        conn2 = ConnectionGene(node, conn.to_node, random.uniform(-1, 1))

        # update class variables
        self.layers += 1
        self.connections.append(conn1)
        self.connections.append(conn2)
        self.nodes.append(node)
        self.nextNode += 1

    def fullyConnected(self):
        max_conn = 0
        nodes_perlayer = [None for i in range(self.layers)]
        for i in self.nodes:
            if nodes_perlayer[i.lay]:
                nodes_perlayer[i.lay] += 1
            else:
                nodes_perlayer[i.lay] = 1

        for i in range(self.layers-1):
            for j in range(i+1, self.layers):
                max_conn += nodes_perlayer[i] * nodes_perlayer[j]
        # print(max_conn)
        return (max_conn == len(self.connections))

    def nodes_connected(self, n1, n2):
        for i in self.connections:
            if (i.from_node == n1 and i.to_node == n2) or (i.from_node == n2 and i.to_node == n1):
                return True
        return False

    def add_connection(self):
        if not self.fullyConnected():
            n1, n2 = random.choice(self.nodes), random.choice(self.nodes)
            while ((n1.lay == n2.lay) or self.nodes_connected(n1, n2) or (n1.isOut and n2.isOut)):
                n1, n2 = random.choice(self.nodes), random.choice(self.nodes)
            if n1.lay > n2.lay:
                temp = n1
                n1 = n2
                n2 = temp
            new_conn = ConnectionGene(n1, n2, random.uniform(-1, 1))
            self.connections.append(new_conn)

    def clone(self):
        clone = Genome(self.num_in, self.num_in, self.id)
        clone.nodes = self.nodes
        clone.connections = self.connections
        return clone

    def getNode(self, n):
        for i in range(len(self.nodes)):
            if self.nodes[i].inum == n:
                return i

    def getWeight(self):
        return len(self.connections) + len(self.nodes)

    def mutate(self):
        if random.random() < 0.8:
            # print("Mutating Connections !")
            for i in self.connections:
                i.mutateWeight()

        if random.random() < 0.5:
            # print("Mutating Biases !")
            for i in self.nodes:
                i.mutateBias()

        if random.random() < 0.01:
            # print("Adding Node !")
            self.add_node()

        if random.random() < 0.05:
            # print("Adding Connections !")
            self.add_connection()

        if random.random() < 0.1:
            #print("change activation functions")
            n = random.choice(self.nodes)
            if not n.isOut:
                n.mutateActivation()
        # print("END MUTATION ")

    def crossover(self, partner):
        child = Genome(self.num_in, self.num_out, 0, True)
        child.nextNode = self.nextNode

        # get all nodes from self and 50% chance of output node from partner
        for n in self.nodes:
            node = n.clone()
            if n.isOut:
                pNode = partner.nodes[partner.getNode(node.inum)]
                if random.random() < 0.5:
                    node.bias = pNode.bias
            child.nodes.append(node)

        # randomly take connections from this node or parent node
        for i in self.connections:
            index = self.commonConnection(
                i.getInnovationNum(), partner.connections)
            if index != -1:
                # there is a common connection
                if random.random() < 0.5:
                    conn = i.clone()
                else:
                    conn = partner.connections[index].clone()
            else:
                conn = i.clone()

            fNode = child.nodes[child.getNode(conn.from_node.inum)]
            lNode = child.nodes[child.getNode(conn.to_node.inum)]
            conn.from_node = fNode
            conn.to_node = lNode
            if fNode and lNode:
                child.connections.append(conn)

        child.layers = self.layers
        return child


# f = Genome(2, 2, 'd')
# print(f.fullyConnected())
# f.add_node()
# f.add_node()
# print(f.fullyConnected())
