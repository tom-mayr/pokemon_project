# Project Description

This project intends to model a simplified Pokémon battle and train a reinforcement learning algorithm on it. The Pokémon battle model is based on the 1. generation of Pokémon games first published in 1996. The goal is to model the battle situation in varying degrees of complexity and observe the resulting performance of reinforcement algorithms. 

A pokemon battle in its simplest form has the follwing properties:

* **Turn-based:** Each turn the player and the opponent choose their actions. These actions will result in new states.
* **Actions:** The defining actions of a battle are the moves / attacks that the players choose. Each Pokémon has up to four available moves.
* **States:** A state is mainly given by the amount of health points that the Pokémon have left. Most moves deduct health points directly.
* **Attributes:** Each Pokémon has certain attributes that modify the behaviour of their moves or have an effect on their or the opponent's next state. For example, a move of type 'Fire' used on a 'Grass' Pokémon will be very effective and deduct more health points than if it were used on a 'Water' Pokémon. Other moves might lower the chances of success of the enemy's move or increase their own health points.

## Essential goals:

* Model a Pokémon battle as a MDP.
* Train reinforcement learning algorithms on this MDP and observe performance and experiment with the parameters of the algorithms and the way the game is modeled.
* Introduce added layers of complexity by transforming the MDP from a deterministic to a stochastic environment and increasing the amount of actions available and states achievable.

## Ultimate goal:

The ultimate goal of this project is to mimic the final battle against the player's rival in the 1. generation of Pokémon. In the games this battle represents the ultimate test of the player's skills learned over the course of playing. The challenge consists of approximating the complexity of this battle and experimenting with different algorithms and model setups to find out if a reinforcement learning algorithm can consistently win this battle. The defining features of the battle should be that each player has multiple Pokémon available, the algorithm has the option to switch out their Pokémon and the opponent behaves not completely randomly, e.g. the oppponent uses pre-defined heuristics to choose favorable moves to make it more challenging for the algorithm.
