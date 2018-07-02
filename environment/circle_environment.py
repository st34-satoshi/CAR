# circle environment
from environment import super_environment
import constant
from calculation import calc

import pygame
import random


class CircleEnvironment(super_environment.Environment):
    def __init__(self, size_x, size_y):
        super().__init__(size_x, size_y)
        self.center_x = size_x / 2
        self.center_y = size_y / 2

    @staticmethod
    def environment_type():
        return 'circle'

    def draw_environment(self, screen):
        # draw the circle of environment.
        pygame.draw.circle(screen, constant.environment_circle_color, (int(self.center_x), int(self.center_y)), constant.environment_circle_radius, 3)

    def get_position_randomly(self, radius):
        # decide the first position randomly.return the position and a direction
        distance = random.randint(0, constant.environment_circle_radius - radius)
        direction = random.randint(0, 359)
        x = distance * calc.get_cosin(direction) + int(self.screen_size_x / 2)
        y = distance * calc.get_sin(direction) + int(self.screen_size_y / 2)
        di = random.randint(0, 359)
        return (x, y), di

    def get_distance_direction(self, position):
        # return the distance and direction from the present position.現在のポジションで中心からの距離と角度を返す
        distance = self.distance((self.center_x, self.center_y), position)
        direction = self.aim_direction((self.center_x, self.center_y), position)
        return distance, direction

    def get_position_farthest(self, direction, radius):
        # return the position which is farthest from the center of the circle.中心からの距離が一番遠い所のポジションを返す
        # radius is the players radius.
        distance = constant.environment_circle_radius - radius
        x = distance * calc.get_cosin(direction) + self.center_x
        y = distance * calc.get_sin(direction) + self.center_y
        return x, y

    def get_converted_position(self, position_before, position_after, radius):
        # return the able position.if the position over the edge wall it is impossible.
        # if the player is out of the circle , he is paced in the circle
        x = position_after[0]
        y = position_after[1]
        distance_direction = self.get_distance_direction((x, y))
        if constant.environment_circle_radius - radius < distance_direction[0]:
            return self.get_position_farthest(distance_direction[1], radius)
        else:
            return x, y

    def max_distance(self):
        return constant.environment_circle_radius * 2