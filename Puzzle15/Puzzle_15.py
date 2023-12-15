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


################################
# Part (a)
################################

def HASH_alg(s:str, verbose = False) -> int:
  value = 0
  for char in s:
    if verbose: print(char)
    a = ord(char)
    if verbose: print("ASCII value of " + char + " is " + str(a))
    if verbose: print("Adding " + str(a) + " to " + str(value) + " gives: ", end = '')
    value += a
    if verbose: print(value)
    if verbose: print("Multiplying " + str(value) + " by 17 " + " gives: ", end = '')
    value = value * 17
    if verbose: print(value)
    if verbose: print("Reducing " + str(value) + " mod 256 " + " gives: ", end = '')
    value = value % 256
    if verbose: print(value)
  return value

print(HASH_alg("HASH"))

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