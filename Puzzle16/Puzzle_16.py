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

# A list of points (r,c) that have a beam passing through
energised = [(0,0)]
# The wavefront is an ordered dictionary of points; 
# `wavefront[pt]` is a list of directions in which beams are moving through `pt`
# It's ordered so at each step we can `pop` an element from it to advance
wavefront = OrderedDict()
wavefront[(0,0)] = ['E']

while wavefront:
  (pt, dirs) = wavefront.popitem()
  pass

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