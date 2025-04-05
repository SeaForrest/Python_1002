import turtle
import random
blank_tile_index = 0


def init_game_board(size):
    """Initializes the game window."""
    turtle.clear()
    board_size = size * 90
    turtle.setup(board_size + 100, board_size + 100)
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")
    turtle.tracer(0, 0)


def conversion(row, col, list1):
    """Converts row and column to linear index"""
    serial = size * (row - 1) + (col - 1)
    list1[list1.index(0)] = list1[serial]
    list1[serial] = 0


def random_shuffle(numbers, size):
    """Shuffles the puzzle"""
    for i in range(120*size):
        x_coordinate = numbers.index(0) // size + 1
        y_coordinate = numbers.index(0) % size + 1
        valid_moves = []
        if y_coordinate != 1:
            valid_moves.append('left')
        if y_coordinate != size:
            valid_moves.append('right')
        if x_coordinate != 1:
            valid_moves.append('up')
        if x_coordinate != size:
            valid_moves.append('down')

        move = random.choice(valid_moves)

        if move == 'left':
            y_coordinate = y_coordinate - 1
            conversion(x_coordinate, y_coordinate, numbers)
        elif move == 'right':
            y_coordinate = y_coordinate + 1
            conversion(x_coordinate, y_coordinate, numbers)
        elif move == 'up':
            x_coordinate = x_coordinate - 1
            conversion(x_coordinate, y_coordinate, numbers)
        elif move == 'down':
            x_coordinate = x_coordinate + 1
            conversion(x_coordinate, y_coordinate, numbers)
    return numbers


def generate_puzzle(size):
    """Generates a solvable puzzle of given size."""
    numbers = list(range(1, size*size))
    numbers.append(0)
    numbers = random_shuffle(numbers, size)
    if numbers == list(range(1, size*size)):
        numbers = generate_puzzle(size)
    return numbers


def test(size):
    """Create a list to indicate the end of the game"""
    list_test = list(range(1, size * size))
    list_test.append(0)
    return list_test


def draw_puzzle(numbers, size):
    """Draws the entire puzzle."""
    turtle.clear()
    for index, number in enumerate(numbers):
        x = (index % size) * 90 - (size * 90) / 2
        y = (size * 90) / 2 - (index // size) * 90
        if number == 0:
            draw_tile(x, y, number, clear=True)
        else:
            draw_tile(x, y, number)
    turtle.update()


def draw_tile(x, y, number, clear=False):
    """Draws a single tile at given position."""
    if clear:
        turtle.color("white")
    else:
        turtle.color("lightgrey")

    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(80)
        turtle.right(90)
    turtle.end_fill()

    if not clear:
        turtle.penup()
        turtle.goto(x + 15, y - 35)
        turtle.color("black")
        turtle.write(number, font=("Arial", 18, "normal"))


def draw_tile_moving(x, y, clear=False):
    """Draws a tile while moving."""
    if clear:
        turtle.color("white")
    else:
        turtle.color("lightgrey")

    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(80)
        turtle.right(90)
    turtle.end_fill()


def get_game_size():
    """Gets the game size from user input."""
    size = turtle.numinput("Sliding Puzzle", "Enter the size (3, 4, 5):", 3, minval=3, maxval=5)
    if int(size) != size:
        return get_game_size()
    return int(size)


def is_tile_movable(index, size):
    """Checks if the clicked tile can be moved."""
    global blank_tile_index
    row_diff = abs(index // size - blank_tile_index // size)
    col_diff = abs(index % size - blank_tile_index % size)
    return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)


def move_tile(index, numbers, size):
    """Moves the tile and simulates animation effect."""
    global blank_tile_index
    if is_tile_movable(index, size):
        steps = 40
        dx = ((blank_tile_index % size) - (index % size)) * 80 / steps
        dy = ((blank_tile_index // size) - (index // size)) * 80 / steps

        for step in range(0, steps+1):
            draw_tile_moving(((index % size) * 90 - (size * 90) / 2) + dx * step,
                             ((size * 90) / 2 - (index // size) * 90) - dy * step,
                             clear=True)

            draw_tile_moving(((index % size) * 90 - (size * 90) / 2) + dx * (step+1),
                             ((size * 90) / 2 - (index // size) * 90) - dy * (step+1))

            turtle.update()

        numbers[blank_tile_index], numbers[index] = numbers[index], numbers[blank_tile_index]
        blank_tile_index = index
        draw_puzzle(numbers, size)
        if numbers[:] == list_test:
            draw_puzzle_end(numbers, size)


def end(x, y, number, clear=False):
    """To transfer the tile into red at the end of the game"""
    if clear:
        turtle.color("white")
    else:
        turtle.color("red")

    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(80)
        turtle.right(90)
    turtle.end_fill()

    if not clear:
        turtle.penup()
        turtle.goto(x + 15, y - 35)
        turtle.color("black")
        turtle.write(number, font=("Arial", 18, "normal"))


def draw_puzzle_end(numbers, size):
    """To transfer the tile into red at the end of the game"""
    turtle.clear()
    for index, number in enumerate(numbers):
        x = (index % size) * 90 - (size * 90) / 2
        y = (size * 90) / 2 - (index // size) * 90
        if number == 0:
            end(x, y, number, clear=True)
        else:
            end(x, y, number)
    turtle.update()


def on_click(x, y):
    """To determined where you click and transfer it into index"""
    global blank_tile_index
    col = int((x + (size * 90) / 2) // 90)
    row = int((size - (y + (size * 90) / 2) / 90))
    index = row * size + col
    if 0 <= index < size**2:
        move_tile(index, numbers, size)


def setup_mouse_listener():
    turtle.onscreenclick(on_click)


def main():
    global size, numbers, blank_tile_index, list_test
    size = get_game_size()
    init_game_board(size)
    numbers = generate_puzzle(size)
    list_test = test(size)
    blank_tile_index = numbers.index(0)
    draw_puzzle(numbers, size)
    setup_mouse_listener()
    turtle.done()


if __name__ == "__main__":
    main()
