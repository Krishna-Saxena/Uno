from collections import Counter

from Uno.UnoEnums import Color, Value
from Uno.Card import Card
from Players import CardPriorityPlayer


class Friends_Player(CardPriorityPlayer.CardPriorityPlayer):
    def choose_color(self, **kwargs):
        discard = kwargs['discard_deck']

        if len(self.hand) == 0:
            # player will win after calling any color
            return Color.GREEN

        color_counts = Counter([c.color for c in self.hand])
        most_common_colors = color_counts.most_common(2)

        if most_common_colors[0][0] is Color.BLACK and most_common_colors[0][1] == len(self.hand):
            return Color.GREEN

        # 2nd [0] to access key of (key, value) tuples in most_common_colors
        return most_common_colors[0][0] if most_common_colors[0][0] is not Color.BLACK else most_common_colors[1][0]

    def _get_priority(self, card, top_card, **kwargs):
        last_cards = kwargs['last_cards']
        next_turn = kwargs['next_turn']
        discard = kwargs['discard']
        hand_lens = kwargs['hand_lens']
        total_turns = kwargs['total_turns']
