# https://adventofcode.com/2023/day/15

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
  ip_file = f.read().split(",")
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle15_test.txt")
input      = parse_file_a("Puzzle15_input.txt")

ip = test_input
# ip = input
# show(ip)
print(len(ip))

################################
# Part (a)
################################

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