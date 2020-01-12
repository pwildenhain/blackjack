"""Test running a blackjack game"""
# The test function name is the docstring
# pylint: disable=missing-docstring
# Disable this pylint rule because of a conflict with @pytest.fixture
# See: stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
# pylint: disable=redefined-outer-name
import pytest
from blackjack.game import Blackjack
from tests.test_roles import custom_deck


@pytest.fixture
def new_blackjack_game():
    from terminal_playing_cards import Deck
    from blackjack.roles import Player, Dealer

    return Blackjack(
        deck=Deck(), dealer=Dealer(), players=[Player(bank=500), Player(bank=500)]
    )


@pytest.fixture
def fixed_blackjack_game(new_blackjack_game, custom_deck):
    new_blackjack_game.deck = custom_deck

    return new_blackjack_game


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


def test_cards_are_dealt_to_players(new_blackjack_game):
    new_blackjack_game.deal()
    players_have_two_cards = [
        len(player.hand) == 2 for player in new_blackjack_game.players
    ]
    assert all(players_have_two_cards)


def test_cards_are_dealt_to_dealer(new_blackjack_game):
    new_blackjack_game.deal()
    assert len(new_blackjack_game.dealer.hand) == 2


def test_dealer_second_card_is_hidden(new_blackjack_game):
    new_blackjack_game.deal()
    dealer_hand = new_blackjack_game.dealer.hand

    assert not dealer_hand[0].hidden
    assert dealer_hand[1].hidden


def test_one_player_wins_and_player_loses_bet(fixed_blackjack_game, mocker):
    # Mock out input calls for self.take_bets()
    mocker.patch("blackjack.game.input", side_effect=["100", "200"])
    mocker.patch("blackjack.roles.Player.choose_move", side_effect=["hit", "hit"])
    fixed_blackjack_game.play_round()

    assert fixed_blackjack_game.players[0].bank == 600
    assert fixed_blackjack_game.players[1].bank == 300
    # Assert players deserved to win/lose bets
    assert (
        21 >= fixed_blackjack_game.players[0].total > fixed_blackjack_game.dealer.total
    )
    assert fixed_blackjack_game.players[1].total > 21


def test_players_win_bet_because_dealer_busts(fixed_blackjack_game, mocker):
    mocker.patch("blackjack.game.input", side_effect=["100", "200"])
    mocker.patch("blackjack.roles.Player.choose_move", side_effect=["stay", "stay"])
    fixed_blackjack_game.play_round()

    assert fixed_blackjack_game.players[0].bank == 600
    assert fixed_blackjack_game.players[1].bank == 700
    assert fixed_blackjack_game.dealer.total > 21


def test_dealer_total_beats_player_total(fixed_blackjack_game, mocker):
    mocker.patch("blackjack.game.input", side_effect=["100", "200"])
    mocker.patch("blackjack.roles.Player.choose_move", side_effect=["stay", "stay"])
    # Pop out the next two cards in the deck, because they're designed to make the dealer bust
    for _ in range(2):
        fixed_blackjack_game.deck.pop()
    
    fixed_blackjack_game.play_round()

    assert fixed_blackjack_game.players[0].bank == 400
    assert fixed_blackjack_game.players[1].bank == 300
    assert  21 >= fixed_blackjack_game.dealer.total > fixed_blackjack_game.players[0].total
    assert  21 >= fixed_blackjack_game.dealer.total > fixed_blackjack_game.players[1].total

def test_no_one_wins_blackjack_round(new_blackjack_game, mocker):
    from terminal_playing_cards import Card

    # Ensure that all roles get 21
    custom_cards = [
        Card("A", "clubs", value=1),
        Card("K", "clubs", value=10),
        Card("A", "clubs", value=1),
        Card("K", "clubs", value=10),
        Card("A", "clubs", value=1),
        Card("K", "clubs", value=10),
    ]

    new_blackjack_game.deck = custom_cards
    mocker.patch("blackjack.game.input", side_effect=["100", "200"])
    new_blackjack_game.play_round()

    assert new_blackjack_game.players[0].bank == 500
    assert new_blackjack_game.players[1].bank == 500
