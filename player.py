class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        """Draw a card from the deck and add it to the player's hand."""
        if deck:
            self.hand.append(deck.pop())
            return True
        return False

    def has_playable_card(self, top_card):
        """Check if player has a playable card."""
        return any(card.matches(top_card) for card in self.hand)
    
    def get_playable_cards(self, top_card):
        """Return a list of playable cards."""
        return [card for card in self.hand if card.matches(top_card)]
    
    def play_card(self, card_index):
        """Play a card from player's hand by index."""
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None