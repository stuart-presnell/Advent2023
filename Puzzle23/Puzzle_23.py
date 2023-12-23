# https://adventofcode.com/2023/day/23

import re
from Dijkstra import Dijkstra
from math import ceil, log10, inf
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
# TTT = Timer(1)

################################

def parse_file(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

# test_input = parse_file("Puzzle23_test.txt")
input      = parse_file("Puzzle23_input.txt")

# ip = test_input
ip = input
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

################################
################################

# DONE: We're going to run individual mice through the maze.
# DONE: Each mouse will record its current and previous positions and the distance it has travelled. 
# DONE: Keep a queue of mice currently running. 
# DONE: At each step a mouse updates and replaces itself on the queue 
  # with a copy of itself for each available forward step. 
# DONE: When a mouse hits `E`, collect its distance and let it fall off the queue.

def ACCESSIBLE_NEIGHBOURS_a(matrix, st):
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

def non_previous_neighbours(matrix, pos, prev):
  '''Filter out `prev` from the accesible neighbours of `st`.'''
  return [pt for pt in ACCESSIBLE_NEIGHBOURS_a(matrix, pos) if pt != prev]

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
  
# print(main_a("Puzzle23_test.txt"))  #   94
# print(main_a("Puzzle23_input.txt")) # 2042

# TTT.timecheck("Part (a)")  # ~ 140 ms

################################
# Part (b)
################################

# "Now, treat all slopes as if they were normal paths."


def ACCESSIBLE_NEIGHBOURS_b(matrix, st):
  '''Given the `matrix` and a particular position `st = (r,c)`, 
  return the list of accessible positions reachable in one step from `st`.'''
  # Just in case we're passed an illegal position
  if st not in matrix:
    return []
  # We can AT MOST step in the 4 cardinal directions
  (r,c) = st
  NSWE = [(r-1, c),(r+1, c),(r, c-1),(r, c+1)]
  
  # Now filter down to those positions that are actually in `matrix`.
  return [pt for pt in NSWE if pt in matrix]



# TODO: Let's start by extracting a graph from the given grid; 
# so rather than traversing through the grid step by step we can hop from vertex to vertex.

M = matrix_to_dict(ip)
# showD(M)
ht = len(ip)
wd = len(ip[0])
S = (0,1)
E = (ht-1, wd-2)
# print(E)


def extract_graph(matrix):
  '''Given a dictionary `matrix` representing the grid, return a graph 
  represented by a set of vertices and a set `(v1, v2, l)` and `(v2, v1, l)` of weighted edges.'''
  unvisited = set(matrix.keys())
  vertices = {S, E}
  edges = set()
  # A list of half-edges `(V, pt, l)`, each emanating from vertex `V`, 
  # reaching to `pt` so far, currently of length `l`.
  tendrils = [(S,S,0)]   
  while tendrils:
    # print(tendrils)
    (V, pt, l) = tendrils.pop()
    # print("Growing tendril", V, pt, l)
    if (pt in vertices) & (l > 0): # if this is an extended tendril reaching a known vertex
      # print("Found a new edge between ", V, " and ", pt)
      edges.add((V, pt, l))
      # edges.add((pt, V, l))
      if pt == E:  # if, moreover, the vertex is `E` then there's nothing more to do
        pass
      else:  # otherwise start a new tendril from this vertex, ready to start growing
        tendrils.append((pt, pt, 0))
      continue  # we're done with this tendril; move on to the next
    # Otherwise, the tendril has not extended to a known vertex, 
    # so we need to know about the neighbourhood ot `pt`.
    N = ACCESSIBLE_NEIGHBOURS_b(matrix, pt)
    if (len(N) >= 3) & (l > 0):    # if this is an extended tendril reaching a NEW vertex
      # print("Found a new vertex at ", pt)
      vertices.add(pt)
      edges.add((V, pt, l))
      # edges.add((pt, V, l))
      # print("Adding the edge between ", V, " and ", pt)
      tendrils.append((pt, pt, 0))
    # Otherwise, it's either a tendril of length zero at a vertex, or a tendril mid-way along an edge
    # Either way, let it grow into all unvisited neighbouring squares
    elif (len(N) == 2):  # if it's midway along an edge
      for pt2 in N:
        if (pt2 in unvisited) & (pt2 != V):  # don't let it grow backward or into its starting vertex
          tendrils.append((V, pt2, l+1))
      unvisited.remove(pt)
    elif (l == 0):  # if it's a tendril of length zero at a vertex
      # Filter N to just the unvisited neighbouring points
      N = [pt for pt in N if pt in unvisited]
      # if there are no unvisited paths neighbouring this vertex then it's done
      if N == []:
        # unvisited.remove(pt)
        continue  # move on to the next tendril
      else:
      # we want to start one tendril growing along an unvisited path departing this vertex
      # but we also want to revisit this vertex later to let further tendrils grow from it.
        pt2 = N[-1]
        tendrils.append((pt,pt,0))
        tendrils.append((pt,pt2,1))
  return vertices, edges

def make_simpler_graph(V, E):
  '''Given a set of vertices `V` and a set of edges `E` of the form `(v1,v2,w)`, 
  return a dictionary `G` whose keys are numbers `0,...,|V|`
  where `G[n]` is a list of pairs indicating all vertices adjacent to vertex `n` and the edge weight.
  Using an idea from: https://stackoverflow.com/a/29321323
  '''
  V = list(V)
  E = list(E)
  V.sort()
  V_dict = {V[i] : i for i in range(len(V))}

  G = defaultdict(list)
  for (s,t,l) in E:
    G[V_dict[s]].append((V_dict[t],l))
    G[V_dict[t]].append((V_dict[s],l))
  return G

# G = make_simpler_graph(*extract_graph(M))


# print(main_b_v1("Puzzle23_test.txt"))  # 154
# print(main_b_v1("Puzzle23_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################

# def main_b_v1(ip_filename):
#   '''Now let each mouse record the path it has taken. 
#   So each mouse is just a trail, with its current position at the end. 
#   When deciding which squares are accessible, don't let it retrace its steps.'''
#   ip = parse_file(ip_filename)
#   ht = len(ip)
#   wd = len(ip[0])
#   S = (0,1)
#   E = (ht-1, wd-2)
#   M = matrix_to_dict(ip)
#   # We start with one mouse at `S`.
#   current_mice = [[S]]
#   # At the start, no mice have escaped to report path lengths
#   complete_path_lengths = []

#   while current_mice:
#     mouse_path = current_mice.pop()
#     pos = mouse_path[-1]
#     if pos == E:  # if this mouse has escaped
#       complete_path_lengths.append(len(mouse_path) - 1)  # record the length of the path taken
#     for next_pos in ACCESSIBLE_NEIGHBOURS_b(M, pos):
#       if next_pos not in mouse_path:
#         current_mice.append(mouse_path + [next_pos])

#   # print(complete_path_lengths)
#   return max(complete_path_lengths)
