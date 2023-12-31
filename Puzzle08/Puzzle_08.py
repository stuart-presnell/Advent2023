# https://adventofcode.com/2023/day/8

from itertools import takewhile, dropwhile
from math import lcm
from functools import reduce
from time import perf_counter

TIMING = False
if TIMING: start_time = perf_counter()

################################

f = open("Puzzle08_test_1.txt")
test_input_1 = f.read().splitlines()
f.close()

f = open("Puzzle08_test_2.txt")
test_input_2 = f.read().splitlines()
f.close()

f = open("Puzzle08_test_b.txt")
test_input_b = f.read().splitlines()
f.close()

f = open("Puzzle08_input.txt")
input = f.read().splitlines()
f.close()

def parse_ip(ip_file):
  route_code = list(takewhile(lambda x: x != "", ip_file))[0]
  tree_list = list(dropwhile(lambda x: x != "", ip_file))[1:]  # Remove blank line at start
  tree = {}
  for line in tree_list:
    [node, pair] = line.split(" = ")
    [left, right] = pair[1:-1].split(", ")
    tree[node] = [left,right]
  return (route_code, tree)

# Starting with AAA, you need to look up the next element 
# based on the next left/right instruction in your input.

def next_step(route_code, tree, i, current_node, verbose=False):
  if verbose: print(current_node, end='\n')
  step = i%len(route_code)    # loop around when we fall off the end of the string
  # look up where to go next
  if verbose: print(route_code[step])
  if route_code[step] == 'L':
    next_node = tree[current_node][0]
  elif route_code[step] == 'R':
    next_node = tree[current_node][1]
  else:
    raise ValueError
  return next_node

def follow_route(route_code, tree, stop_criterion, current_node = None, verbose = False):
  '''Given instructions for how to step and a tree to step through, 
  a function reporting whether to stop, [and optionally a starting point, or 'AAA'],
  return the number of steps taken until reaching a stopping node.'''
  if not current_node:
    current_node = 'AAA'
  i = 0
  while not stop_criterion(current_node):
    next_node = next_step(route_code, tree, i, current_node)
    current_node = next_node
    i += 1
  if verbose: print(current_node, end='\n\n')
  return i

################################
# Part (a)
################################

# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

def is_ZZZ(s):
  return s == 'ZZZ'

def main_a(ip_file):
  (route_code, tree) = parse_ip(ip_file)
  i = follow_route(route_code, tree, is_ZZZ)
  print(i)

main_a(test_input_1)  # 2
main_a(test_input_2)  # 6
main_a(input)         # 12083

################################
# Part (b)
################################

def ends_Z(s):
  return s[-1] == 'Z'

def X_nodes(t, X):
  return [item for item in t.keys() if item[2]==X]

# For each starting node, find how long it takes to reach a stopping node
# Then take the lowest common multiple of these cycles
def main_b(ip_file):
  (route_code, tree) = parse_ip(ip_file)
  x = [follow_route(route_code, tree, ends_Z, node) for node in X_nodes(tree, 'A')]
  l = reduce(lcm, x)
  print(l)

main_b(test_input_1)  # 2
main_b(test_input_2)  # 6
main_b(test_input_b)  # 6
main_b(input)         # 13385272668829

################################
if TIMING:
  end_time = perf_counter()
  print()
  print("Time taken: ", (end_time - start_time)*1000, "ms")

################################
################################

# Original attempt at part (b): keep a list of current nodes and update them all together
# Since the answer is ~13.4 trillion, this method was insufficiently quick

# def all_end_Z(L):
#   return all([item[-1] == 'Z' for item in L])

# def follow_route_b(route_code, tree, current_nodes = None, verbose = False):
#   if not current_nodes:
#     current_nodes = X_nodes(tree, 'A')
#   i = 0
#   # n = len(route_code)
#   # nodes_visited = []
#   while not all_end_Z(current_nodes):
#     # step every current node simultaneously
#     next_nodes = [next_step(route_code, tree, i, node) for node in current_nodes]
#     if verbose: print(next_nodes)
#     current_nodes = next_nodes
#     i += 1
#   return i
