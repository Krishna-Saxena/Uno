from collections import Counter

import numpy as np

from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players import CardPriorityPlayer


class Friends_Player(CardPriorityPlayer.CardPriorityPlayer):
    def __init__(self, beta):
        super().__init__()
        self.beta = beta

    def choose_color(self, **kwargs):
        total_turns = kwargs['total_turns']
        discard = kwargs['discard']

        most_discarded_color = super()._choose_most_common_non_black(discard)

        if len(self.hand) == 0:
            # player will win after calling any color
            #   so call the most used color
            return most_discarded_color

        if np.exp(-self.beta*total_turns) > 0.5:
            return super().choose_color(**kwargs)

        color_counts = Counter([c.color for c in self.hand])
        least_common_colors = sorted(color_counts.items(), key=lambda pair: pair[1], reverse=True)

        if least_common_colors[0][0] is Color.BLACK and least_common_colors[0][1] == len(self.hand):
            return most_discarded_color

        # 2nd [0] to access key of (key, value) tuples in most_common_colors
        return least_common_colors[0][0] if least_common_colors[0][0] is not Color.BLACK else least_common_colors[1][0]

    def _get_priority(self, card, top_card, **kwargs):
        last_cards = kwargs['last_cards']
        next_turn = kwargs['next_turn']
        discard = kwargs['discard']
        hand_lens = kwargs['hand_lens']
        total_turns = kwargs['total_turns']
