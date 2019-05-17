"""Test the Card and Deck classes"""

from blackjack.cards import Card


def test_card_str_value():
    """Ensure the string value given the card"""
    ace_spades = Card("A", "spades")
    ace_spades_string = (
        "\x1b[47m\x1b[30m\nA      \n\u2660      \n   \u2660   \n      \u2660\n      A"
    )
    assert str(ace_spades) == ace_spades_string

