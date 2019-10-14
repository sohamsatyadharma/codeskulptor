import simplegui
import random

print "Welcome to pong!"
print "Move the left paddle up and down using 'W' and 'S' respectively"
print "Move the right paddle up and down using 'up arrow' and 'down arrow' respectively"
print "Enjoy and may the force be with the best!"

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0.0, 0.0]
paddle1_pos = paddle2_pos = HEIGHT / 2 
paddle1_vel = paddle2_vel = 0
direction = LEFT 
v = 6
score1 = score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] 
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2,4)
        ball_vel[1] = -random.randrange(1,3)
    else:
        ball_vel[0] = -random.randrange(2,4)
        ball_vel[1] = -random.randrange(1,3)
  


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    paddle1_pos = paddle2_pos = HEIGHT / 2  	
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1] 
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle1_pos - HALF_PAD_HEIGHT <= 0 or paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle1_vel = 0
    if paddle2_pos - HALF_PAD_HEIGHT <= 0 or paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle2_vel = 0
    
    # draw paddles
    
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 8, "cyan")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 8, "cyan")
    
    # determine whether paddle and ball collide
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1    
    
    # draw scores
    canvas.draw_text(str(score1), [150, 50], 30, "Yellow")
    canvas.draw_text(str(score2), [450, 50], 30, "Yellow")
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel, v
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -v
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = v
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -v
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = v
     
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
