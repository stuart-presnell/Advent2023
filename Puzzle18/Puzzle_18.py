# https://adventofcode.com/2023/day/18

from math import inf

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, parse_nums, rotate90, close_bracket, cmp, qsort, 
nwise_cycled,
Best, 
Timer,
)
TTT = Timer()

################################

################################
# Part (a)
################################

corner_shape = {}
corner_shape['RD'] = '7'
corner_shape['RU'] = 'J'
corner_shape['LD'] = 'F'
corner_shape['LU'] = 'L'
corner_shape['UL'] = '7'
corner_shape['DL'] = 'J'
corner_shape['UR'] = 'F'
corner_shape['DR'] = 'L'

def parse_file_a(filename):
  f = open(filename)
  ip_file = [line.split() for line in f.read().splitlines()]
  f.close()
  ip_file = [[d, int(n), c] for [d, n, c] in ip_file]
  op = []
  for i in range(len(ip_file)):
    corner_code = ip_file[i-1][0] + ip_file[i][0]
    op.append(ip_file[i] + [corner_shape[corner_code]])
  return op

test_input = parse_file_a("Puzzle18_test.txt")
input      = parse_file_a("Puzzle18_input.txt")

ip = test_input
# ip = input
show(ip)


# How to step in each cardinal direction (change in row, change in column)
dir_lookup = {
  'U':(-1,0),
  'D':( 1,0),
  'L':(0,-1),
  'R':(0, 1)
}

def n_steps(dug, pt, dir, n = 1):
  '''Given a set of `dug` squares, a starting `pt`, a `dir` and a number of squares to dig, 
  return an updated `dug` and a new position.'''
  (r,c) = pt
  match dir:
    case 'U': 
      for i in range(n):
        dug.add((r-i-1, c))
      return (dug, (r-n, c))
    case 'D': 
      for i in range(n):
        dug.add((r+i+1, c))
      return (dug, (r+n, c))
    case 'R': 
      for i in range(n):
        dug.add((r, c+i+1))
      return (dug, (r, c+n))
    case 'L': 
      for i in range(n):
        dug.add((r, c-i-1))
      return (dug, (r, c-n))
  
def follow_instr(ip):
  pt = (0,0)        # Initial square is defined to be (0,0)
  dug = {(0,0)}     # Set of squares that have been dug out
  for [dir, n, _, _] in ip:
    (dug, pt) = n_steps(dug, pt, dir, n)
  return dug

def get_dimensions(L):
  '''Extract the min and max dimensions of the list of points.'''
  min_r = Best(inf, lambda x,y:x<y)
  min_c = Best(inf, lambda x,y:x<y)
  max_r = Best(-inf, lambda x,y:x>y)
  max_c = Best(-inf, lambda x,y:x>y)
  min_r.reduce([pt[0] for pt in L])
  max_r.reduce([pt[0] for pt in L])
  min_c.reduce([pt[1] for pt in L])
  max_c.reduce([pt[1] for pt in L])
  return (min_r.best_so_far,min_c.best_so_far,max_r.best_so_far,max_c.best_so_far)


def display_grid(S):
  '''Show the subset of points included in set `S`.'''
  (min_r, min_c, max_r, max_c) = get_dimensions(S)
  for row in range(min_r, max_r+1):
    for col in range(min_c, max_c+1):
      print('#' if (row,col) in S else '.', end='')
    print()

def flood_fill(dug, seed):
  to_check = [seed]
  while to_check:
    pt = to_check.pop()
    if pt in dug:
      continue
    else:  # fill this square and add the 4 cardinal neighbours to `to_check`
      (r,c) = pt
      dug.add(pt)
      to_check.append((r-1,c))  # N
      to_check.append((r+1,c))  # S
      to_check.append((r,c+1))  # E
      to_check.append((r,c-1))  # W
  return dug

def main_a(ip_file, seed = (1,1), verbose = False):
  dug = follow_instr(ip_file)  # Dig out the boundary according to the instructions
  dug = flood_fill(dug, seed)    # Guessing a good starting point
  if verbose: display_grid(dug)
  return len(dug)
  
def corners_and_verts(ip):
  '''Given a list of instructions `ip` of the form `[dir, n, _]`, 
  return a list of points visited when we jump along those instructions, starting at `(0,0)`;
  annotate each corner with its shape, 'L', 'J', 'F', or '7'.
  Also return a list of the vertical runs.'''
  verts = []
  visited = []
  pt = (0,0)
  m = len(ip)
  for i in range(len(ip)):
    [dir, n, _, shape] = ip[i]
    step = dir_lookup[dir]
    next_pt = (pt[0] + n*step[0], pt[1] + n*step[1])
    corner_type = ip[(i+1)%m][3]
    visited.append((next_pt[0], next_pt[1], corner_type))
    if (dir == 'U') | (dir == 'D'):
      verts.append([pt, next_pt])
    pt = next_pt
  if visited[-1] == visited[0]:
    visited.pop()
  visited.sort()
  verts.sort()
  return (visited, verts)

show(corners_and_verts(test_input))

def which_step(pt1, pt2):
  '''Given two consecutive points, what direction was the step from `pt1` to `pt2`?'''
  step = (pt2[0] - pt1[0], pt2[1] - pt1[1])
  if (step[0] == 0):
    if step[1] < 0:
      return 'W'
    elif step[1] > 0:
      return 'E'
  elif (step[1] == 0):
    if step[0] < 0:
      return 'N'
    elif step[0] > 0:
      return 'S'
  else:
    raise ValueError("Points were not distinct and orthogonal")

# TODO: From a list of corner positions and corner shapes 
  # we should be able to calculate the enclosed area.
  # Think of the corners as stakes with string tied between them.
  # In each row we need to know in which columns the strings sit, then take an alternating sum.
  # As we go along the row we toggle between INSIDE and OUTSIDE as we cross a string or a 'L' or 'J'.

# dug = follow_instr(ip)
# display_grid(dug)
# print(corners(ip))

# print(main_a(test_input, verbose=True))  # 62
# print(main_a(input))       # 62500

# TTT.timecheck("Part (a)")  # ~ 57 ms

################################
# Part (b)
################################

# Each hexadecimal code is six hexadecimal digits long. 
# The first five encode the distance in meters as a five-digit hexadecimal number. 
# The last hexadecimal digit encodes the direction to dig: 
# 0 means R, 1 means D, 2 means L, and 3 means U.

def parse_hex_colour(H):
  dir_lookup = ['R', 'D', 'L', 'U']
  (n,d) = int(H[2:-2], 16), int(H[-2])
  return [dir_lookup[d], n, '']

def parse_file_b(filename):
  f = open(filename)
  ip_file = [line.split() for line in f.read().splitlines()]
  ip_file = [parse_hex_colour(c) for [_,_, c] in ip_file]
  f.close()
  return ip_file

# test_input_b = parse_file_b("Puzzle18_test.txt")
# input_b      = parse_file_b("Puzzle18_input.txt")

# ip = test_input_b
# ip = input_b
# show(ip)


# TODO: Find a new way to compute the area of the bounded region
#   Don't store all points of border that are dug, just corners; use this to infer others
#   Work row-by-row; store just positions of boundary points in each row
#   Assume no borders are adjacent, so we can combine runs of '#' to single points
#   Use even/odd to distinguish inside from outside
#   Just count differences between exit and entrance points, don't fill between them.


# def main_b(ip_file):
#   pass

# print(main_a(test_input_b, (0,0)))  # 6405262 is the wrong answer, should be 952408144115
# print(main_a(input))       # 

# TTT.timecheck("Part (b)")  #

################################