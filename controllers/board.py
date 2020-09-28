import json
from random import *
import time
import os
from controllers.trash_can import TrashCan
from controllers.trash import Trash



class Board:
    def __init__(self, robot1, robot2):
        with open("configs/configs.json") as i:
            self.__config = json.load(i)

        self.trash_can_x = TrashCan(self.__config["trash_x_y"], self.__config["trash_x_x"], "X")
        self.trash_can_y = TrashCan(self.__config["trash_y_y"], self.__config["trash_y_x"], "Y")
        self.incinerator_x = self.__config["incinerator_x"]
        self.incinerator_y = self.__config["incinerator_y"]
        self.trash_number = self.__config["trash_number"]
        self.recycler_x = self.__config["recycler_x"]
        self.recycler_y = self.__config["recycler_y"]
        self.size_x = self.__config["size_x"]
        self.size_y = self.__config["size_y"]
        self.robot1 = robot1
        self.robot2 = robot2
        self.trash_list = []
        self.tab = [[]]


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
        self.tab[self.incinerator_y][self.incinerator_x] = "I"
        self.tab[self.recycler_y][self.recycler_x] = "R"
        trash_list = self.trash_gen()

        for i in trash_list:
            self.tab[i.y][i.x] = i

        return self.tab

    def trash_gen(self):
        coordinates = []
        while len(coordinates) < 40:
            rand = (randint(2, 19), randint(2, 19))
            if rand not in coordinates:
                coordinates.append(rand)

        for i in range(len(coordinates)):
            self.trash_list.append(Trash(i, coordinates[i][0], coordinates[i][1], choice(["i", "r"])))

        return self.trash_list

    def busca_lixo(self, direction):
        if direction == 4:
            movimento = self.robot1.x - 1

            if self.tab[self.robot1.y][movimento] == " " or self.tab[self.robot1.y][movimento] in self.trash_list:
                self.robot1.x -= 1

            return self.robot1.y, self.robot1.x

        if direction == 6:
            movimento = self.robot1.x + 1

            if self.tab[self.robot1.y][movimento] == " " or self.tab[self.robot1.y][movimento] in self.trash_list:
                self.robot1.x += 1

            return self.robot1.y, self.robot1.x

        if direction == 8:
            movimento = self.robot1.y - 1

            if self.tab[movimento][self.robot1.x] == " " or self.tab[movimento][self.robot1.x] in self.trash_list:                
                self.robot1.y -= 1

            return self.robot1.y, self.robot1.x

        if direction == 2:
            movimento = self.robot1.y +1
            
            if self.tab[movimento][self.robot1.x] == " " or self.tab[movimento][self.robot1.x] in self.trash_list:
                self.robot1.y += 1
            return self.robot1.y, self.robot1.x


    def busca_lixeira(self, direction):
        lixeira = " "
        if direction == 4:
            movimento = self.robot1.x - 1

            if self.tab[self.robot1.y][movimento] == self.trash_can_x:
                lixeira = self.trash_can_x     
            elif self.tab[self.robot1.y][movimento] == self.trash_can_y:
                lixeira = self.trash_can_y                
            elif self.tab[self.robot1.y][movimento] == " ":
                self.robot1.x -= 1

            return self.robot1.y, self.robot1.x, lixeira

        if direction == 6:
            movimento = self.robot1.x + 1

            if self.tab[self.robot1.y][movimento] == self.trash_can_x:
                lixeira = self.trash_can_x     
            elif self.tab[self.robot1.y][movimento] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[self.robot1.y][movimento] == " ":
                self.robot1.x += 1

            return self.robot1.y, self.robot1.x, lixeira

        if direction == 8:
            movimento = self.robot1.y - 1

            if self.tab[movimento][self.robot1.x] == self.trash_can_x:
                lixeira =  self.trash_can_x
            elif self.tab[movimento][self.robot1.x] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[movimento][self.robot1.x] == " ":                
                self.robot1.y -= 1

            return self.robot1.y, self.robot1.x, lixeira        

        if direction == 2:
            movimento = self.robot1.y +1
            
            if self.tab[movimento][self.robot1.x] == self.trash_can_x:
                lixeira =  self.trash_can_x
            elif self.tab[movimento][self.robot1.x] == self.trash_can_y:
                lixeira = self.trash_can_y
            elif self.tab[movimento][self.robot1.x] == " ":
                self.robot1.y += 1
            return self.robot1.y, self.robot1.x, lixeira  
    
    def reativo_simples_lixo(self):

        while self.trash_list:            	                
            direction = choice([2, 4, 6, 8])
            
            old_x = self.robot1.x
            old_y = self.robot1.y

            y, x = self.busca_lixo(direction)            
            
            if not self.robot1.content:
                if self.tab[y][x] in self.trash_list:
                    lixo = self.tab[y][x]
                    self.robot1.content.append(lixo)
                    self.trash_list.remove(lixo)
                self.tab[y][x] = self.robot1
                self.tab[old_y][old_x] = " "
            else:
                self.reativo_simples_lixeira()
            
            self.show()
            time.sleep(0.01)

    def reativo_simples_lixeira(self):

        while self.robot1.content:             
            direction = choice([2, 4, 6, 8])
            
            old_x = self.robot1.x
            old_y = self.robot1.y

            y, x, lixeira = self.busca_lixeira(direction)            
            
            if lixeira !=" ":
                lixo = self.robot1.content[-1]
                lixeira.content.append(lixo)
                self.robot1.content.pop()
            self.tab[y][x] = self.robot1
            self.tab[old_y][old_x] = " "
            
            self.show()
            time.sleep(0.01)

        
    def show(self):
              
        clear = lambda: os.system('clear')
        clear()
        for i in range(self.size_y):
            print("\n", end="")
            for j in range(self.size_x):
                print(self.tab[i][j], end="")
        
        print("\n")
        print("R1 y:{},x:{}, LIXO:{}, LIXEIRA_X: {}, LIXEIRA_Y:{}".format(self.robot1.y, self.robot1.x, len(self.trash_list), len(self.trash_can_x.content), len(self.trash_can_y.content)))
        print(" ")
        

	    
