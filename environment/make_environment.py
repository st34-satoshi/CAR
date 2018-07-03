# when you make new environment, you should change this function

import constant
from environment import square_normal_environment
from environment import circle_environment
from environment import torus_environment


def make_environment():
    environment = constant.environment
    screen_size_x = constant.screen_size_x
    screen_size_y = constant.screen_size_y
    if environment == 'square':
        return square_normal_environment.SquareNormal(screen_size_x, screen_size_y)
    elif environment == 'circle':
        return circle_environment.CircleEnvironment(screen_size_x, screen_size_y)
    elif environment == 'torus':
        return torus_environment.TorusEnvironment(screen_size_x, screen_size_y)
    else:
        print("error: no environment in make_environment. "+str(environment))

