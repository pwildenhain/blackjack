"""Roles for playing blackjack.
Includes base class, with player and dealer implementation.
"""

from terminal_playing_cards import Deck, View, Card


class Role:
    """Base class for the a role in a blackjack game.
    Implemented by Player and Dealer.

    Attributes:
        hand: View of playing cards for blackjack.
        total: Integer of total score for current hand of blackjack.
    """

    def __init__(self, hand: View = None, name: str = None):
        """Set up the role, with an optional hand attribute"""
        # Set the total before the hand, because the hand can change the total
        self.total = None
        self._hand = None
        self.hand = hand
        self.name = name

    @property
    # pylint: disable=missing-docstring
    def hand(self):
        return self._hand

    # pylint: enable=missing-docstring

    @hand.setter
    def hand(self, value: View):
        """Calculate the total when a View is added to the hand"""
        self._hand = value
        # Set other attributes if hand isn't None
        if value:
            self.set_ace_value()
            self.total = sum(self._hand)

    def set_ace_value(self) -> None:
        """Re-evaluate the current value for an ace"""
        for card in self.hand:
            if card.face == "A":
                card.value = 11 if sum(self.hand) + 10 <= 21 else 1
                break

    def hit(self, card: Card) -> None:
        """Add a card to the hand from the deck. Recalculate the hand total."""
        self.hand += [card]
        self.set_ace_value()
        self.total = sum(self.hand)


class Dealer(Role):
    """Dealer in a blackjack game. This class does **not**
    run the whole game, like in the real word. Rather it's
    a simple implementation of Role.
    """

    def __init__(self, hand: View = None):
        super().__init__(hand=hand, name="Dealer")

    def play(self, deck: Deck):
        """Follow the strict rules of how a dealer is supposed to play
        blackjack. This includes unhiding the second card in the hand
        and only playing until the total hits 17 or above.
        """
        self.hand[1].hidden = False

        while self.total < 17:
            self.hit(card=deck.pop())
            print(self.hand)


class Player(Role):
    """A player in a blackjack game. This class is
    given options as to what to do when it plays. It
    also has a bank that keeps track of it's money,
    and stores the bet that the player made
    """

    def __init__(
        self, hand: View = None, name: str = None, bank: int = None, bet: int = None
    ):
        """Store the name, bank roll, current bet, and moves of the player"""
        super().__init__(hand=hand, name=name)
        self.bank = bank
        self.bet = bet
        self.moves = {0: "hit", 1: "stay"}

    def choose_move(self):
        """Allow the player to choose which move to take from the moves attribute"""
        user_choice = ""
        while user_choice not in self.moves.keys():
            for choice, move in self.moves.items():
                print(f"{choice}: {move.title()}")
            try:
                user_choice = int(input("Choose a move: "))
            except ValueError:
                print("Numbers only please :-)")
                continue

        return self.moves.get(user_choice)

    def play(self, deck: Deck):
        """If a player doesn't have blackjack, allow them to choose
        their move and calculate and new hand total. Keep asking for
        a move until bust or blackjack
        """
        if self.total == 21:
            return None
        keep_playing = self.choose_move() == "hit"
        while keep_playing:
            self.hit(card=deck.pop())
            print(self.hand)
            if self.total >= 21:
                break
            keep_playing = self.choose_move() == "hit"
