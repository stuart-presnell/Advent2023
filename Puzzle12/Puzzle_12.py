# https://adventofcode.com/2023/day/12

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
parse_nums, 
# rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

# The condition records show every spring and whether it is 
# operational (.), damaged (#), or unknown (?)

# After the list of springs for a given row, 
# the size of each contiguous group of damaged springs is listed in the order those groups appear.
# This list always accounts for every damaged spring, 
# and each number is the entire size of its contiguous group 
# (that is, groups are always separated by at least one operational spring: 
# #### would always be 4, never 2,2).

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  ip_file = [line.split() for line in ip_file]
  ip_file = [[c, parse_nums(n, ",")] for [c,n] in ip_file] 
  return ip_file

test_input = parse_file_a("Puzzle12_test.txt")
input      = parse_file_a("Puzzle12_input.txt")

show(test_input)

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