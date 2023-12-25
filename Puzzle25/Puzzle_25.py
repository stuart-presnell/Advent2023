# https://adventofcode.com/2023/day/25

from collections import defaultdict

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

showD(make_graph(ip))


################################
# Part (a)
################################

def main_a(ip_filename):
  ip = parse_file(ip_filename)
  pass

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