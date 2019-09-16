"""Roles for playing blackjack.
Includes base class, with player and dealer implementation.
"""

from terminal_playing_cards import View, Card


class Role:
    """Base class for the a role in a blackjack game.
    Implemented by Player and Dealer.

    Attributes:
        hand: Hand of playing cards for blackjack.
        total: Total score for current hand of blackjack.
    """

    def __init__(self, hand: View = None):
        """Set up the role, with an optional hand attribute"""
        # Set the total before the hand, because the hand can change the total
        self.total = None
        self._hand = None
        self.hand = hand

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
