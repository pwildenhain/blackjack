from colorama import init, Fore, Back

# Reset foreground and background when done
init(autoreset=True)

label = 2
suit_small = "\u2666"
suit_big = "\u25C6"
style = Back.WHITE + Fore.RED
first_layer = f"{label}{' ' * 2}{suit_big}{' ' * 4}"
second_layer = f"{suit_small}{' ' * 7}"
third_layer = " " * 8
fourth_layer = f"{' ' * 7}{suit_small}"
fifth_layer = f"{' ' * 3}{suit_big}{' ' * 3}{label}"

# think about each space of the card as a position (instead of in layers)
# and then the suit goes in it's corresponding position
# for a given label - a dict could accomplish this
# probably belongs in some config file

# Nested list data structure?
# Example coordinates for a two
# 1st layer, 3rd spot and 5th layer, 3rd spot
# the suit coordinate would be the dict, key = label, value = coordinates
suit_coordinates = [(0, 3), (4, 3)]
# positions might be most intuitive as coordinates
card_map = [
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
]
# could be accessed like this
for layer, position in suit_coordinates:
    card_map[layer][position] = suit_big


# boolean attribute for whether or not it's face up
# optional attribute for symbol -- used for J, Q, K -- will go in the center

card = f"{first_layer}\n{second_layer}\n{third_layer}\n{fourth_layer}\n{fifth_layer}"

print(style + card)
