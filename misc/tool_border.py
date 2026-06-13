import curses
import os
import pathlib
import sys
import time

KEY2CHAR = {
    curses.KEY_DC: 0xFF,
    ord('1'): 0xA1,
    ord('2'): 0x51,
    ord('3'): 0x50,
    ord('4'): 0x54,
    ord('5'): 0x57,
    ord('6'): 0x5A,
    ord('7'): 0x5D,
    ord('8'): 0x69,
    ord('9'): 0x66,
    ord('0'): 0x60,
    ord('-'): 0x63,
    ord('='): 0x6C,
}

TABLE_X = 0
TABLE_Y = 0
TABLE_COLS = 32
TABLE_ROWS = 8

THUMB_X = 34
THUMB_Y = 0

MIN_W = 60
MIN_H = 12

data = bytearray([0xFF for _i in range(256)])

exit_code = 0
exit_print = False

#region helper

def getchar(raw:int): return ' ' if (raw == 0xFF) else chr(0x2500 | raw)

def print_line(win:curses.window, offset:int, text:None|str = None):
    h, w = win.getmaxyx()
    if text is None: text = ' ' * w
    elif len(text) > w: text = text[:w]
    elif len(text) < w: text = text + ' ' * (w - len(text))
    try: win.addstr(offset, 0, text)
    except: pass

def prompt_yn(win:curses.window, offset:int, text:str):
    print_line(win, offset, f"{text} YN")
    win.refresh()
    while True:
        ch = win.getch()
        if ch == ord('Y') or ch == ord('y'):
            result = True
            break
        if ch == ord('N') or ch == ord('n'):
            result = False
            break
    print_line(win, offset)
    return result

def prompt_ync(win:curses.window, offset:int, text:str):
    print_line(win, offset, f"{text} YNC")
    win.refresh()
    while True:
        ch = win.getch()
        if ch == ord('Y') or ch == ord('y'):
            result = 1
            break
        if ch == ord('N') or ch == ord('n'):
            result = 0
            break
        if ch == ord('C') or ch == ord('c'):
            result = -1
            break
    print_line(win, offset)
    return result

def prompt_quit(win:curses.window, offset:int, path:pathlib.Path):
    global data, exit_print
    # Prompt 1
    prompt = prompt_ync(win, offset, "Save changes?")
    if prompt == 0: return True # User answered no
    if prompt == -1: return False # User answered cancel
    # Save
    with open(path, 'wb') as file:
        file.write(data)
    # Prompt 2
    exit_print = prompt_yn(win, offset, "Print python source code?")
    # Success!!!
    return True

#endregion

def main(win:curses.window):
    if len(sys.argv) == 0: return 1
    curses.curs_set(0)
    try:
        global data
        # Valid size?
        win_h, win_w = win.getmaxyx()
        if win_w < MIN_W: return 1
        if win_h < MIN_H: return 1
        msgoffset = win_h - 1
        # Load data
        datapath = pathlib.Path(sys.argv[0]).parent.joinpath("border.bin")
        if os.path.exists(datapath):
            with open(datapath, 'rb') as _file:
                data = bytearray(_file.read())
                if len(data) < 256: data.extend([0 for _i in range(len(data), 256)])
                elif len(data) > 256: data = data[:256]
        # Loop
        cursor = 0
        while True:
            win.clear()
            #region Print table
            # Print row header
            win.addstr(TABLE_Y, TABLE_X + 1, "0123456789ABCDEF0123456789ABCDEF")
            # Print column header
            for _i in range(TABLE_ROWS): win.addch(TABLE_Y + 1 + _i, TABLE_X, f"{(_i * 2):01X}")
            # Print cells
            for _i in range(256):
                _x = TABLE_X + 1 + _i % 32
                _y = TABLE_Y + 1 + _i // 32
                _c = getchar(data[_i])
                _a = curses.A_STANDOUT if (_i == cursor) else curses.A_NORMAL
                win.addch(_y, _x, _c, _a)
            #endregion
            #region Print selected
            # Print border
            win.addstr(THUMB_Y, THUMB_X, chr(0x0250C) + chr(0x02500) * 3 + chr(0x02510))
            for _i in range(3): win.addstr(THUMB_Y + 1 + _i, THUMB_X, chr(0x02502) + ' ' * 3 + chr(0x02502))
            win.addstr(THUMB_Y + 4, THUMB_X, chr(0x02514) + chr(0x02500) * 3 + chr(0x02518))
            # Print "walls"
            _item = data[cursor]
            if (cursor & 0b00000001) != 0: win.addch(THUMB_Y + 1, THUMB_X + 2, chr(0x2588))
            if (cursor & 0b00000010) != 0: win.addch(THUMB_Y + 3, THUMB_X + 2, chr(0x2588))
            if (cursor & 0b00000100) != 0: win.addch(THUMB_Y + 2, THUMB_X + 1, chr(0x2588))
            if (cursor & 0b00001000) != 0: win.addch(THUMB_Y + 2, THUMB_X + 3, chr(0x2588))
            if (cursor & 0b00010000) != 0: win.addch(THUMB_Y + 1, THUMB_X + 1, chr(0x2588))
            if (cursor & 0b00100000) != 0: win.addch(THUMB_Y + 1, THUMB_X + 3, chr(0x2588))
            if (cursor & 0b01000000) != 0: win.addch(THUMB_Y + 3, THUMB_X + 1, chr(0x2588))
            if (cursor & 0b10000000) != 0: win.addch(THUMB_Y + 3, THUMB_X + 3, chr(0x2588))
            # Print character
            win.addch(THUMB_Y + 2, THUMB_X + 2, getchar(_item))
            #endregion
            # Refresh screen
            win.refresh()
            #region Get input
            _key = win.getch()
            # Quit
            if _key == 0x1B:
                if prompt_quit(win, msgoffset, datapath): break
            # Left
            elif _key == curses.KEY_LEFT:
                if (cursor % TABLE_COLS) != 0:
                    cursor -= 1
            # Right
            elif _key == curses.KEY_RIGHT:
                    if (cursor % TABLE_COLS) != TABLE_COLS - 1:
                        cursor += 1
            # Up
            elif _key == curses.KEY_UP:
                if (cursor // TABLE_COLS) != 0:
                    cursor -= TABLE_COLS
            # Down
            elif _key == curses.KEY_DOWN:
                if (cursor // TABLE_COLS) != TABLE_ROWS - 1:
                    cursor += TABLE_COLS
            # Char
            elif _key in KEY2CHAR:
                data[cursor] = KEY2CHAR[_key]
            #endregion
    finally:
        curses.curs_set(1)
    return 0

def wrapped(win:curses.window):
    global exit_code
    exit_code = main(win)

if __name__ == "__main__":
    # Main
    curses.wrapper(wrapped)
    # Print python source (if requested)
    if exit_print:
        print("_C_BORDERCHARS = [\\")
        for _y in range(16):
            print("    ", end = '')
            for _x in range(16):
                if _x > 0: print(f" ", end='')
                _item = data[_y * 16 + _x]
                print(f"0x{_item:02X}", end=',')
            print('\\' if (_y < 15) else ']')
    # Exit
    sys.exit(exit_code)