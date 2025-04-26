import heapq
import random
from collections import Counter

def a_star_search(hand, top_card, current_color):
    
    frontier = []
    explored = set()
    
    initial_state = (calculate_hand_cost(hand), tuple(hand), [], current_color)
    heapq.heappush(frontier, initial_state)
    
    while frontier and len(frontier) < 100:  
        cost, current_hand, path, current_active_color = heapq.heappop(frontier)
        
        hand_key = tuple((card.color, card.value) for card in current_hand)
        if hand_key in explored:
            continue
        
        explored.add(hand_key)
        
        if not current_hand or (path and len(current_hand) <= len(hand) - 3):
            return path[0] if path else None
        
        playable_cards = [card for card in current_hand 
                         if card.color == current_active_color or 
                            card.value == top_card.value or 
                            card.is_wild() or 
                            card.is_plus_four()]
        
        if not playable_cards and not path:
            return None
        
        if playable_cards and path:
            return path[0]
        
        for card in playable_cards:
            new_hand = list(current_hand)
            new_hand.remove(card)
            
            new_color = current_active_color
            if card.is_wild() or card.is_plus_four():
                new_color = choose_color(new_hand)
            elif card.color != "Wild":
                new_color = card.color
            
            new_cost = calculate_hand_cost(new_hand)
            
            if card.is_special():
                new_cost -= 2
            
            new_path = path + [card]
            heapq.heappush(frontier, (new_cost, tuple(new_hand), new_path, new_color))
    
    return path[0] if path else None

def calculate_hand_cost(hand):
    """Calculate the cost of a hand state (lower is better)."""
    if not hand:
        return -1000
    
    cost = len(hand) * 10
    special_cards = sum(1 for card in hand if card.is_special())
    cost -= special_cards * 5
    
    wild_cards = sum(1 for card in hand if card.is_wild() or card.is_plus_four())
    cost += wild_cards * 3
    
    colors = set(card.color for card in hand if card.color != "Wild")
    cost -= len(colors) * 2
    
    return cost

def expectimax(hand, top_card, current_color, depth=2):
    
    playable_cards = [card for card in hand 
                     if card.color == current_color or 
                        card.value == top_card.value or 
                        card.is_wild() or 
                        card.is_plus_four()]
    
    if not playable_cards:
        return None
    
    best_card = None
    best_value = float('-inf')
    
    for card in playable_cards:
        new_hand = list(hand)
        new_hand.remove(card)
        
        value = expectimax_value(new_hand, card, top_card, current_color, depth, True)
        
        if value > best_value:
            best_value = value
            best_card = card
    
    return best_card

def expectimax_value(hand, played_card, top_card, current_color, depth, is_chance_node):
    """Recursive function to calculate expectimax value."""
    if depth == 0 or not hand:
        return evaluate_hand(hand)
    
    new_color = current_color
    if played_card.is_wild() or played_card.is_plus_four():
        new_color = choose_color(hand)
    elif played_card.color != "Wild":
        new_color = played_card.color
    
    if is_chance_node:
        value = 0
        
        value += 0.7 * expectimax_value(hand, played_card, played_card, new_color, depth-1, False)
        
        value += 0.2 * (evaluate_hand(hand) - 10)
        
        value += 0.1 * expectimax_value(hand, played_card, played_card, new_color, depth-1, False)
        
        return value
    
    else:
        playable_cards = [card for card in hand 
                         if card.color == new_color or 
                            card.value == played_card.value or 
                            card.is_wild() or 
                            card.is_plus_four()]
        
        if not playable_cards:
            return evaluate_hand(hand) - 5
        
        best_value = float('-inf')
        for card in playable_cards:
            new_hand = list(hand)
            new_hand.remove(card)
            value = expectimax_value(new_hand, card, played_card, new_color, depth-1, True)
            best_value = max(best_value, value)
        
        return best_value

def evaluate_hand(hand):
    """Evaluate the quality of a hand (higher is better)."""
    if not hand:
        return 1000
    
    score = 0
    
    score -= len(hand) * 10
    
    score += sum(5 for card in hand if card.is_special())
    
    colors = set(card.color for card in hand if card.color != "Wild")
    score += len(colors) * 3
    
    score += sum(8 for card in hand if card.is_wild() or card.is_plus_four())
    
    return score

def get_best_move(hand, top_card, current_color=None):
    
    if current_color is None:
        current_color = top_card.color
    
    playable_cards = [card for card in hand 
                     if card.color == current_color or 
                        card.value == top_card.value or 
                        card.is_wild() or 
                        card.is_plus_four()]
    
    if not playable_cards:
        return None
    
    a_star_result = a_star_search(hand, top_card, current_color)
    expectimax_result = expectimax(hand, top_card, current_color)
    
    
    if not a_star_result:
        return expectimax_result
    if not expectimax_result:
        return a_star_result
    
    if len(hand) <= 3:
        
        return a_star_result
    elif any(card.is_special() for card in [a_star_result, expectimax_result]):
        
        return expectimax_result if expectimax_result.is_special() else a_star_result
    else:
        
        return random.choices([a_star_result, expectimax_result], weights=[0.4, 0.6])[0]

def choose_color(hand):
    
    color_counts = Counter(card.color for card in hand if card.color != "Wild")
    
    if not color_counts:
        
        return random.choice(["Red", "Green", "Blue", "Yellow"])
    
    return color_counts.most_common(1)[0][0]