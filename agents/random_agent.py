import random

from Game.data.cards import ActionType
from Game.data.game_state import GameState
from base_agent import Agent, Decision


class RandomAgent(Agent):
    def __init__(self, rng: random.Random):
        self._rng = rng

    def choose_action(self, state: GameState) -> Decision:
        return self._rng.choice(list(Decision))

    def choose_target(self, state: GameState, action_type: ActionType, legal_targets: list[int]) -> int:
        return self._rng.choice(legal_targets)