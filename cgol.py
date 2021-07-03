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
                print("*", end="")
            else:
                print(" ", end="")
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
    return grid


def next_gen(grid: list, y: int, x: int):
    new = grid.copy()
    cb = ((-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1), (0, 1), (1, 0), (1, 1))
    breakpoint()
    for i in range(y):
        for j in range(x):
            neigh = 0
            for k in cb:
                if 0 <= i+k[0] < y and 0 <= j+k[1] < x:
                    if grid[i+k[0]][j+k[1]]:
                        neigh += 1
            if grid[i][j] and (neigh < 2 or neigh > 3):
                new[i][j] = False
            elif not grid[i][j] and neigh == 3:
                new[i][j] = True
    return new


def start(x: int, y: int, t: int):
    grid = []
    grid = gen_grid(grid, y, x)
    try:
        while True:
            print_grid(grid, y, x)
            next_gen(grid, y, x)
            time.sleep(t)
            print(f"\033[{y+2}A", end="")

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
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
        "-t", default=1, type=int,
        help="refresh time, default 1")
    args = arg.parse_args()
    start(args.x, args.y, args.t)
