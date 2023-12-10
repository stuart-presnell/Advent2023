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
Best
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

test_input1 = parse_file_a("Puzzle10_test1.txt")
test_input2 = parse_file_a("Puzzle10_test2.txt")
test_input3 = parse_file_a("Puzzle10_test3.txt")
test_input4 = parse_file_a("Puzzle10_test4.txt")
input       = parse_file_a("Puzzle10_input.txt")

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
# ht = len(matrix)
# wd = len(matrix[0])

# def neighbours(x,y):
#   '''Given a pair of coordinates, return a list of all NSWE neighbours within [0,wd) * [0,ht)'''
#   raw_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
#   return [(a,b) for (a,b) in raw_neighbours if (0 <= a < ht) and (0 <= b < wd)]

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




def accessibility_criterion(M, here, other) -> bool:
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
  h = M[Hx][Hy]
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
      return accessibility_criterion(M, other, here)
    case '.':
      return False  # We can't get out of the network, and we can't get back in from '.'
    case _:
      raise ValueError(str(here) + " contains `" + h + "` which is not a recognised pipe section.")



# How many steps along the loop does it take 
# to get from the starting position `S`` to the point farthest from the starting position?
# https://en.wikipedia.org/wiki/Dijkstras_algorithm

def Dijkstra(matrix, START, END, criterion = lambda other,here: other <= here + 1, verbose = False):
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
    return [(a,b) for (a,b) in neighbours(x,y) if criterion(matrix, (x,y), (a,b))]

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
    unvis_neighbours = [(a,b) for (a,b) in accessible_neighbours(x,y) if is_unvisited((a,b))]
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

def main_a(matrix):
  # show(matrix)
  S = find_X('S', matrix)
  t = Dijkstra(matrix, S, END = None, criterion = accessibility_criterion)
  # print()
  # show(t)
  # Now find the largest value in t
  bsf = Best()
  for row in t:
    row = [x for x in row if x < inf]  # get rid of any `inf` values
    bsf.reduce(row)
  return bsf.best_so_far


print(main_a(test_input1))  # 4
print(main_a(test_input2))  # 4
print(main_a(test_input3))  # 8
print(main_a(test_input4))  # 8
# print(main_a(input))        # 6725

# Time: ~5440 ms!
# Time: ~4800 ms

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