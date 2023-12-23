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
# S = (0,1)
# E = (-1,-2)  # But we can't use this as the literal coords of `E`

# ht = len(ip)
# wd = len(ip[0])
# E = (ht-1, wd-2)

# What is the longest walk you can take from `S` to `E` without stepping on the same square twice?

def ACCESSIBLE_NEIGHBOURS(matrix, st):
  '''Given the `matrix` and a particular position `st = (r,c)`, 
  return the list of accessible positions reachable in one step from `st`.'''
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

################################
################################

# DONE: We're going to run individual mice through the maze.
# DONE: Each mouse will record its current and previous positions and the distance it has travelled. 
# DONE: Keep a queue of mice currently running. 
# DONE: At each step a mouse updates and replaces itself on the queue 
  # with a copy of itself for each available forward step. 
# DONE: When a mouse hits `E`, collect its distance and let it fall off the queue.

def non_previous_neighbours(matrix, pos, prev):
  '''Filter out `prev` from the accesible neighbours of `st`.'''
  return [pt for pt in ACCESSIBLE_NEIGHBOURS(matrix, pos) if pt != prev]

def main_a(ip_filename):
  ip = parse_file(ip_filename)
  ht = len(ip)
  wd = len(ip[0])
  S = (0,1)
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
  
print(main_a("Puzzle23_test.txt"))  #   94
print(main_a("Puzzle23_input.txt")) # 2042

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