# if you want to make new environment , you should inherit this class
import random
import math
import constant


class Environment:
    def __init__(self, size_x, size_y):
        self.screen_size_x = size_x
        self.screen_size_y = size_y

    @staticmethod
    def environment_type():
        return 'super'

    def draw_environment(self, screen):
        # draw the environment.
        pass

    def get_converted_position(self, position_before, position_after, radius):
        # if the position is over the environment, change the position to in the environment.
        # positionをもらってafterが環境の外に出ていたりしたら環境の中に変換した後のポジションを返す
        return position_after

    def get_position_randomly(self, radius):
        # decide the first position randomly.return the position and a direction
        x = random.randint(radius, self.screen_size_x - radius)
        y = random.randint(radius, self.screen_size_y - radius)
        di = random.randint(0, 359)
        return (x, y), di

    @staticmethod
    def distance(po1, po2):
        # calculate the distance.
        x = po1[0] - po2[0]
        y = po1[1] - po2[1]
        return math.sqrt(x * x + y * y)

    @staticmethod
    def aim_direction(position_from, aim_position):
        # calculate the direction.
        x = aim_position[0] - position_from[0]
        y = aim_position[1] - position_from[1]
        if x == 0:
            if y > 0:
                return 90
            else:
                return 270
        turn = math.atan(y / x) * 180.0 / math.pi
        if turn < 0:
            if x < 0:
                turn += 180.0
            else:
                turn += 360.0
        else:
            if x < 0:
                turn += 180.0
        return turn

    def distance_with_turn(self, position_from, aim_position, direct):
        # get the distance considering the turn.
        dis = self.distance(position_from, aim_position)
        turn = self.aim_direction(position_from, aim_position)
        dif_dire = turn - direct
        # dif_dire is under 180.
        if dif_dire < 0:
            dif_dire = dif_dire * -1
        if dif_dire > 180:
            dif_dire -= 180
        return dis + dif_dire/constant.ratio_speed_direction

    def max_distance(self):
        return self.distance((0, 0), (self.screen_size_x, self.screen_size_y))


