import json
from random import *
from controllers.trash_can import TrashCan
from controllers.trash import Trash


class Board:
    def __init__(self, robot1, robot2):
        with open("configs/configs.json") as i:
            self.__config = json.load(i)

        self.trash_can_x = TrashCan(self.__config["trash_x_y"], self.__config["trash_x_x"])
        self.trash_can_y = TrashCan(self.__config["trash_y_y"], self.__config["trash_y_x"])
        self.incinerator_x = self.__config["incinerator_x"]
        self.incinerator_y = self.__config["incinerator_y"]
        self.trash_number = self.__config["trash_number"]
        self.recycler_x = self.__config["recycler_x"]
        self.recycler_y = self.__config["recycler_y"]
        self.size_x = self.__config["size_x"]
        self.size_y = self.__config["size_y"]
        self.robot1 = robot1
        self.robot2 = robot2
        self.tab = [[]]
        self.trash = []

    def create(self):
        self.tab = [[" "] * self.size_x for i in range(self.size_y)]

        for i in range(self.size_y):
            for j in range(self.size_x):
                if i == 0 or i == self.size_y - 1:
                    self.tab[i][j] = "%"
                elif j == 0 or j == self.size_x - 1:
                    self.tab[i][j] = "%"
        self.tab[self.robot1.y][self.robot1.x] = "1"
        self.tab[self.robot2.y][self.robot2.x] = "2"
        self.tab[self.trash_can_x.y][self.trash_can_x.x] = "X"
        self.tab[self.trash_can_y.y][self.trash_can_y.x] = "Y"
        self.tab[self.incinerator_y][self.incinerator_x] = "I"
        self.tab[self.recycler_y][self.recycler_x] = "R"
        trash_list = self.trash_gen()

        for i in trash_list:
            self.tab[i.y][i.x] = i.kind

        return self.tab

    def trash_gen(self):
        coordinates = []
        while len(coordinates) < 40:
            rand = (randint(2, 19), randint(2, 19))
            if rand not in coordinates:
                coordinates.append(rand)

        for i in range(len(coordinates)):
            self.trash.append(Trash(i, coordinates[i][0], coordinates[i][1], choice(["i", "r"])))

        return self.trash

    def random_mov(self):
        old_x = self.robot1.x
        old_y = self.robot1.y

        self.robot1.random_position()
        self.tab[self.robot1.y][self.robot1.x] = "1"
        self.tab[old_x][old_y] = ' '

    def validate_move(self, x, y):
        if y <= 0 or y >= self.size_y - 1:
            return False
        elif x <= 0 or x >= self.size_x - 1:
            return False
        return True

    def move_robot1(self, direction):
        old_x = self.robot1.x
        old_y = self.robot1.y

        y, x = self.robot1.move(direction)
        if self.validate_move(x, y):
            self.tab[y][x] = "1"
            self.tab[old_y][old_x] = " "
            print("MOVIMENTO VALIDO")
            print("old: y:{},x:{}".format(old_y, old_x))
            print("new: y:{},x:{}".format(y, x))
        else:
            print("MOVIMENTO INVALIDO")

    def show(self):
        for i in range(self.size_y):
            print("\n", end="")
            for j in range(self.size_x):
                print(self.tab[i][j], end="")
        print("\n")
