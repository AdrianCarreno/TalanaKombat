import random
import re
import typing

from talanakombat import exceptions


class BaseCharacter:
    def __init__(self, name: str, health: int, special_attacks: dict) -> None:
        if type(name) is not str:
            raise TypeError('Name must be a string')
        if len(name) <= 0:
            raise ValueError('Name must be a non empty string')
        if type(health) is not int:
            raise TypeError('Health must be an integer greater than 0')
        if health <= 0:
            raise ValueError('Health must be an integer greater than 0')
        if type(special_attacks) is not dict:
            raise TypeError('Special attacks must be a dictionary')
        if len(special_attacks) <= 0:
            raise ValueError('Special attacks must be a non empty dictionary')

        for attack in special_attacks.values():
            if type(attack) is not dict:
                raise TypeError(
                    'Special attacks elements must be a dictionary')
            if 'name' not in attack:
                raise KeyError('Special attacks must have a name')
            if type(attack['name']) is not str:
                raise TypeError('Special attacks names must be a string')
            if len(attack['name']) == 0:
                raise ValueError('Special attacks names cannot be empty')
            if 'damage' not in attack:
                raise KeyError('Special attacks must have a damage')
            if type(attack['damage']) is not int:
                raise TypeError('Special attacks damage must be an integer')
            if attack['damage'] <= 0:
                raise ValueError(
                    'Special attacks must have a damage greater than 0')

        self.__name = name
        self.__health = health
        self.__special_attacks = special_attacks

    def __str__(self) -> str:
        return f"{self.name} has {self.health} health"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def health(self) -> int:
        return self.__health

    @property
    def special_attacks(self) -> dict:
        try:
            return self.__special_attacks
        except AttributeError:
            return {}

    def is_alive(self) -> bool:
        return self.health > 0

    def receive_damage(self, amount_of_damage: int) -> None:
        self.__health = max(self.health - amount_of_damage, 0)
        if self.health == 0:
            raise exceptions.DeadPlayerException(f"{self.name} is dead")

    def is_special_attack(self, play: str) -> tuple[str, typing.Union[dict, None]]:
        for attack in self.special_attacks:
            if attack in play:
                movement = play[:-len(attack)].replace('+', '')
                return movement, self.special_attacks[attack]
        return play.replace('+', ''), None

    @staticmethod
    def describe_movement(movement: str) -> str:
        assert type(movement) is str, 'Movements must be a string'
        assert len(movement) <= 5, 'Movements must be 5 or less characters'
        assert not re.match(
            '[^WASD]', movement, re.IGNORECASE), 'Movements must be only W, A, S or D characters'

        description = ''
        moves = {'W': 'up', 'A': 'left', 'S': 'down', 'D': 'right'}

        for i, move in enumerate(movement):
            if len(movement) > 1:
                if i == len(movement) - 1:
                    description += ' and'
                elif i != 0:
                    description += ','

            description += f" moved {moves[move]}"

        return description

    def describe_special_attack(self, attack: dict) -> str:
        verbs = ['landed a', 'connected a', 'hit a', 'imparted a']

        return f" {random.choice(verbs)} {attack['name']} attack"

    def make_move(self, move: str) -> tuple[str, int]:
        assert type(move) is str, 'Move must be a string'

        movement, special_attack = self.is_special_attack(move)

        description = self.name
        if not movement and not special_attack:
            return description + ' did nothing', 0

        description += BaseCharacter.describe_movement(movement)
        if movement and special_attack:
            description += ', and'
        if special_attack:
            description += self.describe_special_attack(special_attack)

        return description, (special_attack['damage'] if special_attack else 0)


class TonynStallone(BaseCharacter):
    def __init__(self, **kwargs) -> None:
        health = kwargs.get('health', 6)
        special_attacks = kwargs.get('special_attacks', {
            'DSD+P': {'name': 'Taladoken', 'damage': 3},
            'SD+K': {'name': 'Remuyuken', 'damage': 2},
            'P': {'name': 'Punch', 'damage': 1},
            'K': {'name': 'Kick', 'damage': 1},
        })
        super().__init__('Tonyn Stallone', health, special_attacks)

    def __repr__(self) -> str:
        return f"TalanaKombat.TonynStallone(health={self.health}, special_attacks={self.special_attacks})"


class ArnaldorShuatseneguer(BaseCharacter):
    def __init__(self, **kwargs) -> None:
        health = kwargs.get('health', 6)
        special_attacks = kwargs.get('special_attacks', {
            'ASA+P': {'name': 'Taladoken', 'damage': 2},
            'SA+K': {'name': 'Remuyuken', 'damage': 3},
            'P': {'name': 'Punch', 'damage': 1},
            'K': {'name': 'Kick', 'damage': 1},
        })
        super().__init__('Arnaldor Shuatseneguer', health, special_attacks)

    def __repr__(self) -> str:
        return f"TalanaKombat.ArnaldorShuatseneguer(health={self.health}, special_attacks={self.special_attacks})"
