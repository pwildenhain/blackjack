"""Play blackjack in the terminal"""

from terminal_playing_cards import Deck, View
from blackjack.roles import Dealer, Player

print("*Starting Game*")

DECK = Deck(specifications=["face_cards_are_ten"])
DECK.shuffle()

DEALER = Dealer(hand=View([DECK.pop() for _ in range(2)]))
DEALER.hand[0].hidden = True
PLAYER = Player(hand=View([DECK.pop() for _ in range(2)]))
print("Dealer has:")
print(DEALER.hand)
print("Player has:")
print(PLAYER.hand)
for role in [PLAYER, DEALER]:
    role_name = role.__class__.__name__
    print(f"Begin {role_name}'s turn")
    role.play(deck=DECK)
    print(f"{role_name} final hand:")
    print(role.hand)

if PLAYER.total > 21:
    WINNER = "dealer"
elif DEALER.total > 21:
    WINNER = "player"
elif DEALER.total > PLAYER.total:
    WINNER = "dealer"
elif PLAYER.total > DEALER.total:
    WINNER = "player"
else:
    WINNER = "no one"

print(f"{WINNER.title()} is the winner")
