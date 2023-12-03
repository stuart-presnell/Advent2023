# https://adventofcode.com/2023/day/3

# test_input : list[str] = [

# ]


# f = open("Puzzle03_test.txt")
f = open("Puzzle03_input.txt")
M = f.read().splitlines()
f.close()

def show(x):
  for line in x:
    print(line)
  print("-" * len(x[0]))
  print()

# show(M)

def pad(M):
  '''Given an m by n matrix M, represented as a list[str],
  add a layer of dots around its border (to avoid index errors)'''
  width = len(M[0])
  output = []
  pad_row = "o" * (width + 2)
  output.append(pad_row)
  for row in M:
    padded_row = "o" + row + "o"
    output.append(padded_row)
  output.append(pad_row)
  return output

M = pad(M)

# show(M)


def isdigit(x:str) -> bool:
  return x in ['1','2','3','4','5','6','7','8','9','0']

def neighbours(M, row, col_start, col_end) -> str:
  '''In matrix M, given a row and a range of columns,
  return the contents of all neighbouring cells as a string'''
  output = ""
  output += M[row-1][col_start-1:col_end+2]
  # output += "\t"
  output += M[row][col_start-1]
  # output += "\t"
  output += M[row][col_end+1]
  # output += "\t"
  output += M[row+1][col_start-1:col_end+2]
  return output

################################
# Part (a)
################################

def gather_number(M, row, col):
  '''In matrix M a nunmber starts at M[row][col]; return this number as a string'''
  output = "" # initialise the string
  for i in range(len(M[0])-col):
    if isdigit(M[row][col+i]):
      output += M[row][col+i]
    else:
      break
  return output

def reduce_to_symbols(s:str):
  '''Filter a string to keep just the symbols'''
  output = ""
  for x in s:
    if isdigit(x) | (x=='o') | (x=='.'):
      pass
    else:
      output += x
  return output

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
# 114 (top right) and 58 (middle right).
# Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

def find_and_classify_numbers(M):
  '''Find all the part numbers and non-part numbers in matrix M'''
  part_numbers = []
  non_part_numbers = []
  height = len(M)
  width  = len(M[0])
  for row in range(1, height-1):
    col = 1
    while col < width:
      if not isdigit(M[row][col]):
        col += 1
      else:
        x = gather_number(M, row, col)
        l = len(x)
        N = neighbours(M, row, col, col+l-1)
        neighbour_symbols = reduce_to_symbols(N)
        # print("neighbours of " + str(x) + " are: " + N)
        if neighbour_symbols:
          part_numbers.append(x)
        else:
          non_part_numbers.append(x)
        col += l  # jump the pointer ahead
  return (part_numbers, non_part_numbers)

# print(find_and_classify_numbers(M))

# What is the sum of all of the part numbers in the engine schematic?

(pn, npn) = find_and_classify_numbers(M)
pn = map(int, pn)
pn = list(pn)
# print(pn)
s = sum(pn)

# print(s) # 535235

################################
# Part (b)
################################

# A gear is any * symbol that is adjacent to exactly two part numbers.
# Its gear ratio is the result of multiplying those two numbers together.

def find_stars(M):
  star_coords = []
  height = len(M)
  width  = len(M[0])
  for row in range(1, height-1):
    for col in range(1, width-1):
      if M[row][col] == "*":
        star_coords.append((row,col))
  return star_coords

def find_and_locate_numbers(M):
  '''Find all numbers in matrix M; return them and their locations'''
  op = [[]] # initialise with one blank row corresponding to the row of padding in M
  height = len(M)
  width  = len(M[0])
  for row in range(1, height-1):
    op_row = []
    col = 1
    while col < width:
      if not isdigit(M[row][col]):
        col += 1
      else:
        x = gather_number(M, row, col)
        op_row.append([x, row, col, col+len(x)-1])
        col += len(x)  # jump the pointer ahead
    op.append(op_row)
  return op

# show(find_and_locate_numbers(M))


NUMBER_LOCS = find_and_locate_numbers(M)

def isadj(pos, range_start, range_end) -> bool:
  return (range_start <= pos+1) & (range_end >= pos-1)

def find_adj_numbers(row, col):
  '''Given coords in M, find all numbers adjacent to that position'''
  op = []
  for r in range(row-1, row+2): # only check the current row and those immediately above and below
    for entry in NUMBER_LOCS[r]: # check every number recorded in these rows
      n = entry[0]
      range_start = entry[2]
      range_end   = entry[3]
      if isadj(col, range_start, range_end):
        op.append(n)
  return op

# print(find_adj_numbers(9,6))

# print(find_stars(M))


# What is the sum of all of the gear ratios in your engine schematic?

op = 0
for star in find_stars(M):
  (row,col) = star
  adj = find_adj_numbers(row, col)
  # print(star, adj, len(adj))
  if len(adj) == 2:
    x = int(adj[0])
    y = int(adj[1])
    op += x*y

print(op) # 79844424
