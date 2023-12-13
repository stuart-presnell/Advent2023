# https://adventofcode.com/2022/day/13

# My utility functions
from utils import (
show, 
chunk_splitlines, 
# printT, showM, parse_nums, 
rotate90, 
# close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = chunk_splitlines(f.read())
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle13_test.txt")
input      = parse_file_a("Puzzle13_input.txt")

ip = test_input

# Each line of `ip` is one block
[block0, block1] = test_input
block98 = input[98]

# show(block0)
show(block98)

def check_row_symmetry(row, pos) -> bool:
  '''Given a row, e.g. "#.##..##.", and a position, check whether `row` is symmetric about `pos`.'''
  L = len(row)
  if pos <= L//2:
    left  = row[:pos]
    right = row[pos:2*pos]
  else:
    chunk_size = L-pos
    left  = row[L-2*chunk_size:pos]
    right = row[pos:]
  return (left == right[::-1])

def find_row_symmetries(row):
  '''Given a row, e.g. "#.##..##.", return all positions around which it's vertically symmetric.'''
  return set([pos for pos in range(1,len(row)) if check_row_symmetry(row, pos)])

def find_vertical_symmetry(block):
  s = [find_row_symmetries(row) for row in block]
  i = list(set.intersection(*s))
  return i

# s = find_vertical_symmetry(block1)
# print(s)

def find_block_symmetry(block):
  v = find_vertical_symmetry(block)
  if v:
    v = v[0]    # Assuming there's exactly one symmetry
    return [v, "V"]
  else:
    h = find_vertical_symmetry(rotate90(block))
    h = h[0]    # Assuming there's exactly one symmetry
    return [h, "H"]

def find_both_symmetries(block):
  v = find_vertical_symmetry(block)
  h = find_vertical_symmetry(rotate90(block))
  return [v,h]

for block in input:
  [v,h] = find_both_symmetries(block)
  if v:
    if h:
      print("Both!")



#     match len(s):
#       case 0: # If we've eliminated all positions for a vertical symmetry
#         if H:
#           raise ValueError("This block appear to have no symmetry at all!")
#         else:
#           print("No vertical symmetry, try horizontal")
#           block = rotate90(block)
#           return find_block_symmetry(block, H = True)
#       # case 1: # If we've 
#       #   print("Found it!")
#       #   return (s[0], H)  # 
#       case _: pass

################################
# Part (a)
################################

# def main_a(ip):
#   pass

# main_a(test_input)  # 
# main_a(input)       # 


################################
# Part (b)
################################

# def main_b(ip):
#   pass

# main_b(test_input)  # 
# main_b(input)       # 


################################

# TTT.timecheck("Final")