import pygame
import random


class World:
    def __init__(self, screen: pygame.surface.Surface, obstacle_count: int):
        self.screen = screen
        self.obstacles = []
        self.obstacle_count = obstacle_count
        self.obstacle_max_x = 40
        self.obstacle_max_y = 40
        self.regenerate()


    def update(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (0, 0, 0), obstacle)

    def regenerate(self):
        self.obstacles.clear()
        for i in range(self.obstacle_count):
            self.obstacles.append(pygame.Rect(random.randint(0, self.screen.get_width() - self.obstacle_max_x),
                                              random.randint(0, self.screen.get_height() - self.obstacle_max_y),
                                              random.randint(5, self.obstacle_max_x),
                                              random.randint(5, self.obstacle_max_y)))
        # Field borders
        self.obstacles.append(pygame.Rect(0, 0, self.screen.get_width(), 1))  # Top
        self.obstacles.append(pygame.Rect(0, 0, 1, self.screen.get_height()))  # Left
        self.obstacles.append(pygame.Rect(self.screen.get_width() - 1, 0, 1, self.screen.get_height()))  # Right
        self.obstacles.append(pygame.Rect(0, self.screen.get_height() - 1, self.screen.get_width(), 1))  # Bottom