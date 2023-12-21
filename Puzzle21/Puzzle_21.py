# https://adventofcode.com/2023/day/21

import numpy as np
from scipy.sparse import coo_array

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, 
unzip, 
# parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
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

(M, S) = test_input
# (M, S) = input
# show(M)

# For testing purposes, extract the top left corner of `M`
M4 = [row[:4] for row in M[:4]]
show(M4)

def step(current, free):
  '''Given a list/set of `current` positions
  and a function reporting whether a square is `free`, 
  return a set of the free spaces that are 1 step away from a current position.'''
  op = set()
  for (r,c) in current:
    ngb = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    for pos in ngb:
      if free(*pos):
        op.add(pos)
  return op

################################
# Part (a)
################################

def main_a(ip_filename, n):
  (M, S) = parse_file_a(ip_filename)
  ht = len(M)
  wd = len(M[0])
  def free(r,c):
    if (0 <= r < ht) & (0 <= c < wd):
      return (M[r][c] != '#')
    else:
      return False
  current = {S}
  for _ in range(n):
    current = step(current, free)
  return len(current)

# print(main_a("Puzzle21_test.txt", 64))   # 42
# print(main_a("Puzzle21_input.txt", 64))  # 3532


# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

STEPS_TO_TAKE = 26501365

def encode(r,c, WD):
  '''Squares of `grid` are numbered row-by-row, so `(r,c)` is square number `r*WD + c`.'''
  return (r * WD) + c


def make_matrix(grid):
  '''Given a `grid` (represented as a list of strings)
  in which some squares are accessible (`'.'` and `'S'`) and others are blocked (`'#'`),
  return its adjacency matrix.  If `grid` is `ht x wd` then the number of squares is 
  `(ht * wd)` and so the adjacency matrix is `(ht * wd) x (ht * wd)`.'''
  ht = len(grid)
  wd = len(grid[0])
  
  # The adjacency matrix `Adj` has an entry for each pair of squares in `grid`.
  # For most of these, the entry is zero; hence we use a sparse matrix.
  # We populate `Adj` by providing three lists.
  # To set `Adj[R][C] = d` we put (for some index `k`) 
  # * `row[k]  = R`
  # * `col[k]  = C`
  # * `data[k] = d`
  
  # Go through each square of `grid`, 
  # populating `Adj` with the adjacencies to and from that square.
  # We use the fact that accessibility is symmetric and irreflexive in this grid,  

  data_points = []
  for r in range(ht):
    for c in range(wd):
      ngb = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    for pos in ngb:
      if free(*pos):
        data_points.append([1, encode(r,c), encode(*pos)])
  
  print(data_points)
  # [data, R, C] = unzip(data_points)
  # Adj = coo_array((data, (R, C)), shape=(ht * wd, ht * wd))
  # print(Adj.toarray())
  pass

# make_matrix(M4)

# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################