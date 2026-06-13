import curses
import sys
import time

import boacon

DELAY = 0.05

time_alive = 0.0

def postdraw(args:boacon.BCPostDrawArgs):
    global time_alive
    args.win.addstr(0, 1, f"{time_alive:.2f} sec")

def on_init():
    boacon.postdraw().connect(postdraw)

def on_final():
    boacon.postdraw().disconnect(postdraw)

def main():
    global time_alive
    boacon.on_init().connect(on_init)
    boacon.on_final().connect(on_final)
    boacon.init()
    try:
        # Pane
        pane = boacon.BCConsolePane()
        pane.x.dis0 = 3
        pane.x.dis1 = 3
        pane.y.dis0 = 3
        pane.y.dis1 = 3
        pane.print("Line 1\nLine 2\nLine 3\nLine 4")
        pane.print()
        pane.print("Hello world!!!")
        pane.print("Press Esc to exit.")
        boacon.panes().append(pane)
        # Loop
        while True:
            ch = boacon.getch()
            if ch == 0x1B: break
            boacon.refresh()
            time.sleep(DELAY)
            time_alive += DELAY # Assume the pause took exactly this long
    finally:
        boacon.final()
    return 0

if __name__ == '__main__':
    sys.exit(main())