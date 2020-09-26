import json
from controllers.board import Board
from controllers.robot import Robot


def main():
    with open("configs/configs.json") as i:
        __config = json.load(i)

    r1 = Robot(__config["robot_1_y"], __config["robot_1_x"])
    r2 = Robot(__config["robot_2_y"], __config["robot_2_x"])

    board = Board(r1, r2)
    board.create()
    board.show()

    for x in range(5):
        board.move_robot1(2)
        board.show()


if __name__ == '__main__':
    main()
