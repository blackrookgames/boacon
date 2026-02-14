import curses
import sys
import time

import lib as boacon

def main():
    boacon.init()
    try:
        while True:
            assert boacon._f_win is not None
            ch = boacon.getch()
            if ch == 0x1B: return 0
            boacon._m_setchr_nocolor(0, 0, boacon.BCChar(0x30, attr = boacon.attr_create(color = 2, emp = True)))
            boacon._f_win.refresh()
            time.sleep(0.05)
    finally:
        boacon.final()
    return 0

if __name__ == '__main__':
    sys.exit(main())