# https://adventofcode.com/2023/day/23

from Dijkstra import Dijkstra

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
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

dirs = ['^', '>', 'v', '<']

# What is the longest walk you can take from `S` to `E` without stepping on the same square twice?
# https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs
# "For a [directed acyclic graph], the longest path from a source vertex to all other vertices 
# can be obtained by running the shortest-path algorithm on −G [...] 
# derived from G by changing every weight to its negation.""

################################
# Part (a)
################################

def get_matrix(ip_file):
  '''Given the parsed input file, return 
  a dictionary whose keys are states positions `(r,c)` and values are the content of that square.'''
  pass

def ACCESSIBLE_NEIGHBOURS(matrix, st):
  '''Given the `matrix` and a particular position `st = (r,c)`, 
  return the list of accessible positions reachable in one step from `st`.
  NB: DO WE NEED TO DO SOMETHING TO PREVENT THE ALGORITHM FROM RE-CROSSING ITS PATH?'''
  pass

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