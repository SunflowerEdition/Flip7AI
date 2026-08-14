import random

import pygame

from agents.ev_agent import EVAgent
from agents.num_cards_agent import NumCardsAgent
from agents.num_points_agent import NumPointsAgent
from agents.player_agent import PlayerAgent
from agents.random_agent import RandomAgent
from game.logic.game_loop import play_game
from game.render.pygame_renderer import CardRenderer
from tournament import run_tournament

if __name__ == '__main__':
    run_tournament()
    '''pygame.init()

    num_players = 5
    window_size = CardRenderer.required_window_size(num_players, card_size=(72, 100), padding=8)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Flip 7")

    rng = random.Random()
    agents = [
        EVAgent("EV Agent"),
        NumCardsAgent(4, "4 Cards"),
        NumCardsAgent(5, "5 Cards"),
        NumPointsAgent(23, "23 Points"),
        RandomAgent(rng, "R1")
    ]
    renderer = CardRenderer(screen, num_players, logging=False, steps=True)

    final_state = play_game(agents, rng, renderer=renderer)

    pygame.quit()'''