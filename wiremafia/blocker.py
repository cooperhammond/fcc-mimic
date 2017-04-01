import os, sys
from .ansi import *
import subprocess

def get_sudo():
    # you need sudo access for changing wifi groups
    try:
        subprocess.check_call("sudo test .".split(" "))
    except (subprocess.CalledProcessError, OSError):
        print (RED + 'Must have sudo access to manage namespaces and network access.' + END)
        sys.exit(1)

    # set up the namespace "python-blockade" with no network access
    os.system("sudo ip netns add python-blockade > /dev/null 2>&1")


def block_program(program, pid=None):
    get_sudo()
    # Get the current user
    user = os.popen("whoami").read().strip("\n")

    # Kill the running program in order to restart it
    if pid:
        os.system("kill {}".format(pid))

    # Start the program as the current user in the "python-blockade" namespace
    # This really long line means that the started application will still have
    # all of the current user's preferences loaded, rather than root's
    os.system(
        ("sudo ip netns exec python-blockade su {0} -c '{1}'"
        .format(user, program)))