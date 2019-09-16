"""Roles for playing blackjack.
Includes base class, with player and dealer implementation.
"""
from typing import Union
from terminal_playing_cards import View, Card


class Role:
    """Base class for the a role in a blackjack game.
    Implemented by Player and Dealer.

    Attributes:
        hand: Hand of playing cards for blackjack.
        total: Total score for current hand of blackjack.
    """

    def __init__(self, hand: View = None):
        """Set up the role, and calculate the blackjack hand starting total."""
        self._hand = None
        self.hand = hand

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value: Union[Card, View]):
        """Recalculate the total each time a Card/View is added to the hand"""
        # Skip setting if the hand is empty
        if not value:
            return None

        if isinstance(value, View):
            self._hand = value
        elif isinstance(value, Card):
            self._hand += [value]
        elif self._hand:
            raise NotImplementedError(
                f"""
            The Role.hand attribute only accepts a Card or View object,
            not: '{type(value)}'
            """
            )

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
