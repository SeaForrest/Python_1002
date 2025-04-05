import random

list0 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
inverse_num = 0  # This block is used for basic variables initializing
count = 0  # Movements number count initializing


def initialize():
    global left, right, up, down
    a_str = input('Enter the four letters used for left, right, up and down move > ')
    try:
        list_store = []
        for j in a_str.replace(" ", ""):
            list_store.append(j)
        # Collect the input which stands for movement at the beginning of the game
        left, right, up, down = list_store
        wrong_check(left, right, up, down)
    except:
        print('Invalid input. Please enter again.\n')
        return initialize()


def launch(alist):
    random.shuffle(alist)

    list_check = alist[:]
    del list_check[list_check.index(9)]

    p = is_solvable(list_check)
    if p == 1:
        return launch(alist)
    elif p == 0:
        return alist  # Shuffle the list and check whether it is solvable


def is_solvable(alist):
    global inverse_num

    if len(alist) == 1:
        num = inverse_num
        inverse_num = 0
        return num % 2

    first_num = alist[0]
    for j in alist[1: len(alist)]:
        if first_num > j:
            inverse_num += 1
    # Use inversion to check whether the puzzle is solvable
    return is_solvable(alist[1:])


def wrong_check(le, rg, u, dw):
    if type(le) is not type('string') or type(rg) is not type('string') or type(u) is not type(
            'string') or type(dw) is not type('string'):
        print('Invalid input. Please enter again.\n')
        return initialize()

    if le == rg or le == u or le == dw or rg == u or rg == dw or u == dw:
        print('Invalid input. Please enter again.\n')
        return initialize()

    try:
        if type(eval(le)) is type(1) or type(eval(rg)) is type(1) or \
         type((eval(u))) is type(1) or type((eval(dw))) is type(1):
            print('Invalid input. Please enter again.\n')
            return initialize()
    except:
        return None  # Determine wrong input


def display(alist):
    num_count = 0
    print(' ')
    for k in alist:
        if k == 9:
            print(' ', end='')
        else:
            print(k, end='')  # Use '9' to stand for white space
        num_count += 1
        if num_count % 3 != 0:
            print(' ', end='')
        else:
            print('\n', end='')
    print(' ')  # Transfer the list into a 3*3 matrix


x_coordinate, y_coordinate = None, None
left, right, up, down = 'None', 'None', 'None', 'None'
# Declare the variable which is used during game_progression.


def game_progression(alist):
    global x_coordinate, y_coordinate, count
    le = 'left-' + left + ' '
    rg = 'right-' + right + ' '
    u = 'up-' + up + ' '
    dw = 'down-' + down + ' '

    x_coordinate = alist.index(9) // 3 + 1
    y_coordinate = alist.index(9) % 3 + 1

    if x_coordinate == 1:
        dw = ''
    if x_coordinate == 3:
        u = ''
    if y_coordinate == 1:
        rg = ''
    if y_coordinate == 3:
        le = ''  # Transfer into row, col coordinate. Find that only in 1, 3 has special properties

    if alist == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print('Congratulations! You solved the puzzle in ', count, ' moves!', sep='')
        end()  # To end the game
        return None

    print('The direction in which you could move next:', '( ', le, rg, u, dw, ')', sep='')
    step = input('Enter your choice here:')

    if 'left-' + step + ' ' == le:
        count = count + 1
        y_coordinate = y_coordinate + 1
        conversion(x_coordinate, y_coordinate, list0)
        return game_progression(list0)
    elif 'right-' + step + ' ' == rg:
        count = count + 1
        y_coordinate = y_coordinate - 1
        conversion(x_coordinate, y_coordinate, list0)
        return game_progression(list0)
    elif 'up-' + step + ' ' == u:
        count = count + 1
        x_coordinate = x_coordinate + 1
        conversion(x_coordinate, y_coordinate, list0)
        return game_progression(list0)
    elif 'down-' + step + ' ' == dw:
        count = count + 1
        x_coordinate = x_coordinate - 1
        conversion(x_coordinate, y_coordinate, list0)
        return game_progression(list0)  # This block is used for determining the input and moving

    else:
        print('Invalid input. Please enter again.')
        display(list0)
        return game_progression(list0)


def conversion(row, col, list1):
    serial = 3 * (row - 1) + (col - 1)
    list1[list1.index(9)] = list1[serial]
    list1[serial] = 9
    display(list1)


def main():
    global count, left, right, up, down
    count = 0

    print("Welcome to Kinley's puzzle game. The objective of the game\
is to rearrange\nthe numbered tiles into a sequential\
order by their numbers(left to right,\ntop to bottom) by\
repeatedly sliding one adjacent tile into the empty space.\n")
    initialize()
    launch(list0)
    display(list0)
    game_progression(list0)  # Use this function to organize the functions and start the game


def play_again():
    global count
    count = 0
    launch(list0)
    display(list0)
    game_progression(list0)  # Use this function play the game again


def end():
    sign_play_again = input(
        'Enter “n” for another game, or “q” to end the game >')
    if sign_play_again == 'n':
        play_again()
    if sign_play_again == 'q':
        return None
    else:
        print('Sorry, there is something wrong in your input.\n')
        return end()  # Determine wrong input and end the game


main()
