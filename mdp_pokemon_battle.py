import numpy as np
from pokemon_class import Pokemon
from type_chart import type_chart
from attacks import attacks
from attack_effect import attack_effect

class PokemonBattleMDP:
    def __init__(self, ai_pokemon_name: str, opponent_pokemon_name: str):
        self.discount_factor = 0.9  # Discount factor for future rewards

        self.ai_pokemon = Pokemon(ai_pokemon_name)
        self.opponent_pokemon = Pokemon(opponent_pokemon_name)

    def reset(self):
        self.ai_pokemon.current_hp = self.ai_pokemon.max_hp
        self.opponent_pokemon.current_hp = self.opponent_pokemon.max_hp
        self.ai_pokemon.status = None
        self.opponent_pokemon.status = None
        self.ai_pokemon.accuracy = 1
        return self.get_state()

    def get_state(self):
        return (self.ai_pokemon.current_hp, self.opponent_pokemon.current_hp)
    
    def get_actions(self):
        return (self.ai_pokemon.moveset)
    
    def attack_power(self, attack_name, attacking_pokemon, defending_pokemon):
        attack = attacks[attack_name]
        defending_type = defending_pokemon.type
        effectiveness = type_chart.loc[type_chart['Attacking'] == attack['type'], defending_type].values[0]
        attack_power = attack['power'] * effectiveness
        hit = (np.random.random() < attack['accuracy'])
        attack_power = attack_power * hit
        return int(attack_power)

    def choose_ai_action(self, action):
        ai_action_name = self.ai_pokemon.moveset[action]
        return ai_action_name

    def choose_opponent_action(self):
        action = np.random.choice(len(self.opponent_pokemon.moveset))
        opponent_action = self.opponent_pokemon.moveset[action]
        return opponent_action

    def is_terminal(self):
        return self.ai_pokemon.current_hp <= 0 or self.opponent_pokemon.current_hp <= 0

    def get_reward(self):
        if self.opponent_pokemon.current_hp <= 0:  # ai wins
            return 1
        elif self.ai_pokemon.current_hp <= 0:  # ai loses
            return -1
        else:
            return 0

    def step(self, ai_action):
        ai_action = self.choose_ai_action(ai_action)
        opponent_action = self.choose_opponent_action()

        attack_effect(ai_action, self.ai_pokemon, self.opponent_pokemon)
        attack_effect(opponent_action, self.opponent_pokemon, self.ai_pokemon)

        reward = self.get_reward()
        return self.get_state(), reward, self.is_terminal()