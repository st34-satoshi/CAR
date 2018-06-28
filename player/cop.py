from player import player
import constant


class Cop(player.Player):
    def __init__(self, environment, id):
        self.radius = constant.cop_radius
        random_state = environment.get_position_randomly(self.radius)  # it has position and direction
        super().__init__(constant.cop_radius, constant.cop_eye_radius, random_state[1], random_state[0], constant.cop_color, constant.cop_eye_color, id)
        self.max_speed = constant.cop_max_speed
        self.max_turn = self.max_speed*constant.ratio_speed_direction

    def move_cop(self, ratio_speed, ratio_direction, environment):
        # always use this function when the cop move.
        if ratio_speed < 0:
            ratio_speed = 0
        if ratio_speed > 1:
            ratio_speed = 1
        if ratio_direction > 1:
            ratio_direction = 1
        if ratio_direction < -1:
            ratio_direction = -1
        if ratio_speed + abs(ratio_direction) > 1:
            print("error: cop move ratio " + str(ratio_direction + ", " + str(ratio_speed)))
            ratio_direction = 1 - ratio_speed
        self.change_direction(ratio_direction*self.max_turn)
        self.move_to_direction(ratio_speed*self.max_speed, environment)
