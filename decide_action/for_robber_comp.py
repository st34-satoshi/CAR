from calculation import calc
import constant


def get_weight_wall(position, size_x, size_y, weight_wall, environment):
    # make the direction and how much the robber want to leave from the wall.
    right = weight_wall/position[0]  # how much the robber want to go to the right direction.
    left = weight_wall/(size_x - position[0])
    below = weight_wall/(position[1])
    above = weight_wall/(size_y - position[1])
    right = right - left
    below = below - above
    weight = environment.distance((0, 0), (right, below))  # the size of vector.
    direction = environment.aim_direction((0, 0), (right, below))
    return direction, weight


def get_weight_cops(position, list_cops, weight_cops, environment):
    # calculate how the robber want to flee from the cop , and which direction the robber want to go.
    sum_weight = 0
    sum_direction = 0
    for cop in list_cops:
        weight = weight_cops/environment.distance(position, cop[1])
        direction = environment.aim_direction(cop[1], position)
        # synthesis of vector.
        x_s = sum_weight*calc.get_cosin(sum_direction)
        y_s = sum_weight*calc.get_sin(sum_direction)
        x = weight*calc.get_cosin(direction) + x_s
        y = weight*calc.get_sin(direction) + y_s
        sum_weight = environment.distance((0, 0), (x, y))
        sum_direction = environment.aim_direction((0, 0), (x, y))
    return sum_direction, sum_weight


def get_weight_corner(position, weight_corner, environment):
    # how much the robber want to leave from the corner.
    list_corner = ((0, 0), (0, environment.screen_size_y), (environment.screen_size_x, 0), (environment.screen_size_x, environment.screen_size_y))
    sum_weight = 0
    sum_direction = 0
    for po in list_corner:
        weight = weight_corner/environment.distance(po, position)
        direction = environment.aim_direction(po, position)
        # synthesis of vector.
        x_s = sum_weight * calc.get_cosin(sum_direction)
        y_s = sum_weight * calc.get_sin(sum_direction)
        x = weight * calc.get_cosin(direction) + x_s
        y = weight * calc.get_sin(direction) + y_s
        sum_weight = environment.distance((0, 0), (x, y))
        sum_direction = environment.aim_direction((0, 0), (x, y))
    return sum_direction, sum_weight


def get_direction_from_cops_and_wall(rob_state, list_cops, environment):
    # decide the direction to go by the cops places and the distance to the wall
    # rob_state is id, position, direction
    position = rob_state[1]
    # direction = shape_player.get_direction()  # どの方向を向いているかも考慮できると良い
    size_x = environment.screen_size_x
    size_y = environment.screen_size_y
    weight_wall = 400  # Inversely proportional constant.
    weight_cops = 2500
    weight_corner = 900
    wall = get_weight_wall(position, size_x, size_y, weight_wall, environment)
    cops = get_weight_cops(position, list_cops, weight_cops, environment)
    # not go to the corner.
    corner = get_weight_corner(position, weight_corner, environment)
    # return the direction.返すのは方向だけ
    x = wall[1]*5*calc.get_cosin(wall[0]) + cops[1]*calc.get_cosin(cops[0]) + corner[1]*5*calc.get_cosin(corner[0])
    y = wall[1]*5*calc.get_sin(wall[0]) + cops[1]*calc.get_sin(cops[0]) + corner[1]*5*calc.get_sin(corner[0])
    return environment.aim_direction((0, 0), (x, y))


def weight_circumference(position, weight_c, environment):
    # calculate the weight.how the robber want to avoid the circumference
    direction = environment.aim_direction(position, [environment.center_x, environment.center_y])
    distance_to_circumference = constant.environment_circle_radius - environment.distance([environment.center_x, environment.center_y],
                                                                                      position)
    weight = weight_c/distance_to_circumference
    return direction, weight


def direction_from_cops_circumference(rob_state, list_cops, environment):
    # decide the direction to go , by the cops places and the distance to the circumference
    # rob_state is id, position, direction
    weight_cops = 2500
    weight_c = 400
    cops = get_weight_cops(rob_state[1], list_cops, weight_cops, environment)
    circumference = weight_circumference(rob_state[1], weight_c, environment)
    x = circumference[1]*5*calc.get_cosin(circumference[0]) + cops[1]*calc.get_cosin(cops[0])
    y = circumference[1] * 5 * calc.get_sin(circumference[0]) + cops[1]*calc.get_sin(cops[0])
    return environment.aim_direction((0, 0), (x, y))


def direction_from_cops_torus(rob_state, list_cops, environment):
    # consider only cops. there are no wall
    return get_weight_cops(rob_state[1], list_cops, 10, environment)[0]


def direction(rob_state, list_placed, list_cops, environment):
    # decide the robber aim direction by the cops and the edge of the environment.
    # rob_state is id, position, direction
    if environment.environment_type() == 'square':
        return get_direction_from_cops_and_wall(rob_state, list_cops, environment)
    elif environment.environment_type() == 'circle':
        return direction_from_cops_circumference(rob_state, list_cops, environment)
    elif environment.environment_type() == 'torus':
        return direction_from_cops_torus(rob_state, list_cops, environment)
    else:
        print("error: no environment in get_direction function in for_robber_comp file")
        return 0


change_angle = 5  # this must be divisor of 180.


def direction_stop(rob_state, list_cops, environment):
    # list_cops contain only cops to consider.
    # decide the direction when the robber stop.
    move_distance = 200  # the distance the robber supposedly move  when the robber stop.

    if len(list_cops) == 1:
        # flee to opposite direction from the cop , if there is one cop.not to collide the wall.
        direction_aim = environment.aim_direction(list_cops[0][1], rob_state[1])
        direction_plus = direction_aim
        direction_minus = direction_aim
        while True:
            if not calc.get_collision_wall(rob_state[1], direction_plus, move_distance, environment):
                return direction_plus
            if not calc.get_collision_wall(rob_state[1], direction_minus, move_distance, environment):
                return direction_minus
            direction_minus -= change_angle
            if direction_minus < 0:
                direction_minus += 360.0
            direction_plus += change_angle
            if direction_plus >= 360:
                direction_plus -= 360.0
    else:
        # when there are some cops, go to the direction where is far from the cops. considering no to  collide the wall.
        # copsが複数の時はそれぞれの中間の方向で一番差が大きいところに行く。壁にはぶつからないところ
        list_dif_cop = []  # copまでの方向との差とcopへの本当の方向
        list_direction_cops = []  #
        for cop in list_cops:
            direct = environment.aim_direction(rob_state[1], cop[1])
            # the direct must be from 0 to 360.
            if direct < 0 or direct >= 360:
                print('error: direction in get_direction_stop in get_robber_direction file')
            list_direction_cops.append(direct)
        list_direction_cops.sort()  # sort. from small.
        for i in range(len(list_direction_cops)):
            dif = list_direction_cops[i] - list_direction_cops[i-1]
            if dif < 0:
                dif += 360
            list_dif_cop.append((-1*dif/2, list_direction_cops[i]))
            list_dif_cop.append((dif/2, list_direction_cops[i-1]))
        # check there is wall.the direction which is the largest difference in the list_dif_cop.
        while True:
            max_dif = 0
            max_pair = list_dif_cop[0]
            for pair in list_dif_cop:
                if abs(pair[0]) > max_dif:
                    max_dif = abs(pair[0])
                    max_pair = pair

            if calc.get_collision_wall(rob_state[1], max_pair[1]+max_pair[0], move_distance, environment):
                # if go to the direction max_pair, collide the wall.
                # remove it from the list.add the new dif close to the cop.
                list_dif_cop.remove(max_pair)
                dif = max_pair[0] - change_angle
                if max_pair[0] < 0:
                    dif = max_pair[0] + change_angle
                list_dif_cop.append((dif, max_pair[1]))
            else:
                # if go this direction, the robber do not collide the wall
                direction_go = max_pair[1] + max_pair[0]
                if direction_go >= 360:
                    direction_go -= 360.0
                if direction_go < 0:
                    direction_go += 360.0
                return direction_go


def direction_emergency(rob_state, list_cops_emergency, environment):
    # decide the direction when emergency. if there is the cop at the aim direction, change the aim direction.
    # if there are cops at the all of the direction, the farthest cop remove from the list
    direction_plus = rob_state[2]
    direction_minus = rob_state[2]
    # make the copy list.
    list_cops = []
    for cop in list_cops_emergency:
        list_cops.append(cop)
    # if there is no cop at this direction , go to this direction.
    count = 0
    while True:
        # cannot go if there is one cop at the aim direction.
        check = 0
        for cop in list_cops:
            if calc.check_will_collision(rob_state[1], cop[1], constant.cop_radius+constant.robber_radius+5, direction_plus, environment):
                # there is at least one cop, the robber should not go this direction.
                check = 1
                break
        if check == 0:
            return direction_plus
        # search same things at direction_minus.
        check = 0
        for cop in list_cops:
            if calc.check_will_collision(rob_state[1], cop[1], constant.cop_radius+constant.robber_radius+5, direction_minus, environment):
                check = 1
                break
        if check == 0:
            return direction_minus
        direction_plus += change_angle
        direction_minus -= change_angle
        if direction_plus > 360:
            direction_plus -= 360
        if direction_minus < 0:
            direction_minus += 360
        count += 1
        if count > 200/change_angle:  # this can be 180 not 200.180でいいはず
            count = 0
            direction_plus = rob_state[2]
            direction_minus = rob_state[2]
            # remove the farthest cop from the list_cops.list_copsから一番遠いやつを除く
            max_dist = 0
            max_cop = list_cops[0]
            for cop in list_cops:
                d = calc.get_distance(rob_state[1], cop.get_position())
                if d > max_dist:
                    max_dist = d
                    max_cop = cop
            list_cops.remove(max_cop)
