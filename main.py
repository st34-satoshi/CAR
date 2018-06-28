
import constant
from player import cop
from player import robber
from environment import make_environment
from decide_action import next_action
import pygame
from pygame.locals import *
import sys


def draw_circle(screen, circle):
    pygame.draw.circle(screen, circle.get_color(), circle.get_position(), circle.get_radius(), 0)


def main():
    # animation
    pygame.init()
    screen = pygame.display.set_mode((constant.screen_size_x, constant.screen_size_y))
    pygame.display.set_caption("Cops and Robbers")
    # make first state.
    environment = make_environment.make_environment()
    action_class = next_action.NextAction()
    cops_array = []
    robbers_array = []
    id = 1
    for i in range(constant.cops_number):
        cp = cop.Cop(environment, id)
        cops_array.append(cp)
        id += 1
    for i in range(constant.robbers_number):
        rob = robber.Robber(environment, id)
        robbers_array.append(rob)
        id += 1
    while True:
        # display the animation
        screen.fill((255, 255, 255, 8))  # background color
        environment.draw_environment(screen)
        for cp in cops_array:
            draw_circle(screen, cp.make_circle_me())
            draw_circle(screen, cp.make_eye_circle())
        for rob in robbers_array:
            draw_circle(screen, rob.make_circle_me())
            draw_circle(screen, rob.make_eye_circle())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        # make state array. state has id, position, direction
        cops_state_array = []
        robbers_state_array = []
        for cp in cops_array:
            cops_state_array.append(cp.make_state())
        for rob in robbers_array:
            robbers_state_array.append(rob.make_state())
        # decide decide_action
        cops_action_array, robbers_action_array = action_class.decide_next_action(cops_state_array, robbers_state_array)
        for cp in cops_array:
            for cp_action in cops_action_array:
                if cp.id == cp_action[0]:
                    cp.move_cop(cp_action[1][0], cp_action[1][1], environment)
        # move cops and robbers. and get next state


if __name__ == '__main__':
    main()
