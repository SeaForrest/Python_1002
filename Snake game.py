import turtle
import random

# Variables related to the setup
size = 20

# Variables related to the foods
foods = []

# Variables related to the snake
snake_time = 200  # Used for ontimer to slow down when eating food
snake_position = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
snake_velocity = size
snake_len = 5
x_speed = 0  # 0=pause; 1=right; -1=left
y_speed = 0  # 0=pause; 1=up; -1=down
x_sub = 0  # Store the speed in order to resume after pause
y_sub = 0

# Variables related to the monsters
monster_position = [[0, 0], [0, 0], [0, 0], [0, 0]]
monster_contact = 0
delay = 200

# Variables related to the procession
pause = False
over = False
success = False
protection = 0  # Used to let the food and the monsters not move at the beginning
pass_time = 0
timer = 0


# Functions that is commonly used
def init():
    turtle.setup(580, 660)
    turtle.tracer(0)
    turtle.hideturtle()
    turtle.listen()  # listen to the keyboard input

    turtle.onkey(key_left, 'Left')
    turtle.onkey(key_right, 'Right')
    turtle.onkey(key_up, 'Up')
    turtle.onkey(key_down, 'Down')
    turtle.onkey(key_pause, 'space')

    turtle.onscreenclick(receiver)

    turtle.up()
    turtle.goto(-230, 160)
    turtle.write('Please click to start the game', font=("Arial", 24, "normal"))

    gen_food()
    gen_monster()
    draw_monster()
    draw_snake()
    set_up_screen()


def set_up_screen():  # Used to produce a border
    turtle.up()
    turtle.goto(-260, 240)
    turtle.down()
    turtle.color('black')
    turtle.pensize(5)
    for i in range(4):
        turtle.forward(520)
        turtle.right(90)
    turtle.up()
    turtle.down()
    turtle.goto(-260, 240)
    turtle.forward(520)
    turtle.left(90)
    turtle.forward(60)
    turtle.left(90)
    turtle.forward(520)
    turtle.left(90)
    turtle.forward(60)
    turtle.up()
    turtle.left(90)
    turtle.pensize(1)


def draw_rect(x, y, length=20, color='red'):  # Used to draw a rectangle
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.color(color)
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(length)
        turtle.left(90)
    turtle.end_fill()
    turtle.color('grey')
    for i in range(4):
        turtle.forward(length)
        turtle.left(90)
    turtle.up()


# Functions related to food
def gen_food():  # Used for generating food
    for number in range(1, 6):
        x = 20 * random.randrange(-200 // 20, 200 // 20)
        y = 20 * random.randrange(-230 // 20, 170 // 20)
        food = (x, y, number)
        foods.append(food)


def food_move():  # To move the food
    global protection
    if protection >= 10:
        for i in range(0, len(foods)):
            food = foods[i]
            x, y, number = food
            x += 20 * random.randrange(-2, 2)
            y += 20 * random.randrange(-2, 2)
            food = x, y, number
            foods[i] = food
        determine_food_pos()
    turtle.ontimer(food_move, 5000)


def determine_food_pos():  # Check whether the food is out of the screen
    for food in foods:
        x, y, number = food
        foods.remove(food)
        if x >= 210:
            x = x - 40
        if x <= -210:
            x = x + 40
        if y >= 180:
            y = y - 40
        if y <= -240:
            y = y + 40
        food = x, y, number
        foods.append(food)


def draw_foods():
    for food in foods:
        x, y, number = food
        draw_number(x, y, number)


def draw_number(x, y, number):  # Transfer the position into the number on the screen
    turtle.up()
    turtle.color('black')
    turtle.goto(x+5, y-5)
    turtle.down()
    turtle.write(number, font=("Arial", 18, "normal"))
    turtle.up()


def collision_food():  # Snake eat the food
    global snake_len, snake_position, foods
    food_eat = []
    snake_x, snake_y = snake_position[-1]
    for food in foods:
        x, y, number = food
        if snake_x == x and snake_y == y:
            food_eat = x, y, number
            for i in range(0, number):
                snake_position.insert(0, [x, y])
    if len(food_eat):  # If it isn't empty, remove the tuple in foods
        foods.remove(food_eat)
        if not foods:
            game_success()


# Functions related to the snake
def draw_snake():
    for pos in snake_position[:-1]:
        draw_rect(pos[0], pos[1])
    draw_rect(snake_position[-1][0], snake_position[-1][1], 20, 'black')


def update_snake():  # To make the snake move
    global pause, x_speed, y_speed
    global snake_position
    head_x = snake_position[-1][0] + x_speed * snake_velocity
    head_y = snake_position[-1][1] + y_speed * snake_velocity
    if pause is False:
        snake_position.append([head_x, head_y])
        snake_position.pop(0)


def snake_eat_food():  # When eating food, make snake slow
    global snake_time
    slow = False
    for pos in snake_position[1:]:
        if pos == snake_position[0]:
            slow = True
    if slow is True:
        snake_time = 300
    else:
        snake_time = 200


# Functions of the monsters
def gen_monster():
    for i in range(0, 4):
        x = 0
        y = 0
        x_det = random.choice([-1, 1])
        y_det = random.choice([-1, 1])  # Used for generate monster far from the snake
        if x_det == 1:
            x = 20 * random.randrange(x_det * 120 // 20, x_det * 200 // 20)
        if x_det == -1:
            x = 20 * random.randrange(x_det * 200 // 20, x_det * 120 // 20)
        if y_det == 1:
            y = 20 * random.randrange(y_det * 90 // 20, y_det * 170 // 20)
        if y_det == -1:
            y = 20 * random.randrange(y_det * 230 // 20, y_det * 150 // 20)
        mon = [x, y]
        monster_position[i] = mon


def draw_monster():
    for mon in monster_position:
        draw_rect(mon[0], mon[1], size, 'purple')


def collision_monster():  # Contact the head
    snake_x, snake_y = snake_position[-1]
    for mon in monster_position:
        x, y = mon
        if snake_x == x and snake_y == y:
            game_over()


def contact_monster():  # Contact the body
    global monster_contact
    for i in snake_position[1: len(snake_position)+1]:
        snake_x, snake_y = i
        for mon in monster_position:
            x, y = mon
            if snake_x == x and snake_y == y:
                monster_contact += 1


def monster_move_1():  # The following four monsters' movement
    global snake_time, delay, protection
    if protection >= 10:
        delay = random.randint(snake_time + 400, snake_time + 1000)
        mon = monster_position[0]
        snake_x = snake_position[-1][0]
        snake_y = snake_position[-1][1]
        x, y = mon
        if abs(x - snake_x) >= abs(y - snake_y):
            if x - snake_x <= 0:
                x += size
            else:
                x -= size
        else:
            if y - snake_y <= 0:
                y += size
            else:
                y -= size
        monster_position[0] = [x, y]
    turtle.ontimer(monster_move_1, delay)


def monster_move_2():
    global snake_time, delay, protection
    if protection >= 10:
        delay = random.randint(snake_time + 400, snake_time + 1000)
        mon = monster_position[1]
        snake_x = snake_position[-1][0]
        snake_y = snake_position[-1][1]
        x, y = mon
        if abs(x - snake_x) >= abs(y - snake_y):
            if x - snake_x <= 0:
                x += size
            else:
                x -= size
        else:
            if y - snake_y <= 0:
                y += size
            else:
                y -= size
        monster_position[1] = [x, y]
    turtle.ontimer(monster_move_2, delay)


def monster_move_3():
    global snake_time, delay, protection
    if protection >= 10:
        delay = random.randint(snake_time + 400, snake_time + 1000)
        mon = monster_position[2]
        snake_x = snake_position[-1][0]
        snake_y = snake_position[-1][1]
        x, y = mon
        if abs(x - snake_x) >= abs(y - snake_y):
            if x - snake_x <= 0:
                x += size
            else:
                x -= size
        else:
            if y - snake_y <= 0:
                y += size
            else:
                y -= size
        monster_position[2] = [x, y]
    turtle.ontimer(monster_move_3, delay)


def monster_move_4():
    global snake_time, delay, protection
    if protection >= 10:
        delay = random.randint(snake_time + 400, snake_time + 1000)
        mon = monster_position[3]
        snake_x = snake_position[-1][0]
        snake_y = snake_position[-1][1]
        x, y = mon
        if abs(x - snake_x) >= abs(y - snake_y):
            if x - snake_x <= 0:
                x += size
            else:
                x -= size
        else:
            if y - snake_y <= 0:
                y += size
            else:
                y -= size
        monster_position[3] = [x, y]
    turtle.ontimer(monster_move_4, delay)


# Functions of the process
def run():
    global snake_time, delay, protection, timer, pass_time

    collision_monster()
    collision_food()
    collision_wall()
    contact_monster()

    if over is True or success is True:
        turtle.clear()
        status_bar()
        set_up_screen()

        draw_foods()
        draw_snake()
        draw_monster()

        turtle.up()
        turtle.goto(-120, 0)
        turtle.down()
        turtle.color('black')
        if over is True:
            turtle.write('Game Over!', font=("Arial", 36, "normal"))
            turtle.up()
        if success is True:
            turtle.write('Your Win!', font=("Arial", 36, "normal"))
            turtle.up()

    else:
        turtle.clear()
        set_up_screen()
        status_bar()

        protection += 1
        timer += 1
        snake_eat_food()
        if protection <= 15:
            snake_time = 200
        if timer >= 5:
            timer = 0
            pass_time += 1
        update_snake()

        draw_foods()
        draw_snake()
        draw_monster()

        turtle.ontimer(run, snake_time)


def game_over():
    global over
    over = True


def game_success():
    global success
    success = True


def status_bar():  # To draw the status bar
    global pass_time, x_speed, y_speed, pause
    turtle.up()
    turtle.goto(-250, 250)
    turtle.down()
    turtle.color('black')
    turtle.write('Contact:', font=("Arial", 20, "normal"))
    turtle.up()
    turtle.forward(110)
    turtle.down()
    turtle.write(monster_contact, font=("Arial", 20, "normal"))
    turtle.up()
    turtle.forward(50)
    turtle.down()
    turtle.write('Time:', font=("Arial", 20, "normal"))
    turtle.up()
    turtle.forward(75)
    turtle.down()
    turtle.write(pass_time, font=("Arial", 20, "normal"))
    turtle.up()
    turtle.forward(75)
    turtle.down()
    if x_speed == 1:
        motion = 'Left'
    elif x_speed == -1:
        motion = 'Right'
    elif y_speed == 1:
        motion = 'Up'
    elif y_speed == -1:
        motion = 'Down'
    else:
        motion = 'Pause'
    turtle.write('Motion:', font=("Arial", 20, "normal"))
    turtle.up()
    turtle.forward(95)
    turtle.down()
    turtle.write(motion, font=("Arial", 20, "normal"))
    turtle.up()


def collision_wall():  # When contact the wall, make it pause
    global x_speed, y_speed, pause
    if x_speed == 1 and snake_position[-1][0] == 240:
        pause = True
    if x_speed == -1 and snake_position[-1][0] == -260:
        pause = True
    if y_speed == 1 and snake_position[-1][1] == 220:
        pause = True
    if y_speed == -1 and snake_position[-1][1] == -280:
        pause = True


def key_left():  # Listen to the key tap
    global x_speed, y_speed, pause
    x_speed = -1
    y_speed = 0
    pause = False


def key_right():
    global x_speed, y_speed, pause
    x_speed = 1
    y_speed = 0
    pause = False


def key_up():
    global y_speed, x_speed, pause
    y_speed = 1
    x_speed = 0
    pause = False


def key_down():
    global y_speed, x_speed, pause
    y_speed = -1
    x_speed = 0
    pause = False


def key_pause():
    global y_speed, x_speed, pause, x_sub, y_sub
    pause = not pause
    if pause is True:
        x_sub = x_speed
        y_sub = y_speed
        y_speed = 0
        x_speed = 0
    else:
        x_speed = x_sub
        y_speed = y_sub


def main_loop():
    run()
    food_move()
    monster_move_1()
    monster_move_2()
    monster_move_3()
    monster_move_4()
    turtle.onscreenclick(None)


def receiver(x, y):  # Use it to start the mainloop
    main_loop()


if __name__ == '__main__':
    init()
    while True:
        turtle.update()
