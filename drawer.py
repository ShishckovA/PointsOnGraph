import sys

import networkx as nx

from graph import Vertex, Edge, Point, Graph
from matplotlib import pyplot as plt
from math import sqrt

import pygame
import random

WIDTH = 1920
HEIGHT = 1080
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CENTER = 0.5, -0.6
ZOOM = 250


class Drawer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def draw(self, g: Graph, t: float=0):
        pos = {
            "L1": (-1.7, 0.55), "L2": (-1.92, -1.28),
            "A": (-1.02, -0.19), "B": (0.7, -0.24),
            "R1": (2.71, 0.74), "R2": (2.77, -1.89)
        }
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                sys.exit(0)

        self.screen.fill(WHITE)
        for edge in g.get_edges():
            b, e = pos[edge.begin.name], pos[edge.end.name]

            pygame.draw.line(self.screen, BLACK, (self.to_screen(*b)), (self.to_screen(*e)), width=3)

        for point in g.get_points():
            edge = point.edge
            b, e = pos[edge.begin.name], pos[edge.end.name]
            f = point.t / edge.t
            posx = b[0] + (e[0] - b[0]) * f
            posy = b[1] + (e[1] - b[1]) * f
            pygame.draw.circle(self.screen, GREEN, self.to_screen(posx, posy), 7)
        pygame.display.flip()
        pygame.display.set_caption(f"Общее число точек: {len(g.get_points())}, прошедшее время: {t:.1f}")
        self.clock.tick(FPS)

    def to_screen(self, x, y):
        x -= CENTER[0]
        y -= CENTER[1]
        return (x) * ZOOM + WIDTH // 2, HEIGHT - ((y) * ZOOM + HEIGHT // 2)
