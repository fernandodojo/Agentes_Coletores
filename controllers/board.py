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
                    self.tab[i][j] = "O"
                elif j == 0 or j == self.size_x - 1:
                    self.tab[i][j] = "O"
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

    def mover_lixo(self, direction):
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

    def mover(self, robot, direction):

        if direction == 4:
            movimento = robot.x - 1
            if self.tab[robot.y][movimento] == " ":
                robot.x -= 1
            return robot.y, robot.x

        if direction == 6:
            movimento = robot.x + 1
            if self.tab[robot.y][movimento] == " ":
                robot.x += 1
            return robot.y, robot.x

        if direction == 8:
            movimento = robot.y - 1
            if self.tab[movimento][robot.x] == " ":
                robot.y -= 1
            return robot.y, robot.x

        if direction == 2:
            movimento = robot.y + 1
            if self.tab[movimento][robot.x] == " ":
                robot.y += 1
            return robot.y, robot.x

    def direcao_lixo(self):
        if self.robot1.pilha_lixo and self.robot1.pilha_lixo_dir:
            return self.robot1.pilha_lixo_dir.pop()
        else:
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

    def direcao_lixeira(self):
        if self.robot1.pilha_lixeira and self.robot1.pilha_lixeira_dir:
            return self.robot1.pilha_lixeira_dir.pop()
        else:
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

    def direcao_lixeira_r2(self):
        if self.robot2.pilha_lixeira and self.robot2.pilha_lixeira_dir:
            return self.robot2.pilha_lixeira_dir.pop()
        else:
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

    def direcao_reciclador(self):
        if self.robot2.pilha_reciclador and self.robot2.pilha_reciclador_dir:
            return self.robot2.pilha_reciclador_dir.pop()
        else:
            right = self.robot2.x + 1
            if (self.tab[self.robot2.y][right] == self.recycler):
                return 6

            down = self.robot2.y + 1
            if (self.tab[down][self.robot2.x] == self.recycler):
                return 2

            return choice([2, 4, 6])

    def direcao_incinerador(self):
        if self.robot2.pilha_incinerador and self.robot2.pilha_incinerador_dir:
            return self.robot2.pilha_incinerador_dir.pop()
        else:
            left = self.robot2.x - 1
            if (self.tab[self.robot2.y][left] == self.incinerator):
                return 4

            down = self.robot2.y + 1
            if (self.tab[down][self.robot2.x] == self.incinerator):
                return 2

            return choice([2, 4, 6])

    def sensor_incinerador(self):
        incinerador = False

        left = self.robot2.x - 1
        if (self.tab[self.robot2.y][left] == self.incinerator):
            return self.tab[self.robot2.y][left]

        down = self.robot2.y + 1
        if (self.tab[down][self.robot2.x] == self.incinerator):
            return self.tab[down][self.robot2.x]

    def sensor_reciclador(self):
        reciclador = False

        right = self.robot2.x + 1
        if (self.tab[self.robot2.y][right] == self.recycler):
            return self.tab[self.robot2.y][right]

        down = self.robot2.y + 1
        if (self.tab[down][self.robot2.x] == self.recycler):
            return self.tab[down][self.robot2.x]

    def sensor_lixo(self):
        lixo = False

        left = self.robot1.x - 1
        if isinstance(self.tab[self.robot1.y][left], Trash):
            return self.tab[self.robot1.y][left]

        right = self.robot1.x + 1
        if isinstance(self.tab[self.robot1.y][right], Trash):
            return self.tab[self.robot1.y][right]

        up = self.robot1.y - 1
        if isinstance(self.tab[up][self.robot1.x], Trash):
            return self.tab[up][self.robot1.x]

        down = self.robot1.y + 1
        if isinstance(self.tab[down][self.robot1.x], Trash):
            return self.tab[down][self.robot1.x]

        return lixo

    def sensor_lixeira(self, robot):
        lixeira = False

        left = robot.x - 1
        if isinstance(self.tab[robot.y][left], TrashCan):
            return self.tab[robot.y][left]

        right = robot.x + 1
        if isinstance(self.tab[robot.y][right], TrashCan):
            return self.tab[robot.y][right]

        up = robot.y - 1
        if isinstance(self.tab[up][robot.x], TrashCan):
            return self.tab[up][robot.x]

        down = robot.y + 1
        if isinstance(self.tab[down][robot.x], TrashCan):
            return self.tab[down][robot.x]

        return lixeira

    def reativo_simples(self):
        while self.trash_list or self.robot1.content or self.trash_can_x.content or self.trash_can_y.content or self.robot2.content:
        #while self.trash_list or self.robot1.content:
            if not self.robot1.content:
                direction = self.direcao_lixo()

                lixeira = self.sensor_lixeira(self.robot1)

                passo = self.__config[str(direction)]

                if lixeira:
                    self.robot1.pilha_lixeira_dir = []
                    self.robot1.pilha_lixeira = []
                    if lixeira not in self.robot1.pilha_lixeira:
                        self.robot1.pilha_lixeira.append(lixeira)
                self.robot1.pilha_lixeira_dir.append(passo)

                old_x = self.robot1.x
                old_y = self.robot1.y

                y, x, lixo = self.mover_lixo(direction)

                if lixo:
                    self.robot1.content.append(lixo)
                    self.trash_list.remove(lixo)
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot1

                self.show()

            if self.robot1.content:
                direction = self.direcao_lixeira()

                lixo = self.sensor_lixo()

                passo = self.__config[str(direction)]

                if lixo:
                    self.robot1.pilha_lixo_dir = []
                    self.robot1.pilha_lixo = []
                    if lixo not in self.robot1.pilha_lixo:
                        self.robot1.pilha_lixo.append(lixo)
                self.robot1.pilha_lixo_dir.append(passo)

                old_x = self.robot1.x
                old_y = self.robot1.y

                y, x = self.mover(self.robot1, direction)
                lixeira = self.sensor_lixeira(self.robot1)

                if lixeira:
                    lixo = self.robot1.content[0]
                    lixeira.content.append(lixo)
                    self.robot1.content.remove(lixo)

                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot1
                self.show()

            if ((not self.robot2.content) and (self.trash_can_x.content)) or ((not self.robot2.content) and (self.trash_can_y.content)):
                direction = self.direcao_lixeira_r2()
                passo = self.__config[str(direction)]

                incinerador = self.sensor_incinerador()
                if incinerador:
                    self.robot2.pilha_incinerador_dir = []
                    self.robot2.pilha_incinerador = []
                    if incinerador not in self.robot2.pilha_incinerador:
                        self.robot2.pilha_incinerador.append(incinerador)
                self.robot2.pilha_incinerador_dir.append(passo)

                reciclador = self.sensor_reciclador()
                if reciclador:
                    self.robot2.pilha_reciclador_dir = []
                    self.robot2.pilha_reciclador = []
                    if reciclador not in self.robot2.pilha_reciclador:
                        self.robot2.pilha_reciclador.append(reciclador)
                self.robot2.pilha_reciclador_dir.append(passo)

                old_x = self.robot2.x
                old_y = self.robot2.y

                #y, x, lixeira = self.busca_lixeira(self.robot2, direction)
                y, x = self.mover(self.robot2, direction)
                lixeira = self.sensor_lixeira(self.robot2)

                if lixeira and lixeira.content:
                    lixo = lixeira.content[0]
                    self.robot2.content.append(lixo)
                    lixeira.content.remove(lixo)
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()

            if self.robot2.content and self.robot2.content[0].kind == "i":
                direction = self.direcao_incinerador()
                passo = self.__config[str(direction)]

                lixeira = self.sensor_lixeira(self.robot2)
                if lixeira and lixeira.content:
                    self.robot2.pilha_lixeira_dir = []
                    self.robot2.pilha_lixeira = []
                    if lixeira not in self.robot2.pilha_lixeira:
                        self.robot2.pilha_lixeira.append(lixeira)
                self.robot2.pilha_lixeira_dir.append(passo)

                reciclador = self.sensor_reciclador()
                if reciclador:
                    self.robot2.pilha_reciclador_dir = []
                    self.robot2.pilha_reciclador = []
                    if reciclador not in self.robot2.pilha_reciclador:
                        self.robot2.pilha_reciclador.append(reciclador)
                self.robot2.pilha_reciclador_dir.append(passo)

                old_x = self.robot2.x
                old_y = self.robot2.y

                y, x = self.mover(self.robot2, direction)
                incinerador = self.sensor_incinerador()

                if incinerador:
                    lixo = self.robot2.content[0]
                    self.incinerator.content.append(lixo)
                    self.robot2.content.remove(lixo)
                    self.qtd_i -= 1
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()

            if self.robot2.content and self.robot2.content[0].kind == "r":
                direction = self.direcao_reciclador()
                passo = self.__config[str(direction)]

                lixeira = self.sensor_lixeira(self.robot2)
                if lixeira and lixeira.content:
                    self.robot2.pilha_lixeira_dir = []
                    self.robot2.pilha_lixeira = []
                    if lixeira not in self.robot2.pilha_lixeira:
                        self.robot2.pilha_lixeira.append(lixeira)
                self.robot2.pilha_lixeira_dir.append(passo)

                incinerador = self.sensor_incinerador()
                if incinerador:
                    self.robot2.pilha_incinerador_dir = []
                    self.robot2.pilha_incinerador = []
                    if incinerador not in self.robot2.pilha_incinerador:
                        self.robot2.pilha_incinerador.append(incinerador)
                self.robot2.pilha_incinerador_dir.append(passo)

                old_x = self.robot2.x
                old_y = self.robot2.y

                y, x = self.mover(self.robot2, direction)
                reciclador = self.sensor_reciclador()

                if reciclador:
                    lixo = self.robot2.content[0]
                    self.recycler.content.append(lixo)
                    self.robot2.content.remove(lixo)
                    self.qtd_r -= 1
                self.tab[old_y][old_x] = " "
                self.tab[y][x] = self.robot2
                self.show()
            # self.show()
            #time.sleep(0.005)

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
        """print("PILHA_LIXO_DIR:{}".format(self.robot1.pilha_lixo_dir))
        print("PILHA_LIXO:{}".format(self.robot1.pilha_lixo))
        print(" ")

        print("PILHA_LIXEIRA:{}".format(self.robot1.pilha_lixeira))
        print("PILHA_LIXEIRA_DIR:{}".format(self.robot1.pilha_lixeira_dir))
        print(" ")

        print("PILHA_LIXEIRA2:{}".format(self.robot2.pilha_lixeira))
        print("PILHA_LIXEIRA_DIR2:{}".format(self.robot2.pilha_lixeira_dir))
        print(" ")

        print("PILHA_INCINERADOR2:{}".format(self.robot2.pilha_incinerador))
        print("PILHA_INCINERADOR2_DIR2:{}".format(self.robot2.pilha_incinerador_dir))
        print(" ")

        print("PILHA_RECICLADOR2:{}".format(self.robot2.pilha_reciclador))
        print("PILHA_RECICLADOR2_DIR2:{}".format(self.robot2.pilha_reciclador_dir))
        print(" ")"""
