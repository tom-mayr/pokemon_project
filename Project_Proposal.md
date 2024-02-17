# Lab of Reinforcement Learning

## Project Proposal: Pokémon Battle

This project intends to model a simplified Pokémon battle and train a reinforcement learning algorithm on it. The Pokémon battle model is based on the 1. generation of Pokémon games first published in 1996. The goal is to model the battle situation in varying degrees of complexity and observe the resulting performance of reinforcement algorithms.

A Pokémon battle is a turn-based game. Each turn the player and the opponent choose an action. The actions essentially modify the state of the game. 

- The player and the opponent can have up to 6 Pokémon each in their team. There is always only 1 Pokémon participating in the battle. Available actions depend on the current Pokémon.
- Each Pokémon has a certain number of health points. If these drop below 0, the Pokémon can no longer participate in the battle and the next Pokémon gets sent out.
- If all the Pokémon of either the player or the opponent are defeated, the game is over.
- Each individual Pokémon has up to 4 moves. The most important kind of moves are attack moves. These moves lower the health points of the opposing Pokémon. Other moves might be status moves, e.g. a Pokémon can paralyze the opposing Pokémon, lowering the chances of their moves successfully hitting the opponent. To not make the game overly complicated, moves will me mostly of the attack kind.
- Each Pokémon and each attack has a type, e.g. a Pokémon like Pikachu is of type 'Electric' and an attack like 'Flame Thrower' is of type 'Fire'. The type of the opposing Pokémon determines the effectiveness of the other Pokémon's attack move. For example, moves of the 'Fire' type will be very effective and deal more damage against a 'Grass' type than to a 'Water' type Pokémon.
- The player has the option of switching their current Pokémon instead of attacking. This gives the player / the algorithm the opportunity to exploit type strengths and weaknesses by sending out a favorable Pokémon. As in the original games, the opponent does not have this option.
- Depending on the chosen setup, the opponent chooses their moves either randomly or using heuristics, e.g. using only moves that are effective against the player Pokémon.

### Goals

- Model a Pokémon Battle as an MDP and implement the game.
- Use one or more of the reinforcement learning algorithms in class and train the model against an opponent.
- Vary hyperparameters of the algorithm and experiment with the structure of the MDP (i.e. moves available, how a state is defined and the reward system) and observe and compare the performance of the algorithm.