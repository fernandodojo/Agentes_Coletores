import json
from controllers.board import Board
from controllers.robot import Robot
from random import *




def main():
    with open("configs/configs.json") as i:
        __config = json.load(i)

    r1 = Robot(__config["robot_1_y"], __config["robot_1_x"], "1")
    r2 = Robot(__config["robot_2_y"], __config["robot_2_x"], "2")

    board = Board(r1, r2)
    board.create()
    board.show()

    board.move_rs()
    board.show()

    


if __name__ == '__main__':
    main()
