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
O = (0,0)
# Destination is bottom right corner
D = (ht-1, wd-1)



def Dijkstra(matrix, START, END, criterion = lambda other,here: other <= here + 1, verbose = False):
  ht = len(matrix)
  wd = len(matrix[0])

# --------------------------------------------------
  # TODO: Change this!  Now we can step up to 3 steps in any direction, but can't reverse
  # During each step, you can move exactly one square up, down, left, or right...
  def neighbours(x,y):
    '''Given a pair of coordinates, return a list of all NSWE neighbours within [0,wd) * [0,ht)'''
    raw_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(a,b) for (a,b) in raw_neighbours if (0 <= a < ht) and (0 <= b < wd)]

  # ...but not every neighbour square is accessible; `criterion` tells us which are
  def accessible_neighbours(x,y):
    '''Given a pair of coordinates,
    return a list of the neighbours that are accessible per the adjacency criterion
    by default: whose height is at most one higher than [x,y]'''
    return [(a,b) for (a,b) in neighbours(x,y) if criterion(matrix, (x,y), (a,b))]
  
  def step_cost(here, other):
    '''Given a pair of coordinates, return the cost of stepping from `here` to `other`'''
    return 1
# --------------------------------------------------


  # Assign to every node a tentative distance value, initialised to infinity
  # t_dist  = [[inf for _ in range(wd)] for _ in range(ht)]
  # Store this in a `defaultdict` for quicker lookup, since we don't need the matrix structure
  t_dist = defaultdict(lambda : inf)

  # (STARTx,STARTy) = START

  # Give the starting node a distance of 0
  t_dist[START] = 0

  # Make a Priority Queue of nodes that have not yet been visited.
  # Each item on the Priority Queue is a pair (t, (x,y)), 
  # where t is the tentative distance to point (x,y)
  # Being a Priority Queue means we can efficiently pop off the item with the smallest t
  unvisited = PQ()
  for x in range(ht):
    for y in range(wd):
        unvisited.add_item((x,y), t_dist[(x,y)])

  def is_unvisited(pt):
    (x,y) = pt
    return unvisited.find_item((x,y))

  def update_one_step():
    # select the unvisited node that is marked with the smallest tentative distance T; 
    # mark it as visited by popping it from `unvisited`
    (T, (x,y)) = unvisited.pop_item_with_priority()
    # If the smallest T of any unvisited node is inf
    # then we've visited every accessible node, 
    # so tell the parent function to break
    if T == inf:  
      return True  # This is collected by the parent function as a variable `FINISHED`
    if verbose: print("Selected point (" + str(x) + "," + str(y) +") which has T = " + str(T)) 
    unvis_neighbours = [(a,b) for (a,b) in accessible_neighbours(x,y) if is_unvisited((a,b))]
    if verbose: print(unvis_neighbours)
    for (a,b) in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to T+1 if that's less than its current value
      cost = step_cost((x,y), (a,b))
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