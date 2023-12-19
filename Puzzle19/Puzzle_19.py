# https://adventofcode.com/2023/day/19

# My utility functions
from utils import (
show, 
chunk_splitlines, 
printT, showM, showD, parse_nums, rotate90, 
# close_bracket, cmp, qsort, nwise_cycled,
# Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = chunk_splitlines(f.read())
  # .splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle19_test.txt")
input      = parse_file_a("Puzzle19_input.txt")

ip = test_input
# ip = input
# show(ip[1])

def parse_machine_part(s):
  '''Given a string such as `'{x=787,m=2655,a=1222,s=2876}'`, return a dictionary.'''
  d = {}
  for item in s[1:-1].split(","):
    [l,n] = item.split('=')
    d[l] = int(n)
  return d

# parse_machine_part('{x=787,m=2655,a=1222,s=2876}')

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