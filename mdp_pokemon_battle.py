import numpy as np
from pokemon_class import Pokemon
from attack_effect import attack_effect

class PokemonBattleMDP:
    def __init__(self, ai_pokemon_name: str, opponent_pokemon_name: str):
        self.discount_factor = 0.9  # Discount factor for future rewards
        self.episode_history = [] # Records history of all episodes played for this instance
        self.episode = [] # Records one episode (gets reset)
        self.ai_pokemon = Pokemon(ai_pokemon_name)
        self.opponent_pokemon = Pokemon(opponent_pokemon_name)

    def reset(self):
        self.ai_pokemon.current_hp = self.ai_pokemon.max_hp
        self.opponent_pokemon.current_hp = self.opponent_pokemon.max_hp
        self.ai_pokemon.status = None
        self.opponent_pokemon.status = None
        self.ai_pokemon.accuracy = 1
        if self.episode != []:
            self.episode_history.append(self.episode)
        self.episode = []
        return self.get_state()

    def get_state(self):
        return (self.ai_pokemon.current_hp, self.opponent_pokemon.current_hp)
    
    def get_actions(self):
        return (self.ai_pokemon.moveset)

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
        # Iniate history for this step
        step_history = {}
        step_history['ai_pokemon'] = {}
        step_history['opponent_pokemon'] = {} 

        # Choose AI and opponent action and record in history
        ai_action = self.choose_ai_action(ai_action)
        opponent_action = self.choose_opponent_action()
        step_history['ai_pokemon']['action'] = ai_action
        step_history['opponent_pokemon']['action'] = opponent_action

        # Get states and attributes before attacks
        step_history['ai_pokemon']['max_hp'] = self.ai_pokemon.max_hp
        step_history['ai_pokemon']['current_hp'] = self.ai_pokemon.current_hp
        step_history['ai_pokemon']['status'] = self.ai_pokemon.status
        step_history['ai_pokemon']['accuracy'] = self.ai_pokemon.accuracy

        step_history['opponent_pokemon']['max_hp'] = self.opponent_pokemon.max_hp
        step_history['opponent_pokemon']['current_hp'] = self.opponent_pokemon.current_hp
        step_history['opponent_pokemon']['status'] = self.opponent_pokemon.status
        step_history['opponent_pokemon']['accuracy'] = self.opponent_pokemon.accuracy

        # Calcualate attack effects, update states and attributes accordingly and return if move hit or not and how effective
        power, hit, effectiveness = attack_effect(ai_action, self.ai_pokemon, self.opponent_pokemon)
        step_history['ai_pokemon']['power'] = power
        step_history['ai_pokemon']['hit'] = hit
        step_history['ai_pokemon']['effectiveness'] = effectiveness

        power, hit, effectiveness = attack_effect(opponent_action, self.opponent_pokemon, self.ai_pokemon)
        step_history['opponent_pokemon']['power'] = power
        step_history['opponent_pokemon']['hit'] = hit
        step_history['opponent_pokemon']['effectiveness'] = effectiveness

        # Add if terminal to history
        step_history['is_terminal'] = self.is_terminal()

        # Get reward and record reward and if terminal (same information in this configuration)
        reward = self.get_reward()
        step_history['is_terminal'] = self.is_terminal()
        step_history['reward'] = reward

        # Add step_history to episode_history
        self.episode.append(step_history)

        return self.get_state(), reward, self.is_terminal()