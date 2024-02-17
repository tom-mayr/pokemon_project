import numpy as np
import random
from typing import List
from pokemon_class import Pokemon
from attack_effect import attack_effect

class PokemonBattleMDP:
    def __init__(self, ai_pokemon_names: List[str], opponent_pokemon_names: List[str], intermediate_rewards = True):
        self.discount_factor = 0.9  # Discount factor for future rewards
        self.episode_history = [] # Records history of all episodes played for this instance
        self.episode = [] # Records one episode (gets reset)
        self.intermediate_rewards = intermediate_rewards # Intermediate rewards or only final

        self.ai_team = [Pokemon(name) for name in ai_pokemon_names]
        self.opponent_team = [Pokemon(name) for name in opponent_pokemon_names]

        # For new states: shows how many pokemon are defeated
        self.ai_team_defeated = [False for i in range(len(self.ai_team))]
        self.opponent_team_defeated = [False for i in range(len(self.opponent_team))]

        self.current_ai_pokemon = 0
        self.current_opponent_pokemon = 0

        # Dictionary of all possible moves indexed
        all_movesets = [pokemon.moveset for pokemon in self.ai_team]
        self.all_moves = [move for moveset in all_movesets for move in moveset]
        self.all_unique_moves = list(set(self.all_moves)) 
        self.switch_actions = list(range(len(self.ai_team))) # first action indeces are reserved for switch actions
        self.dict_all_unique_moves = {index + len(self.switch_actions): move for index, move in enumerate(self.all_unique_moves)}
        self.all_actions = list(range(len(self.ai_team))) + list(range(len(self.ai_team), len(self.ai_team) + len(self.all_unique_moves)))

        # all_movesets = [pokemon.moveset for pokemon in self.opponent_team]
        # all_moves = [element for sublist in all_movesets for element in sublist]
        # self.opponent_all_moves = {index: move for index, move in enumerate(all_moves)}

    def reset(self):
        for pokemon in self.ai_team:
            pokemon.reset()
        for pokemon in self.opponent_team:
            pokemon.reset()

        self.ai_team_defeated = [False for i in range(len(self.ai_team))]
        self.opponent_team_defeated = [False for i in range(len(self.opponent_team))]

        self.current_ai_pokemon = 0
        self.current_opponent_pokemon = 0

        if self.episode != []:
            self.episode_history.append(self.episode)
        self.episode = []

        return self.get_state()


    def get_state(self):
        #state_ai_team = [pokemon.current_hp for pokemon in self.ai_team]
        #state_opponent_team = [pokemon.current_hp for pokemon in self.opponent_team]

        ai_team_defeated = sum(self.ai_team_defeated)
        opponent_team_defeated = sum(self.opponent_team_defeated)
        
        current_ai_pokemon = self.current_ai_pokemon
        current_opponent_pokemon = self.current_opponent_pokemon

        return (ai_team_defeated, opponent_team_defeated, current_ai_pokemon, current_opponent_pokemon)
    

    def switch_pokemon(self, new_pokemon: int):
        self.current_ai_pokemon = new_pokemon


    def get_actions(self) -> list:
        return self.ai_team[self.current_ai_pokemon].moveset
    

    def get_actions_indexes(self) -> list:
        '''Get indexes of available moves'''
        available_moves = [i for i, x in self.dict_all_unique_moves.items() if x in self.ai_team[self.current_ai_pokemon].moveset]
        available_switches = [index for index, defeated in enumerate(self.ai_team_defeated) if not defeated]
        available_switches.remove(self.current_ai_pokemon) # Don't switch to current Pokemon
        available_actions = available_switches + available_moves
        return available_actions


    def choose_ai_action(self, action: int) -> str:
        if action in self.dict_all_unique_moves:
            ai_action_name = self.dict_all_unique_moves[action]
        else:
            new_pokemon_name = self.ai_team[action].name
            ai_action_name = f'switch to {new_pokemon_name}'
        #ai_action_name = self.ai_team[self.current_ai_pokemon].moveset[action]


        return ai_action_name


    def choose_opponent_action(self) -> str:
        action = np.random.choice(len(self.opponent_team[self.current_opponent_pokemon].moveset))
        opponent_action = self.opponent_team[self.current_opponent_pokemon].moveset[action]
        return opponent_action
    
    
    def next_pokemon(self):
        '''get next opponent pokemon if current one is defeated'''
        if self.opponent_team[self.current_opponent_pokemon].current_hp <= 0 and self.current_opponent_pokemon < (len(self.opponent_team) + 1):
            self.current_opponent_pokemon += 1


    def next_ai_pokemon(self):
        '''get next ai pokemon if current one is defeated'''
        # if self.ai_team[self.current_ai_pokemon].current_hp <= 0 and sum(self.ai_team_defeated) < len(self.ai_team_defeated):
        #     self.current_ai_pokemon += 1
        if self.ai_team[self.current_ai_pokemon].current_hp <= 0 and sum(self.ai_team_defeated) < len(self.ai_team_defeated):
            available_pokemon = [index for index, defeated in enumerate(self.ai_team_defeated) if not defeated]
            random_new_pokemon = random.choice(available_pokemon)
            self.current_ai_pokemon = random_new_pokemon


    def is_terminal(self) -> bool:
        terminal = all([pokemon.current_hp <= 0 for pokemon in self.ai_team]) or all([pokemon.current_hp <= 0 for pokemon in self.opponent_team])
        return terminal


    def get_reward(self, ai_pokemon_defeated = False, opponent_pokemon_defeated = False) -> int:
        reward = 0
        if self.intermediate_rewards:
            if self.opponent_team[self.current_opponent_pokemon].current_hp <= 0:
                reward += 1
            if self.ai_team[self.current_ai_pokemon].current_hp <= 0:
                reward -= 1

        if  all([pokemon.current_hp <= 0 for pokemon in self.opponent_team]):  # ai wins
            reward += 10
        elif all([pokemon.current_hp <= 0 for pokemon in self.ai_team]):  # ai loses
            reward -=10
        return(reward)


    def step(self, ai_action):
        # Iniate history for this step
        step_history = {}
        step_history['ai_team'] = {}
        step_history['opponent_team'] = {}
        step_history['ai_team']['current_pokemon'] = self.current_ai_pokemon
        step_history['opponent_team']['current_pokemon'] = self.current_opponent_pokemon

        # Choose AI and opponent action and record in history
        ai_action_name = self.choose_ai_action(ai_action)
        opponent_action = self.choose_opponent_action()
        step_history['ai_team']['action'] = ai_action_name
        step_history['opponent_team']['action'] = opponent_action

        # Get states and attributes before attacks
        step_history['ai_team']['full_state'] = {}
        for pokemon in self.ai_team:
            name = pokemon.name
            step_history['ai_team']['full_state'][name] = {}
            step_history['ai_team']['full_state'][name]['max_hp'] = pokemon.max_hp
            step_history['ai_team']['full_state'][name]['current_hp'] = pokemon.current_hp
            step_history['ai_team']['full_state'][name]['status'] = pokemon.status
            step_history['ai_team']['full_state'][name]['accuracy'] = pokemon.accuracy

        step_history['opponent_team']['full_state'] = {}
        for pokemon in self.opponent_team:
            name = pokemon.name
            step_history['opponent_team']['full_state'][name] = {}
            step_history['opponent_team']['full_state'][name]['max_hp'] = pokemon.max_hp
            step_history['opponent_team']['full_state'][name]['current_hp'] = pokemon.current_hp
            step_history['opponent_team']['full_state'][name]['status'] = pokemon.status
            step_history['opponent_team']['full_state'][name]['accuracy'] = pokemon.accuracy

        # Check if switch pokemon otherwise:
        # Calcualate attack effects, update states and attributes accordingly and return if move hit or not and how effective
        if ai_action in self.switch_actions:
            self.switch_pokemon(new_pokemon=ai_action)
            power, hit, effectiveness = None, None, None
        else:
            power, hit, effectiveness = attack_effect(ai_action_name, self.ai_team[self.current_ai_pokemon], self.opponent_team[self.current_opponent_pokemon])

        step_history['ai_team']['power'] = power
        step_history['ai_team']['hit'] = hit
        step_history['ai_team']['effectiveness'] = effectiveness

        power, hit, effectiveness = attack_effect(opponent_action, self.opponent_team[self.current_opponent_pokemon], self.ai_team[self.current_ai_pokemon])
        step_history['opponent_team']['power'] = power
        step_history['opponent_team']['hit'] = hit
        step_history['opponent_team']['effectiveness'] = effectiveness

        # Update defeated Pokemon lists
        self.ai_team_defeated = [pokemon.current_hp <= 0 for pokemon in self.ai_team]
        self.opponent_team_defeated = [pokemon.current_hp <= 0 for pokemon in self.opponent_team]

        # Add if terminal to history
        step_history['is_terminal'] = self.is_terminal()

        # Get reward and record reward and if terminal (same information in this configuration)
        reward = self.get_reward()
        step_history['is_terminal'] = self.is_terminal()
        step_history['reward'] = reward

        # Add step_history to episode_history
        self.episode.append(step_history)

        # get next pokemon
        if self.is_terminal() is False:
            self.next_ai_pokemon()
            self.next_pokemon()

        return self.get_state(), reward, self.is_terminal()