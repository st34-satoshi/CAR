import math

import constant


def collision_robbers_array(list_cops, list_robbers, environment):
    # check there are some cops collision to the robber.
    # return collision_robbers_array
    list_collision_robber = []
    for rob in list_robbers:
        for cop in list_cops:
            # the distance between the cop and robber is smaller than the sum of the radius , it means they collide.
            dis = environment.distance(rob.get_position(), cop.get_position())
            if dis < (rob.radius+cop.radius):
                list_collision_robber.append(rob)
                break

    return list_collision_robber


def get_cosin(direction):
    return math.cos((direction/180.0)*math.pi)


def get_sin(direction):
    return math.sin((direction/180.0)*math.pi)


def synthesis_vector(direction_a, weight_a, direction_b, weight_b, environment):
    # synthesis of vector.ベクトルの合成。ベクトルは方向と大きさがある
    x = weight_a*get_cosin(direction_a) + weight_b*get_cosin(direction_b)
    y = weight_a*get_sin(direction_a) + weight_b*get_sin(direction_b)
    sum_weight = environment.distance((0, 0), (x, y))
    sum_direction = environment.aim_direction((0, 0), (x, y))
    return sum_direction, sum_weight


def check_collision_wall_normal_square(position_me, direction, distance, environment):
    x = position_me[0] + distance * get_cosin(direction)
    y = position_me[1] + distance * get_sin(direction)
    if x <= 0 or x >= environment.screen_size_x or y <= 0 or y >= environment.screen_size_y:
        return True
    return False


def check_collision_wall_circle(position_me, direction, distance, environment):
    x = position_me[0] + distance * get_cosin(direction)
    y = position_me[1] + distance * get_sin(direction)
    distance_from_center = environment.distance((x, y), [environment.center_x, environment.center_y])
    if distance_from_center > constant.environment_circle_radius:
        return True
    return False


def get_collision_wall(position_me, direction, distance, environment):
    # distance : if the robber move this distance, is there a collision?
    # do not consider players radius
    if environment.environment_type() == 'square':
        return check_collision_wall_normal_square(position_me, direction, distance, environment)
    elif environment.environment_type() == 'circle':
        return check_collision_wall_circle(position_me, direction, distance, environment)
    # elif mc_file.environment == 11:
    #     # player cannot collide the wall. because there is no wall
    #     return False
    else:
        print("error: no environment get_collision_wall in calc file")


def check_will_collision(position_me, position_opponent, sum_radius, direction_aim, environment):
    # check it will collide.
    angle_dif = direction_aim - environment.aim_direction(position_me, position_opponent)
    if angle_dif < 0:
        # change to plus.
        angle_dif = angle_dif * -1
    if angle_dif > 180:
        # if angle_dif over 180 , 360-angle_dif is the true difference.
        angle_dif = 360 - angle_dif
    if angle_dif > 90:
        return False
    distance = environment.distance(position_me, position_opponent)
    if distance*get_sin(angle_dif) <= sum_radius:
        return True
    return False
