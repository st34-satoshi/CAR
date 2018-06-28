from player import player
import constant


class Cop(player.Player):
    def __init__(self, environment):
        self.radius = constant.cop_radius
        random_state = environment.get_position_randomly(self.radius)  # it has position and direction
        super().__init__(constant.cop_radius, constant.cop_eye_radius, random_state[1], random_state[0], constant.cop_color, constant.cop_eye_color)
