import random

from game.data.cards import ActionType
from game.data.game_state import GameState
from agents.base_agent import Agent, Decision


class RandomAgent(Agent):
    def __init__(self, rng: random.Random, name: str):
        super().__init__(name)
        self._rng = rng

    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        return self._rng.choice(list(Decision))

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        return self._rng.choice(legal_targets)