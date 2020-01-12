"""Play blackjack in the terminal"""

from terminal_playing_cards import Deck
from blackjack.game import Blackjack
from blackjack.roles import Dealer, Player

print("*Starting Game*")

while True:
    try:
        num_players = int(input("Number of players: "))
        break
    except ValueError:
        print("Numbers only please :-)")

PLAYER_LIST = []
for player_num in range(num_players):
    name = input("Player name: ")
    while True:
        try:
            bank = int(input(f"Starting bank roll for {name}: "))
            if bank % 25 != 0:
                print("Bank roll must be in increments of $25")
                continue
            break
        except ValueError:
            print("Numbers only please :-)")
    PLAYER_LIST.append(Player(name=name, bank=bank))

BIG_DECK = Deck(specifications=["face_cards_are_ten"])
for _ in range(5):
    BIG_DECK += Deck(specifications=["face_cards_are_ten"])

BIG_DECK.shuffle()

BLACKJACK_GAME = Blackjack(deck=BIG_DECK, dealer=Dealer(), players=PLAYER_LIST)

BLACKJACK_GAME.play_game()
