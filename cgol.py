#!/usr/bin/env python3
import sys
import time
import argparse


def print_grid(grid: list, y: int, x: int):
    print("+"+"-"*x+"+")
    for i in range(y):
        print("|", end="")
        for j in range(x):
            if grid[i][j]:
                print("\033[48;2;0;0;0m \033[m", end="")
            else:
                print("\033[48;2;255;255;255m \033[m", end="")
        print("|", end="")
        print()
    print("+"+"-"*x+"+")


def gen_grid(grid: list, y: int, x: int):
    for i in range(y):
        temp = []
        for j in range(x):
            temp.append(False)
        grid.append(temp)
    inp = b""
    while inp not in ("x", "e"):
        if not isinstance(inp, bytes):
            print(f"\033[{y+5}A", end="")
        print_grid(grid, y, x)
        print("e for exit, x for accepting")
        print(f"x,y (x in <1,{x}>|y in <1,{y}>) for adding/removing ")
        inp = input("> ")
        print(f"\033[{1}A", end="")
        print(" "*80)
        try:
            cellx, celly = inp.split(",")
            cellx = int(cellx)-1
            celly = int(celly)-1
            if 0 <= cellx < x and 0 <= celly < y:
                if grid[celly][cellx]:
                    grid[celly][cellx] = False
                else:
                    grid[celly][cellx] = True
        except Exception:
            pass
    if inp == "e":
        sys.exit(0)
    print(f"\033[{3}A", end="")
    print(" "*80)
    print(" "*80)
    print(" "*80)
    print(f"\033[{5+y}A", end="")
    return grid


def next_gen(grid: list, y: int, x: int, b: bool):
    new = []
    for i in range(y):
        new.append(grid[i].copy())
    cb = ((-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1), (0, 1), (1, 0), (1, 1))
    for i in range(y):
        for j in range(x):
            neigh = 0
            for k in cb:
                ok = [0, 0]
                xn = j+k[1]
                yn = i+k[0]
                if 0 <= yn < y and 0 <= xn < x and b:
                    ok = [yn, xn]
                if not b:
                    ok = [yn, xn]
                    if yn < 0:
                        ok[0] = yn+y
                    if yn > y-1:
                        ok[0] = yn-y
                    if xn < 0:
                        ok[1] = xn+x
                    if xn > x-1:
                        ok[1] = xn-x
                if grid[ok[0]][ok[1]]:
                    neigh += 1
            if grid[i][j] and (neigh < 2 or neigh > 3):
                new[i][j] = False
            elif not grid[i][j] and neigh == 3:
                new[i][j] = True
    return new


def start(y: int, x: int, t: int, b: bool):
    grid = []
    try:
        grid = gen_grid(grid, y, x)
        while True:
            print_grid(grid, y, x)
            grid = next_gen(grid, y, x, b)
            time.sleep(t)
            print(f"\033[{y+2}A", end="")
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)


if __name__ == "__main__":
    import os
    if os.name != "nt":
        import readline
    arg = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Conway's Game of Life implementation")
    arg.add_argument(
        "-x", default=20, type=int,
        help="grid width, default 20")
    arg.add_argument(
        "-y", default=10, type=int,
        help="grid height, default 10")
    arg.add_argument(
        "-t", default=1, type=float,
        help="refresh time in seconds, default 1")
    arg.add_argument(
        "-b", default=False, action="store_true",
        help="blocking grid borders, default False")
    args = arg.parse_args()
    start(args.y, args.x, args.t, args.b)
