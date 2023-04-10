import sys
from math import *
from collections import Counter, deque, defaultdict
from bisect import bisect_left, bisect_right
from heapq import nsmallest, nlargest, heapify, heappop, heappush

input = lambda: sys.stdin.buffer.readline().decode().rstrip()
get_int = lambda: int(input())
get_str = lambda: list(input())
get_list = lambda dtype: [dtype(x) for x in input().split()]
print = lambda *args, end="\n": sys.stdout.write(" ".join([str(x) for x in args]) + end)
yes = lambda: print("YES")
no = lambda: print("NO")


# Solution here
def solve(tt):
    $0


def main():
    test_case = 1
    test_case = get_int()
    for tt in range(1, test_case + 1):
        solve(f"{tt}: -------------------------")
    return


def dbg(*args):
    import inspect
    import re

    debug = lambda *args, end="\n": sys.stderr.write(
        " ".join([str(x) for x in args]) + end
    )
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    var_name = r.split(", ")
    sys.stderr.write("\n")
    for i, (var, val) in enumerate(zip(var_name, args)):
        debug(f"{var} = {val}")


if __name__ == "__main__":
    main()