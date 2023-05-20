from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players import CardPriorityPlayer

# Priority:
# draw 2 > skip > reverse > value > color > wild > wild4
class SRVCWDW4_Player(CardPriorityPlayer.CardPriorityPlayer):
    def _get_priority(self, card, top_card, **kwargs):
        # give cards priority by value as described above
        if card.value is Value.SKIP:
            return 0
        elif card.value is Value.REV:
            return 1
        elif type(top_card) is Card and card.value is top_card.value:
            return 2
        elif card.color is (top_card.color if type(top_card) is Card else top_card):
            return 3
        elif card.value is Value.WILD:
            return 4
        elif card.value is Value.DRAW2:
            return 5
        elif card.value is Value.WILD4:
            return 6
        # this card is unplayable this turn
        return 10