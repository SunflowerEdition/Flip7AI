import random

import numpy as np

from game.data.cards import CardId
from game.data.game_state import GameState


def create_deck() -> list[CardId]:
    """Create the deck of cards used for playing.

    Currently, this function only creates one standard deck of Flip 7.

    :return: A list containing the standard deck of cards.
    """
    deck: list[CardId] = []
    for value in range(13):
        count = value if value > 0 else 1
        deck.extend([CardId(value)] * count)
    deck.extend([CardId.PLUS_2, CardId.PLUS_4, CardId.PLUS_6, CardId.PLUS_8, CardId.PLUS_10, CardId.TIMES_2])
    deck.extend([CardId.FREEZE] * 3 + [CardId.FLIP_THREE] * 3 + [CardId.SECOND_CHANCE] * 3)
    return deck


def count_unseen_cards(pile: list[CardId]) -> np.ndarray:
    """Returns how many of each card remaining in the drawn pile.

    This is used by the agents to determine the probability of selecting
    a card from the draw pile at any given moment.

    :param pile: The list of cards to count, indexed by CardId value.
    :return: An array of len(CardId) where index i holds the count of CardId(i) in pile.
    """
    counts = np.zeros(len(CardId), dtype=np.int8)
    for card_id in pile:
        counts[card_id] += 1
    return counts


def draw_card(state: GameState, rng: random.Random) -> CardId:
    """Draws a random card from the draw pile.

    If there are no more cards left in the deck, the discard pile is shuffled
    and returned to the draw pile. All cards still in play (even if held by
    a player who has busted) are NOT included, and remain on the board.

    :param state: The current game state.
    :param rng: The random number generator.
    :return: The cards drawn from the draw pile.
    """
    if not state.draw_pile:
        if not state.discard_pile:
            raise RuntimeError("Draw pile and discard pile both empty")
        state.draw_pile, state.discard_pile = state.discard_pile, []
        state.unseen_cards = count_unseen_cards(state.draw_pile)
        rng.shuffle(state.draw_pile)

    card = state.draw_pile.pop()
    state.unseen_cards[card] -= 1
    return card
