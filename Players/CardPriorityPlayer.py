from abc import ABC, abstractmethod

from Uno.UnoEnums import Color
from Uno.Card import Card
from Players.Player import Player

class CardPriorityPlayer(Player):
    @abstractmethod
    def _get_priority(self, card, top_card, **kwargs):
        pass

    def play_card(self, top_card, **kwargs):
        # NOTE: type(top_card) can be Card or Color
        
        # sort hand by priority
        self.hand = sorted(self.hand, key=lambda card : self._get_priority(card, top_card, **kwargs))
        # print('sorted hand', ','.join(str(card) for card in self.hand))

        # play the highest priority valid card
        #   by checking whether idx'th card in hand is valid
        idx = 0
        while idx < len(self.hand):
            card = self.hand[idx]
            if card.color is Color.BLACK:
                break
            elif type(top_card) is Card and card.value is top_card.value:
                break
            elif card.color is (top_card.color if type(top_card) is Card else top_card):
                break
            idx += 1
        # print('idx', idx, 'hand[idx]', self.hand[idx] if idx != len(self.hand) else None)
        return self.hand.pop(idx) if idx != len(self.hand) else None

    def choose_color(self):
        return super().choose_color()