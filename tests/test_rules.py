import random

from game.data.cards import CardId
from game.data.player import Player
from game.logic.rules import resolve_drawn_card, end_round
from tests.conftest import create_test_state, TestingAgent
import numpy as np


agents = [TestingAgent(), TestingAgent(), TestingAgent(), TestingAgent(), TestingAgent()]

def test_resolve_drawing_number():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=[], rng=random.Random())

    player = players[0]
    assert(CardId.NUMBER_2 in player.number_cards)
    assert(len(player.number_cards) == 1)
    assert(len(player.modifier_cards) == 0)
    assert(player.count_score() == 2)
    assert(player.dealt_first_card == False) # Does not get decided here
    assert(player.stayed == False)
    assert(player.busted == False)
    assert(player.frozen == False)
    assert(player.second_chance == False)
    assert(player.score == 0)

def test_resolve_busting():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=[], rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=[], rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 2)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == True)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)

def test_resolve_drawing_second_chance():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.SECOND_CHANCE, agents=agents, rng=random.Random())

    player = players[0]
    assert (len(player.number_cards) == 0)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == False)
    assert (player.second_chance == True)
    assert (player.score == 0)

def test_resolve_busting_saved():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.SECOND_CHANCE, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 1)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 2)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    assert (CardId.SECOND_CHANCE in game_state.discard_pile)
    assert (CardId.NUMBER_2 in game_state.discard_pile)
    assert (len(game_state.discard_pile) == 2)

def test_resolve_freeze():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FREEZE, agents=agents, rng=random.Random())

    player = players[0]
    assert (len(player.number_cards) == 0)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == True)
    assert (player.second_chance == False)
    assert (player.score == 0)

def test_resolve_flip_three():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile=[CardId.NUMBER_2, CardId.TIMES_2, CardId.PLUS_10]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 1)
    assert (CardId.TIMES_2 in player.modifier_cards)
    assert (CardId.PLUS_10 in player.modifier_cards)
    assert (len(player.modifier_cards) == 2)
    assert (player.count_score() == 14)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)

def test_resolve_flip_three_bust():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.TIMES_2, CardId.PLUS_10, CardId.NUMBER_2]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 2)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == True)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [CardId.TIMES_2, CardId.PLUS_10])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE])

def test_resolve_flip_three_freeze():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.TIMES_2, CardId.PLUS_10, CardId.FREEZE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (len(player.number_cards) == 0)
    assert (CardId.PLUS_10 in player.modifier_cards)
    assert (CardId.TIMES_2 in player.modifier_cards)
    assert (len(player.modifier_cards) == 2)
    assert (player.count_score() == 10)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == True)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE])

def test_resolve_flip_three_freeze_and_bust():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_2, CardId.NUMBER_2, CardId.FREEZE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 2)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == True)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FREEZE, CardId.FLIP_THREE])

def test_resolve_double_flip_three():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_7, CardId.NUMBER_6, CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_3, CardId.NUMBER_2, CardId.FLIP_THREE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (CardId.NUMBER_3 in player.number_cards)
    assert (CardId.NUMBER_4 in player.number_cards)
    assert (CardId.NUMBER_5 in player.number_cards)
    assert (CardId.NUMBER_6 in player.number_cards)
    assert (len(player.number_cards) == 5)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 20)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [CardId.NUMBER_7])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE, CardId.FLIP_THREE])

def test_resolve_double_flip_three_and_flip_seven():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_7, CardId.NUMBER_6, CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_3, CardId.NUMBER_2,
                 CardId.FLIP_THREE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_12, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_10, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_9, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_8, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (CardId.NUMBER_3 in player.number_cards)
    assert (CardId.NUMBER_4 in player.number_cards)
    assert (len(player.number_cards) == 7)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 63)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [CardId.NUMBER_7, CardId.NUMBER_6, CardId.NUMBER_5])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE, CardId.FLIP_THREE])

def test_resolve_double_flip_three_and_freeze():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_3, CardId.NUMBER_2, CardId.FREEZE, CardId.FLIP_THREE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (CardId.NUMBER_3 in player.number_cards)
    assert (CardId.NUMBER_4 in player.number_cards)
    assert (CardId.NUMBER_5 in player.number_cards)
    assert (len(player.number_cards) == 4)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 14)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == True)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE, CardId.FLIP_THREE])

def test_resolve_double_flip_three_and_freeze_alt_order():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_3, CardId.NUMBER_2, CardId.FLIP_THREE, CardId.FREEZE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 1)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 2)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == False)
    assert (player.frozen == True)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_3])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE, CardId.FLIP_THREE])

def test_resolve_double_flip_three_and_bust():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    draw_pile = [CardId.NUMBER_5, CardId.NUMBER_4, CardId.NUMBER_2, CardId.NUMBER_2, CardId.FREEZE, CardId.FLIP_THREE]
    game_state = create_test_state(draw_pile=draw_pile, players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FLIP_THREE, agents=agents, rng=random.Random())

    player = players[0]
    assert (CardId.NUMBER_2 in player.number_cards)
    assert (len(player.number_cards) == 2)
    assert (len(player.modifier_cards) == 0)
    assert (player.count_score() == 0)
    assert (player.dealt_first_card == False)  # Does not get decided here
    assert (player.stayed == False)
    assert (player.busted == True)
    assert (player.frozen == False)
    assert (player.second_chance == False)
    assert (player.score == 0)
    np.testing.assert_array_equal(game_state.draw_pile, [CardId.NUMBER_5, CardId.NUMBER_4])
    np.testing.assert_array_equal(game_state.discard_pile, [CardId.FLIP_THREE, CardId.FREEZE, CardId.FLIP_THREE])

def test_end_round():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=1, card_id=CardId.NUMBER_3, agents=agents, rng=random.Random())
    end_round(game_state)
    assert(players[0].score == 2)
    assert (players[0].dealt_first_card == False)  # Does not get decided here
    assert (players[0].stayed == False)
    assert (players[0].busted == False)
    assert (players[0].frozen == False)
    assert (players[0].second_chance == False)
    np.testing.assert_array_equal(players[0].number_cards, [])
    assert (players[1].score == 3)
    assert (players[1].dealt_first_card == False)  # Does not get decided here
    assert (players[1].stayed == False)
    assert (players[1].busted == False)
    assert (players[1].frozen == False)
    assert (players[1].second_chance == False)
    np.testing.assert_array_equal(players[1].number_cards, [])
    assert(len(game_state.discard_pile) == 2)
    assert (CardId.NUMBER_2 in game_state.discard_pile)
    assert (CardId.NUMBER_3 in game_state.discard_pile)

def test_end_round_two():
    players = [Player(), Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.NUMBER_2, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.TIMES_2, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.SECOND_CHANCE, agents=agents, rng=random.Random())
    resolve_drawn_card(state=game_state, player_idx=0, card_id=CardId.FREEZE, agents=agents, rng=random.Random())
    end_round(game_state)
    assert(players[0].score == 4)
    assert (players[0].dealt_first_card == False)  # Does not get decided here
    assert (players[0].stayed == False)
    assert (players[0].busted == False)
    assert (players[0].frozen == False)
    assert (players[0].second_chance == False)
    np.testing.assert_array_equal(players[0].number_cards, [])
    np.testing.assert_array_equal(players[0].modifier_cards, [])
    assert(len(game_state.discard_pile) == 4)
    assert (CardId.NUMBER_2 in game_state.discard_pile)
    assert (CardId.TIMES_2 in game_state.discard_pile)
    assert (CardId.SECOND_CHANCE in game_state.discard_pile)
    assert (CardId.FREEZE in game_state.discard_pile)