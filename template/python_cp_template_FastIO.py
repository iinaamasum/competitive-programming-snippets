"""
    Author   : @iinaamasum
    Mail     : iinaamasum@gmail.com
    GitHub   : https://github.com/iinaamasum
    LinkedIn : https://www.linkedin.com/in/iinaamasum/
"""
import sys

input = sys.stdin.readline
get_int = lambda: int(input())
get_ints = lambda: map(int, input().split())
get_list = lambda: list(map(int, input().split()))
get_str = lambda: input().rstrip("\n\r")
get_list_str = lambda: list(map(str, input().rstrip("\n\r").split(" ")))
output = lambda *args, end="\n": sys.stdout.write(
    " ".join([str(x) for x in args]) + end
)
yes = lambda: output("YES")
no = lambda: output("NO")

# Solution here
def solve():
    


def main():
    test_case = 1
    test_case = get_int()
    while test_case:
        solve()
        test_case -= 1
    return


if __name__ == "__main__":
    main()
