# Get some battle data from history of a battle

def get_move_counts(battle_data: dict):
    # get data for ai (or agent) pokemon and opponent pokemon
    # These are instances of the Pokemon class
    ai_pokemon = battle_data['ai_pokemon']
    opponent_pokemon = battle_data['opponent_pokemon']

    # get moveset data and iniate dictionary with move names and 0 counts
    ai_move_count_dict = {move: 0 for move in ai_pokemon.moveset}
    opponent_move_count_dict = {move: 0 for move in opponent_pokemon.moveset}

    # count ai and opponent moves for every turn in the battle
    for turn in battle_data['turns']:
        ai_move = turn['ai_move']
        ai_move_count_dict[ai_move] += 1
        opponent_move = turn['opponent_move']
        opponent_move_count_dict[opponent_move] += 1

    move_counts = {'ai_move_counts': ai_move_count_dict, 'opponent_move_counts': opponent_move_count_dict}

    return move_counts

# Test
# from pokemon_class import Pokemon

# test_battle = {'ai_pokemon': Pokemon('Venusaur'), 'opponent_pokemon': Pokemon('Charizard'),
#                'turns': [{'ai_move': 'Vine Whip', 'opponent_move': 'Flame Thrower'},
#                          {'ai_move': 'Synthesis', 'opponent_move': 'Flame Thrower'}]}

# get_move_counts(test_battle)