"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import sys
import copy
import ctypes
from getpass import getpass
from collections import namedtuple
from functools import partial

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.5.0"

#: A menu entry that can call a function when selected.
MenuEntry = namedtuple("MenuEntry", "name desc func args krgs")

#: Prompt start character sequence.
QSTR = "[?] "

#: User input start character sequence.
ISTR = ": "

#: User input function.
_input = input if sys.version_info >= (3, 0) else raw_input

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class Menu:
    """Menu object that will show the associated MenuEntry items."""
    def __init__(self, entries=None, **kwargs):
        """Initializes menu object. Any kwargs supplied will be passed as
        defaults to show_menu()."""
        self.entries = entries or []
        self._show_kwargs = kwargs
    def add(self, name, desc, func=None, args=None, krgs=None):
        """Add a menu entry."""
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def enum(self, desc, func=None, args=None, krgs=None):
        """Add a menu entry."""
        name = str(len(self.entries))
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def show(self, **kwargs):
        """Shows the menu."""
        self._show_kwargs.update(kwargs)
        return show_menu(self.entries, **self._show_kwargs)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

try:
    print("", end="", flush=True)
    echo = partial(print, end="\n", flush=True)
except TypeError:
    # TypeError: 'flush' is an invalid keyword argument for this function
    def echo(text, end="\n", flush=True):
        """Generic echo/print function; based off code from ``blessed`` package."""
        sys.stdout.write(u'{0}{1}'.format(text, end))
        if flush:
            sys.stdout.flush()

def show_limit(entries, **kwargs):
    """Shows a menu but limits the number of entries shown at a time.
    Functionally equivalent to show_menu() with the limit parameter set."""
    limit = kwargs.pop('limit', 5)
    if limit <= 0:
        limit = 1
    istart = 0 # Index of group start.
    iend = limit # Index of group end.
    while True:
        if istart < 0:
            istart = 0
            iend = limit
        if iend > len(entries):
            iend = len(entries)
            istart = iend - limit
        unext = len(entries) - iend # Number of next entries.
        uprev = istart # Number of previous entries.
        nnext = "" # Name of 'next' menu entry.
        nprev = "" # Name of 'prev' menu entry.
        dnext = "" # Description of 'next' menu entry.
        dprev = "" # Description of 'prev' menu entry.
        group = copy.deepcopy(entries[istart:iend])
        names = [i.name for i in group]
        if unext:
            for i in ["n", "N", "next", "NEXT", "->", ">>", ">>>"]:
                if i not in names:
                    nnext = i
                    dnext = "Next %u entries." % (unext)
                    group.append(MenuEntry(nnext, dnext, None, None, None))
                    break
        if uprev:
            for i in ["p", "P", "prev", "PREV", "<-", "<<", "<<<"]:
                if i not in names:
                    nprev = i
                    dprev = "Previous %u entries." % (uprev)
                    group.append(MenuEntry(nprev, dprev, None, None, None))
                    break
        result = show_menu(group, **kwargs)
        if result == nnext or result == dnext:
            istart += limit
            iend += limit
        elif result == nprev or result == dprev:
            istart -= limit
            iend -= limit
        else:
            return result

def show_menu(entries, **kwargs):
    """Showns a menu with the given list of MenuEntry items.

    **Params**:
      - header (str) - String to show above menu.
      - msg (str) - String to show below menu.
      - compact (bool) - If true, the menu items will not be displayed.
      - returns (str) - Controls what part of the menu entry is returned.
      - limit (int) - If set, limits the number of menu entries show at a time.
    """
    header = kwargs.get('header', "** MENU **")
    msg = kwargs.get('msg', "Enter menu selection")
    compact = kwargs.get('compact', False)
    returns = kwargs.get('returns', "name")
    limit = kwargs.get('limit', None)
    if limit:
        return show_limit(entries, **kwargs)
    def show_banner():
        echo(header)
        for i in entries:
            echo("  (%s) %s" % (i.name, i.desc))
    valid = [i.name for i in entries]
    if not compact:
        show_banner()
    choice = ask(msg, vld=valid)
    entry = [i for i in entries if i.name == choice][0]
    if entry.func:
        if entry.args and entry.krgs:
            entry.func(*entry.args, **entry.krgs)
        elif entry.args:
            entry.func(*entry.args)
        elif entry.krgs:
            entry.func(**entry.krgs)
        else:
            entry.func()
    if "desc" == returns:
        return entry.desc
    return choice

def enum_menu(strs, start=0, **kwargs):
    """Enumerates the given list of strings into a menu."""
    entries = []
    for i,s in enumerate(strs, start):
        entries.append(MenuEntry(str(i), str(s), None, None, None))
    return show_menu(entries, **kwargs)

def cast(val, typ=int):
    """Attempts to cast the given value to the given type otherwise None is
    returned."""
    try:
        val = typ(val)
    except:
        val = None
    return val

def ask(msg="Enter input", dft=None, vld=None, fmt=lambda x: x, shw=True, blk=False):
    """Prompts the user for input and returns the given answer. Optionally
    checks if answer is valid.

    **Params:**
      - msg (str) - Message to prompt the user with.
      - dft (int|float|str) - Default value if input is left blank.
      - vld ([int|float|str]) - Valid input entries.
      - fmt (func) - Function used to format user input.
      - shw (bool) - If true, show the user's input as typed.
      - blk (bool) - If true, accept a blank string as valid input.
    """
    vld = vld or []
    msg = "%s%s" % (QSTR, msg)
    if dft != None:
        dft = fmt(dft)
        msg += " [%s]" % (dft if type(dft) is str else repr(dft))
        vld.append(dft)
    if vld:
        # Sanitize valid inputs.
        vld = sorted(list(set([fmt(v) if fmt(v) else v for v in vld ])))
    msg += ISTR
    ans = None
    while ans is None:
        get_input = _input if shw else getpass
        ans = get_input(msg)
        if "?" == ans:
            if vld:
                echo(vld)
            ans = None
            continue
        if "" == ans:
            if dft != None:
                ans = dft if not fmt else fmt(dft)
                break
            if not blk:
                ans = None
                continue
        try:
            ans = ans if not fmt else fmt(ans)
        except:
            ans = None
        if vld:
            for v in vld:
                if type(v) is type and cast(ans, v) is not None:
                    ans = cast(ans, v)
                    break
                elif ans in vld:
                    break
            else:
                ans = None
    return ans

def ask_yesno(msg="Proceed?", dft=None):
    """Prompts the user for a yes or no answer. Returns True for yes, False
    for no."""
    yes = ["y", "yes", "Y", "YES"]
    no = ["n", "no", "N", "NO"]
    if dft != None:
        dft = yes[0] if (dft in yes or dft == True) else no[0]
    return ask(msg, dft=dft, vld=yes+no) in yes

def ask_int(msg="Enter an integer", dft=None, vld=[int]):
    """Prompts the user for an integer."""
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=int))

def ask_float(msg="Enter a float", dft=None, vld=[float]):
    """Prompts the user for a float."""
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=float))

def ask_str(msg="Enter a string", dft=None, vld=[str], shw=True, blk=True):
    """Prompts the user for a string."""
    return ask(msg, dft=dft, vld=vld, shw=shw, blk=blk)

def pause():
    """Pauses and waits for user interaction."""
    getpass("Press ENTER to continue...")

def status(*args, **kwargs):
    """Prints a status message at the start and finish of an associated
    function. Can be used as a function decorator or as a function that accepts
    another function as the first parameter.

    **Params:**
      - msg (str) [args] - Message to print at start of `func`.
      - func (func) - Function to call. First `args` if using `status()` as a
        function. Automatically provided if using `status()` as a decorator.
      - args (list) - Remainder of `args` are passed to `func`.
      - fin (str) [kwargs] - Message to print when `func` finishes.
      - kwargs (dict) - Remainder of `kwargs` are passed to `func`.
    """
    def decor(func):
        def wrapper(*fargs, **fkwargs):
            echo("[!] " + msg, end=" ", flush=True)
            result = func(*fargs, **fkwargs)
            echo(fin, flush=True)
            return result
        return wrapper
    fin = kwargs.pop('fin', "DONE.")
    args = list(args)
    if len(args) > 1 and callable(args[1]):
        msg = args.pop(0)
        func = args.pop(0)
        return decor(func)(*args, **kwargs)
    msg = args.pop(0)
    return decor

def alert(msg, **kwargs):
    """Prints alert message to console."""
    echo("[!] " + msg, **kwargs)

def error(msg, **kwargs):
    """Prints error message to console."""
    echo("[ERROR] " + msg, **kwargs)

def warn(msg, **kwargs):
    """Prints warning message to console."""
    echo("[WARNING] " + msg, **kwargs)

def title(msg):
    """Sets the title of the console window."""
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleA(msg)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
