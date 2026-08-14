import random

from game.data.cards import ActionType, CardId, CARD_METADATA, CardCategory
from game.data.game_state import GameState
from agents.base_agent import Agent, Decision


class EVAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)

    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """
        Will calculate a very basic E.V. value, and hit based on its expected value.
        Doesn't take action cards into account.
        """
        if state.players[player_idx].second_chance:
            return Decision.DRAW
        ev_stay = state.players[player_idx].count_score()
        flip_seven_bonus = 15 if len(state.players[player_idx].number_cards) == 6 else 0

        unseen_cards = state.unseen_cards
        total_unseen = int(unseen_cards.sum())
        if total_unseen == 0:
            raise RuntimeError("THIS SHOULD NEVER HAPPEN!")

        ev_draw = 0.0
        for card_id in CardId:
            if CARD_METADATA[card_id].category == CardCategory.ACTION:
                continue
            count = unseen_cards[card_id]
            probability = count / total_unseen

            if CARD_METADATA[card_id].category == CardCategory.MODIFIER:
                if card_id == CardId.TIMES_2:
                    number_total = sum(CARD_METADATA[c].value for c in state.players[player_idx].number_cards)
                    modifier_and_bonus = ev_stay - number_total
                    ev_draw += (number_total * 2 + modifier_and_bonus) * probability
                else:
                    ev_draw += (ev_stay + CARD_METADATA[card_id].value) * probability
            elif card_id not in state.players[player_idx].number_cards:
                ev_draw += (ev_stay + CARD_METADATA[card_id].value + flip_seven_bonus) * probability

        if ev_draw > ev_stay:
            return Decision.DRAW
        return Decision.STAY

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        # Player second chance on yourself, or the player with the least overall points if you can't
        if action_type == ActionType.SECOND_CHANCE:
            if player_idx in legal_targets:
                return player_idx
            return min(legal_targets, key=lambda p_idx: state.players[p_idx].score)

        # Player flip three on yourself if you have 2 or fewer cards, otherwise on the player with the most round points
        elif action_type == ActionType.FLIP_THREE:
            if player_idx in legal_targets and len(state.players[player_idx].number_cards) <= 2:
                return player_idx
            targets = [p_idx for p_idx in legal_targets if p_idx != player_idx]
            return max(targets or legal_targets, key=lambda p_idx: state.players[p_idx].count_score())

        # Freeze the player with the most overall points (not including themselves)
        targets = [p_idx for p_idx in legal_targets if p_idx != player_idx]
        return max(targets or legal_targets, key=lambda p_idx: state.players[p_idx].score)