# https://adventofcode.com/2023/day/23

from Dijkstra import Dijkstra

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
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

test_input = parse_file("Puzzle23_test.txt")
input      = parse_file("Puzzle23_input.txt")

ip = test_input
# ip = input
show(ip)

# "You're currently on the single path tile in the top row; 
# your goal is to reach the single path tile in the bottom row."
# By inspection, these are as follows in both `test_input` and `input`:
S = (0,1)
E = (-1,-2)

STARTS = [S]
ENDS = None  # Leave this empty so the algorithm explores for as long as possible

# What is the longest walk you can take from `S` to `E` without stepping on the same square twice?
# https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs
# "For a [directed acyclic graph], the longest path from a source vertex to all other vertices 
# can be obtained by running the shortest-path algorithm on −G [...] 
# derived from G by changing every weight to its negation.""

################################
# Part (a)
################################

def get_matrix(ip_file):
  '''Given the parsed input file, return a dictionary 
  whose keys are positions `(r,c)` 
  and whose values are the content of that square.
  Don't represent squares that are `'#'`, just ignore them.'''
  M = {}
  for r in range(len(ip_file)):
    for c in range(len(ip_file[0])):
      sq = ip_file[r][c]
      if sq != '#':
        M[(r,c)] = sq
  return M

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

# M = get_matrix(test_input)
# # showD(M)
# print(ACCESSIBLE_NEIGHBOURS(M, (4,3)))


def STEP_COST(matrix, st, st2):
  '''Since we're looking for the longest path, the step cost will be -1.'''
  return -1

def main_a(ip_filename):
  ip = parse_file(ip_filename)
  pass

# print(main_a("Puzzle23_test.txt"))  # 
# print(main_a("Puzzle23_input.txt")) # 

# TTT.timecheck("Part (a)")  #

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