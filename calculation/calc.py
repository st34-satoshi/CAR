import math


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

