from agents.base_agent import Agent, Decision
from game.data.cards import CardId, ActionType
from game.data.game_state import GameState
from game.data.player import Player
from game.logic.deck import count_unseen_cards


NUM_CARDS_IN_FULL_DECK = 94
NUM_UNIQUE_CARDS = len(CardId)

def create_test_state(
        draw_pile: list[CardId],
        discard_pile: list[CardId] | None = None,
        players: list[Player] | None = None
) -> GameState:
    unseen_cards = count_unseen_cards(draw_pile)

    if discard_pile is None:
        discard_pile = []
    if players is None:
        players = []

    return GameState(
        draw_pile=draw_pile.copy(),
        discard_pile=discard_pile.copy(),
        players=players.copy(),
        starting_player_idx=0,
        current_player_idx=0,
        round_number=1,
        unseen_cards=unseen_cards,
    )

def create_full_unseen_card_pile():
    return [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 1, 1, 1, 1, 1, 3, 3, 3]

class TestingAgent(Agent):
    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """Always draws a card."""
        return Decision.DRAW

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        """Always choose itself."""
        return player_idx

class AlwaysStayAgent(Agent):
    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """Always stay."""
        return Decision.STAY

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        """Always choose itself."""
        return player_idx