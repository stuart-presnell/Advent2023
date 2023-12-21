# https://adventofcode.com/2023/day/21

import numpy as np
from scipy.sparse import coo_array
from math import log10, ceil
from numpy.linalg import matrix_power

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, 
showM, 
# showD, 
unzip, 
# parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
TTT = Timer(1)

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

# For testing purposes, extract the top left corner of `M`

def top_corner(grid, n):
  return [row[:n] for row in grid[:n]]

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

def show_encoded(grid):
  '''Given a `grid`, show the code numbers for each square, or `#`.'''
  ht = len(grid)
  wd = len(grid[0])
  max_digits = ceil(log10(ht*wd)) - 1
  blocked = ' '*(max_digits+1)  + '#'
  showM(
    [[encode(r,c,wd) if grid[r][c] != '#' else blocked for c in range(wd)] for r in range(ht)], 
    max_digits
    )

def make_coo(data_coords, HT, WD):
  '''Given a list of triples `[d, r, c]` encoding that matrix element `M[r][c] = d`,
  and the required `HT` and `WD` of the matrix,
  return the sparse matrix `M` as a `coo_array`.'''
  [data, R, C] = unzip(data_coords)
  return coo_array((data, (R, C)), shape=(HT, WD))


def make_matrix(grid):
  '''Given a `grid` (represented as a list of strings)
  in which some squares are accessible (`'.'` and `'S'`) and others are blocked (`'#'`),
  return its adjacency matrix.  If `grid` is `ht x wd` then the number of squares is 
  `(ht * wd)` and so the adjacency matrix is `(ht * wd) x (ht * wd)`.'''
  ht = len(grid)
  wd = len(grid[0])

  def free(r,c):
    if (0 <= r < ht) & (0 <= c < wd):
      return (grid[r][c] != '#')
    else:
      return False

  # Go through each square of `grid`, 
  # populating `Adj` with the adjacencies to and from that square.
  # We use the fact that accessibility is symmetric and irreflexive in this grid,  

  data_points = []
  for r in range(ht):
    for c in range(wd):
      if grid[r][c] == '#': 
        # print("Skipping blocked square ", encode(r,c,wd))
        continue  # Skip blocked squares
  
      # print("Looking for adjacencies for point ", encode(r,c,wd))
      ngb = [(r,c+1), (r+1,c)]  # Only need to consider points to S and E
      for pos in ngb:
        if free(*pos):
          data_points.append([1, encode(r,c, wd), encode(*pos, wd)])
          data_points.append([1, encode(*pos, wd), encode(r,c, wd)])
  
  # data_points.sort()
  # show([(r,c) for [d,r,c] in data_points])
  return make_coo(data_points, ht*wd, ht*wd)


# M2 = top_corner(M, 2)
# M5 = top_corner(M, 5)
# show(M5)
# show_encoded(M5)


# (M, S) = test_input
(M, S) = input
Adj2 = make_matrix(M)

TTT.timecheck("After `make_matrix`")  # ~ 50 ms for `input`

# Adj2.toarray()

Adj2_CSR = Adj2.tocsr()

TTT.timecheck("After `tocsr`")  # No further time


# Adj2_sq = Adj2_CSR ** 2  # This is doing element-wise squaring, not matrix power!
# Adj2_sq = Adj2_CSR @ Adj2_CSR # This works to square the matrix
# TTT.timecheck("After squaring")  # No further time

Adj2_dense = Adj2_CSR.todense()
TTT.timecheck("After `todense`")  #  ~ 30 ms

# Adj2_sq = matrix_power(Adj2_dense, 2)
# TTT.timecheck("After squaring dense matrix")  # > 30 seconds!

# Adj2_sq


# Adj2_STHG = Adj2.to



# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################