# https://adventofcode.com/2023/day/11

# My utility functions
from utils import (
# chunk_splitlines, printT, 
show, 
# showM, parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
Timer,
)

# from time import perf_counter
# TIMING = False
# if TIMING: start_time = perf_counter()

# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle11_test.txt")
input      = parse_file_a("Puzzle11_input.txt")

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
# if TIMING:
#   end_time = perf_counter()
#   print()
#   print("Time taken: ", (end_time - start_time)*1000, "ms")

# TTT.timecheck("Final")