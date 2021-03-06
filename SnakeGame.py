import os
import turtle
import time
import random


delay = 0.11

# Score

score = 0
high_score = 0
#Setting up the Screen
wn = turtle.Screen()
wn.title("The Snake Game By _mishp_")
wn.bgcolor("green")
wn.setup(width=600,height=600)
wn.tracer(0) # Turns off screen updates

#Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("white")
head.penup()
head.goto(0,0)
head.direction="stop"


# Snake food

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("blue")
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Score : 0  High Score: 0", align= "center", font=("Courier", 24,"normal"))
# Functions

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"



def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
        
# Keyboard Bindings
wn.listen()
wn.onkeypress(go_up,"w")
wn.onkeypress(go_down,"s")
wn.onkeypress(go_left,"a")
wn.onkeypress(go_right,"d")




# Main game loop
while True:

    # Check coordinates for wall collisions
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"


        # Hide segments
        for segment in segments:
            segment.goto(1000,1000)

        # clear segment list
        segments.clear()

        # reset delay
        delay = 0.11

        # Reset Score
        score = 0
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score,high_score),align="center",font=("Courier", 24,"normal"))

    wn.update()
    # Check for Food collision
    if head.distance(food) < 20:
        # Move food
        x = random.randint(-290,290)
        y = random.randint(-290,290)
        food.goto(x,y)

        # Add segment
        new_segment=turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        new_segment.color("black")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten delay to compensate
        delay -= 0.001

        # Increase Score
        score += 10
        if score > high_score:
            high_score = score
            pen.clear()
        pen.write("Score: {}  High Score: {}".format(score,high_score),align="center",font=("Courier", 24,"normal"))

    # Move end segment first in reverse ordr
    for index in range(len(segments)-1,0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)


    # Move segment zero to where head is
    if len(segments)>0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
        
    move()

    # Check for body collision
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            # Hide segments
            for segment in segments:
                segment.goto(1000,1000)

            # clear segment list
            segments.clear()

            # reset delay
            delay = 0.11

            # Reset Score
            score = 0
        
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score,high_score),align="center",font=("Courier", 24,"normal"))

      

    time.sleep(delay)
wn.mainloop() 
