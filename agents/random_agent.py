import random

from Game.data.cards import ActionType
from Game.data.game_state import GameState
from base_agent import Agent, Decision


class RandomAgent(Agent):
    def choose_action(self, state: GameState) -> Decision:
        return random.choice(list(Decision))

    def choose_target(self, state: GameState, action_type: ActionType, legal_targets: list[int]) -> int:
        return random.choice(legal_targets)