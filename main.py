import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

from card import Card, generate_deck
from player import Player
from ai import get_best_move, choose_color

class UNOGame:
    def __init__(self, root):
        self.root = root
        self.root.title("UNO Game")
        self.root.geometry("1920x1800")
        self.root.configure(bg="#2E8B57")
        self.root.resizable(True, True)
        
        self.reset_game()
        
        self.create_widgets()
        
        self.update_ui()

    def reset_game(self):
        self.deck = generate_deck()
        self.discard_pile = []
        self.player = Player("Human")
        self.bot = Player("Bot")
        
        for _ in range(7):
            self.player.draw_card(self.deck)
            self.bot.draw_card(self.deck)
        
        self.top_card = self.deck.pop()
        while self.top_card.is_wild() or self.top_card.is_plus_four():
            self.discard_pile.append(self.top_card)
            self.top_card = self.deck.pop()
        
        self.discard_pile.append(self.top_card)
        self.current_color = self.top_card.color
        self.turn = 0
        self.game_over = False
        self.waiting_for_color_choice = False

    def create_widgets(self):
        self.info_frame = tk.Frame(self.root, bg="#2E8B57")
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.bot_label = tk.Label(self.info_frame, text="Bot's Cards: 7", font=("Arial", 14), bg="#2E8B57", fg="white")
        self.bot_label.pack(side=tk.LEFT, padx=10)
        
        self.turn_label = tk.Label(self.info_frame, text="Your Turn", font=("Arial", 18, "bold"), bg="#2E8B57", fg="white")
        self.turn_label.pack(side=tk.LEFT, expand=True)
        
        self.deck_label = tk.Label(self.info_frame, text=f"Deck: {len(self.deck)}", font=("Arial", 14), bg="#2E8B57", fg="white")
        self.deck_label.pack(side=tk.RIGHT, padx=10)
        
        self.middle_frame = tk.Frame(self.root, bg="#2E8B57")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.discard_frame = tk.Frame(self.middle_frame, bg="#2E8B57")
        self.discard_frame.pack(pady=20)
        
        self.top_card_label = tk.Label(self.discard_frame, text="", font=("Arial", 16), width=15, height=8, 
                                      relief=tk.RAISED, bg="white")
        self.top_card_label.pack()
        
        color_frame = tk.Frame(self.discard_frame, bg="#2E8B57")
        color_frame.pack(pady=5)
        
        tk.Label(color_frame, text="Current Color:", font=("Arial", 14, "bold"), bg="#2E8B57", fg="white").pack(side=tk.LEFT)
        
        self.color_indicator = tk.Label(color_frame, text="Red", font=("Arial", 14), width=8, height=2, relief=tk.RAISED)
        self.color_indicator.pack(side=tk.LEFT, padx=10)
        
        self.message_label = tk.Label(self.middle_frame, text="", font=("Arial", 14), bg="#2E8B57", fg="white", wraplength=500)
        self.message_label.pack(pady=10)
        
        self.draw_button = tk.Button(self.middle_frame, text="Draw Card", font=("Arial", 14), 
                                    bg="#4CAF50", fg="white", command=self.draw_card)
        self.draw_button.pack(pady=10)
        
        self.uno_button = tk.Button(self.middle_frame, text="Say UNO!", font=("Arial", 14), 
                                   bg="#FF5722", fg="white", command=self.say_uno)
        self.uno_button.pack(pady=5)
        
        self.hand_frame = tk.Frame(self.root, bg="#2E8B57")
        self.hand_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.new_game_button = tk.Button(self.root, text="New Game", font=("Arial", 14), 
                                        bg="#2196F3", fg="white", command=self.new_game)
        self.new_game_button.pack(pady=10)
        
        self.color_selection_frame = tk.Frame(self.root, bg="#2E8B57")
        self.color_buttons = []
        
        for color in ["Red", "Green", "Blue", "Yellow"]:
            bg_color = {"Red": "#FF0000", "Green": "#00FF00", 
                      "Blue": "#0000FF", "Yellow": "#FFFF00"}[color]
            
            text_color = "black" if color in ["Green", "Yellow"] else "white"
            
            button = tk.Button(self.color_selection_frame, text=color, font=("Arial", 14),
                              bg=bg_color, fg=text_color, width=10, height=2,
                              command=lambda c=color: self.select_color(c))
            button.pack(side=tk.LEFT, padx=5)
            self.color_buttons.append(button)

    def format_card_text(self, card):
        if card.color == "Wild":
            return f"{card.value}"
        return f"{card.color}\n{card.value}"

    def get_card_color(self, card):
        color_map = {
            "Red": "#FF6B6B",
            "Green": "#77DD77",
            "Blue": "#779ECB",
            "Yellow": "#FDFD96",
            "Wild": "#D3D3D3"
        }
        return color_map.get(card.color, "#FFFFFF")

    def get_text_color(self, card):
        if card.color in ["Yellow", "Green"]:
            return "black"
        return "white"

    def is_card_playable(self, card):
        if card.is_wild() or card.is_plus_four():
            return True
            
        if card.color == self.current_color:
            return True
            
        if card.value == self.top_card.value:
            return True
            
        return False

    def update_ui(self):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        
        card_text = self.format_card_text(self.top_card)
        self.top_card_label.config(text=card_text, bg=self.get_card_color(self.top_card), 
                                  fg=self.get_text_color(self.top_card))
        
        color_map = {
            "Red": "#FF6B6B",
            "Green": "#77DD77",
            "Blue": "#779ECB",
            "Yellow": "#FDFD96"
        }
        self.color_indicator.config(text=self.current_color, bg=color_map.get(self.current_color, "#FFFFFF"),
                                   fg="black" if self.current_color in ["Yellow", "Green"] else "white")
        
        self.bot_label.config(text=f"Bot's Cards: {len(self.bot.hand)}")
        self.deck_label.config(text=f"Deck: {len(self.deck)}")
        self.turn_label.config(text=f"{'Your Turn' if self.turn == 0 else 'Bot\'s Turn'}")
        
        for idx, card in enumerate(self.player.hand):
            card_button = tk.Button(self.hand_frame, text=self.format_card_text(card), 
                                   font=("Arial", 12), width=8, height=4,
                                   bg=self.get_card_color(card), fg=self.get_text_color(card),
                                   command=lambda idx=idx: self.play_card(idx))
            
            if not self.is_card_playable(card) or self.turn != 0 or self.waiting_for_color_choice:
                card_button.config(state=tk.DISABLED)
                
            card_button.pack(side=tk.LEFT, padx=5)
        
        if self.waiting_for_color_choice:
            self.color_selection_frame.pack(pady=10)
            self.draw_button.config(state=tk.DISABLED)
        else:
            self.color_selection_frame.pack_forget()
            self.draw_button.config(state=tk.NORMAL if self.turn == 0 and not self.game_over else tk.DISABLED)
        
        self.uno_button.config(state=tk.NORMAL if len(self.player.hand) == 2 and self.turn == 0 else tk.DISABLED)

    def draw_card(self):
        if self.turn != 0 or self.game_over or self.waiting_for_color_choice:
            return
        
        if not self.deck:
            self.reshuffle_discard_pile()
            if not self.deck:
                messagebox.showinfo("Game Info", "No cards left in the deck. The game is a draw.")
                self.game_over = True
                return
        
        self.player.draw_card(self.deck)
        self.message_label.config(text="You drew a card.")
        
        drawn_card = self.player.hand[-1]
        if self.is_card_playable(drawn_card):
            self.update_ui()
        else:
            self.turn = 1
            self.update_ui()
            self.root.after(1000, self.bot_turn)

    def play_card(self, card_idx):
        if self.turn != 0 or self.game_over or self.waiting_for_color_choice:
            return
        
        chosen_card = self.player.hand[card_idx]
        
        if not self.is_card_playable(chosen_card):
            self.message_label.config(text="You cannot play that card.")
            return
        
        self.player.play_card(card_idx)
        self.discard_pile.append(self.top_card)
        self.top_card = chosen_card
        
        if chosen_card.is_wild() or chosen_card.is_plus_four():
            self.waiting_for_color_choice = True
            self.message_label.config(text="Choose a color:")
            self.update_ui()
            return
        
        self.current_color = chosen_card.color
        self.message_label.config(text=f"You played {chosen_card}")
        
        if not self.player.hand:
            messagebox.showinfo("Game Over", "You win!")
            self.game_over = True
            return
        
        if chosen_card.is_skip():
            self.message_label.config(text="Skip card played! Bot's turn is skipped.")
            self.turn = 0
        elif chosen_card.is_reverse():
            self.message_label.config(text="Reverse card played! (No effect in 2-player game)")
            self.turn = 0
        elif chosen_card.is_plus_two():
            self.message_label.config(text="+2 card played! Bot draws two cards.")
            for _ in range(2):
                if not self.deck:
                    self.reshuffle_discard_pile()
                    if not self.deck:
                        break
                self.bot.draw_card(self.deck)
            self.turn = 0
        else:
            self.turn = 1
        
        self.update_ui()
        
        if self.turn == 1:
            self.root.after(1000, self.bot_turn)

    def select_color(self, color):
        self.current_color = color
        self.waiting_for_color_choice = False
        
        self.message_label.config(text=f"You chose {color} color.")
        
        if self.top_card.is_plus_four():
            self.message_label.config(text=f"Wild +4 played! Bot draws four cards.")
            for _ in range(4):
                if not self.deck:
                    self.reshuffle_discard_pile()
                    if not self.deck:
                        break
                self.bot.draw_card(self.deck)
        
        self.turn = 1
        self.update_ui()
        
        self.root.after(1000, self.bot_turn)

    def bot_turn(self):
        if self.turn != 1 or self.game_over:
            return
        
        card_to_play = get_best_move(self.bot.hand, self.top_card, self.current_color)
        
        if card_to_play:
            self.bot.hand.remove(card_to_play)
            self.discard_pile.append(self.top_card)
            self.top_card = card_to_play
            
            if card_to_play.is_wild() or card_to_play.is_plus_four():
                chosen_color = choose_color(self.bot.hand)
                self.current_color = chosen_color
                self.message_label.config(text=f"Bot played {card_to_play} and chose {chosen_color} color.")
                
                if card_to_play.is_plus_four():
                    self.message_label.config(text=f"Bot played Wild +4 and chose {chosen_color}! You draw four cards.")
                    for _ in range(4):
                        if not self.deck:
                            self.reshuffle_discard_pile()
                            if not self.deck:
                                break
                        self.player.draw_card(self.deck)
            else:
                self.current_color = card_to_play.color
                self.message_label.config(text=f"Bot played {card_to_play}")
            
            if not self.bot.hand:
                messagebox.showinfo("Game Over", "Bot wins!")
                self.game_over = True
                self.update_ui()
                return
            
            if card_to_play.is_skip():
                self.message_label.config(text="Bot played Skip! Your turn is skipped.")
                self.turn = 1
                self.update_ui()
                self.root.after(1000, self.bot_turn)
                return
            elif card_to_play.is_reverse():
                self.message_label.config(text="Bot played Reverse! (No effect in 2-player game)")
                self.turn = 1
                self.update_ui()
                self.root.after(1000, self.bot_turn)
                return
            elif card_to_play.is_plus_two():
                self.message_label.config(text="Bot played +2! You draw two cards.")
                for _ in range(2):
                    if not self.deck:
                        self.reshuffle_discard_pile()
                        if not self.deck:
                            break
                    self.player.draw_card(self.deck)
                self.turn = 1
                self.update_ui()
                self.root.after(1000, self.bot_turn)
                return
            else:
                self.turn = 0
        else:
            if not self.deck:
                self.reshuffle_discard_pile()
                if not self.deck:
                    messagebox.showinfo("Game Info", "No cards left in the deck. The game is a draw.")
                    self.game_over = True
                    self.update_ui()
                    return
            
            self.bot.draw_card(self.deck)
            self.message_label.config(text="Bot drew a card.")
            
            drawn_card = self.bot.hand[-1]
            if self.is_card_playable(drawn_card):
                self.update_ui()
                self.root.after(1000, lambda: self.bot_play_after_draw(drawn_card))
                return
            
            self.turn = 0
        
        self.update_ui()

    def is_card_playable(self, card):
        if card.is_wild() or card.is_plus_four():
            return True
            
        if card.color == self.current_color:
            return True
            
        if card.value == self.top_card.value:
            return True
            
        return False

    def bot_play_after_draw(self, card):
        if self.game_over:
            return
            
        self.bot.hand.remove(card)
        self.discard_pile.append(self.top_card)
        self.top_card = card
        
        if card.is_wild() or card.is_plus_four():
            chosen_color = choose_color(self.bot.hand)
            self.current_color = chosen_color
            self.message_label.config(text=f"Bot played {card} after drawing and chose {chosen_color} color.")
            
            if card.is_plus_four():
                self.message_label.config(text=f"Bot played Wild +4 after drawing and chose {chosen_color}! You draw four cards.")
                for _ in range(4):
                    if not self.deck:
                        self.reshuffle_discard_pile()
                        if not self.deck:
                            break
                    self.player.draw_card(self.deck)
        else:
            self.current_color = card.color
            self.message_label.config(text=f"Bot played {card} after drawing.")
        
        if not self.bot.hand:
            messagebox.showinfo("Game Over", "Bot wins!")
            self.game_over = True
            self.update_ui()
            return
        
        if card.is_skip():
            self.message_label.config(text="Bot played Skip after drawing! Your turn is skipped.")
            self.turn = 1
            self.update_ui()
            self.root.after(1000, self.bot_turn)
            return
        elif card.is_reverse():
            self.message_label.config(text="Bot played Reverse after drawing! (No effect in 2-player game)")
            self.turn = 1
            self.update_ui()
            self.root.after(1000, self.bot_turn)
            return
        elif card.is_plus_two():
            self.message_label.config(text="Bot played +2 after drawing! You draw two cards.")
            for _ in range(2):
                if not self.deck:
                    self.reshuffle_discard_pile()
                    if not self.deck:
                        break
                self.player.draw_card(self.deck)
            self.turn = 1
            self.update_ui()
            self.root.after(1000, self.bot_turn)
            return
        else:
            self.turn = 0
        
        self.update_ui()

    def reshuffle_discard_pile(self):
        if not self.discard_pile:
            return
            
        top_card = self.discard_pile.pop()
        
        self.deck = self.discard_pile
        random.shuffle(self.deck)
        self.discard_pile = [top_card]
        
        self.message_label.config(text="Deck was empty. Reshuffled discard pile.")

    def say_uno(self):
        if len(self.player.hand) == 2 and self.turn == 0:
            self.message_label.config(text="You said UNO!")
            
        else:
            self.message_label.config(text="You can only say UNO when you have 2 cards left!")

    def new_game(self):
        self.reset_game()
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    game = UNOGame(root)
    root.mainloop()