# https://adventofcode.com/2023/day/11

# My utility functions
from utils import rotate90, Timer

TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle11_test.txt")    # There are 9 '#'s in test_input
input      = parse_file_a("Puzzle11_input.txt")   # There are 455 '#'s in input
expansion_test1 = parse_file_a("expansion_test1.txt")

def duplicate_empty_rows(M, n = 2):
  '''Expand every row and column not containing '#', duplicating it `n` times.'''
  op = []
  for row in M:
    if '#' in row:
      op.append(row)
    else:
      op += ([row] * n)
  return op

def expand_universe(M, n=2):
  M = duplicate_empty_rows(M, n)
  M = rotate90(M)
  M = duplicate_empty_rows(M, n)
  M = rotate90(M)
  M = rotate90(M)
  M = rotate90(M)
  M = ["".join(row) for row in M]
  return M

def find_galaxies(M):
  return [(row,col) for row in range(len(M)) for col in range(len(M[0])) if M[row][col] == '#']

def stepping_distance(P, Q):
  '''Given two points, return the shortest distance between them by NSWE steps'''
  return abs(Q[0] - P[0]) + abs(Q[1] - P[1])

################################
# Part (a)
################################

def main_a(M, n=2):
  M = expand_universe(M, n)
  G = find_galaxies(M)
  x = sum([stepping_distance(G[a], G[b]) for a in range(len(G)) for b in range(a+1, len(G))])
  print(x)

# main_a(test_input)  # 374
# main_a(input)       # 10228230

# Time: ~ 30 ms

################################
# Part (b)
################################

def empty_rows(M):
  return [i for i in range(len(M)) if '#' not in M[i]]

def empty_cols(M):
  return empty_rows(rotate90(M))

def stepping_distance_b(P, Q, ER, EC, n=2):
  '''Given two points, return the shortest distance between them by NSWE steps, 
  while extra-counting empty rows and empty columns by a factor of n.'''
  lox = min(P[0], Q[0])
  hix = max(P[0], Q[0])
  loy = min(P[1], Q[1])
  hiy = max(P[1], Q[1])
  empty_rows_btn = len([x for x in ER if lox < x < hix])
  empty_cols_btn = len([y for y in EC if loy < y < hiy])
  return stepping_distance(P, Q) + ((n-1) * empty_rows_btn) + ((n-1) * empty_cols_btn)

def main_b(M, n=2):
  G = find_galaxies(M)
  ER = empty_rows(M)
  EC = empty_cols(M)
  x = sum([stepping_distance_b(G[a], G[b], ER, EC, n) 
           for a in range(len(G)) for b in range(a+1, len(G))])
  print(x)

main_b(test_input, 2)    # s/b 374
main_b(test_input, 10)   # s/b 1030
main_b(test_input, 100)  # s/b 8410
main_b(input, 2)         # s/b 10228230
main_b(input, 1000000)   # 447073334102

################################

TTT.timecheck("Final")
# Time: ~ 330 ms