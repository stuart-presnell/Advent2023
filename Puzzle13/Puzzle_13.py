# https://adventofcode.com/2022/day/13

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

test_input = parse_file_a("Puzzle13_test.txt")
input      = parse_file_a("Puzzle13_input.txt")

################################
# Part (a)
################################

# def main_a(ip):
#   pass

# main_a(test_input)  # 
# main_a(input)       # 


################################
# Part (b)
################################

# def main_b(ip):
#   pass

# main_b(test_input)  # 
# main_b(input)       # 


################################

# TTT.timecheck("Final")