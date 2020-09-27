import random


class Robot:
    def __init__(self, y, x, name):
        self.name = name
        self.x = x
        self.y = y
        self.trash = None

    def set(self, x, y, trash):
        self.x = x
        self.y = y
        self.trash = trash
        return self

    def move(self, direction):
        if direction == 4:
            self.x -= 1
            return self.y, self.x
        if direction == 8:
            self.y -= 1
            return self.y, self.x
        if direction == 6:
            self.x += 1
            return self.y, self.x
        if direction == 2:
            self.y += 1
            return self.y, self.x

    def random_position(self):
        self.x = random.randint(1, 20)
        self.y = random.randint(1, 20)

    def __str__(self):
        return f"{self.name}"
