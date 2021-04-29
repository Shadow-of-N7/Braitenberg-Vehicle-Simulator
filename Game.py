import pygame

from InstanceHelper import InstanceHelper
from Robot import Robot
from World import World

instance_helper = InstanceHelper()


class Game:
    def __init__(self):
        self.is_active = True
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Mobile Robots')
        self.world = World(self.screen, 100)
        self.robots = []
        instance_helper.world = self.world
        instance_helper.screen = self.screen

    def loop(self):
        """
        Main loop for everything
        :return:
        """
        while self.is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    self.robots.append(Robot(instance_helper, position))
            self.screen.fill((255, 255, 255))

            self.world.update()

            for robot in self.robots:
                robot.update()
                if pygame.display.get_window_size()[0] + robot.radius < robot.position[0] \
                        or pygame.display.get_window_size()[1] + robot.radius < robot.position[1]\
                        or robot.position[0] + robot.radius < 0\
                        or robot.position[1] + robot.radius < 0:
                    self.robots.remove(robot)

            # Update the screen
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def main():
    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
