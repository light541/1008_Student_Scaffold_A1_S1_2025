from __future__ import annotations
from player import Player
from game_board import GameBoard
from card import CardColor, CardLabel, Card
from random_gen import RandomGen
from config import Config
from data_structures import *


class Game:
    """
    Game class to play the game
    """

    def __init__(self) -> None:
        """
        Constructor for the Game class

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        
        Justification:
            Both Best and worse Case is the same because i am just
            initializing the variables with none and creating an empty
            arraylist.

        """
        self.players = ArrayList()
        self.current_color = None
        self.current_label = None
        self.current_player = None
        self.game_board = None

    def generate_cards(self) -> ArrayList[Card]:
        """
        Method to generate the cards for the game

        Args:
            None

        Returns:
            ArrayList[Card]: The list of Card objects generated
        """
        list_of_cards: ArrayList[Card] = ArrayList(Config.DECK_SIZE)
        idx: int = 0

        # Generate 4 sets of cards from 0 to 9 for each color
        for color in CardColor:
            if color != CardColor.BLACK:
                # Generate 4 sets of cards from 0 to 9 for each color
                for i in range(10):
                    list_of_cards.insert(idx, Card(color, CardLabel(i)))
                    idx += 1
                    list_of_cards.insert(idx, Card(color, CardLabel(i)))
                    idx += 1

                # Generate 2 of each special card for each color
                for i in range(2):
                    list_of_cards.insert(idx, Card(color, CardLabel.SKIP))
                    idx += 1
                    list_of_cards.insert(idx, Card(color, CardLabel.REVERSE))
                    idx += 1
                    list_of_cards.insert(idx, Card(color, CardLabel.DRAW_TWO))
                    idx += 1
            else:
                # Generate black crazy and draw 4 cards
                for i in range(4):
                    list_of_cards.insert(idx, Card(CardColor.BLACK, CardLabel.CRAZY))
                    idx += 1
                    list_of_cards.insert(
                        idx, Card(CardColor.BLACK, CardLabel.DRAW_FOUR)
                    )
                    idx += 1

                # Randomly shuffle the cards
                RandomGen.random_shuffle(list_of_cards)

                return list_of_cards

    def initialise_game(self, players: ArrayList[Player]) -> None:
        """
        Method to initialise the game

        Args:
            players (ArrayList[Player]): The list of players
            
        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.players = players
        card = self.generate_cards()
        self.game_board = GameBoard(card)

        for _ in range(Config.NUM_CARDS_AT_INIT):
            for j in self.players:
                cards = self.game_board.draw_card()
                j.add_card(cards)
        
        check = True 
        while check:
            card = self.game_board.draw_card()
            if CardLabel.ZERO <= card.label <= CardLabel.NINE:
                self.current_color = card.color
                self.current_label = card.label 
                
                check = False

            


    def next_player(self) -> Player:
        """
        Method to get the next player

        Args:
            None

        Returns:
            Player: The next player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N) where N =len(self.players)
        
        Justification:
            Best case: When current_player is none, we just 
                       return the first players. This is constant 
                       time.
            
            Worst Case: This happens when current player is the last player in the list 
                        or not even in the list. So it has to iterate through all n players
                        before finding a match, this makes the complexity O(N). Futhermore, the index() method in
                        ArrayList contribute to the O(N).
        """
        
        if self.current_player is None:
            return self.players[0]
        else:
            #gets the index of the next player and it handles wrapping(when index is at the end of the list)
            player_index = (self.players.index(self.current_player) + 1) % len(self.players)
        
        return self.players[player_index]

            

    def reverse_players(self) -> None:
        """
        Method to reverse the order of the players

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N) where N = len(self.players)
            Worst Case Complexity: O(N) where N = len(self.players)
        
        Justification: 
            Both Best case and Worst case is the same. This is because,
            the method needs to perform N/2 swaps to reverse the list. Since 
            each swap takes constant time O(1), the total time becomes O(N/2).
            This is then simplified to O(N). 
        """
        
        start, end = 0, len(self.players) - 1

        # swap players 
        while start < end:
            self.players[start],self.players[end] = self.players[end], self.players[start]
            start += 1
            end -= 1


    def skip_next_player(self) -> None:
        """
        Method to skip the next player in the game

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity:O(1)
            Worst Case Complexity:O(N) where N = len(self.players)
        
        Justification:
            Best Case:This happends when current_player is None so the method directly
                      assigns first player. This is a constant time, because it just 
                      returns the first player 
            
            Worse Case: This happens when current player is not none. Hence, it calls
                        the next_player twice. Next player uses .index(self.current_player) method, it have to 
                        search through all n players to find the current one, this makes each 
                        call O(N).

        """
        if self.current_player is None:
            self.current_player = self.players[0]
            return 
        self.current_player = self.next_player()
        self.current_player = self.next_player()
        

    def play_draw_two(self) -> None:
        """
        Method to play a draw two card

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity:O(1)
            Worst Case Complexity:O(N + H + P) where N = number of cards in drawpile, H= Number of cards in player's hand, P=number of players
        
        Justification:
            Best case: This happens when next_players returns the first player.
                       The drawn cards are inserted at the end of the hand and
                       skip_next_player assigns to the first player. All this operation
                       will result in a constant time.
            
            Worst Case: This happens 
        """
        next_player = self.next_player()

        for _ in range(2):
            cards = self.game_board.draw_card()
            next_player.add_card(cards)
        self.skip_next_player()

        
    def play_black(self, card: Card) -> None:
        """
        Method to play a crazy card

        Args:
            card (Card): The card to be played

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N)
        """
        self.current_color = CardColor(RandomGen.randint(0,3))
        next_player = self.next_player()
        if card.label == CardLabel.DRAW_FOUR:
            
            for _ in range(4):
                cards = self.game_board.draw_card()
                next_player.add_card(cards)
            
            self.skip_next_player()

    def draw_card(self, player: Player, playing: bool) -> Card | None:
        """
        Method to draw a card from the deck

        Args:
            player (Player): The player who is drawing the card
            playing (bool): A boolean indicating if the player is able to play the card

        Returns:
            Card - When drawing a playable card, other return None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N + H) where N=Number of cards in draw pile , H = number of cards in the player's hand

        Justification:
            Best case: This happens when the drawn card is playable and it returns right
                        away. This requires draw operation and a comparison which is O(N).

            Worst case: This happens when card cannot be played and must be added to player's
                        hand. Drawing the card takes up O(N) because it requires shifting all
                        the the remaining cards. Then adding cards into a sorted hand requires shifting 
                        up to h cards, which would give O(H). Hence, O(N + H)

        """
        card = self.game_board.draw_card()

        if playing and (card.color == self.current_color or card.label == self.current_label):
            return card 
        else:
            player.hand.add(card)
            return None


    def play_game(self) -> Player:
        """
        Method to play the game

        Args:
            None

        Returns:
            Player: The winner of the game
        """

        if self.current_player is None:
            self.current_player = self.next_player()
        
        while True:
            #plays the card in the current players hand
            play_card = self.current_player.play_card(self.current_color,self.current_label)
            
            if play_card is not None:
                #card satisfy the condition to be played 
                self.game_board.discard_card(play_card)
            
                # update the current color randomly, when the play_card is black
                if play_card.color == CardColor.BLACK:
                    self.current_color = CardColor(RandomGen.randint(0,3))
                    self.current_label = play_card.label
                else:
                    # update the current color and current label based on the card played if its not black
                    self.current_color = play_card.color 
                    self.current_label = play_card.label
                
                # check if the players hand is empty and won
                if self.current_player.is_empty():
                    return self.current_player
                
                #handles special card
                if play_card.label == CardLabel.DRAW_TWO:
                    self.play_draw_two()
                    continue
                elif play_card.label == CardLabel.DRAW_FOUR:
                    self.play_black(play_card)
                    continue 
                elif play_card.label == CardLabel.REVERSE:
                    self.reverse_players()
                elif play_card.label == CardLabel.SKIP:
                    self.skip_next_player()
                    continue
                
            #if player cannot play any card because they dont satisfy the condition
            else:

                if len(self.game_board.draw_pile) == 0:
                    self.game_board.reshuffle() # reshuffle the discard pile into draw pile

                new_card_drawn = self.draw_card(self.current_player,playing = True)

                if new_card_drawn is not None:

                    #the card drawn can be automatically played
                    self.game_board.discard_card(new_card_drawn) 

                    # update the current color randomly, when the play_card is black
                    if new_card_drawn.color == CardColor.BLACK:
                        self.current_color = CardColor(RandomGen.randint(0,3))
                        self.current_label = new_card_drawn.label
                    else:
                        # update the current color and current label based on the card played if its not black
                        self.current_color = new_card_drawn.color 
                        self.current_label = new_card_drawn.label
                
                    # check if the players hand is empty and won
                    if self.current_player.is_empty():
                        return self.current_player
                    
                    #handles special card
                    if new_card_drawn.label == CardLabel.DRAW_TWO:
                        self.play_draw_two()
                        continue
                    elif new_card_drawn.label == CardLabel.DRAW_FOUR:
                        self.play_black(play_card)
                        continue 
                    elif new_card_drawn.label == CardLabel.REVERSE:
                        self.reverse_players()
                    elif new_card_drawn.label == CardLabel.SKIP:
                        self.skip_next_player()
                        continue  
            
            # move to next player
            self.current_player =self.next_player()  
