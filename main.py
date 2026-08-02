from agents.random_agent import RandomAgent
from Game.logic.game_loop import play_game
import random

if __name__ == '__main__':
    rng = random.Random()
    num_players = 5
    agents = [RandomAgent() for _ in range(num_players)]
    play_game(agents, rng)
