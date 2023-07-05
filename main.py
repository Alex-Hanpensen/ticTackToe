#!/usr/bin/env python3
from dataclasses import dataclass
from colorama import *

init(autoreset=True)


class Board:
    victories = [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8],
                 [0, 4, 8],
                 [2, 4, 6]]

    def __init__(self):
        self.fields: list[Cell, ...] = [Cell(False, i, '.') for i in range(9)]

    def change_cell_state(self, cell_id: int, value: str) -> bool:
        if self.fields[cell_id].isbusy:
            return False
        else:
            self.fields[cell_id].isbusy = True
            self.fields[cell_id].value = value
            return True

    def check_win(self) -> bool:
        for i in self.victories:
            if self.fields[i[0]].value in ('X', 'x') and self.fields[i[1]].value in ('X', 'x') and \
                    self.fields[i[2]].value in ('X', 'x'):
                return True
            if self.fields[i[0]].value in ('O', 'o') and self.fields[i[1]].value in ('O', 'o') and \
                    self.fields[i[2]].value in ('O', 'o'):
                return True
        return False

    def __str__(self):
        result = ''
        for i in range(0, 9, 3):
            result += f'{self.fields[i].cell_id} {self.fields[i + 1].cell_id} {self.fields[i + 2].cell_id}' + '   ' + \
                      f'{self.fields[i].value} {self.fields[i + 1].value} {self.fields[i + 2].value} \n'

        return result


@dataclass
class Cell:
    isbusy: bool
    cell_id: int
    value: str


class Player:
    ...


class Game:
    ...


board = Board()
if __name__ == "__main__":
    board.change_cell_state(7, 'x')
    board.change_cell_state(4, 'x')
    board.change_cell_state(1, 'o')
    board.change_cell_state(2, 'o')
    board.change_cell_state(0, 'o')
    print(board.check_win())
    print(board)
