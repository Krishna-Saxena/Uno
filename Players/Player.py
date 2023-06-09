from abc import ABC, abstractmethod
from collections import Counter

from Uno.UnoEnums import Color
from Uno import Card

class Player(ABC):
    def __init__(self):
        self.hand = []
    
    def get_card(self, card):
        self.hand.append(card)
    
    @abstractmethod
    def play_card(self, top_card, **kwargs):
        # NOTE: type(top_card) can be Card or Color
        return None

    def _choose_most_common_non_black(self, cards):
        color_counts = Counter([c.color for c in cards])
        most_common_colors = color_counts.most_common(2)

        if most_common_colors[0][0] is Color.BLACK and most_common_colors[0][1] == len(cards):
            return Color.GREEN

        # 2nd [0] to access key of (key, value) tuples in most_common_colors
        return most_common_colors[0][0] if most_common_colors[0][0] is not Color.BLACK else most_common_colors[1][0]

    @abstractmethod
    def choose_color(self, **kwargs):
        if len(self.hand) == 0:
            # player will win after calling any color
            return Color.GREEN

        return self._choose_most_common_non_black(self.hand)

    def __str__(self):
        return f"{len(self.hand)} [{','.join((str(card) for card in self.hand))}]"
    
    def __repr__(self):
        return str(self)