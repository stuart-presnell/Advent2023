# https://adventofcode.com/2023/day/10

from PQueue import PQ
from math import inf

# My utility functions
from utils import (
show,
# chunk_splitlines,
# parse_nums,
# rotate90,
# close_bracket,
# cmp,
# qsort
)

from time import perf_counter
TIMING = False
if TIMING: start_time = perf_counter()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle10_test.txt")
input      = parse_file_a("Puzzle10_input.txt")

show(test_input)

################################


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; 
#     there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


def find_X(X, list_of_strings):
  '''Find the first instance of string `X` in `list_of_strings` (earliest row, leftmost position)'''
  for i in range(len(list_of_strings)):
    if X in list_of_strings[i]:
      row = i
      col = list_of_strings[i].find(X)
      return (row,col)
  raise ValueError(X + " was not found in the input")

S = find_X('S', test_input)
print(S)



# How many steps along the loop does it take 
# to get from the starting position `S`` to the point farthest from the starting position?
# https://en.wikipedia.org/wiki/Dijkstras_algorithm

def Dijkstra(matrix, START, END, criterion = lambda other,here: other <= here + 1):
  ht = len(matrix)
  wd = len(matrix[0])

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
    return [(a,b) for (a,b) in neighbours(x,y) if criterion(matrix[a][b], matrix[x][y])]

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
    # select the unvisited node that is marked with the smallest tentative distance; 
    # mark it as visited
    (T, (x,y)) = unvisited.pop_item_with_priority()  # T is the current tentative distance of this node
    # print("Selected point (" + str(x) + "," + str(y) +") which has T = " + str(T)) 
    unvis_neighbours = [(a,b) for (a,b) in accessible_neighbours(x,y) if is_unvisited((a,b))]
    # print(unvis_neighbours)
    for (a,b) in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to t+1 if that's less than its current value
      if T+1 < t_dist[a][b]: 
        # print("Resetting (" + str(a) + "," + str(b) +") to " + str(T+1))
        t_dist[a][b] = T+1
        # replace the point (a,b) in `unvisited` with new tentative distance T+1
        unvisited.add_item((a,b), T+1)  

  # If we have a destination END in mind:
  # Keep taking steps until the destination node END is marked as visited
  if END:
    (ENDx,ENDy) = END
    while is_unvisited(END):
      update_one_step()
    # Now we've visited END, how long is the shortest path from START to END?
    return(t_dist[ENDx][ENDy])
  else:  # If we've passed `END = None` then walk to every square we can reach
    while not unvisited.is_empty():  ###  WHAT DO WE DO IF NOT EVERY SQUARE IS CONNECTED TO `S`?
      update_one_step()
    # Now we've visited every square, return the matrix of shortest paths
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
if TIMING:
  end_time = perf_counter()
  print()
  print("Time taken: ", (end_time - start_time)*1000, "ms")