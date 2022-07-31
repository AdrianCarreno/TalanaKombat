import re

import pytest

from .context import talanakombat as tk


class TestBaseCharacter:
    def test_base_character_init(self):
        special_attacks = {
            'P': {'name': 'Punch', 'damage': 1},
            'K': {'name': 'Kick', 'damage': 1},
        }
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks=special_attacks)
        assert character.name == 'Test'
        assert character.health == 100
        assert character.special_attacks == special_attacks

    def test_base_character_init_no_args(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter()
            assert e.value == "__init__() missing 3 required positional arguments: 'name', 'health', and 'special_attacks'"

    def test_base_character_init_name_not_string(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(name=1, health=1, special_attacks={
                             'P': {'name': 'Punch', 'damage': 1}})
            assert e.value == 'Name must be a string'

    def test_base_character_init_name_empty_string(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(name='', health=1, special_attacks={
                             'P': {'name': 'Punch', 'damage': 1}})
            assert e.value == 'Name must be a non empty string'

    def test_base_character_init_health_not_integer(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(
                name='Test', health='1', special_attacks={'P': {'name': 'Punch', 'damage': 1}})
            assert e.value == 'Health must be an integer greater than 0'

    def test_base_character_init_health_zero(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(name='Test', health=0, special_attacks={
                             'P': {'name': 'Punch', 'damage': 1}})
            assert e.value == 'Health must be an integer greater than 0'

    def test_base_character_init_special_attacks_not_dict(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(
                name='Test', health=1, special_attacks='P')
            assert e.value == 'Special attacks must be a dictionary'

    def test_base_character_init_special_attacks_empty_dict(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(
                name='Test', health=1, special_attacks={})
            assert e.value == 'Special attacks must be a non empty dictionary'

    def test_base_character_init_special_attacks_not_dict_of_dicts(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(name='Test', health=1, special_attacks={'P': 1})
            assert e.value == 'Special attacks elements must be a dictionary'

    def test_base_character_init_special_attacks_no_name(self):
        with pytest.raises(KeyError) as e:
            tk.BaseCharacter(
                name='Test', health=1, special_attacks={'P': {'not_name': 'Punch', 'damage': 1}})
            assert e.value == 'Special attacks must have a name'

    def test_base_character_init_special_attacks_name_not_string(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(name='Test', health=1, special_attacks={
                             'P': {'name': 1, 'damage': 1}})
            assert e.value == 'Special attacks names must be a string'

    def test_base_character_init_special_attacks_name_empty_string(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(name='Test', health=1, special_attacks={
                             'P': {'name': '', 'damage': 1}})
            assert e.value == 'Special attacks must have a name'

    def test_base_character_init_special_attacks_no_damage(self):
        with pytest.raises(KeyError) as e:
            tk.BaseCharacter(
                name='Test', health=1, special_attacks={'P': {'name': 'Punch', 'not_damage': 1}})
            assert e.value == 'Special attacks must have a damage'

    def test_base_character_init_special_attacks_damage_not_integer(self):
        with pytest.raises(TypeError) as e:
            tk.BaseCharacter(
                name='Test', health=1, special_attacks={'P': {'name': 'Punch', 'damage': '1'}})
            assert e.value == 'Special attacks damage must be an integer'

    def test_base_character_init_special_attacks_damage_zero_value(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(name='Test', health=1, special_attacks={
                             'P': {'name': 'Punch', 'damage': 0}})
            assert e.value == 'Special attacks damage must be an integer greater than 0'

    def test_base_character_init_special_attacks_damage_negative_value(self):
        with pytest.raises(ValueError) as e:
            tk.BaseCharacter(name='Test', health=1, special_attacks={
                             'P': {'name': 'Punch', 'damage': -1}})
            assert e.value == 'Special attacks damage must be an integer greater than 0'

    def test_base_character_is_alive(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'P': {'name': 'Punch', 'damage': 1}})
        assert character.is_alive() == True

    def test_base_character_receives_damage(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'P': {'name': 'Punch', 'damage': 1}})
        character.receive_damage(10)
        assert character.health == 90

    def test_base_character_death_raises_exception(self):
        character = tk.BaseCharacter(
            name='Test', health=1, special_attacks={'P': {'name': 'Punch', 'damage': 1}})
        with pytest.raises(tk.DeadPlayerException) as e:
            character.receive_damage(10)
            assert e.value == 'Test is dead'

    def test_base_character_move_is_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.is_special_attack(
            'DDSD+P') == ('D', {'name': 'Taladoken', 'damage': 3})

    def test_base_character_move_is_not_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.is_special_attack(
            'DDS') == ('DDS', None)

    def test_base_character_describes_movement_non_string(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        with pytest.raises(TypeError) as e:
            character.describe_movement(1)
            assert e.value == 'Movements must be a string'

    def test_base_character_describes_movement_string_too_long(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        with pytest.raises(ValueError) as e:
            character.describe_movement('DDSDASDAWS')
            assert e.value == 'Movements must be only W, A, S or D characters'

    def test_base_character_describes_movement_string_bad_characters(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        with pytest.raises(ValueError) as e:
            character.describe_movement('AADP')
            assert e.value == 'Movements must be 5 or less characters'

    def test_base_character_describes_single_movement(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.describe_movement('D') == ' moved right'

    def test_base_character_describes_double_movements(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.describe_movement(
            'DS') == ' moved right and down'

    def test_base_character_describes_multiple_movements(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.describe_movement(
            'DSD') == ' moved right, down and right'

    def test_base_character_describes_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert re.search(' ([a-z]+) a Taladoken attack',
                         character.describe_special_attack({'name': 'Taladoken'}))

    def test_base_character_makes_move_did_nothing(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.make_move('') == ('Test did nothing', 0)

    def test_base_character_makes_move_single_movement(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.make_move('D') == ('Test moved right', 0)

    def test_base_character_makes_move_double_movements(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.make_move('DS') == ('Test moved right and down', 0)

    def test_base_character_makes_move_multiple_movements(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        assert character.make_move('DSD') == (
            'Test moved right, down and right', 0)

    def test_base_character_makes_move_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        description, damage = character.make_move('DSD+P')
        assert re.search(
            'Test did not move, and ([a-z]+) a Taladoken attack', description)
        assert damage == 3

    def test_base_character_makes_move_single_movement_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        description, damage = character.make_move('DDSD+P')
        assert re.search(
            'Test moved right, and ([a-z]+) a Taladoken attack', description)
        assert damage == 3

    def test_base_character_makes_move_double_movements_special_attack(self):
        character = tk.BaseCharacter(
            name='Test', health=100, special_attacks={'DSD+P': {'name': 'Taladoken', 'damage': 3}})
        description, damage = character.make_move('DSDSD+P')
        assert re.search(
            'Test moved right and down, and ([a-z]+) a Taladoken attack', description)
        assert damage == 3


class TestTonynStallone:
    def test_name_is_tonyn_stallone(self):
        character = tk.TonynStallone()
        assert character.name == 'Tonyn Stallone'

    def test_health_is_6(self):
        character = tk.TonynStallone()
        assert character.health == 6

    def test_special_attacks_has_the_correct_number_of_attacks(self):
        character = tk.TonynStallone()
        assert len(character.special_attacks) == 4

    def test_taladoken_is_correct(self):
        character = tk.TonynStallone()
        assert character.special_attacks['DSD+P']['name'] == 'Taladoken'
        assert character.special_attacks['DSD+P']['damage'] == 3

    def test_remuyuken_is_correct(self):
        character = tk.TonynStallone()
        assert character.special_attacks['SD+K']['name'] == 'Remuyuken'
        assert character.special_attacks['SD+K']['damage'] == 2

    def test_punch_is_correct(self):
        character = tk.TonynStallone()
        assert character.special_attacks['P']['name'] == 'Punch'
        assert character.special_attacks['P']['damage'] == 1

    def test_kick_is_correct(self):
        character = tk.TonynStallone()
        assert character.special_attacks['K']['name'] == 'Kick'
        assert character.special_attacks['K']['damage'] == 1


class TestArnaldorShuatseneguer:
    def test_name_is_arnaldor_shuatseneguer(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.name == 'Arnaldor Shuatseneguer'

    def test_health_is_6(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.health == 6

    def test_special_attacks_has_the_correct_number_of_attacks(self):
        character = tk.ArnaldorShuatseneguer()
        assert len(character.special_attacks) == 4

    def test_taladoken_is_correct(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.special_attacks['ASA+P']['name'] == 'Taladoken'
        assert character.special_attacks['ASA+P']['damage'] == 2

    def test_remuyuken_is_correct(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.special_attacks['SA+K']['name'] == 'Remuyuken'
        assert character.special_attacks['SA+K']['damage'] == 3

    def test_punch_is_correct(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.special_attacks['P']['name'] == 'Punch'
        assert character.special_attacks['P']['damage'] == 1

    def test_kick_is_correct(self):
        character = tk.ArnaldorShuatseneguer()
        assert character.special_attacks['K']['name'] == 'Kick'
        assert character.special_attacks['K']['damage'] == 1
