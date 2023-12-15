# https://adventofcode.com/2023/day/12

import re

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
parse_nums, 
# rotate90, close_bracket, cmp, qsort, Best, 
Timer,
)
TTT = Timer()

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
  ip_file = [[rewrite(c), tuple(parse_nums(n, ","))] for [c,n] in ip_file] 
  return ip_file

test_input = parse_file_a("Puzzle12_test.txt")
input      = parse_file_a("Puzzle12_input.txt")

# show(test_input)

################################
# Part (a)
################################

verbose = False

def count_ways_starting_O(s, spec):
  '''Given a string `s` (e.g. `"~~~OXXX"`), and a `spec` (e.g. `[1, 1, 3]`) (both assumed non-empty), 
  return the list of strings starting with `O` that can be made from `s` that fit the spec.'''
  if verbose: print("Starting 'O': \t", s, spec)
  if not spec:
    if ('X' not in s): 
      # print("'O': 'X' not in s \t", s, spec)
      return ["O" * len(s)]   # Every element of the string is 'O', which matches the empty `spec`
    else:
      return []  # If 'X' is in `s` then we can't match an empty `spec`.
  if not s:
    if (spec == []):
      # print ("'O': spec == [] \t", s, spec)
      return [""]
    else:
      return []
  if s[0] == 'X': 
    return []
  else:
    return ['O' + item for item in count_ways(s[1:], spec)]

def count_ways_starting_X(s, spec):
  '''Given a string `s` (e.g. `"~~~OXXX"`), and a `spec` (e.g. `[1, 1, 3]`) (both assumed non-empty),
  return the list of strings starting with `X` that can be made from `s` that fit the spec.'''
  if verbose: print("Starting 'X': \t", s, spec)
  if not spec:    # a string can't start with `X` and meet an empty `spec`!
    return []
  if not s:
    if (spec == []):
      # print ("'X': spec == [] \t", s, spec)
      return [""]
    else:
      return []
  if s[0] == 'O':
    return []
  else:  # either `s` starts with `X` or could be interpreted as starting with `X`, so do so
    if spec[0] == 1:  # if we've completed the current block of 'X's required
      # drop that block from `spec` and then require that the next character is 'O'
      return ['X' + item for item in count_ways_starting_O(s[1:], spec[1:])]
    else:
      reduced_spec = (spec[0]-1, ) + spec[1:]
      return ['X' + item for item in count_ways_starting_X(s[1:], reduced_spec)]

def count_ways(s, spec):
  '''Given a string `s` (e.g. `"~~~OXXX"`), and a `spec` (e.g. `[1, 1, 3]`), 
  return the list of strings that can be made from `s` that fit the spec.'''
  if verbose: print("Counting all: \t", s, spec)
  if not spec:
    if ('X' not in s):
      # print("ALL: 'X' not in s \t", s, spec)
      return ["O" * len(s)]   # Every element of the string is 'O', which matches the empty `spec`
    else:
      return []
  if not s:
    if (spec == []):
      # print ("ALL: spec == [] \t", s, spec)
      return [""]
    else:
      return []
  return count_ways_starting_O(s, spec) + count_ways_starting_X(s, spec)


def main_a(ip_file):
  count = 0
  for line in ip_file:
    cw = count_ways(*line)
    # print(len(cw))
    count += len(cw)
  return count

print(main_a(test_input))  # 21
print(main_a(input))       # 7622

# TTT.timecheck("Part (a)") # ~ 100 ms

################################
# Part (b)
################################

# [s0, spec0] = test_input[0]
# print(s0, spec0)

def unfold_string(s):
  '''Replace the list of spring conditions with five copies of itself (separated by '~')'''
  return ((s + '~') * 5)[:-1]

def unfold_spec(spec):
  '''Replace the `spec` with five copies of itself (separated by ,)'''
  return spec * 5

# unfold_string(s0)
# unfold_spec(spec0)

def main_b_naive(ip_file):
  count = 0
  for [s,spec] in ip_file:
    us = unfold_string(s)
    uspec = unfold_spec(spec)
    cw = count_ways(us, uspec)
    # print(len(cw))
    count += len(cw)
  return count

# main_b_naive(test_input)  # 
# TTT.timecheck("Part (b) -- test_input")

# print(main_b(test_input))  # 
# print(main_b(input))       # 


################################




# def any_number_of(char):
#   return "[" + char + "~]*"

# def any_pos_number_of(char):
#   return "[" + char + "~]+"

# def exactly_n_of(char, n):
#   return "[" + char + "~]{" + str(n) + "}"

