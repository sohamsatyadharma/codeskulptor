import simplegui 

print "Welcome to the stopwatch game!"
print "You have to stop the stopwatch when the number of seconds is a whole number"
print "The numbers on the top right corner show 'successful attempts/attempts'"

value = True
time = x = y = 0

def format(t):
    mins = t // 600
    decisec = t % 10
    sec = (t - mins*600) // 10
    if sec == 0:
        result = str(mins) + ":00." + str(decisec)
    elif sec < 10:
        result = str(mins) + ":0" + str(sec) + "." + str(decisec)
    else:
        result = str(mins) + ":" + str(sec) + "." + str(decisec)
    return result
    
    
def start_handler():
    global value
    timer.start()
    value = True
    
def stop_handler():
    global value, x, y, time
    timer.stop()
    if value == True:
        y += 1
    value = False 
    if time % 10 == 0:	
        x += 1    
    
def reset_handler():
    global time, x, y
    time = x = y = 0
    timer.stop()

def timer_handler():
    global time
    time += 1
       

def draw(canvas) :
    canvas.draw_text(format(time), [90,120], 50, "White")
    canvas.draw_text(str(x) + "/" + str(y), [240,30], 24, "Red")
    
f = simplegui.create_frame("Stopwatch", 300, 200)

timer = simplegui.create_timer(100, timer_handler)
f.add_button("Start", start_handler, 100)
f.add_button("Stop", stop_handler, 100)
f.add_button("Reset", reset_handler, 100)
f.set_draw_handler(draw)

f.start()


