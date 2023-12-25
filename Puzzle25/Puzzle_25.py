# https://adventofcode.com/2023/day/25

from collections import defaultdict
from copy import deepcopy
from random import choice

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
showD, 
# unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
TTT = Timer(1)

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

# test_input = parse_file("Puzzle25_test.txt")
# input      = parse_file("Puzzle25_input.txt")

# ip = test_input
# ip = input
# show(ip)

def get_keys(G):
  return list(G.keys())

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
  '''Given a graph `G` and a vertex `v` in `G`, 
  return a list of the vertices in the connected component of `v` in `G`.'''
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

def find_all_ccs(G):
  '''Given a graph `G`, return a list of all its connected components.'''
  op = []
  # Make a deepcopy of the list of vertices in `G`
  K = deepcopy(list(G.keys()))
  while K:
    v = K[0]
    CC = find_cc(G, v)
    op.append(CC)
    # Now remove from `K` all the vertices in that connected component
    K = [k for k in K if k not in CC]
  return op

def cut_edge(G, v1, v2, strict=True):
  '''Given two vertices `v1` and `v2` in symmetric graph `G`, 
  return a graph in which that edge has been deleted.'''
  # opG = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  opG = G
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
  op_G = G
  for e in edges:
    op_G = cut_edge(op_G, *e)
  return op_G

def contract_edge(G, edge):
  '''Given an edge `e = (v1,v2)` in graph `G`, 
  return a graph in which that edge has been contracted, and also the name given to the new vertex.'''
  # opG = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  opG = G
  (v1,v2) = edge
  new_v = v1+'-'+v2  # Make a name for the new vertex
  # The new vertex should be connected to every vertex that was connected to `v1` or `v2`
  opG[new_v] = opG[v1].union(opG[v2])
  # For every vertex connected to `v1`, remove the connection to `v1` and replace it with `new_v`
  for v in opG[v1]:
    opG[v].discard(v1)
    opG[v].add(new_v)
  # and likewise for `v2`
  for v in opG[v2]:
    opG[v].discard(v2)
    opG[v].add(new_v)
  # Delete the original two vertices
  del opG[v1]
  del opG[v2]
  # If we now have a self-loop on `new_v`, or a link to `v1` or `v2`, remove these
  opG[new_v].discard(new_v)
  opG[new_v].discard(v1)
  opG[new_v].discard(v2)
  return opG

def pick_random_edge(G):
  '''Given a graph `G`, return a randomly-selected edge of `G`.'''
  v1 = choice(list(G.keys()))
  v2 = choice(list(G[v1]))
  return (v1,v2)

def Karger_pass(G):
  '''Given a graph `G`, run one pass of Karger's algorithm on it, 
  contracting random edges until there are only two vertices remaining.
  The original vertices corresponding to each of these two vertices
  are candidates to be the connected components either side of a cut of `G`.
  * https://en.wikipedia.org/wiki/Karger%27s_algorithm'''
  opG = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  # opG = G
  # TTT.timecheck("deepcopy")  #
  edge_count = 0
  while len(opG.keys()) > 2:
    e = pick_random_edge(opG)
    # TTT.timecheck("pick_random_edge")  #
    opG = contract_edge(opG, e)
    edge_count += 1
    # TTT.timecheck("contract_edge")  #
  return opG

def check_candidate_cut(G, V1, V2):
  '''Given a graph `G` and two composite vertices `V1` and `V2` 
  obtained by contracting vertices of `G` (and whose names are concatenations of names of vertices),
  examine the cut of `G` that this produces; 
  return the number of edges in the cut-set and the sizes of the two connected components.'''
  V1 = V1.split('-')
  V2 = V2.split('-')
  # opG = deepcopy(G)  # Make a deepcopy of the input graph to avoid changing it
  opG = G
  # For each pair of vertices, `v1` in `V1` and `v2` in `V2`
  count = 0
  for v1 in V1:
    for v2 in V2:
      # Remove any connections between `v1` and `v2`
      if v2 in opG[v1]:
        count += 1
        opG[v1].discard(v2)
        opG[v2].discard(v1)
  CCs = find_all_ccs(opG)
  if len(CCs) < 2:
    raise ValueError("Didn't find a cut")
  elif len(CCs) > 2:
    raise ValueError("Cut the graph into more than 2 pieces")
  else:
    sizes = [len(x) for x in CCs]
  return (count, sizes)

def Karger_algorithm(G, verbose=False):
  '''Keep running `Karger_pass` on `G` until we find a minimal cut, 
  which in the present case we have been told contains 3 edges.
  Once we find this, return the sizes of the two connected components.'''
  cut_size = 0
  steps = 0
  while cut_size != 3:
    steps += 1
    copyG = deepcopy(G)
    if verbose: print('.', end='')
    KG = Karger_pass(copyG)
    # TTT.timecheck("Karger_pass")  #
    [V1, V2] = get_keys(KG)
    # print(V1, V2)
    (cut_size, comps) = check_candidate_cut(copyG, V1, V2)
    # print("Sizes of two components are: ", comps)
  print("\nNumber of steps :", steps)
  return comps


################################
# Part (a)
################################

# TODO: Find the three wires you need to cut to divide the graph into two separate parts.
# TODO: What do you get if you multiply the sizes of these two groups together?


def main_a(ip_filename, verbose=False):
  ip = parse_file(ip_filename)
  ip_G = make_graph(ip)
  [a,b] = Karger_algorithm(ip_G, verbose)
  if verbose: print()
  return a*b

# print(main_a("Puzzle25_test.txt", True))  # 54
print(main_a("Puzzle25_input.txt", True)) # 551196

TTT.timecheck("Part (a)")  #

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