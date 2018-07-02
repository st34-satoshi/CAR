from player import circle_shape
import math


class Player:
    def __init__(self, radius, eye_radius, direction, position, color, eye_color, id):
        self.radius = radius
        self.eye_radius = eye_radius
        self.direction = direction
        self.position = position
        self.color = color
        self.eye_color = eye_color
        self.id = id
        self.human = False  # if human play, it is True

    def set_human(self):
        self.human = True

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_eye_position(self):
        # return the position of this players eye circle.
        x = (self.radius-self.eye_radius)*math.cos((self.direction/180.0)*math.pi)
        y = (self.radius-self.eye_radius)*math.sin((self.direction/180.0)*math.pi)
        return x+self.position[0], self.position[1]+y

    def get_record_string(self):
        # return the string data of this class
        return str(self.id) + "," + str(self.direction) + "," + str(self.position[0]) + "," + str(self.position[1]) + "," + str(self.human) + ","

    def read_from_data(self, data):
        list_data = data.pop(0).split(",")
        self.id = int(list_data[0])
        self.direction = float(list_data[1])
        x = float(list_data[2])
        y = float(list_data[3])
        self.position = [x, y]
        if list_data[4] == 'True':
            self.human = True

    def make_circle_me(self):
        return circle_shape.CircleShape(self.radius, self.position, self.color)

    def make_eye_circle(self):
        return circle_shape.CircleShape(self.eye_radius, self.get_eye_position(), self.eye_color)

    def make_state(self):
        # state has id, position, direction
        return self.id, self.position, self.direction

    def change_direction(self, add_di):
        self.direction += add_di
        if self.direction > 360:
            self.direction -= 360
        if self.direction < 0:
            self.direction += 360

    def add_position(self, add_x, add_y, environment):
        # change the position. add add_x and add_y.if the new position is out of the environment , change to in it.
        x = self.get_position()[0] + add_x
        y = self.get_position()[1] + add_y
        self.set_position(environment.get_converted_position(self.get_position(), (x, y), self.radius))

    def move_to_direction(self, speed, environment):
        # move to the direction.the speed is the distance to move.
        self.add_position(speed*math.cos((self.direction/180)*math.pi), speed*math.sin((self.direction/180)*math.pi), environment)


