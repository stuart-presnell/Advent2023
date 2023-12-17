# https://adventofcode.com/2023/day/17

from math import inf
from PQueue import PQ
from collections import defaultdict

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = [[int(n) for n in list(row)] for row in f.read().splitlines()]
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle17_test.txt")
input      = parse_file_a("Puzzle17_input.txt")

ip = test_input
# ip = input
show(ip)

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

ht = len(ip)
wd = len(ip[0])

def one_step(pt, dir):
  step = dir_lookup[dir]
  nr = pt[0] + step[0]
  nc = pt[1] + step[1]
  if (0 <= nr < ht) & (0 <= nc < wd):
    return (nr, nc)
  else:
    # print(str((nr,nc)) + " is off the grid, so skip this!")
    return None

# new_pt = one_step(pt, dir)

# Starting point is top left corner
TL = (0,0)
# Destination is bottom right corner
BR = (ht-1, wd-1)


# --------------------------------------------------
# TODO: Change this!  Now we can step up to 3 steps in any direction, but can't reverse
# During each step, you can move exactly one square up, down, left, or right...
def neighbours(x,y):
  '''Given a pair of coordinates, return a list of all NSWE neighbours within [0,wd) * [0,ht)'''
  raw_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
  return [(a,b) for (a,b) in raw_neighbours if (0 <= a < ht) and (0 <= b < wd)]

# ...but not every neighbour square is accessible; `criterion` tells us which are
def ACCESSIBLE_NEIGHBOURS(matrix, x,y, criterion = lambda *args:True):
  '''Given a pair of coordinates,
  return a list of the neighbours that are accessible per the adjacency criterion
  by default: whose height is at most one higher than [x,y]'''
  return [(a,b) for (a,b) in neighbours(x,y) if criterion(matrix, (x,y), (a,b))]

def STEP_COST(matrix, here, other):
  '''Given a pair of coordinates, return the cost of stepping from `here` to `other`'''
  (r1,c1) = here
  (r2,c2) = other
  if r1 == r2:
    c_steps = range(min(c1,c2)+1, max(c1,c2)+1)  # don't include first square, do include last
    return sum([matrix[r1][c] for c in c_steps])
  elif c1 == c2:
    pass
    r_steps = range(min(r1,r2)+1, max(r1,r2)+1)  # don't include first square, do include last
    return sum([matrix[r][c1] for r in r_steps])
  else:
    raise ValueError("Can only move along rows and columns")

# --------------------------------------------------

def Dijkstra(matrix, START, END, ACCESSIBLE_NEIGHBOURS, STEP_COST, verbose = False):
  '''Given a `matrix` of points, with `START` and `END` points (or optionally `END = None`),
  with a function returning a list of the `ACCESSIBLE_NEIGHBOURS` of any point
  and a function returning the `STEP_COST` of stepping from `pt1` to `pt2`,
  run Dijkstra's algorithm to work out the cheapest route from `START` to each reachable point,
  stopping when we reach `END` (if provided).'''
  ht = len(matrix)
  wd = len(matrix[0])

  # Assign to every node a tentative distance value, initialised to infinity
  # Store this in a `defaultdict` for quicker lookup, since we don't need the matrix structure
  t_dist = defaultdict(lambda : inf)

  # Give the starting node a distance of 0
  t_dist[START] = 0

  # Make a Priority Queue of nodes that have not yet been visited.
  # Each item on the queue is a pair (t, (x,y)), where t is the tentative distance to point (x,y)
  # Being a Priority Queue means we can efficiently pop off the item with the smallest t
  unvisited = PQ()
  for x in range(ht):
    for y in range(wd):
        unvisited.add_item((x,y), t_dist[(x,y)])

  def is_unvisited(pt):
    return unvisited.find_item(pt)

  def update_one_step():
    # select the unvisited node that is marked with the smallest tentative distance T; 
    # mark it as visited by popping it from `unvisited`
    (T, (x,y)) = unvisited.pop_item_with_priority()
    # If the smallest T of any unvisited node is inf then we've visited every accessible node, 
    # so tell the parent function to break
    if T == inf:  
      return True  # This is collected by the parent function as a variable `FINISHED`
    if verbose: print("Selected point (" + str(x) + "," + str(y) +") which has T = " + str(T)) 
    # Make a list of all the unvisited neighbours of current point `(x,y)`
    unvis_neighbours = [pt for pt in ACCESSIBLE_NEIGHBOURS(matrix, x,y) if is_unvisited(pt)]
    if verbose: print(unvis_neighbours)
    for (a,b) in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to T + STEP_COST(here, there) if that's less than its current value
      cost = STEP_COST(matrix, (x,y), (a,b))
      if T+cost < t_dist[(a,b)]: 
        if verbose: print("Resetting (" + str(a) + "," + str(b) +") to " + str(T+cost))
        t_dist[(a,b)] = T+cost
        # replace the point (a,b) in `unvisited` with new tentative distance T+cost
        unvisited.add_item((a,b), T+cost)
    return False # We don't think we've reached every reachable square yet

  FINISHED = False
  if END:
    # If we have a destination END in mind:
    # Keep taking steps until the destination node END is marked as visited
    # or `update_one_step` reports that it has FINISHED exploring reachable squares
    while (not FINISHED) & is_unvisited(END):
      FINISHED = update_one_step()
    return(t_dist)
  else:  
    # If we've passed `END = None` then walk to every square we can reach
    while (not FINISHED) & (not unvisited.is_empty()):
      FINISHED = update_one_step()
    return(t_dist)



# Dijkstra(ip, TL, BR, ACCESSIBLE_NEIGHBOURS, STEP_COST)


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