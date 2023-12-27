# https://adventofcode.com/2023/day/17

from Dijkstra import Dijkstra, recover_path
from copy import deepcopy

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, 
showM, 
showD, 
# parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_basic(filename):
  f = open(filename)
  ip_file = [[n for n in list(row)] for row in f.read().splitlines()]
  f.close()
  return ip_file

def parse_file(filename):
  f = open(filename)
  ip_file = [[int(n) for n in list(row)] for row in f.read().splitlines()]
  f.close()
  ht = len(ip_file)
  wd = len(ip_file[0])
  
  # A state is a pair (pt, dir)
  # We define a matrix `M`` indexed by points in the grid and cardinal directions:
  # think of this as 4 copies of the grid stacked on top of each other
  # The value `ip_file[r][c]` tells us the heat loss incurred for entering square (r,c)
  M = {((r,c), d): ip_file[r][c] for r in range(ht) for c in range(wd) for d in ['N','S','W','E']}
  
  # Starting point is top left corner, destination is bottom right corner
  # We'll compute these here while we have access to `wd` and `ht`
  TL = (0,0)
  BR = (ht-1, wd-1)

  # Two possible starting states
  STARTS = [(TL, 'E'), (TL, 'S')]
  # Four possible ending states
  ENDS = [(BR, dir) for dir in ['N','S','W','E']]

  return (M, STARTS, ENDS)

grid = parse_file_basic("Puzzle17_test.txt")
# showM(grid, -1)

test_input = parse_file("Puzzle17_test.txt")
# input      = parse_file("Puzzle17_input.txt")

(M, STARTS, ENDS) = test_input
# showD(M)

################################
# Part (a)
################################

# How to step in each cardinal direction (change in row, change in column)
dir_lookup = {
  'N':(-1,0),
  'S':( 1,0),
  'W':(0,-1),
  'E':(0, 1)
}

# --------------------------------------------------

def turn_lt(dir):
  if dir == 'N': return 'W'
  if dir == 'W': return 'S'
  if dir == 'S': return 'E'
  if dir == 'E': return 'N'

def turn_rt(dir):
  if dir == 'N': return 'E'
  if dir == 'E': return 'S'
  if dir == 'S': return 'W'
  if dir == 'W': return 'N'

def ACCESSIBLE_NEIGHBOURS(matrix, state):
  '''Given a `state = (pt, dir)`, return a list of permitted next states.
  A permitted move from state `(pt, dir)` is 1-3 steps in `dir` from `pt` (staying within grid) followed by a turn to the left or right.'''
  (pt, dir) = state
  step = dir_lookup[dir]
  lt = turn_lt(dir)
  rt = turn_rt(dir)
  op = []
  for n in range(1,4):
    nr = pt[0] + n * step[0]
    nc = pt[1] + n * step[1]
    if ((nr,nc), dir) in matrix:
      op.append(((nr,nc), lt))
      op.append(((nr,nc), rt))
  return op

def STEP_COST(matrix, here, other):
  '''Given a pair of states, return the cost of stepping from `here` to `other`.'''
  ((r1,c1), _) = here
  ((r2,c2), _) = other
  if r1 == r2:
    c_steps = range(min(c1,c2)+1, max(c1,c2)+1)  # don't include first square, do include last
    # The heat loss doesn't depend on direction; just using 'N' as an arbitrary choice
    return sum([matrix[((r1,c), 'N')] for c in c_steps])
  elif c1 == c2:
    pass
    r_steps = range(min(r1,r2)+1, max(r1,r2)+1)  # don't include first square, do include last
    # The heat loss doesn't depend on direction; just using 'N' as an arbitrary choice
    return sum([matrix[((r,c1), 'N')] for r in r_steps])
  else:
    raise ValueError("Can only move along rows and columns")

# --------------------------------------------------

(M, STARTS, ENDS) = test_input
# showD(M)
# print(STARTS)
# print(ENDS)


SE = ((0,0), 'E')
EE = ((12,12), 'E')
(t,p) = Dijkstra(M, 
                 [SE], 
                 [((2,10), 'S')], 
                 ACCESSIBLE_NEIGHBOURS, STEP_COST)

# print(t[EE])

# print([t[e] for e in ENDS])
# showD(p)

# for e in [EE]:
#   print(recover_path(p,e))

PPP = recover_path(p,((2,10), 'S'))
print(PPP)

def show_path(grid, p):
  translate = {
    'N':'^', 
    'S':'V', 
    'W':'<', 
    'E':'>' 
               }
  d = {k:translate[v] for (k,v) in p}
  g2 = deepcopy(grid)
  for r in range(len(g2)):
    for c in range(len(g2[0])):
      if (r,c) in d:
        g2[r][c] = d[(r,c)]
  showM(g2, -1)

show_path(grid, PPP)


# showD(t)

def main_a(ip_file):
  (M, STARTS, ENDS) = ip_file
  (t,p) = Dijkstra(M, STARTS, ENDS, ACCESSIBLE_NEIGHBOURS, STEP_COST)
  return (t,p)
  # return [(e, t[e]) for e in ENDS]




# For `test_input` we get the following minimal costs:
# ((12, 12), 'N')   =>  100
# ((12, 12), 'S')   =>  100
# ((12, 12), 'W')   =>  102
# ((12, 12), 'E')   =>  102

# print(main_a(test_input))  # 
# print(main_a(input))       # 930 is too low

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