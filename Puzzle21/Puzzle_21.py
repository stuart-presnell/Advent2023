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


def make_matrix_data(grid):
  '''Given a `grid` (represented as a list of strings)
  in which some squares are accessible (`'.'` and `'S'`) and others are blocked (`'#'`),
  return the data needed to assemble its adjacency matrix:
  specifically, a list of `[1, R, C]` where 
  `R` is the `encode` of some point pt1 and
  `C` is the `encode` of some adjacent point pt2.'''
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
          data_points.append([True, encode(r,c, wd), encode(*pos, wd)])
          data_points.append([True, encode(*pos, wd), encode(r,c, wd)])
  
  # data_points.sort()
  # show([(r,c) for [d,r,c] in data_points])
  return data_points

def make_matrix(grid):
  '''Given a `grid` (represented as a list of strings), 
  use `make_matrix_data` to assemble the adjacency data, 
  then make the `coo_array`.
  If `grid` is `ht x wd` then the number of squares is 
  `(ht * wd)` and so the adjacency matrix is `(ht * wd) x (ht * wd)`.'''
  ht = len(grid)
  wd = len(grid[0])
  data_points = make_matrix_data(grid)
  return make_coo(data_points, ht*wd, ht*wd)

def make_wraparound_matrix(grid):
  '''Given a `grid` (represented as a list of strings), 
  use `make_matrix_data` to assemble the adjacency data;
  then append more adjacencies corresponding to the toroidal wrap-around across the edges;
  then make the `coo_array`.
  If `grid` is `ht x wd` then the number of squares is 
  `(ht * wd)` and so the adjacency matrix is `(ht * wd) x (ht * wd)`.'''
  ht = len(grid)
  wd = len(grid[0])
  data_points = make_matrix_data(grid)
  for r in range(ht):
    data_points.append([True, encode(r,0, wd), encode(r,wd-1, wd)])
    data_points.append([True, encode(r,wd-1, wd), encode(r,0, wd)])
  for c in range(wd):
    data_points.append([True, encode(0,c, wd), encode(ht-1,c, wd)])
    data_points.append([True, encode(ht-1,c, wd), encode(0,c, wd)])
  return make_coo(data_points, ht*wd, ht*wd)


def sparse_power(M, n):
  '''Compute the `n`th power of sparse matrix `M`, using repeated powers and `@` multiplication.
  https://stackoverflow.com/a/28703334'''
  if n <= 1:
    return M
  temp = sparse_power(M, n//2)
  if n % 2:     # if n is odd
    return M @ temp @ temp
  else:
    return temp @ temp



def main_a_v2(ip_filename, n):
  (M, S) = parse_file_a(ip_filename)
  Adj = make_matrix(M)
  Adj_pow = sparse_power(Adj, n)
  Adj_pow = Adj_pow.tocsr()
  S_code = encode(*S, len(M[0]))
  S_row = Adj_pow[[S_code], :]
  return (S_row.nnz)

print(main_a_v2("Puzzle21_test.txt", 64))   # 42
# print(main_a_v2("Puzzle21_input.txt", 6))   # 16


# TODO: Extract the appropriate row from the powered matrix, corresponding to steps from `S`.
# TODO: Use this row to compute how many squares are exactly `n` steps from `S`
# TODO: Instead of taking powers of `Adj` directly, can we diagonalise `Adj` first?



# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################