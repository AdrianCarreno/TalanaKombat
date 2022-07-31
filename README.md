# Talana Kombat

This is a simple game that confronts 2 characters, _Tonyn Stallone_ and _Arnaldor Shuatseneguer_. It's part of a coding challenge for a job application in [Talana](https://web.talana.com/).

## Dependencies

This game has no dependencies. But if you want to run tests, you need to install the following dependencies:

-   pytest

Or alternatively, run the command:

```
pip install -r tests/requirements.txt
```

## The Game

The game is simple:

-   Each player starts with 6 health points.
-   Each player has 2 special attacks (dealing 2 and 3 points of damage each), and 2 basic attacks (dealing 1 point of damage each).
-   Each player submits their moves for the entire game as a `list` of `strings`.
-   The game is played in turns, and the order of turns is determined by the length of each player's move (shortest first). If the moves are the same length, player one goes first.
-   The first player to reach 0 health points loses. If there are no more moves left and both players have more than 0 health points, the match ends in a draw.
-   All the moves are case-insensitive, and can only be `W`, `A`, `S` or `D` for movement, and `P` or `K` for attacks.

## Usage

To play the game, you must create 2 players, and then add them to the combat. Then you must set the moves for each player, and then start the game.

```python
import talanakombat as tk

# Create combat instance
combat = tk.Combat()

# Create players and add them to the combat
player1 = tk.TonynStallone()
player2 = tk.ArnaldorShuatseneguer()
combat.set_players(player1, player2)

# Set moves for players and add them to the combat
player1moves = ['D+K', 'DSD+P', 'S', 'DSD+K', 'SD+P']
player2moves = ['SA+K', 'SA', 'SA+K', 'ASA+P', 'SA+P']
combat.set_moves(player1moves, player2moves)
```

You can also set the players and moves when creating the combat instance.

```python
import talanakombat as tk

player1 = tk.TonynStallone()
player2 = tk.ArnaldorShuatseneguer()
player1moves = ['D+K', 'DSD+P', 'S', 'DSD+K', 'SD+P']
player2moves = ['SA+K', 'SA', 'SA+K', 'ASA+P', 'SA+P']
combat = tk.Combat(player1, player2, player1moves, player2moves)
```

The `Combat.fight()` method returns a generator that yields the turns of the game. Each turn is a `string` with the player's name and the move they used.

```python
# Start the game
gen = combat.(fight)
for result in gen:
    print(result)
```

The output of the game would be something like this:

```
Tonyn Stallone moved right, and landed a Kick attack
Arnaldor Shuatseneguer did not move, and connected a Remuyuken attack
Arnaldor Shuatseneguer moved down and left
Tonyn Stallone did not move, and hit a Taladoken attack
Tonyn Stallone moved down
Arnaldor Shuatseneguer did not move, and imparted a Remuyuken attack
Tonyn Stallone is dead
Arnaldor Shuatseneguer is the winner and has 2 health
```

The attack verbs (landed, connected, hit, imparted) are random to make the narration more interesting.

## Testing

The package includes a testsuite, which attempts to try every scenario and verify that the game works as expected. The testsuite is run with the command:

```
pytest
```
