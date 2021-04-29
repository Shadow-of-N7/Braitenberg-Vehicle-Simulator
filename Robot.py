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
        self.rotating = False
        self.rotation_direction = False
        self.rotation_offset = 0

    def update(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.position, 15)
        line = pygame.draw.line(self.screen, (255, 75, 0), self.position, self.calculate_line_endpoint(), 4)
        self.position = [sum(x) for x in zip(self.position, self.vector)]
        front_distance = self.front_sensor.update(self.position, self.vector)
        if front_distance < 100:
            self.rotate(4)

        if 180 < front_distance < 185 and not self.rotating:
            self.rotation_direction = self.probe_direction(front_distance)
            self.rotating = True
        elif 120 < front_distance < 180:
            self.rotation_offset = 1
        elif 60 < front_distance < 120:
            self.rotation_offset = 2
        elif front_distance < 60:
            self.rotation_offset = 3
        else:
            self.rotating = False
            pass
        if self.rotating:
            if self.rotation_direction is True:
                self.rotate(-abs(self.rotation_offset))
            else:
                self.rotate(abs(self.rotation_offset))

    def probe_direction(self, left_distance) -> bool:
        """

        :param left_distance:
        :return: True: Left, False: Right
        """
        # Measure distance at 2 points
        self.rotate(1)
        right_distance = self.front_sensor.update(self.position, self.vector)
        self.rotate(-1)
        # Rotate towards the further point
        if left_distance < right_distance:
            return False
        else:
            return True

    def rotate(self, degrees: int):
        arr = np.array(self.vector)
        angle = np.degrees(np.arctan2(*arr.T[::-1]))
        angle += degrees
        rad = np.deg2rad(angle)
        x = math.cos(rad)
        y= math.sin(rad)
        self.vector = x, y
        return x, y

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
        except ZeroDivisionError:
            return 0, 0
        return vec_1, vec_2



