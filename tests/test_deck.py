import random

import pytest

from game.data.cards import CardId
from game.logic.deck import create_deck, draw_card, count_unseen_cards
from conftest import create_test_state
import numpy as np

from tests.conftest import create_full_unseen_card_pile, NUM_CARDS_IN_FULL_DECK, NUM_UNIQUE_CARDS


def test_create_deck_has_correct_size():
    deck = create_deck()
    assert len(deck) == 94

def test_create_deck_has_correct_number_cards():
    deck = create_deck()
    assert deck.count(CardId.NUMBER_0) == 1
    assert deck.count(CardId.NUMBER_1) == 1
    assert deck.count(CardId.NUMBER_2) == 2
    assert deck.count(CardId.NUMBER_3) == 3
    assert deck.count(CardId.NUMBER_4) == 4
    assert deck.count(CardId.NUMBER_5) == 5
    assert deck.count(CardId.NUMBER_6) == 6
    assert deck.count(CardId.NUMBER_7) == 7
    assert deck.count(CardId.NUMBER_8) == 8
    assert deck.count(CardId.NUMBER_9) == 9
    assert deck.count(CardId.NUMBER_10) == 10
    assert deck.count(CardId.NUMBER_11) == 11
    assert deck.count(CardId.NUMBER_12) == 12
    assert deck.count(CardId.FLIP_THREE) == 3
    assert deck.count(CardId.SECOND_CHANCE) == 3
    assert deck.count(CardId.FREEZE) == 3
    assert deck.count(CardId.PLUS_2) == 1
    assert deck.count(CardId.PLUS_4) == 1
    assert deck.count(CardId.PLUS_6) == 1
    assert deck.count(CardId.PLUS_8) == 1
    assert deck.count(CardId.PLUS_10) == 1
    assert deck.count(CardId.TIMES_2) == 1


def test_draw_top_card():
    game_state = create_test_state(draw_pile=create_deck())
    top_card = game_state.draw_pile[-1]
    drawn_card = draw_card(game_state, random.Random())
    assert(top_card == drawn_card)

def test_draw_empty_deck():
    game_state = create_test_state(draw_pile=[], discard_pile=[CardId.NUMBER_0])
    drawn_card = draw_card(game_state, random.Random())
    assert(drawn_card == CardId.NUMBER_0)

def test_many_draws():
    game_state = create_test_state(draw_pile=create_deck())
    for _ in range(NUM_CARDS_IN_FULL_DECK):
        draw_card(game_state, random.Random())
    assert(len(game_state.draw_pile) == 0)
    assert(len(game_state.discard_pile) == 0)

def test_count_unseen_cards():
    game_state = create_test_state(draw_pile=create_deck())
    true_unseen_cards = create_full_unseen_card_pile()
    test_unseen_cards = count_unseen_cards(game_state.draw_pile)
    np.testing.assert_array_equal(test_unseen_cards, true_unseen_cards)

def test_count_unseen_updates():
    game_state = create_test_state(draw_pile=create_deck())
    unseen_cards = create_full_unseen_card_pile()
    card = draw_card(game_state, random.Random())
    unseen_cards[card] -= 1
    np.testing.assert_array_equal(game_state.unseen_cards, unseen_cards)
    assert(len(game_state.draw_pile) == NUM_CARDS_IN_FULL_DECK - 1)

def test_count_unseen_updates_on_deck_shuffle():
    game_state = create_test_state(draw_pile=[], discard_pile=[CardId.NUMBER_0, CardId.FLIP_THREE, CardId.TIMES_2])
    game_state.unseen_cards = count_unseen_cards(game_state.draw_pile)
    true_unseen_cards = [0] * NUM_UNIQUE_CARDS
    true_unseen_cards[CardId.NUMBER_0] += 1
    true_unseen_cards[CardId.FLIP_THREE] += 1
    true_unseen_cards[CardId.TIMES_2] += 1
    drawn_card = draw_card(game_state, random.Random())
    true_unseen_cards[drawn_card] -= 1
    np.testing.assert_array_equal(game_state.unseen_cards, true_unseen_cards)

def test_empty_draw_and_discard_piles():
    game_state = create_test_state(draw_pile=[], discard_pile=[])
    with pytest.raises(RuntimeError):
        draw_card(game_state, random.Random())