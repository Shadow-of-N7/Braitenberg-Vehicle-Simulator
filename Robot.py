import math

import pygame
import random
import numpy as np
from pygame import gfxdraw
from InstanceHelper import InstanceHelper
from InternalMap import InternalMap
from Sensors.DistanceSensor import DistanceSensor


class Robot:
    def __init__(self, instance_helper: InstanceHelper, position: (float, float)):
        self.position = position
        self.vector = self.set_initial_vector()
        self.screen = instance_helper.screen
        self.radius = 15
        self.body = pygame.draw.circle(self.screen, (0, 0, 255), position, self.radius)
        self.front_sensor = DistanceSensor(instance_helper, position, self.vector, 100, 15) # was 15
        self.lidar = DistanceSensor(instance_helper, position, self.vector, 1500, 0.1) # was 15
        self.lidar_vector = self.vector
        self.rotating = False
        self.rotation_direction = False
        self.rotation_offset = 0
        self.speed = 1
        self.internal_map = InternalMap(3000)
        self.internal_map_position = (self.internal_map.dimension >> 1 for x in position)

    def update(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.position, 15)
        line = pygame.draw.line(self.screen, (255, 75, 0), self.position, self.calculate_line_endpoint(), 4)

        # Modify speed (Must be separated from the direction vector)
        speed_vector = tuple(float(x) * float(self.speed) for x in self.vector)
        self.position = [sum(x) for x in zip(self.position, speed_vector)]
        self.internal_map_position = [sum(x) for x in zip(self.internal_map_position, speed_vector)]
        front_distance = self.front_sensor.update(self.position, self.vector)
        lidar_distance = self.lidar.update(self.position, self.rotate_lidar(self.lidar_vector, 1))

        # Transform into map coordinates
        distance_vector = tuple(float(x) * float(lidar_distance) for x in self.calc_unit_vector(self.lidar_vector))
        visual_position = [sum(x) for x in zip(self.internal_map_position, distance_vector)]
        self.internal_map.set_position(visual_position[1], visual_position[0], 1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.internal_map.export()

        if front_distance < 100:
            self.rotate(4)

        if 180 < front_distance < 185 and not self.rotating:
            self.rotation_direction = self.probe_direction(front_distance)
            self.rotating = True
        elif 120 < front_distance < 180:
            self.rotation_offset = 1
            self.speed = 0.9
        elif 60 < front_distance < 120:
            self.rotation_offset = 2
            self.speed = 0.8
        elif front_distance < 60:
            # Quickly ramp up the turning speed if too close to an obstacle
            self.speed = 0.5
            self.rotation_offset += 1
        else:
            self.rotation_offset = 0
            self.speed = 1
            self.rotating = False
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

    def rotate_lidar(self, vector: (float, float), degrees: int, self_update=True):
        arr = np.array(vector)
        angle = np.degrees(np.arctan2(*arr.T[::-1]))
        angle += degrees
        rad = np.deg2rad(angle)
        x = math.cos(rad)
        y= math.sin(rad)
        self.lidar_vector = x, y
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



