from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players.CardPriorityPlayer import CardPriorityPlayer


# Priority:
# wild > draw 2 > skip > reverse > value > color > wild4
class WDSRCVW4_Player(CardPriorityPlayer):
    def _get_priority(self, card, top_card, **kwargs):
        # give cards priority by value as described above
        if card.value is Value.WILD:
            return 0
        elif card.value is Value.DRAW2:
            return 1
        elif card.value is Value.SKIP:
            return 2
        elif card.value is Value.REV:
            return 3
        elif card.color is (top_card.color if type(top_card) is Card else top_card):
            return 4
        elif type(top_card) is Card and card.value is top_card.value:
            return 5
        elif card.value is Value.WILD4:
            # weight this lowest b/c in a real game you must draw 4
            #   if you play this before a different valid card and get caught
            return 6
        # this card is unplayable this turn
        return 10
