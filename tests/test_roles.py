"""Test the roles module, including base class, player, and dealer"""
# The test function name is the docstring
# pylint: disable=missing-docstring
# Disable this pylint rule because of a conflict with @pytest.fixture
# See: stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
# pylint: disable=redefined-outer-name
import pytest
from blackjack.roles import Role


@pytest.fixture
def non_ace_hand():
    from terminal_playing_cards import View, Card

    cards = View([Card("5", "hearts", value=5), Card("K", "hearts", value=10)])
    return Role(hand=cards)


@pytest.fixture
def ace_hand():
    from terminal_playing_cards import View, Card

    cards = View([Card("A", "hearts", value=1), Card("K", "hearts", value=10)])
    return Role(hand=cards)


@pytest.fixture
def queen_spades():
    from terminal_playing_cards import Card

    return Card("Q", "spades", value=10)


def test_hand_total_value(non_ace_hand, ace_hand):
    assert non_ace_hand.total == 15
    assert ace_hand.total == 21


def test_hit_method_adds_to_total(non_ace_hand, queen_spades):
    non_ace_hand.hit(card=queen_spades)
    assert non_ace_hand.total == 25


def test_hit_method_adjusts_ace_value(ace_hand, queen_spades):
    ace_hand.hit(card=queen_spades)
    assert ace_hand.total == 21


def test_role_can_be_created_without_cards():
    role = Role()
    assert isinstance(role, Role)


def test_hand_can_be_set_after_role_creation(queen_spades):
    from terminal_playing_cards import View

    role = Role()
    role.hand = View([queen_spades, queen_spades])
    assert role.total == 20
