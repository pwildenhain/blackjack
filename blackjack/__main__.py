"""Play blackjack in the terminal"""

from terminal_playing_cards import Deck, View
from blackjack.roles import Role

print("*Starting Game*")

DECK = Deck(specifications=["face_cards_are_ten"])
DECK.shuffle()

EX_PLAYER = Role(hand=View([DECK.pop() for _ in range(2)]))

while EX_PLAYER.total < 21:
    print(EX_PLAYER.hand)
    print(f"The hand total is {EX_PLAYER.total}")
    EX_PLAYER.hit(card=DECK.pop())
    print("*Hit Me!*")

print(f"Final hand of {EX_PLAYER.total} is:")

print(EX_PLAYER.hand)
