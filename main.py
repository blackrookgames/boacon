import curses
import sys
import time
from typing import Callable

import lib as boacon

class TestPane(boacon.BCPane):
    def _draw(self, setchr: Callable[[int, int, boacon.BCChar], None]):
        super()._draw(setchr)
        for y in range(self.y.cliplen):
            for x in range(self.x.cliplen):
                setchr(\
                    self.x.clip0 + x,\
                    self.y.clip0 + y,\
                    boacon.BCChar(0x5A))

def main():
    boacon.init()
    try:
        testpane = TestPane()
        testpane.x.dis0 = 3
        testpane.x.dis1 = 3
        testpane.y.dis0 = 3
        testpane.y.dis1 = 3
        boacon.panes().append(testpane)
        while True:
            ch = boacon.getch()
            if ch == 0x1B: break
            boacon.refresh()
    finally:
        boacon.final()
    return 0

if __name__ == '__main__':
    sys.exit(main())