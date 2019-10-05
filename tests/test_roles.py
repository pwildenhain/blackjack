"""Test the roles module, including base class, player, and dealer"""
# The test function name is the docstring
# pylint: disable=missing-docstring
# Disable this pylint rule because of a conflict with @pytest.fixture
# See: stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
# pylint: disable=redefined-outer-name
import pytest
from blackjack.roles import Role, Dealer, Player


@pytest.fixture
def non_ace_hand():
    from terminal_playing_cards import View, Card

    return View([Card("5", "hearts", value=5), Card("K", "hearts", value=10)])


@pytest.fixture
def ace_hand():
    from terminal_playing_cards import View, Card

    return View([Card("A", "hearts", value=1), Card("K", "hearts", value=10)])


@pytest.fixture
def queen_spades():
    from terminal_playing_cards import Card

    return Card("Q", "spades", value=10)


@pytest.fixture
def custom_deck():
    """Custom made, predictable deck, used for testing
    Dealer.play() and Player.play() methods
    """
    from terminal_playing_cards import Deck

    custom_spec = {
        "A": {"clubs": 1},
        "2": {"clubs": 2},
        "J": {"clubs": 10},
        "3": {"clubs": 3},
    }

    return Deck(specifications=custom_spec)


def test_hand_total_value(non_ace_hand, ace_hand):
    role_without_ace = Role(hand=non_ace_hand)
    role_with_ace = Role(hand=ace_hand)
    assert role_without_ace.total == 15
    assert role_with_ace.total == 21


def test_hit_method_adds_to_total(non_ace_hand, queen_spades):
    role = Role(hand=non_ace_hand)
    role.hit(card=queen_spades)
    assert role.total == 25


def test_hit_method_adjusts_ace_value(ace_hand, queen_spades):
    role = Role(hand=ace_hand)
    role.hit(card=queen_spades)
    assert role.total == 21


def test_role_can_be_created_without_cards():
    role = Role()
    assert isinstance(role, Role)


def test_hand_can_be_set_after_role_creation(queen_spades):
    from terminal_playing_cards import View

    role = Role()
    role.hand = View([queen_spades, queen_spades])
    assert role.total == 20


def test_dealer_unhides_card_when_playing(custom_deck, ace_hand):
    # Mimic how cards are dealt in Blackjack class
    ace_hand[0].hidden = True
    dealer = Dealer(hand=ace_hand)

    dealer.play(deck=custom_deck)

    assert not dealer.hand[0].hidden


def test_dealer_stops_playing_over_seventeen(custom_deck, non_ace_hand):
    dealer = Dealer(hand=non_ace_hand)

    dealer.play(deck=custom_deck)

    assert dealer.total == 18
    assert len(dealer.hand) == 4


def test_player_can_be_created_without_attrs():
    player = Player()
    assert isinstance(player, Player)


def test_choose_move_returns_correct_string(mocker):
    player = Player()
    mocker.patch("blackjack.roles.input", side_effect=[0, 1])
    first_move = player.choose_move()
    second_move = player.choose_move()

    assert first_move == "hit"
    assert second_move == "stay"


def test_choose_move_doesnt_allow_bad_input(mocker):
    player = Player()
    moves_mock = mocker.patch("blackjack.roles.input", side_effect=["a", 5, 0])
    move = player.choose_move()
    # Should keep calling "input()" until valid input is received
    assert moves_mock.call_count == 3
    assert move == "hit"


def test_player_cant_play_with_blackjack(mocker, ace_hand, custom_deck):
    player = Player(hand=ace_hand)

    mock_moves = mocker.patch("blackjack.roles.Player.choose_move", side_effect=["hit"])
    player.play(deck=custom_deck)
    # Should not have been given the option to choose since move
    # since the hand total is already blackjack
    mock_moves.assert_not_called()
    assert player.total == 21


def test_player_cant_play_with_gt_twentyone(mocker, non_ace_hand, custom_deck):
    player = Player(hand=non_ace_hand)

    mock_moves = mocker.patch(
        "blackjack.roles.Player.choose_move", side_effect=["hit", "hit", "hit", "hit"]
    )
    player.play(deck=custom_deck)
    # Should not have been given the option to hit a fourth time
    # because total is a bust
    assert mock_moves.call_count == 3
    assert player.total == 28


def test_player_is_allowed_to_stay(mocker, non_ace_hand, custom_deck):
    player = Player(hand=non_ace_hand)

    mock_moves = mocker.patch(
        "blackjack.roles.Player.choose_move", side_effect=["hit", "stay", "hit"]
    )
    player.play(deck=custom_deck)
    # Should have stoppped choosing moves after "stay"
    assert mock_moves.call_count == 2
    assert player.total == 16
