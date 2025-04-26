import random

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
WILD_CARDS = ['Wild', '+4']

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    
    def __str__(self):
        return f"{self.color} {self.value}"
    
    def __lt__(self, other):
        if self.color != other.color:
            return self.color < other.color
        return self.value < other.value
    
    def matches(self, other_card):
        # Check if card matches with the top card
        if self.is_wild() or self.is_plus_four():
            return True  # Wild cards can be played on any card
        return self.color == other_card.color or self.value == other_card.value

    def is_skip(self):
        return self.value == "Skip"

    def is_reverse(self):
        return self.value == "Reverse"
    
    def is_plus_two(self):
        return self.value == "+2"
    
    def is_plus_four(self):
        return self.value == "+4"
    
    def is_wild(self):
        return self.value == "Wild"
    
    def is_special(self):
        return self.is_skip() or self.is_reverse() or self.is_plus_two() or self.is_wild() or self.is_plus_four()

def generate_deck():
    deck = []
    
    # Add regular cards
    for color in COLORS:
        # Add one '0' card for each color
        deck.append(Card(color, '0'))
        
        # Add two of each other number and special cards
        for value in VALUES[1:]:  # Skip '0' since we've already added it
            deck.append(Card(color, value))
            deck.append(Card(color, value))
    
    # Add wild cards
    for _ in range(4):
        deck.append(Card("Wild", "Wild"))
        deck.append(Card("Wild", "+4"))
    
    random.shuffle(deck)
    return deck