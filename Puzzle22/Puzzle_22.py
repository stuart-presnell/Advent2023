# https://adventofcode.com/2023/day/22

# My utility functions
# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def altitude(L):
  '''The `z`-coordinate of the lowest block of the brick.'''
  return min(L[2], L[5])

def parse_file_a(filename):
  '''Parse each line of the file as a list of 6 integers and sort them into order of altitude.'''
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  op = []
  for line in ip_file:
    line = [item.split(',') for item in line.split('~')]
    line = line[0] + line[1]
    line = [int(n) for n in line]
    op.append(line)
  # Finally, sort the bricks into order of altitude 
  op.sort(key = lambda L: min(L[2], L[5]))
  return op

test_input = parse_file_a("Puzzle22_test.txt")
input      = parse_file_a("Puzzle22_input.txt")

ip = test_input
# ip = input
show(ip)

################################
# Part (a)
################################

# def main_a(ip_file):
#   pass

# print(main_a("Puzzle22_test.txt"))  # 
# print(main_a("Puzzle22_input.txt"))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# print(main_b("Puzzle22_test.txt"))  # 
# print(main_b("Puzzle22_input.txt"))       # 

# TTT.timecheck("Part (b)")  #

################################