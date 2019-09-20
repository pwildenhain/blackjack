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

    return View([Card("5", "hearts", value=5), Card("K", "hearts", value=10)])


@pytest.fixture
def ace_hand():
    from terminal_playing_cards import View, Card

    return View([Card("A", "hearts", value=1), Card("K", "hearts", value=10)])


@pytest.fixture
def role_without_ace(non_ace_hand):
    return Role(hand=non_ace_hand)


@pytest.fixture
def role_with_ace(ace_hand):
    return Role(hand=ace_hand)


@pytest.fixture
def queen_spades():
    from terminal_playing_cards import Card

    return Card("Q", "spades", value=10)


def test_hand_total_value(role_without_ace, role_with_ace):
    assert role_without_ace.total == 15
    assert role_with_ace.total == 21


def test_hit_method_adds_to_total(role_without_ace, queen_spades):
    role_without_ace.hit(card=queen_spades)
    assert role_without_ace.total == 25


def test_hit_method_adjusts_ace_value(role_with_ace, queen_spades):
    role_with_ace.hit(card=queen_spades)
    assert role_with_ace.total == 21


def test_role_can_be_created_without_cards():
    role = Role()
    assert isinstance(role, Role)


def test_hand_can_be_set_after_role_creation(queen_spades):
    from terminal_playing_cards import View

    role = Role()
    role.hand = View([queen_spades, queen_spades])
    assert role.total == 20
