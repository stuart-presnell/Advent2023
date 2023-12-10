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

# Now we have to define the accessibility criterion for this maze
matrix = test_input
ht = len(matrix)
wd = len(matrix[0])

def neighbours(x,y):
  '''Given a pair of coordinates, return a list of all NSWE neighbours within [0,wd) * [0,ht)'''
  raw_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
  return [(a,b) for (a,b) in raw_neighbours if (0 <= a < ht) and (0 <= b < wd)]

def neighbour_rel(here, other) -> str:
  '''Given two points, determine whether `other` is to the NSWE of `here`; return as character'''
  (Hx,Hy) = here
  (Ox,Oy) = other
  if   (Ox == Hx) & (Oy == Hy - 1):  # same row, prev col => W
    return 'W'
  elif (Ox == Hx) & (Oy == Hy + 1):  # same row, next col => E
    return 'E'
  elif (Oy == Hy) & (Ox == Hx - 1):  # same col, prev row => N
    return 'N'
  elif (Oy == Hy) & (Ox == Hx + 1):  # same col, next row => S
    return 'S'
  else:
    raise ValueError("Points " + str(here) + " and " + str(other) + " are not NSWE neighbours")




def accessibility_criterion(here, other) -> bool:
  '''This is used in `Dijkstra` as follows:
  Given a pair of coordinates `here`, we first get a list of all NSWE neighbours in the matrix
  as a list of pairs of coordinates, e.g. from `(0,3)` this might be `[(1, 3), (0, 2), (0, 4)]`.
  Now for each of these pairs we have to decide whether it's accessible from `here`.'''
  # ASSUMING THAT THE PIPE NETWORK IS CLOSED, SO NEIGHBOURING PIPES CONNECT TO EACH OTHER
  # e.g. if `here` = '-' then `other` to the left is '-', 'L', 'F', or 'S'
  # Thus whether `other` is accessible depends only on the pipe shape at `here`
  # ALSO ASSUMING THAT `other` IS A NSWE NEIGHBOUR OF `here`

  # First, extract the coords of the two points given, and see what's at those points
  (Hx,Hy) = here
  h = matrix[Hx][Hy]
  rel = neighbour_rel(here, other)  # In what direction is `other` from `here`?
  match h:  
    case '-':
      return (rel == 'W') | (rel == 'E') 
    case '|':
      return (rel == 'N') | (rel == 'S') 
    case 'L':
      return (rel == 'N') | (rel == 'E') 
    case 'J':
      return (rel == 'N') | (rel == 'W') 
    case '7':
      return (rel == 'S') | (rel == 'W') 
    case 'F':
      return (rel == 'S') | (rel == 'E') 
    # We don't know what pipe piece is under an `S` square, 
    # but on the assumption that the pipe network is all connected sensibly
    # we just need to check that we could get *to* `here` *from* `other`.
    case 'S':  
      return accessibility_criterion(other, here)
    case '.':
      return False  # We can't get out of the network, and we can't get back in from '.'
    case _:
      raise ValueError(str(here) + " contains `" + h + "` which is not a recognised pipe section.")

S = find_X('S', test_input)
# X = (1,3)
# print("X: ", X, test_input[X[0]][X[1]])
# for N in neighbours(*X):
#   print(N, neighbour_rel(X,N), accessibility_criterion(X, N))


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
    return [(a,b) for (a,b) in neighbours(x,y) if criterion((x,y), (a,b))]

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
    print("Selected point (" + str(x) + "," + str(y) +") which has T = " + str(T)) 
    unvis_neighbours = [(a,b) for (a,b) in accessible_neighbours(x,y) if is_unvisited((a,b))]
    # print(unvis_neighbours)
    for (a,b) in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to t+1 if that's less than its current value
      if T+1 < t_dist[a][b]: 
        print("Resetting (" + str(a) + "," + str(b) +") to " + str(T+1))
        t_dist[a][b] = T+1
        # replace the point (a,b) in `unvisited` with new tentative distance T+1
        unvisited.add_item((a,b), T+1)  

  # If we have a destination END in mind:
  # Keep taking steps until the destination node END is marked as visited
  if END:
    (ENDx,ENDy) = END
    while is_unvisited(END):
      update_one_step()
    # Now we've visited END, return the matrix of shortest paths
    return(t_dist)
  else:  # If we've passed `END = None` then walk to every square we can reach
    while not unvisited.is_empty():
      update_one_step()
    # Now we've visited every square, return the matrix of shortest paths
    return(t_dist)

t = Dijkstra(test_input, S, END = None, criterion = accessibility_criterion)
print()
show(t)


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