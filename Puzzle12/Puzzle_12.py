# https://adventofcode.com/2023/day/12

import re

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
parse_nums, 
# rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

# The condition records show every spring and whether it is 
# operational (.), damaged (#), or unknown (?)

# After the list of springs for a given row, 
# the size of each contiguous group of damaged springs is listed in the order those groups appear.
# This list always accounts for every damaged spring, 
# and each number is the entire size of its contiguous group 
# (that is, groups are always separated by at least one operational spring: 
# XXXX would always be 4, never 2,2).

def rewrite(s):
  '''Given a string consisting of '.', '#', and '?',
  rewrite it to 'O', 'X', and '~' to avoid having to escape regex characters.'''
  d = {'.':'O', '#':'X', '?':'~'}
  return "".join([d[x] for x in s])

# print(rewrite('???.###'))

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  ip_file = [line.split() for line in ip_file]
  ip_file = [[rewrite(c), parse_nums(n, ",")] for [c,n] in ip_file] 
  return ip_file

test_input = parse_file_a("Puzzle12_test.txt")
input      = parse_file_a("Puzzle12_input.txt")

show(test_input)

[s1, L1] = test_input[0]

################################
# Part (a)
################################



def any_number_of(char):
  return "[" + char + "~]*"

def any_pos_number_of(char):
  return "[" + char + "~]+"

def exactly_n_of(char, n):
  return "[" + char + "~]{" + str(n) + "}"

def count_arrangements(s:str, spec:list[int]):
  '''How many different arrangements of OK/broken springs fit the given spec?
  If the spec is [a,b,...] then its uncorrupted string must consist of:
  * some number of Os (possibly zero)
  * 'a' Xs
  * some number of Os (not zero)
  * 'b' Xs
  * some number of Os (not zero)
  * etc.
  * Finally, some number of Os (possibly zero)'''
  # Base case: empty list only matches empty string
  if len(spec) == 0: return (s == '') * 1
  # Otherwise `spec = x::xs`, so try matching start of `s` to `x`
  x,xs = spec[0], spec[1:]
  
  pass


def create_regex_pattern(spec:list[int]) -> str:
  '''Given nonempty `spec:list[int]`, return a string that will compile to 
  a regex pattern matching that spec, according to the rules given above.'''
  op = "^" + any_number_of('O')
  op += (exactly_n_of('X', spec[0]))
  for n in spec[1:]:
    op += (any_pos_number_of('O'))
    op += (exactly_n_of('X', n))
  op += (any_number_of('O') + '$')
  return op

for [s,spec] in test_input:
  p = create_regex_pattern(spec)
  pattern = re.compile(p)
  result = pattern.findall(s)
  print(result)

# print()

# spec = re.compile("^" + exactly_n_of("X", 5))

# for i in range(len(test_input)):
#   result = spec.match(test_input[i][0])
#   if result:
#     print(result.group(0))
#   else:
#     print(None)


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