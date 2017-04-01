# -*- coding: UTF-8 -*-
from wiremafia.blocker import block_program
from wiremafia.ansi import *
import os, sys
import draftlog

draft = draftlog.inject()

def list_processes():
    return os.popen("ps -A").read().split("\n")[1:-1]

def list_range(offset, length, l):
    # this handles both negative offsets and offsets larger than list length
    if len(l) == 0: return []
    start = offset % len(l)
    end = (start + length) % len(l)
    if end > start:
        return l[start:end]
    return l[start:] + l[:end]

class UserInput:
    def __init__(self):
        self.processes = list_processes()
        self.typing_string = ("{0}?{1} {2}Running processes: {3}"
            .format(GREEN, END, BOLD, END))
        self.waiting_string = (self.typing_string + "{0}(type to search or enter new process){1}"
            .format(DIM, END))
        self.log = draft.log(self.waiting_string)
        self.search = ""

    def parse_input(self, key):
        log = self.log # Ease of access

        # Get rid of the parentheses while typing
        if log.current_text() == self.waiting_string:
            log.update(self.typing_string)

        if "\\x" not in repr(key): # Check if it's not an escape character
            log.update(log.current_text() + key)
            self.search += key
        elif key == "\x7f" and len(self.log.current_text()) > len(self.typing_string):
            # Check if it's a backspace and that it won't delete the "typing_string"
            log.update(log.current_text()[:-1])
            self.search = self.search[:-1]

        # reset the text if no chars are being input
        if len(log.current_text()) == len(self.typing_string):
            log.update(self.waiting_string)

        self.search_processes()

    def give_output(self, klass):
        self.output_list = klass

    def search_processes(self):
        self.processes = list_processes()
        self.processes = [s for s in self.processes if self.search in s]

        self.output_list._shift()



class OutputList:
    def __init__(self, input, r):
        self.r = r
        self.user_input = input
        self.processes = self.user_input.processes
        self.update_processes()
        self.logs = []
        for process in self.list:
            self.logs.append(draft.log(process["text"]))
        self.bottom_text = DIM + "Press enter to restart the process without network." + END
        self.bottom_log = draft.log(self.bottom_text)
        self.select_process(max(self.r[0], self.r[1]) / 2)
        self.results = True

    def update_processes(self):
        self.processes = self.user_input.processes
        self.list = list_range(self.r[0], self.r[1], self.processes)
        self.list = list(map(self.parse_process, self.list))

    def format_process(self, process):
        return "  " + process["name"] + " " + DIM + process["pid"] + END

    def parse_process(self, process):
        process = (' '.join(process.split())).split(" ")
        process = {
            "pid":  process[0],
            "name": process[-1],
        }
        process["text"] = self.format_process(process)
        return process

    def select_process(self, index):
        index = int(index)
        while True:
            try:
                self.logs[index].update(CYAN + "❯ " + self.logs[index].current_text()[2:] + END)
            except KeyError:
                if len(self.logs) >= 1:
                    index -= 1
                    continue
            break

    def cr(self, n):
        self.r = list(map((lambda x: x + n), self.r))

    def down(self):
        self.cr(1)
        self._shift()

    def up(self):
        self.cr(-1)
        self._shift()

    def _shift(self):
        self.update_processes()
        if len(self.list) != 0:
            self.bottom_log.update(self.bottom_text)
            self.results = True
            tmp_processes = []
            for i, log in enumerate(self.logs):
                tmp_processes.append(self.list[i % len(self.list)])
                log.update(self.list[i % len(self.list)]["text"])

            self.select_process(abs(self.r[0] - self.r[1]) / 2)
            self.choice = tmp_processes[int(abs(self.r[0] - self.r[1]) / 2)]
        else:
            for log in self.logs: log.update("")
            self.results = False
            self.bottom_log.update("")
            self.logs[int((len(self.logs) / 2 - 1) % len(self.logs))].update(YELLOW + "No processes found." + END)
            self.logs[int((len(self.logs) / 2) % len(self.logs))].update(
            YELLOW + 'Press enter to start "{}" without network.'.format(self.user_input.search) + END)


def rr(r):
    return range(r[0], r[1])

def main():
    r = [0, 7] # [offset, length]
    user_input = UserInput()
    output_list = OutputList(user_input, r)
    user_input.give_output(output_list)


    while True:
        key = getch() # Start input for ONE key press

        if key in ("\x03", "\x04"): # The keys for ^C and ^D
            break

        elif key == "\x1b[A": # up arrow
            output_list.up()

        elif key == "\x1b[B": # down arrow
            output_list.down()

        elif key == "\r": # enter key (this surprised me, but made sense when I thought about it)
            if output_list.results == True:
                block_program(output_list.choice["name"], pid=output_list.choice["pid"])
            else:
                block_program(user_input.search)
            sys.exit()

        else: # put other keys into the search bar
            user_input.parse_input(key)

if __name__ == "__main__":
    main()