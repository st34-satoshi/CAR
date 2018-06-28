
import constant
from player import cop
from environment import make_environment
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
    cops_array = []
    robbers_array = []
    for i in range(constant.cops_number):
        p = [50, 50]
        cp = cop.Cop(0, p)
        cops_array.append(cp)
    while True:
        # display the animation
        screen.fill((255, 255, 255, 8))  # background color
        environment.draw_environment(screen)
        for cp in cops_array:
            print("cop")
            draw_circle(screen, cp.make_circle_me())
            draw_circle(screen, cp.make_eye_circle())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        # decide action
        # send action array and get next state



if __name__ == '__main__':
    main()