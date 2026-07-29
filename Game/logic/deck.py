import random

from Game.data.cards import CardId
from Game.data.game_state import GameState


def create_deck() -> list[CardId]:
    deck: list[CardId] = []
    for value in range(13):
        count = value if value > 0 else 1
        deck.extend([CardId(value)] * count)
    deck.extend([CardId.PLUS_2, CardId.PLUS_4, CardId.PLUS_6, CardId.PLUS_8, CardId.PLUS_10, CardId.TIMES_2])
    deck.extend([CardId.FREEZE] * 3 + [CardId.FLIP_THREE] * 3 + [CardId.SECOND_CHANCE] * 3)
    return deck

def draw_card(state: GameState, rng: random.Random) -> CardId:
    # If there are no more cards left in the deck, shuffle the discard pile and replace it
    if not state.draw_pile:
        if not state.discard_pile:
            raise RuntimeError("Draw pile and discard pile both empty")
        state.draw_pile, state.discard_pile = state.discard_pile, []
        rng.shuffle(state.draw_pile)

    # Draw card from the top and update tracker
    card = state.draw_pile.pop()
    state.unseen_cards[card] -= 1
    return card