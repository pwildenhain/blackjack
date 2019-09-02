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

    def __init__(self, hand: View):
        """Set up the role, and calculate the blackjack hand starting total."""
        self.hand = hand
        # Evaluate possisble aces before setting total
        self.set_ace_values()
        self.total = sum(hand)

    def show_hand(self) -> None:
        """Print the hand in the terminal."""
        print(self.hand)

    def set_ace_values(self) -> None:
        """Re-evaluate the current values for aces"""
        for card in self.hand:
            if card.face == "A":
                card.value = 11 if sum(self.hand) + 10 <= 21 else 1

    def hit(self, card: Card) -> None:
        """Add a card to the hand from the deck. Recalculate the hand total."""
        self.hand += [card]
        self.set_ace_values()
        self.total = sum(self.hand)
