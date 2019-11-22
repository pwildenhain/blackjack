"""The master class for playing blackjack. All class attributes are required because the
`setup_game()` utility function will always return a Blackjack object with all specified
parameters.
"""

from typing import List
from terminal_playing_cards import Deck, View
from blackjack.roles import Dealer, Player


class Blackjack:
    """Run a blackjack game.

    Attributes:
        deck: Deck of playing cards for blackjack.
        dealer: Dealer for blackjack game.
        players: List of Players in blackjack game.
        bet_checks (dict):
            Dict of quality checks that are performed each
            time a player places a bet on a round of blackjack.
    """

    def __init__(self, deck: Deck, dealer: Dealer, players: List[Player]):
        """Setup a blackjack game"""
        self.deck = deck
        self.dealer = dealer
        self.players = players
        self.bet_checks = {
            "correct_increment": {
                "pass": None,
                "message": "Bets must be placed in increments of $25",
            },
            "minimum_bet_met": {"pass": None, "message": "The minimum bet is $25"},
            "bet_less_than_bank": {
                "pass": None,
                "message": "Bets cannot be more than available funds",
            },
        }

    def take_bets(self):
        """Take the bets of each player before a round of blackjack.
        Perform quality checks on the player bets before storing them.
        """
        for player in self.players:
            # Start with clean slate of checks each time bets are taken
            bet_checks = self.bet_checks.copy()
            while True:
                try:
                    user_bet = int(input("Place bet: "))
                except ValueError:
                    print("Numbers only please :-)")
                    continue

                bet_checks["correct_increment"]["pass"] = user_bet % 25 == 0
                bet_checks["minimum_bet_met"]["pass"] = user_bet >= 25
                bet_checks["bet_less_than_bank"]["pass"] = user_bet <= player.bank

                bet_check_messages = [
                    bet_checks[check].get("message")
                    for check in bet_checks.keys()
                    if not bet_checks[check].get("pass")
                ]

                if len(bet_check_messages) > 0:
                    print("Your bet had the following issue(s):")
                    for message in bet_check_messages:
                        print(f"* {message}")
                    print("Please try again.")
                else:
                    break

            player.bet = user_bet

    def deal(self):
        """Deal cards for a blackjack round. Hide the Dealer's second card"""
        for role in self.players + [self.dealer]:
            role.hand = View([self.deck.pop() for _ in range(2)])
        self.dealer.hand[1].hidden = True

    def play_round(self):
        self.take_bets()
        self.deal()

        for role in self.players + [self.dealer]:
            role_name = role.__class__.__name__
            print(f"{role_name}'s hand:")
            print(role.hand)

        for role in self.players + [self.dealer]:
            role_name = role.__class__.__name__
            print(f"Begin {role_name}'s turn")
            role.play(deck=self.deck)
            print(f"{role_name} final hand:")
            print(role.hand)

        for player in self.players:
            if player.total > 21:
                player.bank -= player.bet
            elif self.dealer.total > 21:
                player.bank += player.bet
            elif player.total < self.dealer.total:
                player.bank -= player.bet
            elif player.total > self.dealer.total:
                player.bank += player.bet
