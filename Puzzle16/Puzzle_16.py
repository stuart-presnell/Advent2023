# https://adventofcode.com/2023/day/16

from collections import OrderedDict

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle16_test.txt")
input      = parse_file_a("Puzzle16_input.txt")

grid = test_input
# grid = input
# show(grid)

ht = len(grid)
wd = len(grid[0])

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

def one_step(pt, dir):
  step = dir_lookup[dir]
  return (pt[0] + step[0], pt[1] + step[1])


# The set of points (r,c) that have a beam passing through
energised = set((0,0))
# The wavefront is an ordered dictionary of points; 
# `wavefront[pt]` is a list of directions in which beams are moving through `pt`
# It's ordered so at each step we can `pop` an element from it to advance
wavefront = OrderedDict()
wavefront[(0,0)] = ['E']

def advance_wave(pt, dir):
  '''Given a point and a direction, advance the beam by one step in that direction, 
  reflecting or splitting as required; 
  put the new point(s) & dir(s) on `wavefront`, and add the points to `energised`.'''
  global energised, wavefront

  # new_pt
  pass

# while wavefront:
#   (pt, dirs) = wavefront.popitem()
#   for dir in dirs:
#     advance_wave(pt, dir)
# show(energised)

# def main_a(ip):
#   pass

# print(main_a(test_input))  # 
# print(main_a(input))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################