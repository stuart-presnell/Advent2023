# https://adventofcode.com/2023/day/18

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
  ip_file = f.read().splitlines()
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