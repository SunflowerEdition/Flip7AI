from dataclasses import dataclass, field

import numpy as np

from game.data.cards import CardId, ActionType
from game.data.player import Player


@dataclass
class GameState:
    """Full state of an in-progress game.

    Both piles, every player, whose turn it is, and a running count of cards not yet drawn this deck-cycle.
    """
    draw_pile: list[CardId]
    discard_pile: list[CardId]

    players: list[Player]
    starting_player_idx: int
    current_player_idx: int
    round_number: int

    # Speeds up "cards remaining" calculation for agents
    unseen_cards: np.ndarray = field(default_factory=lambda: np.zeros(len(CardId), dtype=np.int8))


    def get_active_players(self) -> list[Player]:
        """Returns all active players."""
        return [p for p in self.players if p.is_active()]


    def anyone_flipped_seven(self) -> bool:
        """Returns true if any of the players have flipped seven."""
        return any(len(p.number_cards) >= 7 for p in self.players if not p.busted)


    def update_starting_player_idx(self) -> None:
        """Shifts the starting playing one spot over and sets the current player index."""
        self.starting_player_idx = (self.starting_player_idx + 1) % len(self.players)
        self.current_player_idx = self.starting_player_idx


    def update_active_player_idx(self) -> bool:
        """Shifts the currently playing player's spot over once to the right.

        :return: True if there's an active player, False if there are none remaining.
        """
        n = len(self.players)
        for offset in range(1, n + 1):
            idx = (self.current_player_idx + offset) % n
            if self.players[idx].is_active():
                self.current_player_idx = idx
                return True
        return False


    def legal_targets_for(self, action_type: ActionType) -> list[int]:
        """Returns the legal targets for a given action type.

        :param action_type: Action type.
        :return: List of player indices that are legal for the given action type.
        """
        if action_type == ActionType.SECOND_CHANCE:
            return [i for i, p in enumerate(self.players) if p.is_active() and not p.second_chance]
        elif action_type in (ActionType.FREEZE, ActionType.FLIP_THREE):
            return [i for i, p in enumerate(self.players) if p.is_active()]

        raise ValueError(f"Unhandled action type: {action_type}")
