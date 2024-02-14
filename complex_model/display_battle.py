from attacks import attacks

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
        ai_name,
        ai_current_hp: int,
        ai_status: str,
        ai_max_hp: int = 100,
        ):

    print(f"{ai_name}:") # ai Pokemon name
    print(health_bar(ai_current_hp, ai_max_hp)) # ai Pokemon health bar
    print(f"{ai_current_hp} / {ai_max_hp}") # ai Pokemon HP
    if ai_status is not None:
        print(f"Status: {ai_status}")
    else:
        print('Status:')

def print_opponent_turn(
        opponent_name,
        opponent_current_hp: int,
        opponent_status: str,
        opponent_max_hp: int = 100,
        ):

    print(f"{opponent_name}:") # Opponent Pokemon name
    print(health_bar(opponent_current_hp, opponent_max_hp)) # Opponent Pokemon health bar
    print(f"{opponent_current_hp} / {opponent_max_hp}") # Opponent Pokemon HP
    if opponent_status is not None:
        print(f"Status: {opponent_status}")
    else:
        print('Status:')

def print_attack(pokemon_name, attack: str, hit: bool, effectiveness: float):

    name = pokemon_name
    attack_name = attack

    if attacks[attack]['power'] != 0:
        if hit:
            if effectiveness == 1:
                additional_text = ''
            elif effectiveness == 2 or effectiveness == 4:
                additional_text = 'It\'s super effective!'
            elif effectiveness == 0.5 or effectiveness == 0.25:
                additional_text = 'It\'s not very effective...'
            elif effectiveness == 0:
                additional_text = 'It has no effect.'
        else:
            additional_text = 'It misses!'
    else:
        additional_text = ''

    print(f"{name} uses {attack_name}! {additional_text}")