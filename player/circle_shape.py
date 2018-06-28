

class CircleShape:
    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.color = color

    def get_radius(self):
        return self.radius

    def get_position(self):
        x = round(self.position[0])
        y = round(self.position[1])
        return x, y

    def get_color(self):
        return self.color
