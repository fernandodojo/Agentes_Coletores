import json
from random import *
import time
import os
from controllers.trash_can import TrashCan
from controllers.trash import Trash
from controllers.incinerator import Incinerator
from controllers.recycler import Recycler


class Board:
    def __init__(self, robot1, robot2):
        with open("configs/configs.json") as i:
            self.__config = json.load(i)

        self.trash_can_x = TrashCan(self.__config["trash_x_y"],
                                    self.__config["trash_x_x"], "X")
        self.trash_can_y = TrashCan(self.__config["trash_y_y"],
                                    self.__config["trash_y_x"], "Y")
        self.incinerator = Incinerator(self.__config["incinerator_y"], self.__config["incinerator_x"], "I")
        self.recycler = Recycler(self.__config["recycler_y"], self.__config["recycler_x"], "R")
        self.trash_number = self.__config["trash_number"]
        self.size_x = self.__config["size_x"]
        self.size_y = self.__config["size_y"]
        self.robot1 = robot1
        self.robot2 = robot2
        self.trash_list = []
        self.tab = [[]]
        self.qtd_i = 0
        self.qtd_r = 0

    def create(self):
        self.tab = [[" "] * self.size_x for i in range(self.size_y)]

        for i in range(self.size_y):
            for j in range(self.size_x):
                if i == 0 or i == self.size_y - 1:
                    self.tab[i][j] = "%"
                elif j == 0 or j == self.size_x - 1:
                    self.tab[i][j] = "%"
        self.tab[self.robot1.y][self.robot1.x] = self.robot1
        self.tab[self.robot2.y][self.robot2.x] = self.robot2
        self.tab[self.trash_can_x.y][self.trash_can_x.x] = self.trash_can_x
        self.tab[self.trash_can_y.y][self.trash_can_y.x] = self.trash_can_y
        self.tab[self.incinerator.y][self.incinerator.x] = self.incinerator
        self.tab[self.recycler.y][self.recycler.x] = self.recycler
        trash_list = self.trash_gen()

        for i in trash_list:
            self.tab[i.y][i.x] = i

        """for i in range(len(self.trash_list)):
            lixo = self.trash_list[i]
            if i < 10:
                self.trash_can_x.content.append(lixo)
            elif i >= 10:
                self.trash_can_y.content.append(lixo)

        self.trash_list = []

        for i in self.trash_list:
            self.robot2.content.append(i)

        self.trash_list = []"""

        return self.tab

    def trash_gen(self):
        coordinates = []
        while len(coordinates) < 40:
            rand = (randint(2, 19), randint(2, 19))
            if rand not in coordinates:
                coordinates.append(rand)

        for i in range(len(coordinates)):
            self.trash_list.append(
                Trash(i, coordinates[i][0], coordinates[i][1],
                      choice(["i", "r"])))

        for i in self.trash_list:
            if i.kind == "i":
                self.qtd_i += 1
            else:
                self.qtd_r += 1

        return self.trash_list

    def busca_lixo(self, direction):
        lixo = False

        if direction == 4:
            movimento = self.robot1.x - 1

            if self.tab[self.robot1.y][movimento] in self.trash_list:
                lixo = self.tab[self.robot1.y][movimento]
                self.robot1.x -= 1
            elif self.tab[self.robot1.y][movimento] == " ":
                self.robot1.x -= 1

            return self.robot1.y, self.robot1.x, lixo

        if direction == 6:
            movimento = self.robot1.x + 1

            if self.tab[self.robot1.y][movimento] in self.trash_list:
                lixo = self.tab[self.robot1.y][movimento]
                self.robot1.x += 1
            elif self.tab[self.robot1.y][movimento] == " ":
                self.robot1.x += 1

            return self.robot1.y, self.robot1.x, lixo

        if direction == 8:
            movimento = self.robot1.y - 1

            if self.tab[movimento][self.robot1.x] in self.trash_list:
                lixo = self.tab[movimento][self.robot1.x]
                self.robot1.y -= 1
            elif self.tab[movimento][self.robot1.x] == " ":
                self.robot1.y -= 1

            return self.robot1.y, self.robot1.x, lixo

        if direction == 2:
            movimento = self.robot1.y + 1

            if self.tab[movimento][self.robot1.x] in self.trash_list:
                lixo = self.tab[movimento][self.robot1.x]
                self.robot1.y += 1
            elif self.tab[movimento][self.robot1.x] == " ":
                self.robot1.y += 1
            return self.robot1.y, self.robot1.x, lixo

    def busca_lixo_dir(self):
        lixo = False

        left = self.robot1.x - 1
        if self.tab[self.robot1.y][left] in self.trash_list:
            lixo = self.tab[self.robot1.y][left]
            return self.robot1.y, left, lixo, 4
        return self.robot1.y, self.robot1.x, lixo, 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] in self.trash_list):
            lixo = self.tab[self.robot1.y][right]
            return self.robot1.y, right, lixo, 6
        return self.robot1.y, self.robot1.x, lixo, 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] in self.trash_list):
            lixo = self.tab[up][self.robot1.x]
            return up, self.robot1.x, lixo, 8
        return self.robot1.y, self.robot1.x, lixo, 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] in self.trash_list):
            lixo = self.tab[down][self.robot1.x]
            return down, self.robot1.x, lixo, 2
        return self.robot1.y, self.robot1.x, lixo, 2

    def busca_lixeira(self, robot, direction):
        lixeira = False

        if direction == 4:
            movimento = robot.x - 1

            if self.tab[robot.y][movimento] == self.trash_can_x:
                lixeira = self.trash_can_x
            elif self.tab[robot.y][movimento] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[robot.y][movimento] == " ":
                robot.x -= 1

            return robot.y, robot.x, lixeira

        if direction == 6:
            movimento = robot.x + 1

            if self.tab[robot.y][movimento] == self.trash_can_x:
                lixeira = self.trash_can_x
            elif self.tab[robot.y][movimento] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[robot.y][movimento] == " ":
                robot.x += 1

            return robot.y, robot.x, lixeira

        if direction == 8:
            movimento = robot.y - 1

            if self.tab[movimento][robot.x] == self.trash_can_x:
                lixeira = self.trash_can_x
            elif self.tab[movimento][robot.x] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[movimento][robot.x] == " ":
                robot.y -= 1

            return robot.y, robot.x, lixeira

        if direction == 2:
            movimento = robot.y + 1

            if self.tab[movimento][robot.x] == self.trash_can_x:
                lixeira = self.trash_can_x
            elif self.tab[movimento][robot.x] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[movimento][robot.x] == " ":
                robot.y += 1
            return robot.y, robot.x, lixeira

    def busca_lixeira_dir(self, robot):
        lixeira = False

        left = self.robot1.x - 1
        if (self.tab[self.robot1.y][left] == self.trash_can_x):
            lixeira = self.trash_can_x
            return robot.y, left, lixeira, 4
        return robot.y, robot.x, lixeira, 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] == self.trash_can_y):
            lixeira = self.trash_can_x
            return robot.y, right, lixeira, 6
        return robot.y, robot.x, lixeira, 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] == self.trash_can_x):
            lixeira = self.trash_can_x
            return up, robot.x, lixeira, 8
        return robot.y, robot.x, lixeira, 8

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] == self.trash_can_y):
            lixeira = self.trash_can_y
            return up, robot.x, lixeira, 8
        return robot.y, robot.x, lixeira, 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] == self.trash_can_x):
            lixeira = self.trash_can_x
            return robot.y, robot.x, lixeira, 2
        return robot.y, robot.x, lixeira, 2

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] == self.trash_can_y):
            lixeira = self.trash_can_y
            return robot.y, robot.x, lixeira, 2
        return robot.y, robot.x, lixeira, 2


    def busca_incinerador(self, direction):
        incinerador = False

        if direction == 4:
            movimento = self.robot2.x - 1

            if self.tab[self.robot2.y][movimento] == self.incinerator:
                incinerador = self.incinerator
            elif self.tab[self.robot2.y][movimento] == " ":
                self.robot2.x -= 1

            return self.robot2.y, self.robot2.x, incinerador

        if direction == 6:
            movimento = self.robot2.x + 1

            if self.tab[self.robot2.y][movimento] == self.incinerator:
                incinerador = self.incinerator
            elif self.tab[self.robot2.y][movimento] == " ":
                self.robot2.x += 1

            return self.robot2.y, self.robot2.x, incinerador

        if direction == 8:
            movimento = self.robot2.y - 1

            if self.tab[movimento][self.robot2.x] == self.incinerator:
                incinerador = self.incinerator
            elif self.tab[movimento][self.robot2.x] == " ":
                self.robot2.y -= 1

            return self.robot2.y, self.robot2.x, incinerador

        if direction == 2:
            movimento = self.robot2.y + 1

            if self.tab[movimento][self.robot2.x] == self.incinerator:
                incinerador = self.incinerator
            elif self.tab[movimento][self.robot2.x] == " ":
                self.robot2.y += 1
            return self.robot2.y, self.robot2.x, incinerador

    def busca_reciclador(self, direction):
        reciclador = False

        if direction == 4:
            movimento = self.robot2.x - 1

            if self.tab[self.robot2.y][movimento] == self.recycler:
                reciclador = self.recycler
            elif self.tab[self.robot2.y][movimento] == " ":
                self.robot2.x -= 1

            return self.robot2.y, self.robot2.x, reciclador

        if direction == 6:
            movimento = self.robot2.x + 1

            if self.tab[self.robot2.y][movimento] == self.recycler:
                reciclador = self.recycler
            elif self.tab[self.robot2.y][movimento] == " ":
                self.robot2.x += 1

            return self.robot2.y, self.robot2.x, reciclador

        if direction == 8:
            movimento = self.robot2.y - 1

            if self.tab[movimento][self.robot2.x] == self.recycler:
                reciclador = self.recycler
            elif self.tab[movimento][self.robot2.x] == " ":
                self.robot2.y -= 1

            return self.robot2.y, self.robot2.x, reciclador

        if direction == 2:
            movimento = self.robot2.y + 1

            if self.tab[movimento][self.robot2.x] == self.recycler:
                reciclador = self.recycler
            elif self.tab[movimento][self.robot2.x] == " ":
                self.robot2.y += 1
            return self.robot2.y, self.robot2.x, reciclador

    def sensor_lixo(self):
        left = self.robot1.x - 1
        if (self.tab[self.robot1.y][left] in self.trash_list):
            return 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] in self.trash_list):
            return 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] in self.trash_list):
            return 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] in self.trash_list):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_lixo2(self):
        if self.robot1.pilha_lixo and self.robot1.pilha_lixo_dir:
            return self.robot1.pilha_lixo_dir.pop()

        left = self.robot1.x - 1
        if (self.tab[self.robot1.y][left] in self.trash_list):
            return 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] in self.trash_list):
            return 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] in self.trash_list):
            return 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] in self.trash_list):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_lixeira(self):
        left = self.robot1.x - 1
        if (self.tab[self.robot1.y][left] == self.trash_can_x):
            return 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] == self.trash_can_y):
            return 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] == self.trash_can_x) or (self.tab[up][self.robot1.x] == self.trash_can_y):
            return 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] == self.trash_can_x) or (self.tab[down][self.robot1.x] == self.trash_can_y):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_lixeira2(self):
        if self.robot1.pilha_lixeira and self.robot1.pilha_lixeira_dir:
            return self.robot1.pilha_lixeira_dir.pop()

        left = self.robot1.x - 1
        if (self.tab[self.robot1.y][left] == self.trash_can_x):
            return 4

        right = self.robot1.x + 1
        if (self.tab[self.robot1.y][right] == self.trash_can_y):
            return 6

        up = self.robot1.y - 1
        if (self.tab[up][self.robot1.x] == self.trash_can_x) or (self.tab[up][self.robot1.x] == self.trash_can_y):
            return 8

        down = self.robot1.y + 1
        if (self.tab[down][self.robot1.x] == self.trash_can_x) or (self.tab[down][self.robot1.x] == self.trash_can_y):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_lixeira_r2(self):
        left = self.robot2.x - 1
        if (self.tab[self.robot2.y][left] == self.trash_can_x) and (self.trash_can_x.content):
            return 4

        right = self.robot2.x + 1
        if (self.tab[self.robot2.y][right] == self.trash_can_y) and (self.trash_can_y.content):
            return 6

        up = self.robot2.y - 1
        if (self.tab[up][self.robot2.x] == self.trash_can_x) and (self.trash_can_x.content) or (self.tab[up][self.robot2.x] == self.trash_can_y) and (self.trash_can_y.content):
            return 8

        down = self.robot2.y + 1
        if (self.tab[down][self.robot2.x] == self.trash_can_x) and (self.trash_can_x.content) or (self.tab[down][self.robot2.x] == self.trash_can_y) and (self.trash_can_y.content):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_reciclador(self):
        right = self.robot2.x + 1
        if (self.tab[self.robot2.y][right] == self.recycler):
            return 6

        down = self.robot2.y + 1
        if (self.tab[down][self.robot2.x] == self.recycler):
            return 2

        return choice([2, 4, 6, 8])

    def sensor_incinerador(self):
        left = self.robot2.x - 1
        if (self.tab[self.robot2.y][left] == self.incinerator):
            return 4

        down = self.robot2.y + 1
        if (self.tab[down][self.robot2.x] == self.incinerator):
            return 2

        return choice([2, 4, 6, 8])

    def reativo_simples(self):
        while self.trash_list or self.robot1.content or self.trash_can_x.content or self.trash_can_y.content or self.robot2.content:
            if not self.robot1.content and self.trash_list:
                direction = self.sensor_lixo2()

                lixeira_y, lixeira_x, lixeira_lixeira, passo = self.busca_lixeira_dir(self.robot1)

                if direction == 4:
                    passo = 6
                elif direction == 8:
                    passo = 2
                elif direction == 6:
                    passo = 4
                else:
                    passo = 8

                self.robot1.pilha_lixeira_dir.append(passo)
                if lixeira_lixeira and (lixeira_lixeira not in self.robot1.pilha_lixeira):
                    self.robot1.pilha_lixeira.append(lixeira_lixeira)

                old_x = self.robot1.x
                old_y = self.robot1.y

                y, x, lixo = self.busca_lixo(direction)

                if lixo:
                    """if lixeira_lixeira:
                        self.robot1.pilha_lixeira.remove(lixeira_lixeira)"""
                    self.robot1.content.append(lixo)
                    self.trash_list.remove(lixo)
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot1

                self.show()

            if self.robot1.content:
                direction = self.sensor_lixeira2()

                #passo = self.sensor_lixo()
                lixo_y, lixo_x, lixo_lixo, passo = self.busca_lixo_dir()

                if direction == 4:
                    passo = 6
                elif direction == 8:
                    passo = 2
                elif direction == 6:
                    passo = 4
                else:
                    passo = 8

                self.robot1.pilha_lixo_dir.append(passo)
                if lixo_lixo and (lixo_lixo not in self.robot1.pilha_lixo):
                    self.robot1.pilha_lixo.append(lixo_lixo)

                old_x = self.robot1.x
                old_y = self.robot1.y

                y, x, lixeira = self.busca_lixeira(self.robot1, direction)

                if lixeira:
                    lixo = self.robot1.content[0]
                    if lixo in self.robot1.pilha_lixo:
                        self.robot1.pilha_lixo.remove(lixo)
                    lixeira.content.append(lixo)
                    self.robot1.content.remove(lixo)
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot1
                self.show()

            """if ((not self.robot2.content) and (self.trash_can_x.content)) or ((not self.robot2.content) and (self.trash_can_y.content)):
                direction = self.sensor_lixeira_r2()

                old_x = self.robot2.x
                old_y = self.robot2.y

                y, x, lixeira = self.busca_lixeira(self.robot2, direction)

                if lixeira and lixeira.content:
                    lixo = lixeira.content[0]
                    self.robot2.content.append(lixo)
                    lixeira.content.remove(lixo)
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()

            if self.robot2.content and self.robot2.content[0].kind == "i":
                direction = self.sensor_incinerador()

                old_x = self.robot2.x
                old_y = self.robot2.y

                y, x, incinerador = self.busca_incinerador(direction)

                if incinerador:
                    lixo = self.robot2.content[0]
                    self.incinerator.content.append(lixo)
                    self.robot2.content.remove(lixo)
                    self.qtd_i -= 1
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()

            if self.robot2.content and self.robot2.content[0].kind == "r":
                direction = self.sensor_reciclador()

                old_x = self.robot2.x
                old_y = self.robot2.y

                y, x, reciclador = self.busca_reciclador(direction)

                if reciclador:
                    lixo = self.robot2.content[0]
                    self.recycler.content.append(lixo)
                    self.robot2.content.remove(lixo)
                    self.qtd_r -= 1
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()"""

            # self.show()
            #time.sleep(0.01)

    def show(self):

        clear = lambda: os.system('clear')
        clear()
        for i in range(self.size_y):
            print("\n", end="")
            for j in range(self.size_x):
                print(self.tab[i][j], end="")

        print("\n")
        print("R1 y:{},x:{}, LIXO:{}, LIXEIRA_X: {}, LIXEIRA_Y:{}, R1_CONT:{}".
              format(self.robot1.y, self.robot1.x, len(self.trash_list),
                     len(self.trash_can_x.content),
                     len(self.trash_can_y.content), len(self.robot1.content)))
        print(" ")
        tipo = 0
        if self.robot2.content:
            tipo = self.robot2.content[0].kind


        print("R2 y:{},x:{}, LIXO:{}, LIXEIRA_X: {}, LIXEIRA_Y:{}, R2_CONT:{}, TIPO:{}, QTDR:{} RECICLADOR:{}, QTDI:{}, INCINERADOR:{}".
              format(self.robot2.y, self.robot2.x, len(self.trash_list),
                     len(self.trash_can_x.content),
                     len(self.trash_can_y.content), len(self.robot2.content), tipo, self.qtd_r, len(self.recycler.content), self.qtd_i, len(self.incinerator.content)))
        print(" ")
        #print("PILHA_LIXO:{}".format(self.robot1.pilha_lixo))
        #print("PILHA_LIXO_DIR:{}".format(self.robot1.pilha_lixo_dir))

        print("PILHA_LIXEIRA:{}".format(self.robot1.pilha_lixeira))
        print("PILHA_LIXEIRA_DIR:{}".format(self.robot1.pilha_lixeira_dir))
