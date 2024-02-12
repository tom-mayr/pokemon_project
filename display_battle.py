def health_bar(current_health, max_health, bar_length=50):
    """Draws a text-based health bar with colored health."""
    health_ratio = current_health / max_health
    num_bars = int(health_ratio * bar_length)
    health_bar = "[" + "#" * num_bars + "-" * (bar_length - num_bars) + "]"
    
    # Color the health bar based on health percentage
    if health_ratio > 0.5:
        colored_health_bar = "\033[92m" + health_bar + "\033[0m"  # Green
    elif health_ratio > 0.2:
        colored_health_bar = "\033[93m" + health_bar + "\033[0m"  # Yellow
    else:
        colored_health_bar = "\033[91m" + health_bar + "\033[0m"  # Red
    
    return colored_health_bar

# Example usage
# current_health = 20
# max_health = 100
# print(health_bar(current_health, max_health, bar_length=50))


def print_ai_turn(
        ai_pokemon,
        ai_name: str = 'Venusaur', 
        ai_current_hp: int = 60,
        ai_max_hp: int = 100,
        ):
    
    ai_name = ai_pokemon.name

    print(f"{ai_name}:") # ai Pokemon name
    print(health_bar(ai_current_hp, ai_max_hp)) # ai Pokemon health bar
    print(f"{ai_current_hp} / {ai_max_hp}") # ai Pokemon HP
    # if result == False:
    #     print()
    #     print(f"{ai_name} uses {ai_attack_name}!")

def print_opponent_turn(
        opponent_pokemon,
        opponent_name: str = 'Charizard',
        opponent_current_hp: int = 20,
        opponent_max_hp: int = 100,
        opponent_status: int = 0,
        ):
    
    opponent_name = opponent_pokemon.name

    print(f"{opponent_name}:") # Opponent Pokemon name
    print(health_bar(opponent_current_hp, opponent_max_hp)) # Opponent Pokemon health bar
    print(f"{opponent_current_hp} / {opponent_max_hp}") # Opponent Pokemon HP
    # if opponent_status == 1:
    #    print('Status: ' + "\033[93m" + 'Paralysed' + "\033[0m")
    # if result == False:
    #     print()
    #     print(f"{opponent_name} uses {opponent_attack}!")

def print_ai_attack(ai_pokemon, ai_attack: int):

    ai_name = ai_pokemon.name
    ai_attack_name = ai_pokemon.moveset[ai_attack]

    print(f"{ai_name} uses {ai_attack_name}!")

def print_opponent_attack(opponent_pokemon, opponent_attack: int = 0):
    
    opponent_name = opponent_pokemon.name
    opponent_attack_name = opponent_pokemon.moveset[opponent_attack]
    print(f"{opponent_name} uses {opponent_attack_name}!")