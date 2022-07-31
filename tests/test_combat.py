import pytest
import re

from .context import talanakombat as tk


class TestCombat:
    def test_init_no_args(self):
        combat = tk.Combat()
        assert combat.player1 is None
        assert combat.player2 is None
        assert combat.player1moves is None
        assert combat.player2moves is None

    def test_init_with_args(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer())
        assert combat.player1 is not None
        assert combat.player2 is not None
        assert combat.player1moves is None
        assert combat.player2moves is None

    def test_combat_set_players(self):
        combat = tk.Combat()
        combat.set_players(tk.TonynStallone(), tk.ArnaldorShuatseneguer())
        assert combat.player1 is not None
        assert combat.player2 is not None

    def test_combat_set_players_wrong_type(self):
        combat = tk.Combat()
        with pytest.raises(TypeError) as e:
            combat.set_players(tk.TonynStallone(), 'ArnaldorShuatseneguer')
            assert e.message == 'Player 2 must be a characters.BaseCharacter'

    def test_combat_set_moves(self):
        combat = tk.Combat()
        combat.set_moves(['D+K', 'DSD+P', 'S', 'DSD+K', 'SD+P'],
                         ['SA+K', 'SA', 'SA+K', 'ASA+P', 'SA+P'])
        assert combat.player1moves == ['D+K', 'DSD+P', 'S', 'DSD+K', 'SD+P']
        assert combat.player2moves == ['SA+K', 'SA', 'SA+K', 'ASA+P', 'SA+P']

    def test_combat_set_moves_wrong_type(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer())
        with pytest.raises(TypeError) as e:
            combat.set_moves(['D+K', 'DSD+P', 'S', 'DSD+K',
                             'SD+P'], 'ArnaldorShuatseneguer')
            assert e.message == 'Player 2 moves must be a list of strings'

    def test_combat_cant_start_without_players(self):
        combat = tk.Combat()
        with pytest.raises(AttributeError) as e:
            combat.fight()
            assert e.message == 'Combat must have two players'

    def test_combat_cant_start_without_moves(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer())
        with pytest.raises(AttributeError) as e:
            combat.fight()
            assert e.message == 'Combat must have two sets of moves'

    def test_combat_fight_arnaldor_wins1(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer(),
                           player1moves=['D+K', 'DSD+P', 'S', 'DSD+K', 'SD+P'],
                           player2moves=['SA+K', 'SA', 'SA+K', 'ASA+P', 'SA+P'])
        gen = combat.fight()
        sentences = [
            'Tonyn Stallone moved right, and ([a-z]+) a Kick attack',
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Remuyuken attack',
            'Arnaldor Shuatseneguer moved down and left',
            'Tonyn Stallone did not move, and ([a-z]+) a Taladoken attack',
            'Tonyn Stallone moved down',
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Remuyuken attack',
            'Tonyn Stallone is dead',
            'Arnaldor Shuatseneguer is the winner and has 2 health',
        ]

        for description, sentence in zip(gen, sentences):
            assert re.search(sentence, description)

        assert combat.player1.health == 0
        assert combat.player2.health == 2

    def test_combat_fight_arnarldor_wins2(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer(),
                           player1moves=['DAD+P', 'S'],
                           player2moves=['P', 'ASA', 'DA+P', 'AAA+K', 'K', 'SA+K'])
        gen = combat.fight()
        sentences = [
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Punch attack',
            'Tonyn Stallone moved right, left and right, and ([a-z]+) a Punch attack',
            'Tonyn Stallone moved down',
            'Arnaldor Shuatseneguer moved left, down and left',
            'Tonyn Stallone did nothing',
            'Arnaldor Shuatseneguer moved right and left, and ([a-z]+) a Punch attack',
            'Tonyn Stallone did nothing',
            'Arnaldor Shuatseneguer moved left, left and left, and ([a-z]+) a Kick attack',
            'Tonyn Stallone did nothing',
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Kick attack',
            'Tonyn Stallone did nothing',
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Remuyuken attack',
            'Tonyn Stallone is dead',
            'Arnaldor Shuatseneguer is the winner and has 5 health',
        ]

        for description, sentence in zip(gen, sentences):
            assert re.search(sentence, description)

        assert combat.player1.health == 0
        assert combat.player2.health == 5

    def test_combat_fight_tonyn_wins(self):
        combat = tk.Combat(player1=tk.TonynStallone(),
                           player2=tk.ArnaldorShuatseneguer(),
                           player1moves=['SDD+K', 'DSD+P', 'SA+K', 'DSD+P'],
                           player2moves=['DSD+P', 'WSAW+K', 'AS+K', 'K', 'ASA+P', 'SA+K'])
        gen = combat.fight()
        sentences = [
            'Tonyn Stallone moved down, right and right, and ([a-z]+) a Kick attack',
            'Arnaldor Shuatseneguer moved right, down and right, and ([a-z]+) a Punch attack',
            'Tonyn Stallone did not move, and ([a-z]+) a Taladoken attack',
            'Arnaldor Shuatseneguer moved up, down, left and up, and ([a-z]+) a Kick attack',
            'Tonyn Stallone moved down and left, and ([a-z]+) a Kick attack',
            'Arnaldor Shuatseneguer moved left and down, and ([a-z]+) a Kick attack',
            'Arnaldor Shuatseneguer did not move, and ([a-z]+) a Kick attack',
            'Tonyn Stallone did not move, and ([a-z]+) a Taladoken attack',
            'Arnaldor Shuatseneguer is dead',
            'Tonyn Stallone is the winner and has 2 health',
        ]

        for description, sentence in zip(gen, sentences):
            assert re.search(sentence, description)

        assert combat.player1.health == 2
        assert combat.player2.health == 0
