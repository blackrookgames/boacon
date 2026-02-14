from .c_BCChar import *
from .c_BCError import *
from .c_BCState import *
from .g_attr import *
from .g_key import *

import curses as _curses

_f_state = BCState.NORUN
_f_win:None|_curses.window = None
_f_win_ok = False
_f_win_w = 0
_f_win_h = 0
_f_color = False

#region helper

def _m_verify_run():
    global _f_state
    if _f_state == BCState.RUN: return
    raise BCError("boacon system is not currently running.")

def _m_setcursor(visible:bool):
    global _f_win, _f_win_ok
    assert _f_win is not None
    # Try to hide normally
    if not _f_win_ok:
        try: _curses.curs_set(1 if visible else 0)
        except _curses.error: _f_win_ok = True
    # Try to hide alternatively
    if _f_win_ok: # Do NOT change to else or elif
        try: _f_win.leaveok(not visible)
        except _curses.error: pass

def _m_setchr_color(x:int, y:int, chr:BCChar):
    global _f_win
    assert _f_win is not None
    attr = _curses.A_STANDOUT if attr_emp(chr.attr) else _curses.A_NORMAL
    attr |= _curses.color_pair(0b111 ^ attr_color(chr.attr))
    try: _f_win.addch(y, x, chr.ord, attr)
    except _curses.error: pass

def _m_setchr_nocolor(x:int, y:int, chr:BCChar):
    global _f_win
    assert _f_win is not None
    attr = _curses.A_STANDOUT if attr_emp(chr.attr) else _curses.A_NORMAL
    try: _f_win.addch(y, x, chr.ord, attr)
    except _curses.error: pass

#endregion

#region init/final

def init():
    global _f_state
    if _f_state != BCState.NORUN: return
    _f_state = BCState.INIT
    # Global vars
    global _f_win, _f_win_w, _f_win_h, _panes
    # Initialize window
    _f_win = _curses.initscr()
    _f_win.keypad(True)
    _f_win.nodelay(True)
    _f_win.clear()
    _f_win_w = 0
    _f_win_h = 0
    # Initialize curses
    _curses.noecho()
    _curses.cbreak()
    _m_setcursor(False)
    # Initialize color
    _curses.start_color()
    if _curses.has_colors() and _curses.COLOR_PAIRS >= 8:
        _curses.init_pair(0b001, _curses.COLOR_CYAN, _curses.COLOR_BLACK)
        _curses.init_pair(0b010, _curses.COLOR_MAGENTA, _curses.COLOR_BLACK)
        _curses.init_pair(0b011, _curses.COLOR_BLUE, _curses.COLOR_BLACK)
        _curses.init_pair(0b100, _curses.COLOR_YELLOW, _curses.COLOR_BLACK)
        _curses.init_pair(0b101, _curses.COLOR_GREEN, _curses.COLOR_BLACK)
        _curses.init_pair(0b110, _curses.COLOR_RED, _curses.COLOR_BLACK)
        _curses.init_pair(0b111, _curses.COLOR_BLACK, _curses.COLOR_BLACK)
        _f_color = True
    else:
        _f_color = False
    # Success!!!
    _f_state = BCState.RUN

def final():
    global _f_state
    if _f_state != BCState.RUN: return
    _f_state = BCState.FINAL
    # Global vars
    global _f_win, _panes
    assert _f_win is not None
    # Finalize curses
    _curses.nocbreak()
    _curses.echo()
    _curses.endwin()
    # Finalize window
    _m_setcursor(True)
    _f_win.nodelay(False)
    _f_win.keypad(False)
    # Success!!!
    _f_state = BCState.NORUN

#endregion

#region "properties"

def state():
    """
    State of the boacon system
    """
    global _f_state
    return _f_state

#endregion

#region functions

def refresh():
    """
    Refreshes the screen
    
    :raise BCError:
        boacon system is not currently running
    """
    _m_verify_run()
    global _f_win, _f_win_w, _f_win_h
    assert _f_win is not None
    # Update size
    _new_h, _new_w = _f_win.getmaxyx()
    if _f_win_w != _new_w or _f_win_h != _new_h:
        _f_win_w = _new_w
        _f_win_h = _new_h
        # TODO: resolve pane dimensions
        #     # Clear
    _f_win.clear()
    _f_win.refresh()
    
def getch():
    """
    Gets a character code from the keyboard
    
    :return:
        Character code (or -1 if no character is pressed)
    :raise BCError:
        boacon system is not currently running
    """
    _m_verify_run()
    global _f_win
    assert _f_win is not None
    return _f_win.getch()

#endregion