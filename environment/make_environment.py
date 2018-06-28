import constant
from environment import square_normal_environment


def make_environment():
    environment = constant.environment
    screen_size_x = constant.screen_size_x
    screen_size_y = constant.screen_size_y
    if environment == 'square':
        return square_normal_environment.SquareNormal(screen_size_x, screen_size_y)

