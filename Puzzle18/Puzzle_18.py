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
show(ip)

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
        dug.add((r+i+1, c))
      return (dug, (r+n, c))
    case 'D': 
      for i in range(n):
        dug.add((r-i-1, c))
      return (dug, (r-n, c))
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
  min_x = Best(inf, lambda x,y:x<y)
  min_y = Best(inf, lambda x,y:x<y)
  max_x = Best(-inf, lambda x,y:x>y)
  max_y = Best(-inf, lambda x,y:x>y)
  min_x.reduce([pt[0] for pt in L])
  max_x.reduce([pt[0] for pt in L])
  min_y.reduce([pt[1] for pt in L])
  max_y.reduce([pt[1] for pt in L])
  return (min_x.best_so_far,min_y.best_so_far,max_x.best_so_far,max_y.best_so_far)

print(get_dimensions(dug))

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