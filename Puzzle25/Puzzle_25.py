# https://adventofcode.com/2023/day/25

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
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file("Puzzle25_test.txt")
input      = parse_file("Puzzle25_input.txt")

ip = test_input
# ip = input
show(ip)

################################
# Part (a)
################################

def main_a(ip_filename):
  ip = parse_file(ip_filename)
  pass

# print(main_a("Puzzle25_test.txt"))  # 
# print(main_a("Puzzle25_input.txt")) # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_b("Puzzle25_test.txt"))  # 
# print(main_b("Puzzle25_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################