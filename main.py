import random

import pygame

from agents.random_agent import RandomAgent
from game.logic.game_loop import play_game
from game.render.pygame_renderer import CardRenderer

if __name__ == '__main__':
    pygame.init()

    num_players = 5
    window_size = CardRenderer.required_window_size(num_players, card_size=(72, 100), padding=8)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Flip 7")

    rng = random.Random()
    agents = [RandomAgent(rng) for _ in range(num_players)]
    renderer = CardRenderer(screen, num_players, logging=True, steps=True)

    final_state = play_game(agents, rng, renderer=renderer)

    pygame.quit()