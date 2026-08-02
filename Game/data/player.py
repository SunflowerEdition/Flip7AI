from dataclasses import dataclass, field
from enum import auto, Enum

from Game.data.cards import CardId, CARD_METADATA, CardCategory, ActionType


class AddCardResult(Enum):
    SAFE = auto()
    BUSTED = auto()
    SECOND_CHANCE_USED = auto()


@dataclass
class Player:
    number_cards: list[CardId] = field(default_factory=list)
    modifier_cards: list[CardId] = field(default_factory=list)

    dealt_first_card: bool = False
    stayed: bool = False
    busted: bool = False
    frozen: bool = False
    second_chance: bool = False
    score: int = 0


    def add_card(self, card_id: CardId) -> AddCardResult:
        """
        Add a card to the player's hand.

        :param card_id: The id of the card to add
        :return: The result of adding the card: safe, busted, or a second chance used
        """
        card_category = CARD_METADATA[card_id].category

        # Action card is played on the player
        if card_category == CardCategory.ACTION:
            if CARD_METADATA[card_id].action == ActionType.FREEZE:
                if self.frozen or self.busted:
                    raise RuntimeError(f'Attempted to freeze a frozen ({self.frozen}) or busted ({self.busted}) player')
                self.frozen = True
            elif CARD_METADATA[card_id].action == ActionType.SECOND_CHANCE:
                self.second_chance = True
            elif CARD_METADATA[card_id].action == ActionType.FLIP_THREE:
                raise RuntimeError(f"Flip three card played on player. This shouldn't get to here!")
            else:
                raise RuntimeError(f'Unknown card category {card_category}')

        # Modifier cards simply get added
        elif card_category == CardCategory.MODIFIER:
            self.modifier_cards.append(card_id)

        # Number cards need to verify if busted
        elif card_category == CardCategory.NUMBER:
            if card_id in self.number_cards:
                if self.second_chance:
                    self.second_chance = False
                    return AddCardResult.SECOND_CHANCE_USED
                self.number_cards.append(card_id)
                self.busted = True
                return AddCardResult.BUSTED
            else:
                self.number_cards.append(card_id)

        else:
            raise RuntimeError(f'Unknown card category {card_category}')

        return AddCardResult.SAFE


    def is_active(self) -> bool:
        """Checks if the player is active."""
        return (not self.stayed) and (not self.busted) and (not self.frozen) and (len(self.number_cards) < 7)


    def flipped_seven(self) -> bool:
        """Checks if the player has flipped seven. """
        return (not self.busted) and (len(self.number_cards) >= 7)


    def count_score(self) -> int:
        """Counts the player's score for the round.

        First all number cards are counted. Then, the multiplier card
        is applied (if applicable). Then, the modifier cards are applied.
        Finally, the flip 7 bonus is applied (if applicable).

        :return: The player's score for the round.
        """
        # Bonus points if player flipped seven
        bonus = 0
        if len(self.number_cards) >= 7:
            bonus += 15

        # Sum all number cards
        number_total = 0
        for card_id in self.number_cards:
            number_total += CARD_METADATA[card_id].value

        # Sum all modifiers and check for multipliers
        modifier_total = 0
        times_two_found = 0
        for card_id in self.modifier_cards:
            if card_id == CardId.TIMES_2:
                times_two_found += 1
            else:
                modifier_total += CARD_METADATA[card_id].value

        # Times twos multiply number total only
        for _ in range(times_two_found):
            number_total *= 2

        return number_total + modifier_total + bonus


    def reset_round(self) -> None:
        """Resets the round."""
        self.number_cards.clear()
        self.modifier_cards.clear()
        self.dealt_first_card = False
        self.stayed = False
        self.busted = False
        self.frozen = False
        self.second_chance = False

    def reset_game(self) -> None:
        """Resets the game."""
        self.reset_round()
        self.score = 0