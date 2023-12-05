# https://adventofcode.com/2023/day/5

import re
import time

# f = open("Puzzle05_test.txt")
f = open("Puzzle05_input.txt")
input = f.read().splitlines()
f.close()

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

# show(input[:10])

# The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

# The rest of the almanac contains a list of maps which describe 
# how to convert numbers from a source category into numbers in a destination category.

# the section that starts with seed-to-soil map: 
# describes how to convert a seed number (the source) to a soil number (the destination).

# Rather than list every source number and its corresponding destination number one by one, 
# the maps describe entire ranges of numbers that can be converted.
# Each line within a map contains three numbers: 
# the destination range start, the source range start, and the range length.

# 50 98 2 => source range [98, 99] -> destination range [50, 51]
# seed number 98 corresponds to soil number 50 and seed number 99 corresponds to soil number 51.

# 52 50 48 => source range [50, 50+48-1] -> destination range [52, 52+48-1]
# So, seed number 53 corresponds to soil number 55.

# Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

################################


# chunk the rest of the file after the first line
maps_str_list=[]
current_map=[]
for line in input[2:]:  # skip the 'seeds' line and the blank line after it
  if not line:
    maps_str_list.append(current_map)
    current_map=[]
  else:
    current_map.append(line)
maps_str_list.append(current_map)  # append final map!  

# Cut off header lines
maps_str_list = [map[1:] for map in maps_str_list]

maps = []
for M in maps_str_list:
  maps.append([parse_nums(line) for line in M])

# Each entry of `maps` corresponds to one transition map
# It consists of a list of lists, e.g. [[50, 98, 2], [52, 50, 48]]
# Each list in the map corresponds to one block of the transition
# [50, 98, 2] is the block with destination_start = 50, source_start = 98, range = 2


maps2 = []
for M in maps:
  M2 = []
  for line in M:
    [d,s,r] = line
    M2.append([s, s+r-1, d-s])
  M2.sort()
  maps2.append(M2)

# Each entry of `maps2` corresponds to one transition map
# It consists of a list of lists, e.g. [[50, 97, 2], [98, 99, -48]]
# Each list in the map corresponds to one block of the transition
# [50, 97, 2] is the block that indicates that for any 50 <= x <= 97 we do x -> x + 2
# The block is therefore [lo, hi, off]
# The blocks in a map are sorted by increasing order of `lo`


# show(maps_str_list[5])
# show(maps[5])

# for M in maps2:
#   show(M)

# def check_contiguous(M):
#   op = []
#   for i in range(1,len(M)):
#     x = M[i][0] - M[i-1][1]
#     print(x, end=' ')
#     # op.append(x)
#     # return op
#   print()
# for M in maps2:
#   check_contiguous(M)

def convert_range(range, table):
  '''Given a range [s,e] and a transformation table [[lo1, hi1, off1], [lo2, hi2, off2], ...],
  return a list of ranges'''
  (s,e) = range
  if e < table[0][0]:  # if the entire range lies below the first interval, return unchanged
    return [range]
  elif s > table[-1][1]:
    return [range]       # if the entire range lies above the last interval, return unchanged

  op = [] # initialise the list of ranges to return
  for row in table:
    if e < row[0]:            # se  |-----|
      op.append([s,e])
      return op
    elif s > row[1]:          #     |-----| se
      pass
    elif s < row[0]:          # s < |--e--|    or
      op.append([s,row[0]-1]) # s < |-----| e
      s = row[0]
    elif e <= row[1]:         #     |-s-e-|
      op.append([s+row[2], e+row[2]])
      return op
    elif e > row[1]:          #     |-s---| e
      op.append([s+row[2], row[1]+row[2]])
      s = row[1] + 1
    else:
      raise ValueError  # The above 6 cases should be exhaustive, so reaching here is an error
  return op

# show(maps2[2])

# rng = [0,53]
# x = convert_range(rng, maps2[2])
# print(x)

# x.sort()
# print(x)

def amalgamate_ranges(L):
  '''Given a list of ranges, e.g. [[42, 48], [57, 60], [0, 41], [49, 49]], 
  sort them into order and combine any adjacent ranges, e.g. [[0, 49], [57, 60]]'''
  if not L: return []
  L.sort()  # [[0, 41], [42, 48], [49, 49], [57, 60]]
  op = []
  current_range = []
  for item in L:
    if not current_range:
      current_range = item
      continue
    if item[0] == current_range[1] + 1:
      current_range[1] = item[1]
    else:
      op.append(current_range)
      current_range = item
  op.append(current_range)
  return op
    
# x = amalgamate_ranges([[0, 41], [42, 48], [49, 49], [57, 60]])
# print(x)


def convert_multi_ranges(range_list, table):
  '''Given a list of ranges and a transition table, 
  convert each range and then amalgamate the outputs, returning a list of ranges'''
  op = []
  for range in range_list:
    op += convert_range(range, table)
  return amalgamate_ranges(op)

# x = convert_multi_ranges([[0,3], [5,8], [10,56]], maps2[2])
# print(x)


def chain_conversions(range_list, table_list):
  for table in table_list:
    range_list = convert_multi_ranges(range_list, table)
    # print(range_list)
  return range_list

# rl = [[0,3], [5,8], [10,56]]
# rl = [[13,13]]
# print(rl)
# x = chain_conversions(rl, maps2)
# print(x)

################################
# Part (a)
################################

# Convert each seed number through other categories 
# until you can find its corresponding location number.
# What is the lowest location number that corresponds to any of the initial seed numbers?

seed_line = input[0]
seed_line = seed_line.split(": ")[1]
seed_line = parse_nums(seed_line)

rl = [[x,x] for x in seed_line]
print(rl)
print()

x = chain_conversions(rl, maps2)
print(x)

x.sort()
print(x[0][0]) # 265018614



################################################################################################
################################################################################################
raise SystemExit
################################################################################################
################################################################################################



################################
# Part (b)
################################

# The values on the initial `seeds:` line come in pairs. 
# Within each pair, 
# the first value is the start of the range and 
# the second value is the length of the range. 
# 
# So, in the first line of the example above:
# seeds: 79 14 55 13
# This line describes two ranges of seed numbers to be planted in the garden. 
# The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. 
# The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. 
# What is the lowest location number that corresponds to any of the initial seed numbers?

# print(seed_line)

#  Ranges of seed numbers to check, formatted as (start, end) inclusive
seed_ranges = [(seed_line[i], seed_line[i]+seed_line[i+1]-1) for i in range(0,len(seed_line), 2)]
seed_ranges.sort()

# show(seed_ranges)



def parse_map_b(M:list[str]):
  '''Given a list of strings denoting a conversion table with a header line, 
  return the conversion table'''
  table = []
  for line in M[1:]:  # skip header line
    table.append(parse_nums(line))
  return table

def reparse_map(M):
  '''Given a conversion table in the form [dst, src, rng],
  return a lookup table in the form [src_start, src_end, offset]'''

  return [[s, s+r-1, d-s] for [d,s,r] in M]


# maps = [parse_map_b(M) for M in maps_str_list]
# maps = [reparse_map(M) for M in maps]
# maps = [sorted(M) for M in maps]

# for M in maps:
#   show(M)




# Now we've sorted the conversion tables in order of start-range

def convert_b(x:int, table:list[list[int]]) -> int:
  '''Given a number and a conversion table, return the converted number'''
  if (x < table[0][0]):  # if x is below the start of the first range, return unchanged
    return x
  elif (x >= table[-1][0] + table[-1][1]): # if x is above the end of the last range
    return x
  # Otherwise find its place in the table
  for row in table:
    [s,r,offset] = row
    if (s <= x <= s + r - 1): # if x is in the current range 
      return x + offset
  # If we haven't found the position of x yet, an error has occurred
  raise ValueError






def chain_conversions_b(x:int, map_list):
  for M in map_list:
    x = convert_b(x, M)
  return x

# start_time = time.perf_counter()
# for i in range(100000):
#   chain_conversions_b(seed_ranges[0][0] + 1, maps)
# end_time = time.perf_counter()


# start_time = time.perf_counter()
# locations=[]
# for (start, l) in seed_ranges:
#   for i in range(l):
#     seed = start + i
#     loc = chain_conversions_b(seed, maps)
#     locations.append(loc)
# end_time = time.perf_counter()


# print(len(locations))
# print(min(locations))







################################################################################################
################################################################################################
raise SystemExit
################################################################################################
################################################################################################

#  Previous method:
# First attempt worked number-by-number rather than acting on ranges
# This was ok for part (a), 
# but would have led to 1.5 hour runtimes to process 2.3 billion seeds for part (b)!

# def parse_map(M:list[str]):
#   '''Given a list of strings denoting a conversion table with a header line, 
#   return a dictionary recording the source, destination, and the conversion table'''
#   op = {}
#   header = re.split(("-|\ "), M[0])
#   op['source'] = header[0]
#   op['dest'] = header[2]
#   table = []
#   for line in M[1:]:  # skip header line
#     d = {}
#     [d['dst'], d['src'], d['rng']] = parse_nums(line)
#     table.append(d)
#   op['table'] = table
#   return op


# maps = [parse_map(M) for M in maps_str_list]

# # print(maps[1])

# def convert(x:int, table:list[dict]) -> int:
#   '''Given a number and a conversion table, return the converted number'''
#   for row in table:
#     if (x >= row['src']) & (x <= row['src'] + row['rng'] - 1):
#       return x - row['src'] + row['dst']
#   return x  # if input doesn't fit any of the source ranges, return it unchanged


# def chain_conversions(x:int, map_list):
#   op = [x]
#   for M in map_list:
#     y = convert(op[-1], M['table'])
#     op.append(y)
#   return op
