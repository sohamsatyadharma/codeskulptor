import simplegui
import random

deck = range(8)
deck.extend(range(8))
CARD_WIDTH = 50

# helper function to initialize globals
def new_game():
    global state, turns, first, second, exposed
    state = turns = 0
    first = second = -1
    exposed = [False] * 16
    label.set_text("Turns = 0")
    random.shuffle(deck)
         
# define event handlers
def mouseclick(pos):
    global state, first, second, turns
    for i in range(len(exposed)):
        if pos[0] > CARD_WIDTH * i and pos[0] <= CARD_WIDTH * (i + 1):
            break
    if exposed[i]:
        return
    exposed[i] = True
    if state == 0:
        state = 1
        first = i
        turns += 1
    elif state == 1:
        state = 2
        second = i
    else:
        if deck[first] != deck[second]:
            exposed[first] = exposed[second] = False
        state = 1
        first = i 
        turns += 1
    label.set_text("Turns = " + str(turns))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(exposed)):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [CARD_WIDTH * i + 10, 70], 60, "white")
        else: 
            canvas.draw_line([CARD_WIDTH * i + 24, 0], [CARD_WIDTH * i + 24, 100], 48, "green")
                
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0", 100)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
