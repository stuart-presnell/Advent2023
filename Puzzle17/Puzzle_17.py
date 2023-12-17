# https://adventofcode.com/2023/day/17

from math import inf

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = [[int(n) for n in list(row)] for row in f.read().splitlines()]
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle17_test.txt")
input      = parse_file_a("Puzzle17_input.txt")

ip = test_input
# ip = input
show(ip)

################################
# Part (a)
################################

# How to step in each cardinal direction (change in row, change in column)
dir_lookup = {
  'N':(-1,0),
  'S':( 1,0),
  'W':(0,-1),
  'E':(0, 1)
}

ht = len(ip)
wd = len(ip[0])

def one_step(pt, dir):
  step = dir_lookup[dir]
  nr = pt[0] + step[0]
  nc = pt[1] + step[1]
  if (0 <= nr < ht) & (0 <= nc < wd):
    return (nr, nc)
  else:
    # print(str((nr,nc)) + " is off the grid, so skip this!")
    return None

# new_pt = one_step(pt, dir)

# Starting point is top left corner
O = (0,0)
# Destination is bottom right corner
D = (ht-1, wd-1)




# def main_a(ip_file):
#   pass

# print(main_a(test_input))  # 
# print(main_a(input))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################