import random

from Uno.UnoEnums import Color, Value
from Uno.Card import Card

class Deck:
    def __init__(self):
        self.cards = []

        # initialize a full deck

        # 1. start with the colored cards
        for c in Color:
            if c is Color.BLACK:
                # handle the wilds later
                continue

            for v in Value:
                if v in (Value.WILD, Value.WILD4):
                    # no wild colored cards
                    continue
                elif v is Value.N0:
                    # only 1 "0" card per color
                    self.cards.append(Card(c, v))
                else:
                    # 2 of all other card per color
                    self.cards.append(Card(c, v))
                    self.cards.append(Card(c, v))
        # 2. now create black cards
        for _ in range(4):
            # 4 wilds
            self.cards.append(Card(Color.BLACK, Value.WILD))
            # and 4 wild draw 4
            self.cards.append(Card(Color.BLACK, Value.WILD4))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self, discard):
        # if we run out of cards use the discard pile
        if len(self.cards) == 0:
            # keep the discard pile's top card aside
            top_card = discard[-1]
            # move all the Cards from discard pile to the deck (some elements might be colors)
            self.cards = [card for card in discard[:-1] if type(card) is Card]
            self.shuffle()
            # empty the discard pile and add the saved card back
            discard.clear()
            discard.append(top_card)
        # get the top card
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.insert(0, card)

    def __str__(self):
        return f"[{','.join((str(card) for card in self.cards[-1:-6:-1]))}]"
    
    def __repr__(self):
        return str(self)