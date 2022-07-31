import typing

from talanakombat import characters
from talanakombat import exceptions


class Combat:
    def __init__(self, **kwargs) -> None:
        player1 = kwargs.get('player1', None)
        player2 = kwargs.get('player2', None)
        if player1 and player2:
            self.set_players(player1, player2)
        player1moves = kwargs.get('player1moves', None)
        player2moves = kwargs.get('player2moves', None)
        if player1moves and player2moves:
            self.set_moves(player1moves, player2moves)

    @property
    def player1(self) -> characters.BaseCharacter:
        try:
            return self.__player1
        except AttributeError:
            return None

    @property
    def player2(self) -> characters.BaseCharacter:
        try:
            return self.__player2
        except AttributeError:
            return None

    @property
    def player1moves(self) -> typing.Union[str, None]:
        try:
            return self.__player1moves
        except AttributeError:
            return None

    @property
    def player2moves(self) -> typing.Union[str, None]:
        try:
            return self.__player2moves
        except AttributeError:
            return None

    def set_players(self, player1: characters.BaseCharacter, player2: characters.BaseCharacter) -> 'Combat':
        assert isinstance(
            player1, characters.BaseCharacter), 'Player 1 must be a characters.BaseCharacter'
        assert isinstance(
            player2, characters.BaseCharacter), 'Player 2 must be a characters.BaseCharacter'
        self.__player1 = player1
        self.__player2 = player2

        return self

    def set_moves(self, player1moves: list[str], player2moves: list[str]) -> 'Combat':
        assert type(
            player1moves) is list, 'Player 1 moves must be a list of strings'
        assert type(
            player2moves) is list, 'Player 2 moves must be a list of strings'

        self.__player1moves = player1moves
        self.__player2moves = player2moves
        diff = len(player1moves) - len(player2moves)
        if diff > 0:
            self.__player2moves += [''] * diff
        elif diff < 0:
            self.__player1moves += [''] * -diff

        return self

    def decide_order(self, player1move: str, player2move: str) -> tuple[characters.BaseCharacter, characters.BaseCharacter, str, str]:
        try:
            if len(player1move) < len(player2move):
                return self.player1, self.player2, player1move, player2move
            elif len(player1move) > len(player2move):
                return self.player2, self.player1, player2move, player1move
            elif len(player1move.split('+')[0]) < len(player2move.split('+')[0]):
                return self.player1, self.player2, player1move, player2move
            elif len(player1move.split('+')[0]) > len(player2move.split('+')[0]):
                return self.player2, self.player1, player2move, player1move
            elif len(player1move.split('+')[1]) < len(player2move.split('+')[1]):
                return self.player1, self.player2, player1move, player2move
            elif len(player1move.split('+')[1]) > len(player2move.split('+')[1]):
                return self.player2, self.player1, player2move, player1move
            else:
                return self.player1, self.player2, player1move, player2move
        except IndexError:
            return self.player1, self.player2, player1move, player2move

    def fight(self) -> None:
        assert self.player1, 'Player 1 must be set'
        assert self.player2, 'Player 2 must be set'
        assert self.player1moves, 'Player 1 moves must be set'
        assert self.player2moves, 'Player 2 moves must be set'

        for p1, p2 in zip(self.player1moves, self.player2moves):
            first, second, p1, p2 = self.decide_order(p1, p2)
            try:
                description, damage = first.make_move(p1)
                print(description)
                second.receive_damage(damage)
            except exceptions.DeadPlayerException:
                print(f"{second.name} is dead")
                break
            try:
                description, damage = second.make_move(p2)
                print(description)
                first.receive_damage(damage)
            except exceptions.DeadPlayerException:
                print(f"{first.name} is dead")
                break
        if self.player1.is_alive() and not self.player2.is_alive():
            print(
                f"{self.player1.name} is the winner and has {self.player1.health} health")
        elif self.player2.is_alive() and not self.player1.is_alive():
            print(
                f"{self.player2.name} is the winner and has {self.player2.health} health")
        else:
            print('Combat ended in a draw')
