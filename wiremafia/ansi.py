"""
ANSI, as in the escape characters that trigger actions in the terminal.

Info:
 - https://en.wikipedia.org/wiki/ANSI_escape_code
 - http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
 - http://ascii-table.com/ansi-escape-sequences-vt-100.php
"""

# The escape character in Python
esc = '\x1b['

# The escape characters to clear a line
clearline =  esc + '2K' + esc + '1G'

# To save the cursor state
save = esc + "7"

# To restore the cursor state
restore = esc + "8"

# Move up "n" spaces
def up(n=1):
    return esc + str(n) + 'A'

# Move down "n" spaces
def down(n=1):
    return esc + str(n) + 'B'

def code(code1):
    return "\x1b[%sm" % str(code1)

END = code(0)
BOLD = code(1)
DIM = code(2)
UNDERLINE = code(4)
RED = code(31)
GREEN = code(32)
YELLOW = code(33)
BLUE = code(34)
PURPLE = code(35)
CYAN = code(36)
GRAY = code(37)
BRED = RED + BOLD
BGREEN = GREEN + BOLD
BYELLOW = YELLOW + BOLD
BBLUE = BLUE + BOLD
BPURPLE = PURPLE + BOLD
BCYAN = CYAN + BOLD
BGRAY = GRAY + BOLD

class Getch: # Please note that this only works with Linux and OSX
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x1b": # To make sure that it gets the ENTIRE arrow key characters
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = Getch()