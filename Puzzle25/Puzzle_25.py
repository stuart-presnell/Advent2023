# https://adventofcode.com/2023/day/25

from collections import defaultdict
from copy import deepcopy

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
  op = []
  for line in ip_file:
    line = line.split(": ")
    line[1] = line[1].split(" ")
    op.append(line)
  return op

test_input = parse_file("Puzzle25_test.txt")
input      = parse_file("Puzzle25_input.txt")

ip = test_input
# ip = input
# show(ip)


def make_graph(ip_file):
  '''Given a parse input file, make a symmetric graph from it.'''
  G = defaultdict(set)
  # Insert the nodes that are named on the left side of a colon; 
  # give each an edge to each node on the right of its line
  for line in ip_file:
    G[line[0]] = set(line[1])
  # Now ensure that all nodes on the right of a colon are included,
  # and that each has an edge to the node on the left side of its line
  for line in ip_file:
    for v in line[1]:
      G[v].add(line[0])
  return G

def find_cc(G, v):
  '''Given a graph `G` and a vertex `v` in `G`, return the connected component of `v` in `G`.'''
  # `cc` is a list of all the nodes we visit; it only grows
  cc = [v]
  # `to_consider` is also a list of all the nodes we visit, but we pop items off it until it's empty
  to_consider = [v]
  while to_consider:
    curr = to_consider.pop()
    # Get all the neighbours of `curr` 
    all_nb = list(G[curr])
    # Keep just the neighbours that we haven't already seen are in the connected component
    uv_nb = [x for x in all_nb if x not in cc]
    cc.extend(uv_nb)
    to_consider.extend(uv_nb)
    # break
  return cc

def cut_edge(G, v1, v2, strict=True):
  '''Given two vertices `v1` and `v2` in symmetric graph `G`, 
  return a graph in which that edge has been deleted.'''
  opG = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  if (v1 not in G[v2]) | (v2 not in G[v1]):
    if strict:    # If `strict` is set, require that the vertices are connected
      raise ValueError("Vertices " + v1 + " and " + v2 + "are not connected")
    else:
      return G
  opG[v1].remove(v2)
  opG[v2].remove(v1)
  return opG

def cut_edge_set(G, edges):
  '''Given a symmetric graph `G` and a list of `edges` to cut, each given as a pair `(v1,v2)`,
  return a graph in which those edges have been deleted.'''
  op_G = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  for e in edges:
    op_G = cut_edge(op_G, *e)
  return op_G


# TODO: Find the three wires you need to cut to divide the graph into two separate parts.
# TODO: What do you get if you multiply the sizes of these two groups together?



ip_G = make_graph(ip)
showD(ip_G); print()

G2 = cut_edge_set(ip_G, [('jqt', 'ntq')])

# 'hfx','pzl'
# 'bvb','cmg'
# 'nvd','jqt'

showD(ip_G); print()
# showD(G2); print()

# k = list(ip_G.keys())[0]
# print(k)
# C = find_cc(ip_G, k)
# print(set(C) == set(ip_G.keys())) # True -- the whole graph is connected



################################
# Part (a)
################################

# def main_a(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_a("Puzzle25_test.txt"))  # 
# print(main_a("Puzzle25_input.txt")) # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_b("Puzzle25_test.txt"))  # 
# print(main_b("Puzzle25_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################