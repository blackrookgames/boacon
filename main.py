import curses
import sys
import time

from datetime import datetime

import lib as boacon

def postdraw(win:curses.window):
    win.addstr(0, 0, str(datetime.now()))

def main():
    boacon.init()
    try:
        # Pane
        pane = boacon.BCConsolePane()
        pane.x.dis0 = 3
        pane.x.len = 20
        pane.y.dis0 = 3
        pane.y.dis1 = 3
        pane.print("Line 1\nLine 2\nLine 3\nLine 4")
        pane.print()
        pane.print("Hello world!!!")
        pane.print("This sentence takes multiple lines.")
        boacon.panes().append(pane)
        # Post draw
        boacon.postdraw().connect(postdraw)
        # Loop
        while True:
            ch = boacon.getch()
            if ch == 0x1B: break
            boacon.refresh()
            time.sleep(0.05)
    finally:
        boacon.final()
    return 0

if __name__ == '__main__':
    sys.exit(main())