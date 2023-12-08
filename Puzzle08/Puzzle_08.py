# https://adventofcode.com/2023/day/8

from itertools import takewhile, dropwhile

def show(x):
  for line in x:
    print(line)
  print("-" * len(x[0]))
  print()

def parse_nums(s:str) -> list[int]:
  '''Given a string of the form "a b c ... z", where each entry is a number, return a list[int]'''
  op = s.split()
  op = list(map(int,op))  # This will raise an error if any entry doesn't parse as a number
  return op

def rotate90(M):
  '''Given a matrix `M` consisting of a list of strings (or a list of lists), 
  rotate it 90 degrees clockwise'''
  return [list(reversed([M[j][i] for j in range(len(M))]))
            for i in range(len(M[-1]))]

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

################################
# Part (a)
################################

def parse_ip(ip_file):
  route_code = list(takewhile(lambda x: x != "", ip_file))[0]
  tree_list = list(dropwhile(lambda x: x != "", ip_file))[1:]  # Remove blank line at start
  tree = {}
  for line in tree_list:
    [node, pair] = line.split(" = ")
    [left, right] = pair[1:-1].split(", ")
    tree[node] = [left,right]
  return (route_code, tree)

# print(tree)

# Starting with AAA, you need to look up the next element 
# based on the next left/right instruction in your input.

# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

def follow_route(route_code, tree, verbose = False):
  current_node = 'AAA'
  i = 0
  n = len(route_code)
  nodes_visited = []
  while current_node != 'ZZZ':
    if verbose: print(current_node, end='\n')
    step = i%n    # loop around when we fall off the end of the string
    # look up where to go next
    if verbose: print(route_code[step])
    if route_code[step] == 'L':
      next_node = tree[current_node][0]
    elif route_code[step] == 'R':
      next_node = tree[current_node][1]
    else:
      raise ValueError
    # record where we're going, then step there
    nodes_visited.append(next_node)
    current_node = next_node
    i += 1
  if verbose: print(current_node, end='\n\n')
  return nodes_visited


def main_a(ip_file, verbose = False):
  (route_code, tree) = parse_ip(ip_file)
  nv = follow_route(route_code, tree, verbose)
  print(len(nv))

main_a(test_input_1)  # 2
main_a(test_input_2)  # 6
main_a(input)         # 12083

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# main_b(test_input)  # 
# main_b(input)       # 