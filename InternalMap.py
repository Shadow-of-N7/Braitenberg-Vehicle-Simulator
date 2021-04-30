import pygame
import numpy as np


class InternalMap:
    def __init__(self, map_dimensions: int):
        self.dimension = map_dimensions
        self.map = np.empty((map_dimensions, map_dimensions), int)
        self.map.fill(0)

    def set_position(self, y: int, x: int, value: int):
        self.map[round(y), round(x)] = value

    def export(self):
        surface = pygame.surface.Surface((self.dimension, self.dimension))
        for x in range(self.dimension):
            for y in range(self.dimension):
                value = self.map[y, x]
                if value != 0:
                    surface.set_at((x, y), (0, 0, 0))
                else:
                    surface.set_at((x, y), (255, 255, 255))
        pygame.image.save(surface, "map.png")

