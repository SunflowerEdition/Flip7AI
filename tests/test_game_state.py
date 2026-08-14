from game.data.cards import CardId, ActionType
from game.data.player import Player
from tests.conftest import create_test_state
import numpy as np


def test_get_active_players():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    np.testing.assert_array_equal(game_state.get_active_players(), players)

def test_flipped_seven_false():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.NUMBER_0)
    players[0].add_card(CardId.NUMBER_1)
    players[0].add_card(CardId.NUMBER_2)
    players[0].add_card(CardId.NUMBER_3)
    players[0].add_card(CardId.NUMBER_4)
    players[0].add_card(CardId.NUMBER_5)
    players[0].add_card(CardId.PLUS_2)
    players[0].add_card(CardId.PLUS_4)
    players[0].add_card(CardId.PLUS_6)
    players[0].add_card(CardId.PLUS_8)
    players[0].add_card(CardId.PLUS_10)
    players[0].add_card(CardId.TIMES_2)
    players[0].add_card(CardId.SECOND_CHANCE)
    game_state = create_test_state(draw_pile=[], players=players)
    assert(game_state.anyone_flipped_seven() == False)

def test_flipped_seven_true():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.NUMBER_0)
    players[0].add_card(CardId.NUMBER_1)
    players[0].add_card(CardId.NUMBER_2)
    players[0].add_card(CardId.NUMBER_3)
    players[0].add_card(CardId.NUMBER_4)
    players[0].add_card(CardId.NUMBER_5)
    players[0].add_card(CardId.NUMBER_6)
    game_state = create_test_state(draw_pile=[], players=players)
    assert(game_state.anyone_flipped_seven() == True)

def test_update_starting_player():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    game_state.starting_player_idx = 3
    game_state.update_starting_player_idx()
    assert(game_state.starting_player_idx == 4)
    assert(game_state.current_player_idx == 4)
    game_state.update_starting_player_idx()
    assert (game_state.starting_player_idx == 0)
    assert (game_state.current_player_idx == 0)

def test_update_active_player():
    players = [Player(), Player(), Player(), Player(), Player()]
    game_state = create_test_state(draw_pile=[], players=players)
    game_state.starting_player_idx = 3
    game_state.current_player_idx = 3
    game_state.update_active_player_idx()
    assert (game_state.starting_player_idx == 3)
    assert (game_state.current_player_idx == 4)
    game_state.update_active_player_idx()
    assert (game_state.starting_player_idx == 3)
    assert (game_state.current_player_idx == 0)

def test_legal_actions_for_second_chance_one():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.SECOND_CHANCE)
    players[1].add_card(CardId.SECOND_CHANCE)
    players[4].add_card(CardId.SECOND_CHANCE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.SECOND_CHANCE)
    np.testing.assert_array_equal(target_indices, [2, 3])

def test_legal_actions_for_second_chance_two():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.SECOND_CHANCE)
    players[1].add_card(CardId.SECOND_CHANCE)
    players[2].add_card(CardId.SECOND_CHANCE)
    players[3].add_card(CardId.SECOND_CHANCE)
    players[4].add_card(CardId.SECOND_CHANCE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.SECOND_CHANCE)
    np.testing.assert_array_equal(target_indices, [])

def test_legal_actions_for_second_chance_three():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.SECOND_CHANCE)
    players[1].add_card(CardId.FREEZE)
    players[2].add_card(CardId.NUMBER_2)
    players[2].add_card(CardId.NUMBER_2)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.SECOND_CHANCE)
    np.testing.assert_array_equal(target_indices, [3, 4])

def test_legal_actions_for_freeze_one():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.FREEZE)
    players[1].add_card(CardId.FREEZE)
    players[4].add_card(CardId.FREEZE)
    players[2].add_card(CardId.SECOND_CHANCE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FREEZE)
    np.testing.assert_array_equal(target_indices, [2, 3])

def test_legal_actions_for_freeze_two():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.FREEZE)
    players[1].add_card(CardId.FREEZE)
    players[2].add_card(CardId.FREEZE)
    players[3].add_card(CardId.FREEZE)
    players[4].add_card(CardId.FREEZE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FREEZE)
    np.testing.assert_array_equal(target_indices, [])

def test_legal_actions_for_freeze_three():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.SECOND_CHANCE)
    players[1].add_card(CardId.FREEZE)
    players[2].add_card(CardId.NUMBER_2)
    players[2].add_card(CardId.NUMBER_2)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FREEZE)
    np.testing.assert_array_equal(target_indices, [0, 3, 4])

def test_legal_actions_for_flip_three_one():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.FREEZE)
    players[1].add_card(CardId.FREEZE)
    players[4].add_card(CardId.FREEZE)
    players[2].add_card(CardId.SECOND_CHANCE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FLIP_THREE)
    np.testing.assert_array_equal(target_indices, [2, 3])

def test_legal_actions_for_flip_three_two():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.FREEZE)
    players[1].add_card(CardId.FREEZE)
    players[2].add_card(CardId.FREEZE)
    players[3].add_card(CardId.FREEZE)
    players[4].add_card(CardId.FREEZE)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FLIP_THREE)
    np.testing.assert_array_equal(target_indices, [])

def test_legal_actions_for_flip_three_three():
    players = [Player(), Player(), Player(), Player(), Player()]
    players[0].add_card(CardId.SECOND_CHANCE)
    players[1].add_card(CardId.FREEZE)
    players[2].add_card(CardId.NUMBER_2)
    players[2].add_card(CardId.NUMBER_2)
    game_state = create_test_state(draw_pile=[], players=players)
    target_indices = game_state.legal_targets_for(ActionType.FLIP_THREE)
    np.testing.assert_array_equal(target_indices, [0, 3, 4])