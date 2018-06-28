from player import player
import constant


class Robber(player.Player):
    def __init__(self, environment, id):
        self.radius = constant.robber_radius
        random_state = environment.get_position_randomly(self.radius)  # it has position and direction
        super().__init__(self.radius, constant.robber_eye_radius, random_state[1], random_state[0],
                         constant.robber_color, constant.robber_eye_color, id)