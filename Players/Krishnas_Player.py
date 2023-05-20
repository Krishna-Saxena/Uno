from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players import CardPriorityPlayer

class Krishnas_Player(CardPriorityPlayer.CardPriorityPlayer):
    def _play_defensive(self, card, top_card):
        # give cards priority by value as described above
        if card.value is Value.SKIP:
            return 0
        elif card.value is Value.REV:
            return 1
        elif type(top_card) is Card and card.value is top_card.value:
            return 2
        elif card.color is (top_card.color if type(top_card) is Card else top_card):
            return 3
        elif card.value is Value.DRAW2:
            return 4
        elif card.value is Value.WILD:
            return 5
        elif card.value is Value.WILD4:
            return 6
        # this card is unplayable this turn
        return 10
    
    def _play_attacking(self, card, top_card):
        # give cards priority by value as described above
        if card.value is Value.DRAW2:
            return 0
        elif card.value is Value.SKIP:
            return 1
        elif card.value is Value.REV:
            return 2
        elif card.color is (top_card.color if type(top_card) is Card else top_card):
            return 4
        elif card.value is Value.WILD4:
            return 6
        elif card.value is Value.WILD:
            return 5
        # this card is unplayable this turn
        return 10

    def _get_priority(self, card, top_card, **kwargs):
        last_cards = kwargs['last_cards']
        next_turn = kwargs['next_turn']
        discard = kwargs['discard']
        hand_lens = kwargs['hand_lens']

        if min(hand_lens) > 3:
            return self._play_defensive(card, top_card)
        else:
            return self._play_attacking(card, top_card)

    def choose_color(self, **kwargs):
