

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

