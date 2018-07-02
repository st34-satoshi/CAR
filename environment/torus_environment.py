# torus environment
from environment import super_environment
import constant
from calculation import calc

import pygame
import random
import math


class TorusEnvironment(super_environment.Environment):
    def __init__(self, size_x, size_y):
        super().__init__(size_x, size_y)
        x_center = size_x / 2
        y_center = size_y / 2
        self.center_position = x_center, y_center

    @staticmethod
    def environment_type():
        return 'torus'

    def get_converted_position(self, position_before, position_after, radius):
        # if the position over the edge , go to opposite position.端に行ったら反対側に行く
        x = position_after[0]
        if x < 0:
            x += self.screen_size_x
        elif x > self.screen_size_x:
            x -= self.screen_size_x
        y = position_after[1]
        if y < 0:
            y += self.screen_size_y
        elif y > self.screen_size_y:
            y -= self.screen_size_y
        return x, y

    def max_distance(self):
        x = self.screen_size_x / 2
        y = self.screen_size_y / 2
        return math.sqrt(x * x + y * y)

    def position_number_torus(self, position):
        # 0:left above, 1:right above, 10:left below, 11:right below
        x = position[0]
        y = position[1]
        x_center = self.center_position[0]
        y_center = self.center_position[1]
        if x < x_center:
            # x is left
            if y < y_center:
                return 0
            return 10
        # x is right
        if y < y_center:
            return 1
        return 11

    def position_relation(self, po1, po2):
        # 0:same area, 1:po2 is right, 2:po2 is left, 3:po2 is above, 4:po2 is below, 13,14,23,24:po2 is diagonal
        area1 = self.position_number_torus(po1)
        area2 = self.position_number_torus(po2)
        dif = area1 - area2
        if dif == 0:
            return 'same'
        elif dif == 10:
            return 'above'
        elif dif == -10:
            return 'below'
        elif dif == 1:
            return 'left'
        elif dif == -1:
            return 'right'
        elif dif == 11:
            return 'left_above'
        elif dif == 9:
            return 'right_above'
        elif dif == -11:
            return 'right_below'
        elif dif == -9:
            return 'left_below'
        else:
            print("error: not match the number in position_relation function in calc file")
            return 'error'

    def smaller_dis_dire(self, dis_dire1, dis_dire2):
        # return the smaller one. pair of the distance and direction
        if dis_dire1[0] < dis_dire2[0]:
            return dis_dire1
        return dis_dire2

    def get_distance_direction_torus(self, po1, po2):
        relation = self.position_relation(po1, po2)
        dis_dire_normal = super().distance(po1, po2), super().aim_direction(po1, po2)
        if relation == 'same':
            return dis_dire_normal
        if relation == 'above':
            # po2 is above po1
            position_n = po2[0], po2[1] + self.screen_size_y
            dis_dire = super().distance(po1, position_n), super().aim_direction(po1, position_n)
            return self.smaller_dis_dire(dis_dire_normal, dis_dire)
        elif relation == 'below':
            position_n = po2[0], po2[1] - self.screen_size_y
            dis_dire = super().distance(po1, position_n), super().aim_direction(po1, position_n)
            return self.smaller_dis_dire(dis_dire_normal, dis_dire)
        elif relation == 'left':
            position_n = po2[0] + self.screen_size_x, po2[1]
            dis_dire = super().distance(po1, position_n), super().aim_direction(po1, position_n)
            return self.smaller_dis_dire(dis_dire_normal, dis_dire)
        elif relation == 'right':
            position_n = po2[0] - self.screen_size_x, po2[1]
            dis_dire = super().distance(po1, position_n), super().aim_direction(po1, position_n)
            return self.smaller_dis_dire(dis_dire_normal, dis_dire)
        elif relation == 'left_above':
            position_n1 = po2[0] + self.screen_size_x, po2[1]  # right above
            position_n2 = po2[0] + self.screen_size_x, po2[1] + self.screen_size_y  # right below
            position_n3 = po2[0], po2[1] + self.screen_size_y  # left below
            dis_dire1 = super().distance(po1, position_n1), super().aim_direction(po1, position_n1)
            dis_dire2 = super().distance(po1, position_n2), super().aim_direction(po1, position_n2)
            dis_dire3 = super().distance(po1, position_n3), super().aim_direction(po1, position_n3)
            dis_dire = self.smaller_dis_dire(dis_dire_normal, dis_dire1)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire2)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire3)
            return dis_dire
        elif relation == 'right_above':
            position_n1 = po2[0] - self.screen_size_x, po2[1]  # left above
            position_n2 = po2[0] - self.screen_size_x, po2[1] + self.screen_size_y  # left below
            position_n3 = po2[0], po2[1] + self.screen_size_y  # right below
            dis_dire1 = super().distance(po1, position_n1), super().aim_direction(po1, position_n1)
            dis_dire2 = super().distance(po1, position_n2), super().aim_direction(po1, position_n2)
            dis_dire3 = super().distance(po1, position_n3), super().aim_direction(po1, position_n3)
            dis_dire = self.smaller_dis_dire(dis_dire_normal, dis_dire1)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire2)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire3)
            return dis_dire
        elif relation == 'left_below':
            position_n1 = po2[0] + self.screen_size_x, po2[1]  # right below
            position_n2 = po2[0] + self.screen_size_x, po2[1] - self.screen_size_y  # right above
            position_n3 = po2[0], po2[1] - self.screen_size_y  # left above
            dis_dire1 = super().distance(po1, position_n1), super().aim_direction(po1, position_n1)
            dis_dire2 = super().distance(po1, position_n2), super().aim_direction(po1, position_n2)
            dis_dire3 = super().distance(po1, position_n3), super().aim_direction(po1, position_n3)
            dis_dire = self.smaller_dis_dire(dis_dire_normal, dis_dire1)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire2)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire3)
            return dis_dire
        elif relation == 'right_below':
            position_n1 = po2[0] - self.screen_size_x, po2[1]  # left below
            position_n2 = po2[0] - self.screen_size_x, po2[1] - self.screen_size_y  # left above
            position_n3 = po2[0], po2[1] - self.screen_size_y  # right above
            dis_dire1 = super().distance(po1, position_n1), super().aim_direction(po1, position_n1)
            dis_dire2 = super().distance(po1, position_n2), super().aim_direction(po1, position_n2)
            dis_dire3 = super().distance(po1, position_n3), super().aim_direction(po1, position_n3)
            dis_dire = self.smaller_dis_dire(dis_dire_normal, dis_dire1)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire2)
            dis_dire = self.smaller_dis_dire(dis_dire, dis_dire3)
            return dis_dire
        else:
            print("error : no area in get_distance_torus function in calc file")
            return 0, 0

    def distance(self, po1, po2):
        # calculate the distance.
        return self.get_distance_direction_torus(po1, po2)[0]

    def aim_direction(self, position_from, aim_position):
        # calculate the direction.
        return self.get_distance_direction_torus(position_from, aim_position)[1]

