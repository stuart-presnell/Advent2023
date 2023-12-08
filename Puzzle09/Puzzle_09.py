# https://adventofcode.com/2023/day/09

# My utility functions
from utils import (
show,
# chunk_splitlines,
# parse_nums,
# rotate90,
# close_bracket
)

from time import perf_counter
TIMING = False
if TIMING: start_time = perf_counter()

################################

f = open("Puzzle09_test.txt")
test_input = f.read().splitlines()
f.close()

f = open("Puzzle09_input.txt")
input = f.read().splitlines()
f.close()

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
if TIMING:
  end_time = perf_counter()
  print()
  print("Time taken: ", (end_time - start_time)*1000, "ms")