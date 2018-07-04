import pygame
# you can change the constant
screen_size_x = 600  # 300
screen_size_y = 600

# environment
environment = 'circle'  # choose 'torus' , 'square' or 'circle '
environment_circle_color = (200, 200, 200)
environment_circle_radius = 300  # you can change the circle environment radius

# save record
save_record = True  # it save the record when it is True.

# you can play
your_player = 'none'  # choose 'none', 'cop' or 'robber'.you can play
your_color = pygame.color.Color('green')  # the color of the your player
your_eye_color = pygame.color.Color('gold')  # the color of the your 'eye'

# configuration of cops and robbers
ratio_speed_direction = 1  # the ratio how many degree the player can turn at one move.
# cop
cops_number = 4  # there are this number cops
cop_radius = 20  # the size of cops.
cop_eye_radius = 10  # the size of the 'eye' of cop
cop_color = pygame.color.Color('red')  # the color of the cop
cop_eye_color = pygame.color.Color('green')  # the color of the cop 'eye'
cop_max_speed = 2  # cops speed
# robber
robbers_number = 3  # there are this number robbers
robber_radius = 20  # the size of robbers.
robber_eye_radius = 10  # the size of the robber 'eye'
robber_color = pygame.color.Color('blue')  # the color of the robber
robber_eye_color = pygame.color.Color('yellow')  # the color of the robber 'eye'
robber_max_speed = 3  # robber speed
