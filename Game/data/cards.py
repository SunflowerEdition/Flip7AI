from dataclasses import dataclass
from enum import Enum, auto, IntEnum


class CardCategory(Enum):
    NUMBER = auto()
    ACTION = auto()
    MODIFIER = auto()

class ActionType(Enum):
    FREEZE = auto()
    FLIP_THREE = auto()
    SECOND_CHANCE = auto()

class ModifierType(Enum):
    PLUS_POINTS = auto()
    MULTIPLIER = auto()

@dataclass(frozen=True)
class CardInfo:
    category: CardCategory
    value: int | None = None
    action: ActionType | None = None
    modifier: ModifierType | None = None

class CardId(IntEnum):
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    NUMBER_10 = 10
    NUMBER_11 = 11
    NUMBER_12 = 12
    PLUS_2 = 13
    PLUS_4 = 14
    PLUS_6 = 15
    PLUS_8 = 16
    PLUS_10 = 17
    TIMES_2 = 18
    FREEZE = 19
    FLIP_THREE = 20
    SECOND_CHANCE = 21

CARD_METADATA = {
    CardId.NUMBER_0: CardInfo(category=CardCategory.NUMBER, value=0),
    CardId.NUMBER_1: CardInfo(category=CardCategory.NUMBER, value=1),
    CardId.NUMBER_2: CardInfo(category=CardCategory.NUMBER, value=2),
    CardId.NUMBER_3: CardInfo(category=CardCategory.NUMBER, value=3),
    CardId.NUMBER_4: CardInfo(category=CardCategory.NUMBER, value=4),
    CardId.NUMBER_5: CardInfo(category=CardCategory.NUMBER, value=5),
    CardId.NUMBER_6: CardInfo(category=CardCategory.NUMBER, value=6),
    CardId.NUMBER_7: CardInfo(category=CardCategory.NUMBER, value=7),
    CardId.NUMBER_8: CardInfo(category=CardCategory.NUMBER, value=8),
    CardId.NUMBER_9: CardInfo(category=CardCategory.NUMBER, value=9),
    CardId.NUMBER_10: CardInfo(category=CardCategory.NUMBER, value=10),
    CardId.NUMBER_11: CardInfo(category=CardCategory.NUMBER, value=11),
    CardId.NUMBER_12: CardInfo(category=CardCategory.NUMBER, value=12),
    CardId.PLUS_2: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.PLUS_POINTS, value=2),
    CardId.PLUS_4: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.PLUS_POINTS, value=4),
    CardId.PLUS_6: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.PLUS_POINTS, value=6),
    CardId.PLUS_8: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.PLUS_POINTS, value=8),
    CardId.PLUS_10: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.PLUS_POINTS, value=10),
    CardId.TIMES_2: CardInfo(category=CardCategory.MODIFIER, modifier=ModifierType.MULTIPLIER, value=2),
    CardId.FREEZE: CardInfo(category=CardCategory.ACTION, action=ActionType.FREEZE),
    CardId.FLIP_THREE: CardInfo(category=CardCategory.ACTION, action=ActionType.FLIP_THREE),
    CardId.SECOND_CHANCE: CardInfo(category=CardCategory.ACTION, action=ActionType.SECOND_CHANCE),
}