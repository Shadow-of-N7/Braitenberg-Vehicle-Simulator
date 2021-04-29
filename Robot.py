import math

import pygame
import random
import numpy as np

from InstanceHelper import InstanceHelper
from Sensors.DistanceSensor import DistanceSensor


class Robot:
    def __init__(self, instance_helper: InstanceHelper, position: (int, int)):
        self.position = position
        self.vector = self.set_initial_vector()
        self.screen = instance_helper.screen
        self.radius = 15
        self.body = pygame.draw.circle(self.screen, (0, 0, 255), position, self.radius)
        self.front_sensor = DistanceSensor(instance_helper, position, self.vector, 100, 15)

    def update(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.position, 15)
        line = pygame.draw.line(self.screen, (255, 75, 0), self.position, self.calculate_line_endpoint(), 4)
        self.position = [sum(x) for x in zip(self.position, self.vector)]
        front_distance = self.front_sensor.update(self.position, self.vector)
        if front_distance < 180:
            self.vector = self.rotate(1)
        elif front_distance < 120:
            self.vector = self.rotate(2)
        elif front_distance < 60:
            self.vector = self.rotate(3)

    def rotate(self, degrees: int):
        arr = np.array(self.vector)
        angle = np.degrees(np.arctan2(*arr.T[::-1]))
        angle += degrees
        rad = np.deg2rad(angle)
        return math.cos(rad), math.sin(rad)

    def calculate_line_endpoint(self) -> (int, int):
        arr = np.array(self.vector)
        angle = np.degrees(np.arctan2(*arr.T[::-1]))

        x = self.position[0] + math.cos(math.radians(angle)) * (self.radius - 2)
        y = self.position[1] + math.sin(math.radians(angle)) * (self.radius - 2)
        return x, y

    def set_initial_vector(self) -> (float, float):
        x_vector = random.random()
        y_vector = random.random()
        if bool(random.getrandbits(1)) is False:
            x_vector = -x_vector
        if bool(random.getrandbits(1)) is False:
            y_vector = -y_vector
        return self.calc_unit_vector((x_vector, y_vector))

    def calc_unit_vector(self, vector:(float, float))-> (float, float):
        vector_length = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        try:
            vec_1 = vector[0] / vector_length
            vec_2 = vector[1] / vector_length
        except:
            return (0, 0)
        return vec_1, vec_2



