# https://adventofcode.com/2023/day/24

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def parse_file(filename):
  '''Parse the input file into a list of positions and velocities, 
  each represented as a tuple of three `int`s.'''
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  op = []
  for line in ip_file:
    [pos, vel] = line.split(" @ ")
    pos = tuple([int(x) for x in pos.split(", ")])
    vel = tuple([int(x) for x in vel.split(", ")])
    op.append([pos, vel])
  return op

test_input = parse_file("Puzzle24_test.txt")
input      = parse_file("Puzzle24_input.txt")

ip = test_input
# ip = input
show(ip)

################################
# Part (a)
################################

def main_a(ip_filename):
  ip = parse_file(ip_filename)
  pass

# print(main_a("Puzzle24_test.txt"))  # 
# print(main_a("Puzzle24_input.txt")) # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_b("Puzzle24_test.txt"))  # 
# print(main_b("Puzzle24_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################