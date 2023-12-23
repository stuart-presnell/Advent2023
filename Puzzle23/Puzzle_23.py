# https://adventofcode.com/2023/day/23

from Dijkstra import Dijkstra
from math import ceil, log10
from collections import defaultdict

# My utility functions
from utils import (
show, 
matrix_to_dict,
# chunk_splitlines, printT, 
showM, 
showD, 
# unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def parse_file(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

# test_input = parse_file("Puzzle23_test.txt")
# input      = parse_file("Puzzle23_input.txt")

# ip = test_input
# ip = input
# show(ip)

################################
# Part (a)
################################

# "You're currently on the single path tile in the top row; 
# your goal is to reach the single path tile in the bottom row."
# By inspection, these are as follows in both `test_input` and `input`:
S = (0,1)
# E = (-1,-2)  # But we can't use this as the literal coords of `E`

# ht = len(ip)
# wd = len(ip[0])
# E = (ht-1, wd-2)

# What is the longest walk you can take from `S` to `E` without stepping on the same square twice?
# https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs
# "For a [directed acyclic graph], the longest path from a source vertex to all other vertices 
# can be obtained by running the shortest-path algorithm on −G [...] 
# derived from G by changing every weight to its negation.""


# STARTS = [S]
# ENDS = None  # Leave this empty so the algorithm explores for as long as possible

def ACCESSIBLE_NEIGHBOURS(matrix, st):
  '''Given the `matrix` and a particular position `st = (r,c)`, 
  return the list of accessible positions reachable in one step from `st`.
  - NB: DO WE NEED TO DO SOMETHING TO PREVENT THE ALGORITHM FROM RE-CROSSING ITS PATH?
  OR IS THIS TAKEN CARE OF BY THE USE OF `unvisited`?'''
  # Just in case we're passed an illegal position
  if st not in matrix:
    return []
  # We can AT MOST step in the 4 cardinal directions
  (r,c) = st
  NSWE = [(r-1, c),(r+1, c),(r, c-1),(r, c+1)]
  
  # "if you step onto a slope tile, your next step must be (in the direction the arrow is pointing)"
  dirs = ['^', 'v', '<', '>']
  if matrix[st] in dirs:
    idx = dirs.index(matrix[st])
    NSWE = [NSWE[idx]]
  # Now filter down to those positions that are actually in `matrix`.
  return [pt for pt in NSWE if pt in matrix]

def STEP_COST(matrix, st, st2):
  '''Since we're looking for the longest path, the step cost will be -1.'''
  return -1

# # showD(M)
# print(ACCESSIBLE_NEIGHBOURS(M, (4,3)))

# (T,P) = Dijkstra(M, STARTS, ENDS, ACCESSIBLE_NEIGHBOURS, STEP_COST)
# for pos in T:
#   T[pos] = -T[pos]

def dict_to_matrix(D, ht, wd, default='#'):
  '''Given a dictionary `D` whose keys are pairs `(r,c)`
  representing a (sparse) `ht * wd` matrix, 
  and a default value `default` to fill any empty spaces,
  return a matrix of these values (i.e. a list of lists).'''
  max_val = max(D.values())
  max_digits = ceil(log10(max_val))
  default = ' ' * (max_digits) + default
  op = []
  for r in range(ht):
    op_row = []
    for c in range(wd):
      op_row.append(D[(r,c)] if (r,c) in D else default)
    op.append(op_row)
  return op

# M2 = dict_to_matrix(T, ht, wd)
# showM(M2, 1)

################################
################################

# TODO: Try a different approach to enumerate (the lengths of) all paths from `S` to `E`.
# TODO: Start with [0] at S; {S} is the current set of occupied squares.
# TODO: For each curently occupied square, also record the *previous* square we were at.
# TODO: For each currently occupied square `x`, find all non-previous squares accesible from it.
# TODO: If L is the list of path lengths to `x`, for each of these neighbours we concat `map(+1, L)`.
# TODO: If we arrive at an already-visited square, concatting will combine the sets of paths.

# TODO: Then update the list of currently occupied squares.
# TODO: When we arrive at `E` we should have a list of all path lengths from `S` to `E`.
# TODO: Finally, return the length of the longest path from `S` to `E`.

# M = get_matrix(test_input)
# showD(M)

# A dictionary mapping each visited point to the list of path-lengths from `S` to that point
# path_lengths = defaultdict(list)
# path_lengths[S] = [0]

# A list of currently occupied squares, each tagged with the previous square visited.
# Think of these as mice exploring the graph, each occupying a square and dragging its tail behind.
# current_sites = [(S, S)]   # The mouse starts with its tail curled around it at `S`!

################################
################################

def non_previous_neighbours(matrix, pos, prev):
  '''Filter out `prev` from the accesible neighbours of `st`.'''
  return [pt for pt in ACCESSIBLE_NEIGHBOURS(matrix, pos) if pt != prev]

# TODO: Try something simpler: just run individual mice through the maze, each recording its current and previous positions and the distance it has travelled. Keep a queue of mice currently running. At each step a mouse updates and replaces itself on the queue with a copy of itself for each available forward step. When a mouse hits `E`, collect its distance and let it fall off the queue.


def main_a(ip_filename):
  ip = parse_file(ip_filename)
  ht = len(ip)
  wd = len(ip[0])
  E = (ht-1, wd-2)
  M = matrix_to_dict(ip)
  # We start with one mouse at `S`, with its tail curled around it, having travelled no distance.
  current_mice = [(S,S,0)]
  # At the start, no mice have escaped to report path lengths
  complete_path_lengths = []

  while current_mice:
    (pos, prev, d) = current_mice.pop()
    if pos == E:  # if this mouse has escaped
      complete_path_lengths.append(d)
    for next_pos in non_previous_neighbours(M, pos, prev):
      current_mice.append((next_pos, pos, d+1))

  # print(complete_path_lengths)
  return max(complete_path_lengths)


# print(path_lengths)
# for (pos,prev) in current_sites:
#   pls = [x+1 for x in path_lengths[pos]]
#   n = non_previous_neighbours(M, pos, prev)
#   for pt in n:
#     path_lengths[pt] += pls

# print()
# print(path_lengths)
  
print(main_a("Puzzle23_test.txt"))  # 
print(main_a("Puzzle23_input.txt")) # 

# TTT.timecheck("Part (a)")  #

################################
################################
# Part (b)
################################

# def main_b(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_b("Puzzle23_test.txt"))  # 
# print(main_b("Puzzle23_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################