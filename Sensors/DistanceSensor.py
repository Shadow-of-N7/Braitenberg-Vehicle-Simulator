import math
import pygame
import numpy as np

from InstanceHelper import InstanceHelper

# This sensor shall use raycasting to detect collisions

class DistanceSensor:
    def __init__(self, instance_helper: InstanceHelper, position: (int, int), rotation: (float, float), max_range: int, side_threshold=1):
        """

        :param instance_helper: Instance helper.
        :param position: The caster position.
        :param rotation: Rotation vector of the beam.
        :param max_range: The maximum range of the beam.
        :param side_threshold: The amount of space allowed next to the raycast beam before reporting a collision.
        """
        self.instance_helper = instance_helper
        self.screen = instance_helper.screen
        self.max_range = max_range
        self.position = position
        self.rotation = rotation
        self.side_threshold = side_threshold
        self.unit_vector = self.calc_unit_vector(self.rotation)
        endpoint = self.calc_line_endpoint(position, rotation, max_range)
        self.scanline = pygame.draw.line(self.screen, (0, 255, 0), position, endpoint)

    def update(self, position: (int, int), rotation: (int, int)) -> int:
        """
        :param position: Position of the caster
        :param rotation: Rotation vector of the caster
        :return: The distance to a colliding object
        """
        # Apply position and rotation changes of the robot to the sensor as well
        self.position = position
        self.rotation = rotation
        self.unit_vector = self.calc_unit_vector(self.rotation)

        endpoint = self.raymarch(0, position)
        self.scanline = pygame.draw.line(self.screen, (255, 0, 0), position, endpoint)
        distance = math.sqrt(math.pow(position[0] - endpoint[0], 2) + math.pow(position[1] - endpoint[1], 2))
        return distance

    def calc_line_endpoint(self, position: (int, int), rotation: (int, int), length: int):
        arr = np.array(rotation)
        angle = np.degrees(np.arctan2(*arr.T[::-1]))

        x = position[0] + math.cos(math.radians(angle)) * length
        y = position[1] + math.sin(math.radians(angle)) * length
        return x, y

    def raymarch(self, iteration: int, position: (int, int)):
        """
        Recursively raycasts ahead.
        :param iteration: Iteration number. Increases each iteration.
        :param position: The position of the last iteration or caster.
        :return: Collision point; if not finished: iteration number, too.
        """
        smallest_distance = 1000000000  # Must be something insanely high
        for obstacle in self.instance_helper.world.obstacles:
            distance = self.rect_distance(position, obstacle)
            if distance < smallest_distance:
                smallest_distance = distance

        new_position = (position[0] + (self.unit_vector[0] * smallest_distance), position[1] + (self.unit_vector[1] * smallest_distance))
        # Debug
        pygame.draw.circle(self.screen, (0, 0, 255), position, smallest_distance, width=1)
        if smallest_distance > self.side_threshold \
                and iteration < 50 \
                and position[0] > 0 \
                and position[1] > 0 \
                and position[0] < pygame.display.get_window_size()[0] \
                and position[1] < pygame.display.get_window_size()[1]:
            iteration += 1
            return self.raymarch(iteration, new_position)
        else:
            return new_position

    def calc_unit_vector(self, vector:(float, float))-> (float, float):
        vector_length = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        try:
            vec_1 = vector[0] / vector_length
            vec_2 = vector[1] / vector_length
        except:
            return (0, 0)
        return vec_1, vec_2

    def signed_dist_to_rect(self, point:(int, int), centre: (int, int), size: (int, int)):
        offset = abs(point-centre) - size

    def rect_distance(self, point: (int, int), rect2: pygame.Rect):
        x1, y1 = point
        x1b, y1b = point
        x2, y2 = rect2.topleft
        x2b, y2b = rect2.bottomright
        left = x2b < x1
        right = x1b < x2
        top = y2b < y1
        bottom = y1b < y2
        if bottom and left:
            return math.hypot(x2b - x1, y2 - y1b)
        elif left and top:
            return math.hypot(x2b - x1, y2b - y1)
        elif top and right:
            return math.hypot(x2 - x1b, y2b - y1)
        elif right and bottom:
            return math.hypot(x2 - x1b, y2 - y1b)
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif top:
            return y1 - y2b
        elif bottom:
            return y2 - y1b
        else:  # rectangles intersect
            return 0.