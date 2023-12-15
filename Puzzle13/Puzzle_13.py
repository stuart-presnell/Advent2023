# https://adventofcode.com/2023/day/13

# My utility functions
from utils import chunk_splitlines, rotate90, Timer

TTT = Timer(1)

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

def find_block_symmetry(block):
  '''Given a block that is assumed to have exactly one symmetry, 
  return `[n,d]` where `n` is the row/column of the symmetry and `d` is `'H'` or `'V'`.'''
  v = find_vertical_symmetry(block)
  if v:
    v = v[0]    
    return [v, "V"]
  else:
    h = find_vertical_symmetry(rotate90(block))
    h = h[0]  # But this counts the number of rows BELOW the symmetry, b/c we rotated 90 not -90
    h = len(block) - h
    return [h, "H"]

def find_all_symmetries(block):
  '''Given a block, return all its vertical symmetries and all its horizontal symmetries.'''
  v = find_vertical_symmetry(block)
  h = find_vertical_symmetry(rotate90(block))
  h = [len(block) - x for x in h]
  return (v,h)

################################
# Part (a)
################################

# Add up the number of columns to the left of each vertical line of reflection; 
# to that, also add 100 multiplied by the number of rows above each horizontal line of reflection

def main_a(ip):
  count = 0
  for block in ip:
    [n,d] = find_block_symmetry(block)
    # print(n,d)
    if d == 'V':
      count += n
    elif d == 'H':
      count += n * 100
  return count


print(main_a(test_input))  # 405
print(main_a(input))       # 27742
TTT.timecheck("Part (a)")  # 15 ms

################################
# Part (b)
################################

def neg_char(c):
  return '.' if c == '#' else '#'

def swap(r,c,B):
  B[r] = B[r][:c] + neg_char(B[r][c]) + B[r][c+1:]
  return B

def find_new_symmetry(block):
  (v,h) = find_all_symmetries(block)
  # print(v,h, " is the symmetry of the original block")
  for r in range(len(block)):
    for c in range(len(block[0])):
      B = swap(r,c,block.copy())
      [v1,h1] = find_all_symmetries(B)
      if (v1,h1) == ([],[]):
        continue
      # else:
      if (v1 == v) & (h1 == h):
        continue
      else:
        # print(v1,h1, "is the symmetry of the new block")
        # print("Found a new symmetry")
        # print(v1,h1, r, c)
        nsv = list(set.difference(set(v1),set(v)))
        nsh = list(set.difference(set(h1),set(h)))
        return(nsv, nsh)

def main_b(ip):
  count = 0
  for block in ip:
    [v,h] = find_new_symmetry(block)
    if v:
      count += v[0]
    else:
      count += h[0] * 100
  return count

main_b(test_input)      # 400
main_b(input)           # 32728
TTT.timecheck("Final")  # 1480 ms

################################
