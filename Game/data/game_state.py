from dataclasses import dataclass, field

import numpy as np

from Game.data.cards import CardId, ActionType
from Game.data.player import Player


@dataclass
class GameState:
    draw_pile: list[CardId]
    discard_pile: list[CardId]

    players: list[Player]
    current_player_idx: int
    round_number: int

    # Speeds up "cards remaining" calculation for agents
    unseen_cards: np.ndarray = field(default_factory=lambda: np.zeros(len(CardId), dtype=np.int8))

    def get_active_players(self) -> list[Player]:
        return [p for p in self.players if p.is_active()]

    def legal_targets_for(self, action_type: ActionType) -> list[int]:
        if action_type == ActionType.SECOND_CHANCE:
            return [i for i, p in enumerate(self.players) if p.is_active() and not p.second_chance]
        elif action_type in (ActionType.FREEZE, ActionType.FLIP_THREE):
            return [i for i, p in enumerate(self.players) if p.is_active()]

        raise ValueError(f"Unhandled action type: {action_type}")