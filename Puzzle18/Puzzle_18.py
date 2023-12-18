# https://adventofcode.com/2023/day/18

from math import inf

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, parse_nums, rotate90, close_bracket, cmp, qsort, 
Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = [line.split() for line in f.read().splitlines()]
  ip_file = [[d, int(n), c] for [d, n, c] in ip_file]
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle18_test.txt")
input      = parse_file_a("Puzzle18_input.txt")

ip = test_input
# ip = input
# show(ip)

################################
# Part (a)
################################

# How to step in each cardinal direction (change in row, change in column)
dir_lookup = {
  'U':(-1,0),
  'D':( 1,0),
  'L':(0,-1),
  'R':(0, 1)
}

def n_steps(dug, pt, dir, n = 1):
  '''Given a set of `dug` squares, a starting `pt`, a `dir` and a number of squares to dig, 
  return an updated `dug` and a new position.'''
  (r,c) = pt
  match dir:
    case 'U': 
      for i in range(n):
        dug.add((r-i-1, c))
      return (dug, (r-n, c))
    case 'D': 
      for i in range(n):
        dug.add((r+i+1, c))
      return (dug, (r+n, c))
    case 'R': 
      for i in range(n):
        dug.add((r, c+i+1))
      return (dug, (r, c+n))
    case 'L': 
      for i in range(n):
        dug.add((r, c-i-1))
      return (dug, (r, c-n))
  
def follow_instr(ip):
  pt = (0,0)        # Initial square is defined to be (0,0)
  dug = {(0,0)}     # Set of squares that have been dug out
  for [dir, n, _] in ip:
    (dug, pt) = n_steps(dug, pt, dir, n)
  return dug

dug = follow_instr(test_input)
# dug = list(dug)
# dug.sort()
# print(dug)

def get_dimensions(L):
  '''Extract the min and max dimensions of the list of points.'''
  min_r = Best(inf, lambda x,y:x<y)
  min_c = Best(inf, lambda x,y:x<y)
  max_r = Best(-inf, lambda x,y:x>y)
  max_c = Best(-inf, lambda x,y:x>y)
  min_r.reduce([pt[0] for pt in L])
  max_r.reduce([pt[0] for pt in L])
  min_c.reduce([pt[1] for pt in L])
  max_c.reduce([pt[1] for pt in L])
  return (min_r.best_so_far,min_c.best_so_far,max_r.best_so_far,max_c.best_so_far)


def display_grid(S):
  '''Show the subset of points included in set `S`.'''
  (min_r, min_c, max_r, max_c) = get_dimensions(S)
  for row in range(min_r, max_r+1):
    for col in range(min_c, max_c+1):
      print('#' if (row,col) in S else '.', end='')
    print()

display_grid(dug)
# print(len(dug)) # 38
print()

def fill_row(dug, row, min_c, max_c):
  '''Given a set of dug points, a row, and the max and min cols for that row, 
  fill the interior of the row and return `dug` with those extra pts.'''
  INSIDE = False
  for col in range(min_c-1, max_c+1):
    if (row,col) in dug:
      INSIDE = not INSIDE  # flip INSIDE status when we hit a '#'
    if INSIDE & ((row,col) not in dug):
      dug.add((row,col))
  return dug

(min_r, min_c, max_r, max_c) = get_dimensions(dug)

for row in range(min_r, max_r+1):
  dug = fill_row(dug, row, min_c, max_c)
# display_grid(dug)


def flood_fill(dug, seed):
  (r,c) = seed
  if seed in dug:
    return dug
  else:  # fill this square and flood fill starting from the 4 cardinal neighbours
    dug.add(seed)
    dug = flood_fill(dug, (r-1,c))
    dug = flood_fill(dug, (r+1,c))
    dug = flood_fill(dug, (r,c+1))
    dug = flood_fill(dug, (r,c-1))
  return dug


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