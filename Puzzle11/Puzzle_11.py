# https://adventofcode.com/2023/day/11

# My utility functions
from utils import (
# chunk_splitlines, printT, 
show, 
# showM, parse_nums, 
rotate90, 
# close_bracket, cmp, qsort, Best, 
Timer,
)

# from time import perf_counter
# TIMING = False
# if TIMING: start_time = perf_counter()

TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle11_test.txt")    # There are 9 '#'s in test_input
input      = parse_file_a("Puzzle11_input.txt")   # There are 455 '#'s in input

expansion_test1 = parse_file_a("expansion_test1.txt")

matrix = test_input
show(matrix)

def duplicate_empty_rows(M):
  op = []
  for row in M:
    if '#' in row:
      op.append(row)
    else:
      op.append(row)
      op.append(row)
  return op

def expand_universe(M):
  M = duplicate_empty_rows(M)
  M = rotate90(M)
  M = duplicate_empty_rows(M)
  M = rotate90(M)
  M = rotate90(M)
  M = rotate90(M)
  M = ["".join(row) for row in M]
  return M

matrix = expand_universe(matrix)

TTT.timecheck("Expand")

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