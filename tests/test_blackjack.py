"""Test running a blackjack game"""
# The test function name is the docstring
# pylint: disable=missing-docstring
# Disable this pylint rule because of a conflict with @pytest.fixture
# See: stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
# pylint: disable=redefined-outer-name
import pytest
from blackjack.game import Blackjack


@pytest.fixture
def new_blackjack_game():
    from terminal_playing_cards import Deck
    from blackjack.roles import Player, Dealer

    return Blackjack(
        deck=Deck(hidden=True),
        dealer=Dealer(),
        players=[Player(bank=500), Player(bank=500)],
    )


def test_taking_and_storing_player_bets(new_blackjack_game, mocker):
    bet_mock = mocker.patch("blackjack.game.input", side_effect=["100", "200"])
    new_blackjack_game.take_bets()

    assert bet_mock.call_count == 2
    assert new_blackjack_game.players[0].bet == 100
    assert new_blackjack_game.players[1].bet == 200


def test_taking_bets_with_bad_input(new_blackjack_game, mocker):
    bet_mock = mocker.patch("blackjack.game.input", side_effect=["a", "100", "", "200"])
    new_blackjack_game.take_bets()

    assert bet_mock.call_count == 4
    assert new_blackjack_game.players[0].bet == 100
    assert new_blackjack_game.players[1].bet == 200


def test_rejecting_bets_that_are_too_small(new_blackjack_game, mocker):
    bet_mock = mocker.patch(
        "blackjack.game.input", side_effect=["24", "25", "26", "50"]
    )
    new_blackjack_game.take_bets()

    assert bet_mock.call_count == 4
    assert new_blackjack_game.players[0].bet == 25
    assert new_blackjack_game.players[1].bet == 50


def test_rejecting_bets_that_are_too_big(new_blackjack_game, mocker):
    bet_mock = mocker.patch("blackjack.game.input", side_effect=["525", "500", "500"])
    new_blackjack_game.take_bets()

    assert bet_mock.call_count == 3
    assert new_blackjack_game.players[0].bet == 500
    assert new_blackjack_game.players[1].bet == 500
