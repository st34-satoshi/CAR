from player import player
import constant


class Cop(player.Player):
    def __init__(self, direction, position):
        super().__init__(constant.cop_radius, constant.cop_eye_radius, direction, position, constant.cop_color, constant.cop_eye_color)
