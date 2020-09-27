class Trash:
    def __init__(self, id_number, y, x, kind):
        self.id_number = id_number
        self.x = x
        self.y = y
        self.kind = kind

    def __str__(self):
        return f"{self.kind}"
