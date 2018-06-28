import constant


def move_to_aim_direction(direction, aim_direction, max_turn):
    # return the ratio of move and turn
    difference = aim_direction - direction
    if difference > 180:
        difference -= 360.0
    if difference < -180:
        difference += 360.0
    if abs(difference) > constant.ratio_speed_direction:
        # only turn
        if direction > 0:
            return 0, 1
        return 0, -1
    # turn and move
    turn_ratio = difference / max_turn
    return (1 - abs(turn_ratio)), turn_ratio

