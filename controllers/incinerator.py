class Incinerator:
    def __init__(self, y, x, name):
        self.name = name
        self.y = y
        self.x = x        
        self.content = []

    def __str__(self):
        return f"{self.name}"