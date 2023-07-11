from dataclasses import dataclass
from copy import deepcopy
from colorama import *

init()


@dataclass(slots=True)
class Cell:
    cell_id: int
    isbusy: bool = False
    value: str = ''


class Board:
    __VICTORIES = [(0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6)]

    def __init__(self, fields: list[Cell, ...] = None):
        if fields is None:
            self.fields = [Cell(i) for i in range(9)]
        else:
            self.fields = deepcopy(fields)

    def change_cell_state(self, cell_id: int, value: str) -> bool:
        if self.fields[cell_id].isbusy:
            return False
        else:
            self.fields[cell_id].isbusy = True
            self.fields[cell_id].value = value
            return True

    def check_win(self) -> bool:
        for i in self.__VICTORIES:
            if self.fields[i[0]].value == self.fields[i[1]].value == self.fields[i[2]].value != '':
                return True

        return False

    def check_draw(self):
        return all([i.isbusy for i in self.fields])

    def __str__(self):
        result = ''
        for i in range(0, 9, 3):
            result += f'{self.fields[i].cell_id} {self.fields[i + 1].cell_id} {self.fields[i + 2].cell_id}' + '\t' + \
                      f'[{self.fields[i].value.rjust(1)}][{self.fields[i + 1].value.rjust(1)}]' \
                      f'[{self.fields[i + 2].value.rjust(1)}]\n'

        return result.strip('\n')


class Player:
    __slots__ = 'name', 'wins'

    def __init__(self, name: str, wins: int = 0):
        self.name = name
        self.wins = wins

    def move(self) -> str:
        return input('Введите номер клетки >>> ')


class Game:
    def __init__(self, players: tuple[Player, Player], board: Board = Board(), state: bool = True):
        self.players = players
        self.board = board
        self.state = state

    def __is_valid_move(self, cell_id: str) -> bool:
        return cell_id.isdigit() and \
            int(cell_id) in range(len(self.board.fields)) and \
            not self.board.fields[int(cell_id)].isbusy

    def __start_move(self, player: Player) -> bool:
        cell_id = player.move()
        if self.__is_valid_move(cell_id):
            cell_id = int(cell_id)
            value = f'{Fore.BLUE}0{Fore.RESET}' if self.players.index(player) else f'{Fore.RED}X{Fore.RESET}'
        else:
            print(f'{Fore.RED}Клетка занята или не существует! Повторите попытку.{Fore.RESET}')
            return self.__start_move(player)

        self.board.change_cell_state(cell_id, value)
        print(self.board)
        return self.board.check_win()

    def __add_win(self, player: Player):
        player.wins += 1

    def __start_game(self) -> bool | None:
        self.board = Board()
        print(f'{Fore.GREEN}Игра началась!{Fore.RESET}')
        print(self.board)

        return self.__game()

    def __game(self) -> bool | None:
        while not self.board.check_win():
            for player in self.players:
                if self.__start_move(player):
                    self.__add_win(player)
                    return bool(self.players.index(player))

                if self.board.check_draw():
                    return None

    def __get_score(self) -> str:
        return f'{self.players[0].wins}:{self.players[1].wins}'

    def start_games(self):
        while self.state:
            print('_' * 30)
            result = self.__start_game()
            if result is None:
                print(f'Ничья! Счёт {self.__get_score()}')
            else:
                print(f'Игра завершена! Победил игрок {self.players[result].name}')
                print(f'Счёт {self.__get_score()}')

            self.state = True if input('Хотите сыграть ещё раз (Y/N) >>> ').upper() in ('Y', 'YES') else False


if __name__ == "__main__":
    game = Game((Player('Саша'), Player('Паша')))
    game.start_games()
