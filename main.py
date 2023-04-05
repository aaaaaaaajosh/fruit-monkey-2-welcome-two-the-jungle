import turtle
import random
import math
import time
import os
import tkinter
import winsound
from PIL import Image, ImageOps

# Classes

class Fruit(turtle.Turtle):

    x_speed = float
    y_speed = float
    x_pos = float
    y_pos = float
    width = float
    height = float
    acceleration = -700.0
    score = 0
    image = str

    def __init__(self, width, height, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

    def reset(self):
        self.x_pos = random.randint(-wn.window_width() / 2 + 20, wn.window_width() / 2 - 20)
        self.y_pos = 200
        self.x_speed = random.randint(-500, 500)
        self.y_speed = random.randint(100, 300)



    def check_collision(self, turt: 'Player') -> None:

        distance = math.hypot(self.x_pos - turt.xcor(), self.y_pos - turt.ycor())
        x_intersection = (self.x_pos + self.width / 2 > turt.x_pos - turt.width / 2) and (self.x_pos - self.width / 2 < turt.x_pos + turt.width / 2)
        y_intersection = (self.y_pos + self.height / 2 > turt.y_pos - turt.height / 2) and self.y_pos - self.height / 2 < turt.y_pos + turt.height / 2
        if x_intersection and y_intersection:
            self.reset()
            self.score += 1

        if abs(self.x_pos) > wn.window_width() / 2 - self.width / 2:
            self.x_speed *= -1
            self.x_pos = wn.window_width() / 2 - self.width / 2 if self.x_pos > 0 else -wn.window_width() / 2 + self.width / 2

        if self.y_pos + self.height / 2 < -wn.window_height() / 2:
            self.reset()

    def update(self, dtime: float, turt: turtle.Turtle) -> None:
        self.x_pos += self.x_speed * dtime
        self.y_pos += self.y_speed * dtime
        self.y_speed += self.acceleration * dtime
        self.setx(self.x_pos)
        self.sety(self.y_pos)
        self.check_collision(turt)


    
class Player(turtle.Turtle):

    x_speed = 0.0
    x_pos = 0.0
    y_pos = int
    acceleration_power = 5500
    movement_acceleration = 0
    speed_limit = 750
    drag = .0005
    width = 30
    height = 30
    image = str

    def __init__(self, width: int, height: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.penup()
        self.setheading(90)
        self.setx(self.x_pos)
        self.y_pos = -wn.window_height() / 2 + self.height / 2
        self.sety(self.y_pos)

    def move_left(self) -> None:
        self.movement_acceleration = -self.acceleration_power

    def move_right(self) -> None:
        self.movement_acceleration = self.acceleration_power

    def stop(self) -> None:
        self.movement_acceleration = 0

    def check_collision(self):

        if abs(self.x_pos) > wn.window_width() / 2 - self.width / 2:
            self.x_speed *= -1
            self.x_pos = wn.window_width() / 2 - self.width / 2 if self.x_pos > 0 else -wn.window_width() / 2 + self.width / 2

    def update(self, dtime: float) -> None:
        self.x_pos += self.x_speed * dtime
        self.x_speed += self.movement_acceleration * dtime
        self.x_speed *= self.drag**dtime
        if abs(self.x_speed) > self.speed_limit:
            self.x_speed = self.speed_limit * (self.x_speed / abs(self.x_speed))
        self.setx(self.x_pos)
        self.sety(self.y_pos)
        self.check_collision()

class Writer(turtle.Turtle):

    font = str
    size = int
    color = str

    def __init__(self, font: str = "Comic Sans MS", size: int = 30, color: str = "White", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.font = font
        self.size = size
        self.color = color
        self.hideturtle()
        self.penup()

    def write(self, x, y, words: str, align: str = "center") -> None:
        self.setx(x)
        self.sety(y)
        self.pencolor(self.color)
        super().write(words, False, align=align, font=(self.font, self.size, "normal"))

# Functions

def create_fruit(num: int):
    global fruit_turtles
    global temp_fruit_types
    global fruit_types
    for i in fruit_turtles:
        i.hideturtle()
        i.clear()
    fruit_turtles.clear()
    for i in range(num):
        temp = Fruit(random.randint(75, 125), random.randint(75, 125))
        temp.penup()
        if len(temp_fruit_types) != 1:
            temp.image = temp_fruit_types.pop(random.randint(0, len(temp_fruit_types) - 1))
            set_image(temp)
        else:
            temp.image = temp_fruit_types.pop()
            set_image(temp)
            temp_fruit_types = fruit_types.copy()
        temp.reset()
        fruit_turtles.append(temp)

def set_image(turt: turtle.Turtle, image: str = ...) -> None:
    global image_number
    turt.image = image if turt.image == str else turt.image
    with Image.open(turt.image) as img:
        img = img.resize((turt.width, turt.height))
    img = img.crop(ImageOps.invert(img.convert('RGB')).getbbox())
    img.save("./res/temp/temp"+ (str)(image_number) + ".gif")
    wn.addshape("./res/temp/temp"+ (str)(image_number) + ".gif")
    turt.shape("./res/temp/temp"+ (str)(image_number) + ".gif")
    os.remove("./res/temp/temp"+ (str)(image_number) + ".gif")
    image_number += 1
    

def set_background(image: str) -> None:
    img = Image.open(image)
    img.load()
    img = img.resize((wn.window_width(), wn.window_height()))
    image = os.path.splitext(image)[0]
    image = os.path.split(image)[1]
    img.save("./res/temp/adjusted_" + image + ".gif")
    img.close()
    wn.addshape("./res/temp/adjusted_" + image + ".gif")
    wn.bgpic("./res/temp/adjusted_" + image + ".gif")

def write() -> None:
    global writer
    writer.clear()
    if running:
        writer.write(-wn.window_width() / 2 + 30, wn.window_height() / 2 - 60, "Time: " + "%.2f" % (time_limit - (time.time() - start_time)), align="left")
        writer.write(wn.window_width() / 2 - 30, wn.window_height() / 2 - 60, "Score: " + (str)(score), align="right")
    else:
        writer.write(0, 0, "YOUR SCORE WAS " + (str)(score))

def update() -> None:
    global last_time
    global running
    dtime = time.time() - last_time
    last_time = time.time()
    for i in fruit_turtles:
        i.update(dtime, dog)
    dog.update(dtime)
    set_score()
    write()
    wn.update()
    if running:
        wn.ontimer(update, 5)
        if time.time() - start_time > time_limit:
            start_screen()
            write()
            running = False

def start_screen() -> None:
    global button
    clear_all()
    button = tkinter.Button(wn.getcanvas().master, text="Play Game", command=reset)
    button.pack()
    # button.place(x=wn.window_width() / 2 - 25, y=wn.window_height() / 2 - 5)
    
def clear_all() -> None:
    for i in fruit_turtles:
        i.hideturtle()
        i.clear()

def reset() -> None:
    global start_time
    global score
    global last_time
    global running
    running = True
    button.destroy()
    start_time = time.time()
    score = 0
    create_fruit(num_fruit)
    last_time = time.time()
    winsound.PlaySound("./res/music.wav", winsound.SND_ASYNC)
    update()

def set_score() -> int:
    global score
    for i in fruit_turtles:
        score += i.score
        i.score = 0

def move(direction):
    global current_direction
    if direction == "Left":
        dog.move_left()
        current_direction = "Left"

    if direction == "Right":
        dog.move_right()
        current_direction = "Right"

    if direction == "Not Left" and current_direction == "Left":
        dog.stop()

    if direction == "Not Right" and current_direction == "Right":
        dog.stop()


# Declarations

image_number = 0

num_fruit = 6

running = False

fruit_folder = "./res/fruits/"
fruit_types = []
for i in os.scandir(fruit_folder):
    fruit_types.append(fruit_folder + i.name)

temp_fruit_types = fruit_types.copy()

current_direction = "None"
last_time = float
wn = turtle.Screen()
wn.bgcolor("darkslategray")
wn.setup(500, 500)
wn.cv._rootwindow.resizable(False, False)
wn.tracer(0)
wn.title("Fruit Monkey")
set_background("./res/junjle.jfif")
dog = Player(150, 150)
set_image(dog, "./res/monkey.png")

writer = Writer()

button = ...

fruit_turtles = []

score = 0

time_limit = 30

start_time = float

# Main

start_screen()


# Key Events

wn.onkeypress(lambda dir = "Left": move(dir), "Left")
wn.onkeyrelease(lambda dir = "Not Left": move(dir), "Left")
wn.onkeypress(lambda dir = "Right": move(dir), "Right")
wn.onkeyrelease(lambda dir = "Not Right": move(dir), "Right")

wn.listen()
wn.mainloop()