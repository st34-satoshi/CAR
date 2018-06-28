# if you want to make new environment , you should inherit this class
import random


class Environment:
    def __init__(self, size_x, size_y):
        self.screen_size_x = size_x
        self.screen_size_y = size_y

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