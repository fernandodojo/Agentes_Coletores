import random


class Robot:
    def __init__(self, y, x, name):
        self.name = name
        self.x = x
        self.y = y
        self.content = []
        self.pilha_lixo = []
        self.pilha_lixeira = []
        self.pilha_lixo_dir = []
        self.pilha_reciclador = []
        self.pilha_lixeira_dir = []
        self.pilha_incinerador = []
        self.pilha_reciclador_dir = []
        self.pilha_incinerador_dir = []

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
