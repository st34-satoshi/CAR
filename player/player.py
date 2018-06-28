from player import circle_shape
import math


class Player:
    def __init__(self, radius, eye_radius, direction, position, color, eye_color):
        self.radius = radius
        self.eye_radius = eye_radius
        self.direction = direction
        self.position = position
        self.color = color
        self.eye_color = eye_color

    def get_eye_position(self):
        # return the position of this players eye circle.
        x = (self.radius-self.eye_radius)*math.cos((self.direction/180.0)*math.pi)
        y = (self.radius-self.eye_radius)*math.sin((self.direction/180.0)*math.pi)
        return x+self.position[0], self.position[1]+y

    def make_circle_me(self):
        return circle_shape.CircleShape(self.radius, self.position, self.color)

    def make_eye_circle(self):
        return circle_shape.CircleShape(self.eye_radius, self.get_eye_position(), self.eye_color)

