import simplegui
import random

secret_number = -1
n = 0

print "You have to guess a number in the given range "
print "Enter the number in the text box "
print "The range is [0,100) by default "
print "But you can change it by clicking on the buttons"
print "Best of luck and enjoy! \n "

def new_game():
    range100()
    

def range100():
    global n, secret_number
    n = 7
    print "New game. Range is [0,100)."
    print "Number of remaining guesses is 7 \n "
    secret_number = random.randrange(0,100)
    
def range1000():
    global n, secret_number
    n = 10
    print "New game. Range is [0,1000)."
    print "Number of remaining guesses is 10 \n "
    secret_number = random.randrange(0,1000)
    
def input_guess(guess):
    global secret_number, n
    print "Guess was", int(guess)
    if secret_number  == int(guess):
        print "Correct! \n"
        new_game()
    elif secret_number > int(guess):
        n-=1
        print "Number of remaining guesses is", n
        print "Higher! \n"
    else:
        n-=1
        print "Number of remaining guesses is", n
        print "Lower! \n"
    if n == 0:
        new_game()
   
    

f = simplegui.create_frame("Guess the number", 200, 200)


f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

 
new_game()



