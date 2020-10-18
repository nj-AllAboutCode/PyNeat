import pygame
import random


def visualize(screen, genome, offsetx, offsety, w, h):

    if genome:
        # draw input nodes
        x = 50
        for i in range(genome.num_in):
            n = genome.nodes[i]
            pygame.draw.circle(screen, (255, 30, 30),
                               (int(x+offsetx), int(offsety+h-50)), 15)
            n.draw_center = (int(x+offsetx), int(offsety+h-50))
            x += 50

        # draw output nodes
        x = 50
        for i in range(genome.num_out):
            n = genome.nodes[genome.num_in + i]
            pygame.draw.circle(screen, (255, 255, 30),
                               (int(x+offsetx), int(offsety+50)), 15)
            n.draw_center = (int(x+offsetx), int(offsety+50))
            x += 50

        # draw extra nodes
        x = 50
        y = 100
        for i in range(len(genome.nodes)-genome.num_in-genome.num_out):
            if x > w:
                x = 50
                y += 50
            n = genome.nodes[genome.num_in + genome.num_out + i]
            pygame.draw.circle(screen, (0, 0, 255),
                               (int(x+offsetx), int(offsety+y)), 15)
            n.draw_center = (int(x+offsetx), int(offsety+y))
            x += 50

        # draw connections
        for i in genome.connections:
            pygame.draw.line(screen, (255, 255, 255),
                             i.from_node.draw_center, i.to_node.draw_center, 2)