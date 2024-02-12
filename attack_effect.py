from type_chart import type_chart
from pokemon_class import Pokemon
from attacks import attacks
import numpy as np

def attack_power(attack_name: str, 
                 attacking_pokemon: Pokemon, 
                 defending_pokemon: Pokemon) -> int:
    
    attack = attacks[attack_name]
    defending_type = defending_pokemon.type
    if len(defending_type) == 2:
        effectiveness_type1 = type_chart.loc[type_chart['Attacking'] == attack['type'], defending_type[0]].values[0]
        effectiveness_type2 = type_chart.loc[type_chart['Attacking'] == attack['type'], defending_type[1]].values[0]
        effectiveness = effectiveness_type1 * effectiveness_type2
    else:
        effectiveness = type_chart.loc[type_chart['Attacking'] == attack['type'], defending_type[0]].values[0]
    attack_power = attack['power'] * effectiveness
    hit = (np.random.random() < attack['accuracy']) * (np.random.random() < attacking_pokemon.accuracy)
    attack_power = attack_power * hit
    return int(attack_power)

def attack_effect(attack_name: str, 
                  attacking_pokemon: Pokemon, 
                  defending_pokemon: Pokemon):
    # get attack
    attack = attacks[attack_name]

    # get current state of pokemon
    attacking_pokemon_attr = attacking_pokemon.__dict__
    defending_pokemon_attr = defending_pokemon.__dict__

    # calculate attack_power
    power = attack_power(attack_name, attacking_pokemon, defending_pokemon)
    if 'fixed_power' in attack:
        power = attack['fixed_power']
    new_defending_current_hp = max(defending_pokemon.current_hp - power, 0)
    defending_pokemon_attr['current_hp'] = new_defending_current_hp
    
    # status move
    if 'status_move' in attack and attack['status_move'] == True:
        new_defending_status = attack['status'] if (np.random.random() < attack['status_affliction_probability']) else None
        if defending_pokemon_attr['status'] is None:
            defending_pokemon_attr['status'] = new_defending_status
        if defending_pokemon_attr['status'] == 'Paralysis':
            defending_pokemon_attr['accuracy'] = 0.75
    
    # heal move
    if 'heal_move' in attack and attack['heal_move'] == True:
        heal_amount = int(attacking_pokemon.max_hp * attack['heal_amount'])
        new_attacking_current_hp = min(attacking_pokemon.current_hp + heal_amount, attacking_pokemon.max_hp)
        attacking_pokemon_attr['current_hp'] = new_attacking_current_hp

    attacking_pokemon.__dict__.update(attacking_pokemon_attr)
    defending_pokemon.__dict__.update(defending_pokemon_attr)

    # return new
    return attacking_pokemon.__dict__, defending_pokemon.__dict__