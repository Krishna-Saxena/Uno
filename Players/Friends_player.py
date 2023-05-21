from collections import Counter

import numpy as np

from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players import CardPriorityPlayer


class Friends_Player(CardPriorityPlayer.CardPriorityPlayer):
    def __init__(self, beta):
        super().__init__()
        self.beta = beta
        self.cutoff = -np.log(self.beta)

    def _is_end_game(self, turn):
        return turn > self.cutoff

    def choose_color(self, **kwargs):
        total_turns = kwargs['total_turns']
        discard = kwargs['discard']

        colored_cards = [c for c in discard if type(c) is Card]
        most_discarded_color = super()._choose_most_common_non_black(colored_cards) \
            if len(colored_cards) > 0 else Color.GREEN

        if len(self.hand) == 0:
            # player will win after calling any color
            #   so call the most used color
            return most_discarded_color

        # if it is late in the game, choose the most common color in your hand
        if self._is_end_game(total_turns):
            return super().choose_color(**kwargs)

        # otherwise call the least common in your hand
        color_counts = Counter([c.color for c in self.hand])
        least_common_colors = sorted(color_counts.items(), key=lambda pair: pair[1], reverse=True)

        # if you only have black cards, call the most discarded color
        if least_common_colors[0][0] is Color.BLACK and least_common_colors[0][1] == len(self.hand):
            return most_discarded_color
        # return the least common non-black color in your hand
        return least_common_colors[0][0] if least_common_colors[0][0] is not Color.BLACK else least_common_colors[1][0]

    def _get_priority(self, card, top_card, **kwargs):
        total_turns = kwargs['total_turns']

        if self._is_end_game(total_turns):
            # play DSRVCW4W
            if card.value is Value.DRAW2:
                return 0
            elif card.value is Value.REV:
                return 1
            elif card.value is Value.SKIP:
                return 2
            elif type(top_card) is Card and card.value is Value.N0 and top_card.value is Value.N0:
                return 2.5
            elif type(top_card) is Card and card.value is top_card.value:
                return 3
            elif card.color is (top_card.color if type(top_card) is Card else top_card):
                return 4
            elif card.value is Value.WILD4:
                return 5
            elif card.value is Value.WILD:
                return 6
            # this card is unplayable this turn
            return 10

        else:
            # prioritize infrequent non-black cards
            if card.color is Color.BLACK:
                return 10
            else:
                # s = 0
                # for c in self.hand:
                #     if :
                #         s += 1
                # # return s
                return sum((1 if c.color is card.color else 0 for c in self.hand))