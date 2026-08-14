import pytest

from game.data.cards import CardId
from game.data.player import Player, AddCardResult


def test_add_number_card():
    player = Player()
    res = player.add_card(CardId.NUMBER_1)
    assert(CardId.NUMBER_1 in player.number_cards)
    assert(res == AddCardResult.SAFE)
    res = player.add_card(CardId.NUMBER_2)
    assert(CardId.NUMBER_1 in player.number_cards)
    assert(CardId.NUMBER_2 in player.number_cards)
    assert (res == AddCardResult.SAFE)
    assert(len(player.number_cards) == 2)
    assert(len(player.modifier_cards) == 0)
    assert(len(player.modifier_cards) == 0)

def test_add_freeze_card():
    player = Player()
    assert(player.frozen == False)
    res = player.add_card(CardId.FREEZE)
    assert(player.frozen == True)
    assert(res == AddCardResult.SAFE)

def test_freeze_frozen_player():
    player = Player()
    player.add_card(CardId.FREEZE)
    with pytest.raises(RuntimeError):
        player.add_card(CardId.FREEZE)

def test_add_second_chance():
    player = Player()
    assert (player.second_chance == False)
    res = player.add_card(CardId.SECOND_CHANCE)
    assert (player.second_chance == True)
    assert (res == AddCardResult.SAFE)

def test_second_chance_double():
    player = Player()
    player.add_card(CardId.SECOND_CHANCE)
    with pytest.raises(RuntimeError):
        player.add_card(CardId.SECOND_CHANCE)

def test_adding_flip_three():
    player = Player()
    with pytest.raises(RuntimeError):
        player.add_card(CardId.FLIP_THREE)

def test_adding_modifier_cards():
    player = Player()
    res = player.add_card(CardId.PLUS_2)
    assert(CardId.PLUS_2 in player.modifier_cards)
    assert(res == AddCardResult.SAFE)
    res = player.add_card(CardId.TIMES_2)
    assert(CardId.PLUS_2 in player.modifier_cards)
    assert(CardId.TIMES_2 in player.modifier_cards)
    assert(res == AddCardResult.SAFE)

def test_busting():
    player = Player()
    res = player.add_card(CardId.NUMBER_2)
    assert(res == AddCardResult.SAFE)
    assert(CardId.NUMBER_2 in player.number_cards)
    res = player.add_card(CardId.NUMBER_2)
    assert(player.busted == True)
    assert(res == AddCardResult.BUSTED)
    assert(len(player.number_cards) == 2)

def test_second_chance_save():
    player = Player()
    assert(player.second_chance == False)
    player.add_card(CardId.SECOND_CHANCE)
    assert(player.second_chance == True)
    res = player.add_card(CardId.NUMBER_3)
    assert(res == AddCardResult.SAFE)
    res = player.add_card(CardId.NUMBER_3)
    assert(res == AddCardResult.SECOND_CHANCE_USED)
    assert(len(player.number_cards) == 1)
    assert(player.second_chance == False)
    res = player.add_card(CardId.NUMBER_3)
    assert(res == AddCardResult.BUSTED)
    assert(len(player.number_cards) == 2)
    assert(player.busted == True)

def test_flipped_seven():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_3)
    player.add_card(CardId.NUMBER_4)
    player.add_card(CardId.NUMBER_5)
    assert(player.flipped_seven() == False)
    player.add_card(CardId.NUMBER_6)
    assert(player.flipped_seven() == True)

def test_is_active_on_bust():
    player = Player()
    assert(player.is_active() == True)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_2)
    assert(player.is_active() == False)

def test_is_active_on_freeze():
    player = Player()
    assert(player.is_active() == True)
    player.add_card(CardId.FREEZE)
    assert(player.is_active() == False)

def test_is_active_on_flip_seven():
    player = Player()
    assert (player.is_active() == True)
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_3)
    player.add_card(CardId.NUMBER_4)
    player.add_card(CardId.NUMBER_5)
    player.add_card(CardId.NUMBER_6)
    assert (player.is_active() == False)

def test_is_active_on_stay():
    player = Player()
    player.stayed = True
    assert (player.is_active() == False)

def test_count_points():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    assert(player.count_score() == 3)

def test_count_points_on_bust():
    player = Player()
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_2)
    assert(player.count_score() == 0)

def test_count_points_on_freeze():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.FREEZE)
    assert (player.count_score() == 3)

def test_count_points_on_flip_seven():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_3)
    player.add_card(CardId.NUMBER_4)
    player.add_card(CardId.NUMBER_5)
    player.add_card(CardId.NUMBER_6)
    assert(player.count_score() == (0 + 1 + 2 + 3 + 4 + 5 + 6 + 15))

def test_count_points_on_modifiers():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.PLUS_10)
    player.add_card(CardId.PLUS_8)
    player.add_card(CardId.PLUS_6)
    player.add_card(CardId.PLUS_4)
    player.add_card(CardId.PLUS_2)
    assert(player.count_score() == (1 + 10 + 8 + 6 + 4 + 2))

def test_count_points_on_multiplier():
    player = Player()
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.TIMES_2)
    assert(player.count_score() == 2)

def test_count_points_on_multiple_multipliers():
    player = Player()
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.TIMES_2)
    player.add_card(CardId.TIMES_2)
    assert (player.count_score() == 8)

def test_count_points_on_multiplier_and_modifiers():
    player = Player()
    player.add_card(CardId.PLUS_10)
    player.add_card(CardId.TIMES_2)
    assert(player.count_score() == 10)

def test_count_points_on_everything():
    player = Player()
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.NUMBER_2)
    player.add_card(CardId.NUMBER_3)
    player.add_card(CardId.NUMBER_4)
    player.add_card(CardId.NUMBER_5)
    player.add_card(CardId.PLUS_10)
    player.add_card(CardId.TIMES_2)
    player.add_card(CardId.NUMBER_6)
    assert(player.count_score() == ((1+2+3+4+5+6)*2 + 15 + 10))

def test_reset_round():
    player = Player()
    player.score = 100
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.TIMES_2)
    player.add_card(CardId.SECOND_CHANCE)
    assert(len(player.modifier_cards) == 1)
    assert(player.frozen == False)
    assert(player.second_chance == True)
    player.add_card(CardId.FREEZE)
    player.stayed = True
    player.busted = True
    player.dealt_first_card = True
    player.reset_round()
    assert(len(player.modifier_cards) == 0)
    assert(len(player.number_cards) == 0)
    assert(player.stayed == False)
    assert(player.dealt_first_card == False)
    assert(player.busted == False)
    assert(player.frozen == False)
    assert(player.score == 100)

def test_reset_game():
    player = Player()
    player.score = 100
    player.add_card(CardId.NUMBER_0)
    player.add_card(CardId.NUMBER_1)
    player.add_card(CardId.TIMES_2)
    player.add_card(CardId.SECOND_CHANCE)
    assert(len(player.modifier_cards) == 1)
    assert(player.frozen == False)
    assert(player.second_chance == True)
    player.add_card(CardId.FREEZE)
    player.stayed = True
    player.busted = True
    player.dealt_first_card = True
    player.reset_game()
    assert(len(player.modifier_cards) == 0)
    assert(len(player.number_cards) == 0)
    assert(player.stayed == False)
    assert(player.dealt_first_card == False)
    assert(player.busted == False)
    assert(player.frozen == False)
    assert(player.score == 0)