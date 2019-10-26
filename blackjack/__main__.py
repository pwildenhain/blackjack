"""Play blackjack in the terminal"""

from terminal_playing_cards import Deck, View
from blackjack.game import Blackjack
from blackjack.roles import Dealer, Player

print("*Starting Game*")

DECK = Deck(specifications=["face_cards_are_ten"])
DECK.shuffle()

BLACKJACK_GAME = Blackjack(
    deck=DECK, dealer=Dealer(), players=[Player(bank=500)]
)

BLACKJACK_GAME.take_bets()

BLACKJACK_GAME.deal()

print("Dealer has:")
print(BLACKJACK_GAME.dealer.hand)
print("Player has:")
print(BLACKJACK_GAME.players[0].hand)
for role in [BLACKJACK_GAME.players[0], BLACKJACK_GAME.dealer]:
    role_name = role.__class__.__name__
    print(f"Begin {role_name}'s turn")
    role.play(deck=DECK)
    print(f"{role_name} final hand:")
    print(role.hand)

if BLACKJACK_GAME.players[0].total > 21:
    WINNER = "dealer"
elif BLACKJACK_GAME.dealer.total > 21:
    WINNER = "player"
elif BLACKJACK_GAME.dealer.total > BLACKJACK_GAME.players[0].total:
    WINNER = "dealer"
elif BLACKJACK_GAME.players[0].total > BLACKJACK_GAME.dealer.total:
    WINNER = "player"
else:
    WINNER = "no one"

print(f"{WINNER.title()} won ${BLACKJACK_GAME.players[0].bet}")
