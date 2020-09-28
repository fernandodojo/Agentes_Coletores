import random


class Robot:
    def __init__(self, y, x, name):
        self.name = name
        self.x = x
        self.y = y
        self.content = []

    def set(self, x, y, trash):
        self.x = x
        self.y = y
        self.trash = trash
        return self

    
    def random_position(self):
        self.x = random.randint(1, 20)
        self.y = random.randint(1, 20)

    def __str__(self):
        return f"{self.name}"
