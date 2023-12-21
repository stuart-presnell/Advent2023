# https://adventofcode.com/2023/day/21

# My utility functions
# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  for r in range(len(ip_file)):
    if 'S' in ip_file[r]:
      col = ip_file[r].index('S')
      start = (r,col)
      break
  return ip_file, start

test_input = parse_file_a("Puzzle21_test.txt")
input      = parse_file_a("Puzzle21_input.txt")

# (M, S) = test_input
(M, S) = input
# show(M)
# print(S)

ht = len(M)
wd = len(M[0])

def free(r,c):
  if (0 <= r < ht) & (0 <= c < wd):
    return (M[r][c] != '#')
  else:
    return False

# Where could we be standing now?
current = {S}

def step(current):
  '''Return all the free spaces that are 1 step away from a current position.'''
  op = set()
  for (r,c) in current:
    ngb = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    for pos in ngb:
      if free(*pos):
        op.add(pos)
  return op

def n_steps(current, n):
  for _ in range(n):
    current = step(current)
  return current

print(len(n_steps(current, 64))) # 3532

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