# Stubs for re
# Ron Murawski <ron@horizonchess.com>
# 'bytes' support added by Jukka Lehtosalo

# based on: http://docs.python.org/3.2/library/re.html
# and http://hg.python.org/cpython/file/618ea5612e83/Lib/re.py

from typing import (
    List, Iterator, Callable, Tuple, Sequence, Dict, Union,
    Generic, AnyStr, Match, Pattern
)

# ----- re variables and constants -----
A = 0
ASCII = 0
DEBUG = 0
I = 0
IGNORECASE = 0
L = 0
LOCALE = 0
M = 0
MULTILINE = 0
S = 0
DOTALL = 0
X = 0
VERBOSE = 0
U = 0
UNICODE = 0

class error(Exception): ...

def compile(pattern: AnyStr, flags: int = ...) -> Pattern[AnyStr]: ...
def search(pattern: AnyStr, string: AnyStr,
           flags: int = ...) -> Match[AnyStr]: ...
def match(pattern: AnyStr, string: AnyStr,
          flags: int = ...) -> Match[AnyStr]: ...
def split(pattern: AnyStr, string: AnyStr, maxsplit: int = ...,
          flags: int = ...) -> List[AnyStr]: ...
def findall(pattern: AnyStr, string: AnyStr,
            flags: int = ...) -> List[AnyStr]: ...

# Return an iterator yielding match objects over all non-overlapping matches
# for the RE pattern in string. The string is scanned left-to-right, and
# matches are returned in the order found. Empty matches are included in the
# result unless they touch the beginning of another match.
def finditer(pattern: AnyStr, string: AnyStr,
             flags: int = ...) -> Iterator[Match[AnyStr]]: ...

def sub(pattern: AnyStr, repl: Union[AnyStr, Callable[[Match[AnyStr]], AnyStr]],
        string: AnyStr, count: int = ..., flags: int = ...) -> AnyStr: ...

def subn(pattern: AnyStr, repl: Union[AnyStr, Callable[[Match[AnyStr]], AnyStr]],
         string: AnyStr, count: int = ..., flags: int = ...) -> Tuple[AnyStr, int]:
    ...

def escape(string: AnyStr) -> AnyStr: ...

def purge() -> None: ...
