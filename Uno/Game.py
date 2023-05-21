import random

from Uno.UnoEnums import Color, Value
from Uno.Deck import Deck
from Uno.Card import Card

class Game:
    def __init__(self, players, seed=381):
        random.seed(seed)

        # create a new deck and shuffle it
        self.deck = Deck()
        self.deck.shuffle()

        # create a discard deck
        self.discard_deck = []

        # save the players
        self.players = players
        self.n_players = len(players)
        # save the last card each player played
        self.players_last_cards = [None]*self.n_players

        # deal 7 cards to each player
        for player in self.players:
            for _ in range(7):
                player.get_card(self.deck.get_card(self.discard_deck))

        # whose turn is it?
        self.turn = random.randrange(self.n_players)
        self.dir = 1
        self.total_turns = 1

    def _incr_turn(self):
        self.total_turns += 1
        self.turn = (self.turn + self.dir) % self.n_players

    def _next_turn(self):
        return (self.turn + self.dir) % self.n_players

    def _get_winner(self):
        for i, player in enumerate(self.players):
            if len(player.hand) == 0:
                return i
        return -1

    def setup_round(self):
        # add the first card in the deck to discard deck
        c = self.deck.get_card(self.discard_deck)
        # however, we cannot start with black +4
        while c is Card(Color.BLACK, Value.WILD4):
            self.deck.add_card(c)
        self.discard_deck.append(c)

        # there are rules for special cards on 1st turn
        
        # draw 2 on 1st turn:
        if c.value is Value.DRAW2:
            #   startng player must draw 2
            self.players[self.turn].get_card(self.deck.get_card(self.discard_deck))
            self.players[self.turn].get_card(self.deck.get_card(self.discard_deck))
            #   and lose turn
            self._incr_turn()
        
        # reverse on 1st turn:
        elif c.value is Value.REV:
            #   change direction of play
            self.dir = -1
        
        # skip on 1st turn:
        elif c.value is Value.SKIP:
            #   skip a player
            self._incr_turn()
        
        # wild on 1st turn:
        elif c.value is Value.WILD:
            #   player chooses color
            color = self.players[self.turn].choose_color(
                total_turns=self.total_turns,
                discard=self.discard_deck
            )
            self.discard_deck.append(color)
            #   and keeps turn
    
    def round(self):
        # NOTE: type(card) can be Card or Color
        top_card = self.discard_deck[-1]

        # calculate the length of everyone's hand
        player_hand_lens = [len(player.hand) for player in self.players]

        player_card = self.players[self.turn].play_card(
            top_card,
            last_cards=self.players_last_cards,
            next_turn=self._next_turn(),
            discard=self.discard_deck,
            hand_lens=player_hand_lens,
            total_turns=self.total_turns
        )

        if player_card is None:
            # if the player doesn't have a matching card
            # give the player a card
            self.players[self.turn].get_card(self.deck.get_card(self.discard_deck))

            player_hand_lens[self.turn] += 1
            # player gets another chance to play
            player_card = self.players[self.turn].play_card(
                top_card,
                last_cards=self.players_last_cards,
                next_turn=self._next_turn(),
                discard=self.discard_deck,
                hand_lens=player_hand_lens,
                total_turns=self.total_turns
            )
        
        # the player played a card
        if player_card is not None:
            if player_card.color is not Color.BLACK:
                self.players_last_cards[self.turn] = player_card

            # add the card to the top of the discard deck
            self.discard_deck.append(player_card)
            if player_card.value is Value.DRAW2:
                # go to the next player
                self._incr_turn()
                # give next player 2 cards
                for _ in range(2):
                    self.players[self.turn].get_card(self.deck.get_card(self.discard_deck))
            elif player_card.value is Value.REV:
                #   change direction of play
                self.dir = -self.dir
            elif player_card.value is Value.SKIP:
                # go to the next player
                self._incr_turn()
            elif player_card.value is Value.WILD:
                # player chooses new color
                color = self.players[self.turn].choose_color(
                    last_cards=self.players_last_cards,
                    next_turn=self._next_turn(),
                    discard=self.discard_deck,
                    hand_lens=player_hand_lens,
                    total_turns=self.total_turns
                )
                self.discard_deck.append(color)
            elif player_card.value is Value.WILD4:
                # player chooses new color
                color = self.players[self.turn].choose_color(
                    last_cards=self.players_last_cards,
                    next_turn=self._next_turn(),
                    discard=self.discard_deck,
                    hand_lens=player_hand_lens,
                    total_turns=self.total_turns
                )
                self.discard_deck.append(color)
                # go to the next player
                self._incr_turn()
                # give next player 4 cards
                for _ in range(4):
                    self.players[self.turn].get_card(self.deck.get_card(self.discard_deck))
        
        # the turn ends after next player is chosen
        self._incr_turn()
        # check for a winner
        return self._get_winner()

    def __str__(self):
        newln = '\n'
        tab = '\t'
        return f"""
Deck: {self.deck}
Discard: [{','.join((str(card) for card in self.discard_deck[-1:-5:-1]))}]

Turn: {self.turn}
{newln.join(f'{i}:{tab}{player}' for i, player in enumerate(self.players))}
        """
    
    def __repr__(self):
        return str(self)