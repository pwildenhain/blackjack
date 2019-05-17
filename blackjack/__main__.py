from blackjack import cards, cards_config

suits = cards_config.SUIT_SYMBOL_DICT.keys()
# faces = card_config.CARD_FACE_DICT.keys()
faces = ["2"]
# Going to need a hand_grid variable for printing out the entire hand
full_deck = [(face, suit) for face in faces for suit in suits]

if __name__ == "__main__":
    for face, suit in full_deck:
        print(cards.Card(face, suit))
