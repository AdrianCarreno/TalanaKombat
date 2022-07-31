from flask import Flask, request
import talanakombat as tk

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/combat', methods=['POST'])
def index():
    data = request.get_json()

    p1 = data['jugador1'] if 'jugador1' in data else data['player1']
    p2 = data['jugador2'] if 'jugador2' in data else data['player2']

    p1_m = p1['movimientos'] if 'movimientos' in p1 else p1['movements']
    p2_m = p2['movimientos'] if 'movimientos' in p2 else p2['movements']

    p1_a = p1['golpes'] if 'golpes' in p1 else p1['attacks']
    p2_a = p2['golpes'] if 'golpes' in p2 else p2['attacks']

    player1moves = [f"{m}+{a}" if m != '' and a !=
                    '' else m or a for m, a in zip(p1_m, p1_a)]
    player2moves = [f"{m}+{a}" if m != '' and a !=
                    '' else m or a for m, a in zip(p2_m, p2_a)]

    player1 = tk.TonynStallone()
    player2 = tk.ArnaldorShuatseneguer()

    combat = tk.Combat(
        player1=player1,
        player2=player2,
        player1moves=player1moves,
        player2moves=player2moves
    )

    gen = combat.fight()

    narration = [move for move in gen]

    return {
        'winner': player1.name if player1.is_alive() else player2.name,
        'narration': narration,
        'player1': {
            'name': player1.name,
            'health': player1.health,
            'moves': player1moves,
        },
        'player2': {
            'name': player2.name,
            'health': player2.health,
            'moves': player2moves,
        }
    }
