from abc import ABC, abstractmethod
from enum import Enum, auto

from game.data.cards import ActionType
from game.data.game_state import GameState


class Decision(Enum):
    DRAW = auto()
    STAY = auto()


class Agent(ABC):
    @abstractmethod
    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """
        Decide which action to take given the state of the game.

        :param state: The state of the game.
        :param player_idx: The index of this agent's player in state.players.
        :return: To action to take.
        """
        pass

    @abstractmethod
    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        """
        Decide which player to target given the game state and action card pulled.

        :param state: The state of the game.
        :param player_idx: The index of this agent's player in state.players.
        :param action_type: The action card to apply.
        :param legal_targets: The legal targets.
        :return: The index of the player to target.
        """
        pass
