import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = player_in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        s = ""
        for card in self.hand:
            s += card.__str__()
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        flag = hand_value = 0
        for card in self.hand:
            rank = card.get_rank()
            hand_value += VALUES[rank]
        for card in self.hand:
            if card.get_rank() == 'A':
                flag = 1
        if not flag:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_pos = pos
        for card in self.hand:
            card.draw(canvas, card_pos)
            card_pos[0] += 80
                
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank)) 
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        card = random.choice(self.deck)
        self.deck.pop(self.deck.index(card))
        return card
        
    
    def __str__(self):
        # return a string representing the deck
        s = ""
        for card in self.deck:
            s += card.__str__() + " "
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, player_in_play, score
    if in_play:
        score -= 1
        outcome = "You Lose!"
    deck = Deck()
    dealer_hand = Hand()
    player_hand = Hand()
    deck.shuffle()
    for i in range(2):
        dealer_hand.add_card(deck.deal_card()) 
        player_hand.add_card(deck.deal_card())
    if deck == []:
        deck = Deck()
    in_play = player_in_play = True
    

def hit():
    # if the hand is in play, hit the player
    global in_play, outcome, score, player_in_play
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            in_play = player_in_play = True
        if player_hand.get_value() > 21:
            in_play = player_in_play = False
            score -= 1
        outcome = "You lose!"
    # if busted, assign a message to outcome, update in_play and score
       
def stand():	
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, in_play, score, player_in_play
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck.deal_card())
            player_in_play = False
        if dealer_hand.get_value() >= 21:
            in_play = player_in_play = False
            score += 1
            outcome = "You win!"
        else:
            if player_hand.get_value() < dealer_hand.get_value():
                score -= 1
                in_play = player_in_play = False
                outcome = "You lose!"
            else:
                score += 1
                in_play = player_in_play = False
                outcome = "You win!"
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play, player_in_play, outcome
    canvas.draw_text("BLACKJACK", [300,60], 70, "blue", "monospace")
    canvas.draw_text("Dealer", [20,150], 30, "black")
    canvas.draw_text("Player", [20,420], 30, "black")
    canvas.draw_text("Score : " + str(score), [730,90], 30, "black")    
    dealer_hand.draw(canvas, [10, 180])
    player_hand.draw(canvas, [10, 450])
    if outcome == "You Lose!":
        canvas.draw_text("New Deal?", [400,370], 30, "black")
        canvas.draw_text(outcome, [400,320], 30, "black")         
    elif in_play: 
        canvas.draw_text("Hit or stand?", [390,345], 30, "black")
    else:
        canvas.draw_text("New Deal?", [400,370], 30, "black")
        canvas.draw_text(outcome, [400,320], 30, "black")
    
    if player_in_play:
        card_loc = CARD_BACK_CENTER
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [46, 228], CARD_BACK_SIZE)
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 900, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

