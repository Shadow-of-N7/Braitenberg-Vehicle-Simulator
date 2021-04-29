import pygame
import random


class World:
    def __init__(self, screen: pygame.surface.Surface, obstacle_count: int):
        self.screen = screen
        self.obstacles = []
        self.obstacle_max_x = 40
        self.obstacle_max_y = 40
        for i in range(obstacle_count):
            self.obstacles.append(pygame.Rect(random.randint(0, self.screen.get_width() - self.obstacle_max_x),
                                              random.randint(0, self.screen.get_height() - self.obstacle_max_y),
                                              random.randint(5, self.obstacle_max_x), random.randint(5, self.obstacle_max_y)))

    def update(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (0, 0, 0), obstacle)
