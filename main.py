import curses

ROWS = 6
COLUMNS = 7

RED_DOT = '*'
YELLOW_DOT = '0'

EMPTY_FIELD = ''


class MoveOrder:
    __is_red_move = True

    @classmethod
    def is_red_move(cls):
        return cls.__is_red_move

    @classmethod
    def switch_move(cls):
        cls.__is_red_move = not cls.__is_red_move


def draw_field(stdscr, field):
    for x in range(COLUMNS + 1):
        for y in range(ROWS):
            stdscr.addstr(y + 2, x * 2, '|')
    for x in range(ROWS):
        for y in range(COLUMNS):
            color = curses.color_pair(2 if field[x][y] == RED_DOT else 1)
            if field[x][y] != EMPTY_FIELD:
                stdscr.addstr(y + 2, x * 2 + 1, field[x][y], color)


def drop_ball(field, cursor_x):
    try:
        x, y = find_ball_position(field, cursor_x)
    except ValueError:
        return
    field[x][y] = RED_DOT if MoveOrder.is_red_move() else YELLOW_DOT
    MoveOrder.switch_move()


def find_ball_position(field, cursor_x):
    if field[cursor_x][0] != EMPTY_FIELD:
        raise ValueError("No empty rows")
    for y in range(1, ROWS):
        if field[cursor_x][y] != EMPTY_FIELD:
            return cursor_x, y - 1
    return cursor_x, ROWS - 1


def draw_move_message(stdscr):
    color = curses.color_pair(2 if MoveOrder.is_red_move() else 1)
    stdscr.addstr(0, 0, f"It's {'red' if MoveOrder.is_red_move() else 'yellow'} move", color)


def winning_move(field, ball):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if (
                    field[r][c] == ball
                    and field[r][c + 1] == ball
                    and field[r][c + 2] == ball
                    and field[r][c + 3] == ball
            ):
                return True
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (

                    field[r][c] == ball
                    and field[r + 1][c] == ball
                    and field[r + 2][c] == ball
                    and field[r + 3][c] == ball
            ):
                return True
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if (
                    field[r][c] == ball
                    and field[r + 1][c + 1] == ball
                    and field[r + 2][c + 2] == ball
                    and field[r + 3][c + 3] == ball
            ):
                return True
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if (
                    field[r][c] == ball
                    and field[r - 1][c + 1] == ball
                    and field[r - 2][c + 2] == ball
                    and field[r - 3][c + 3] == ball
            ):
                return True


def draw_game_over(stdscr):
    stdscr.clear()
    stdscr.refresh()
    midx, midy = (int(c // 2) for c in stdscr.getmaxyx())
    stdscr.addstr(midx, midy, "Game over! (field is full)", curses.color_pair(3))


def draw_winning_message(stdscr, player):
    stdscr.clear()
    stdscr.refresh()
    midx, midy = (int(c // 2) for c in stdscr.getmaxyx())
    stdscr.addstr(midx, midy, f"{player} won!", curses.color_pair(3))


def draw(stdscr):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    k = 0
    cursor_x = 0
    field = [[EMPTY_FIELD for _ in range(COLUMNS)] for _ in range(ROWS)]

    # Loop where k is the last character pressed
    while k != ord('q'):
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1
        if k == curses.KEY_DOWN:
            drop_ball(field, cursor_x)
            stdscr.refresh()

        draw_move_message(stdscr)
        draw_field(stdscr, field)

        cursor_x = max(0, cursor_x)
        cursor_x = min(COLUMNS - 1, cursor_x)

        # Render status bar
        if winning_move(field, RED_DOT):
            draw_winning_message(stdscr, 'Red')
            stdscr.getch()
            return
        elif winning_move(field, YELLOW_DOT):
            draw_winning_message(stdscr, 'Yellow')
            stdscr.getch()
            return

        stdscr.addstr(height - 1, 0, "Press 'q' to exit", curses.color_pair(3))
        stdscr.move(1, cursor_x * 2 + 1)

        stdscr.refresh()
        k = stdscr.getch()


def main():
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
