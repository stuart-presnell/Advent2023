# https://adventofcode.com/2023/day/5

import re

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

seed_line = input[0]
seed_line = seed_line.split(": ")[1]
seed_line = parse_nums(seed_line)

# chunk the rest of the file
maps_str_list=[]
current_map=[]
for line in input[2:]:  # skip the 'seeds' line and the blank line after it
  if not line:
    maps_str_list.append(current_map)
    current_map=[]
  else:
    current_map.append(line)
maps_str_list.append(current_map)  # append final map!  

seed_soil = maps_str_list[0]

# show(seed_soil)


def parse_map(M:list[str]):
  '''Given a list of strings denoting a conversion table with a header line, 
  return a dictionary recording the source, destination, and the conversion table'''
  op = {}
  header = re.split(("-|\ "), M[0])
  op['source'] = header[0]
  op['dest'] = header[2]
  table = []
  for line in M[1:]:  # skip header line
    d = {}
    [d['dst'], d['src'], d['rng']] = parse_nums(line)
    table.append(d)
  op['table'] = table
  return op


maps = [parse_map(M) for M in maps_str_list]

# print(maps[1])

def convert(x:int, table:list[dict]) -> int:
  '''Given a number and a conversion table, return the converted number'''
  for row in table:
    if (x >= row['src']) & (x <= row['src'] + row['rng'] - 1):
      return x - row['src'] + row['dst']
  return x  # if input doesn't fit any of the source ranges, return it unchanged


def chain_conversions(x:int, map_list):
  op = [x]
  for M in map_list:
    y = convert(op[-1], M['table'])
    op.append(y)
  return op

locations=[]
for seed in seed_line:
  loc = chain_conversions(seed, maps)[-1]
  locations.append(loc)

print(min(locations))


################################

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
# Part (a)
################################

# Convert each seed number through other categories 
# until you can find its corresponding location number.
# What is the lowest location number that corresponds to any of the initial seed numbers?

################################
# Part (b)
################################

