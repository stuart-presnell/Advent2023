# https://adventofcode.com/2023/day/11

# My utility functions
from utils import (
# chunk_splitlines, printT, 
show, 
# showM, parse_nums, 
rotate90, 
# close_bracket, cmp, qsort, Best, 
Timer,
)

from PQueue import PQ
from math import inf

# from time import perf_counter
# TIMING = False
# if TIMING: start_time = perf_counter()

TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle11_test.txt")    # There are 9 '#'s in test_input
input      = parse_file_a("Puzzle11_input.txt")   # There are 455 '#'s in input

expansion_test1 = parse_file_a("expansion_test1.txt")

matrix = test_input
# show(matrix)  # Original input matrix

def duplicate_empty_rows(M):
  op = []
  for row in M:
    if '#' in row:
      op.append(row)
    else:
      op.append(row)
      op.append(row)
  return op

def expand_universe(M):
  M = duplicate_empty_rows(M)
  M = rotate90(M)
  M = duplicate_empty_rows(M)
  M = rotate90(M)
  M = rotate90(M)
  M = rotate90(M)
  M = ["".join(row) for row in M]
  return M

matrix = expand_universe(matrix)

TTT.timecheck("Expand")

def find_galaxies(M):
  return [(row,col) for row in range(len(M)) for col in range(len(M[0])) if M[row][col] == '#']

show(matrix)    # Expanded universe
find_galaxies(matrix)


def Dijkstra(matrix, START, END, criterion = lambda other,here: True, verbose = False):
  ht = len(matrix)
  wd = len(matrix[0])

  # During each step, you can move exactly one square up, down, left, or right...
  def neighbours(x,y):
    '''Given a pair of coordinates, return a list of all NSWE neighbours within [0,wd) * [0,ht)'''
    raw_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(a,b) for (a,b) in raw_neighbours if (0 <= a < ht) and (0 <= b < wd)]

  # # ...but not every neighbour square is accessible; `criterion` tells us which are
  # def accessible_neighbours(x,y):
  #   '''Given a pair of coordinates,
  #   return a list of the neighbours that are accessible per the adjacency criterion
  #   by default: whose height is at most one higher than [x,y]'''
  #   return [(a,b) for (a,b) in neighbours(x,y) if criterion(matrix, (x,y), (a,b))]

  # Assign to every node a tentative distance value, initialised to infinity
  t_dist  = [[inf for _ in range(wd)] for _ in range(ht)]

  (STARTx,STARTy) = START

  # Give the starting node a distance of 0
  t_dist[STARTx][STARTy] = 0

  # Make a Priority Queue of nodes that have not yet been visited
  # each item on the Priority Queue is a pair (t, (x,y)), 
  # where t is the tentative distance to point (x,y)
  # Being a Priority Queue means we can efficiently pop off the item with the smallest t
  unvisited = PQ()
  for x in range(ht):
    for y in range(wd):
        unvisited.add_item((x,y), t_dist[x][y])

  def is_unvisited(pt):
    (x,y) = pt
    return unvisited.find_item((x,y))

  def update_one_step():
    # select the unvisited node that is marked with the smallest tentative distance T; 
    # mark it as visited
    (T, (x,y)) = unvisited.pop_item_with_priority()
    # If the smallest T of any unvisited node is inf
    # then we've visited every accessible node, 
    # so tell the parent function to break
    if T == inf:  
      return True  # This is collected by the parent function as a variable `finished`
    if verbose: print("Selected point (" + str(x) + "," + str(y) +") which has T = " + str(T)) 
    unvis_neighbours = [(a,b) for (a,b) in neighbours(x,y) if is_unvisited((a,b))]
    if verbose: print(unvis_neighbours)
    for (a,b) in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to t+1 if that's less than its current value
      if T+1 < t_dist[a][b]: 
        if verbose: print("Resetting (" + str(a) + "," + str(b) +") to " + str(T+1))
        t_dist[a][b] = T+1
        # replace the point (a,b) in `unvisited` with new tentative distance T+1
        unvisited.add_item((a,b), T+1)
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




################################
# Part (a)
################################

# def main_a(ip):
#   pass

# main_a(test_input)  # 
# main_a(input)       # 


################################
# Part (b)
################################

# def main_b(ip):
#   pass

# main_b(test_input)  # 
# main_b(input)       # 


################################
# if TIMING:
#   end_time = perf_counter()
#   print()
#   print("Time taken: ", (end_time - start_time)*1000, "ms")

# TTT.timecheck("Final")