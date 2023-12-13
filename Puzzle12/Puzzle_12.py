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
  ip_file = [[rewrite(c), parse_nums(n, ",")] for [c,n] in ip_file] 
  return ip_file

test_input = parse_file_a("Puzzle12_test.txt")
input      = parse_file_a("Puzzle12_input.txt")

# show(test_input)

################################
# Part (a)
################################

verbose = True

def count_ways_starting_O(s, spec):
  '''Given a string e.g. `"~~~OXXX"`, and a spec, e.g. `[1, 1, 3]` (both assumed non-empty), 
  return the number of ways the `~`s in the string can be filled in with `O`s and `X`s
  to make a string that fits the spec *and* starts with `O`.'''
  if verbose: print("Starting 'O': \t", s, spec)
  if not spec:
    if ('X' not in s): 
      return 1
    else:
      return 0
  if not s:
    if (spec == []):
      return 1
    else:
      return 0
  if s[0] == 'X': 
    return 0
  else:
    return count_ways(s[1:], spec)

def count_ways_starting_X(s, spec):
  '''Given a string e.g. `"~~~OXXX"`, and a spec, e.g. `[1, 1, 3]` (both assumed non-empty),
  return the number of ways the `~`s in the string can be filled in with `O`s and `X`s
  to make a string that fits the spec *and* starts with `X`.'''
  if verbose: print("Starting 'X': \t", s, spec)
  if not spec:    # a string can't start with `X` and meet an empty `spec`!
    return 0
  if not s:
    if (spec == []):
      return 1
    else:
      return 0
  if s[0] == 'O':
    return 0
  else:  # either `s` starts with `X` or could be interpreted as starting with `X`, so do so
    if spec[0] == 1:  # if we've completed the current block of 'X's required
      # drop that block from `spec` and then require that the next character is 'O'
      return count_ways_starting_O(s[1:], spec[1:])
    spec[0] -= 1
    return count_ways(s[1:], spec)

def count_ways(s, spec):
  '''Given a string e.g. `"~~~OXXX"`, and a spec, e.g. `[1, 1, 3]`, 
  return the number of ways the `~`s in the string can be filled in with `O`s and `X`s
  to make a string that fits the spec.'''
  if verbose: print("Counting all: \t", s, spec)
  if not spec:
    if ('X' not in s):
      return 1
    else:
      return 0
  if not s:
    if (spec == []):
      return 1
    else:
      return 0
  return count_ways_starting_O(s, spec) + count_ways_starting_X(s, spec)

print(test_input[1])
count_ways(*test_input[1])
# print(count_ways('X~XO~', [3]))

# for [s,spec] in test_input:
#   # print(s)
#   print(count_ways(s,spec))

# def create_regex_pattern(spec:list[int]) -> str:
#   '''Given nonempty `spec:list[int]`, return a string that will compile to 
#   a regex pattern matching that spec, according to the rules given above.'''
#   op = "^" + any_number_of('O')
#   op += (exactly_n_of('X', spec[0]))
#   for n in spec[1:]:
#     op += (any_pos_number_of('O'))
#     op += (exactly_n_of('X', n))
#   op += (any_number_of('O') + '$')
#   return op

# for [s,spec] in test_input:
#   p = create_regex_pattern(spec)
#   pattern = re.compile(p)
#   result = pattern.findall(s)
#   print(result)

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


# def any_number_of(char):
#   return "[" + char + "~]*"

# def any_pos_number_of(char):
#   return "[" + char + "~]+"

# def exactly_n_of(char, n):
#   return "[" + char + "~]{" + str(n) + "}"




# def count_arrangements(s:str, spec:list[int], block, at_start = False):
#   '''How many different arrangements of O/X fit the given spec?
#   If the spec is [a,b,...] then its uncorrupted string must consist of:
#   * some number of Os (possibly zero)
#   * 'a' Xs
#   * some number of Os (not zero)
#   * 'b' Xs
#   * some number of Os (not zero)
#   * etc.
#   * Finally, some number of Os (possibly zero).
#   So at the start we want '[O~]*', and then for each `x` in `spec` we want `[X~]{x}[O~]+`.
#   So we need to count how many ways there are to match '[O~]*' at the start;
#   then for each of these, how many ways to match `[X~]{spec[0]}[O~]+` on the remainder;
#   then for each of these, how many ways to match `[X~]{spec[1]}[O~]+` on the remainder; and so on.'''
#   # Base case: empty list => some number of Os (possibly zero)
#   if len(spec) == 0: 
#       return 1 if re.fullmatch(any_number_of('O'), s) else 0
#   if at_start:
#     result = re.match("^[O~]*", s)
#     if not result:  # if the start of the string doesn't match a run of 'O'; should be IMPOSSIBLE
#       return 0
#     else:
#       count = 0
#       run_of_Os = result.end() # The number of ways to match '[O~]*' at the start
#       for i in range(run_of_Os + 1):
#         count += count_arrangements(s[i:], spec, 'X')
#       return count
#   # Now we're not at the start, and `spec` isn't empty
#   if block == 'X':     # Trying to match `^[X~]{spec[0]}`
#     a = spec[0]
#     pattern = "^[X~]{" + str(a) + "}"
#     result = re.match(pattern, s)
#     if not result:  # if the current string doesn't start with `a` Xs
#       return 0  # this arrangement fails, terminate it
#     else:   # if the current string starts with `a` Xs
#       return count_arrangements(s[a:], spec[1:], 'O')  # try to match the rest, starting with 'O'
#   elif block =='O':     # Trying to match `^[O~]+`
#     pattern = "^[O~]+"
#     result = re.match(pattern, s)
#     if not result:
#       return 0
#     else:
#       count = 0
#       run_of_Os = result.end() # The number of ways to match '[O~]*' at the start
#       for i in range(run_of_Os + 1):
#         count += count_arrangements(s[i:], spec, 'X')
#       return count




# # z = re.fullmatch(any_number_of('O'), 'O')
# # print(z)

# # x = count_arrangements('~X~', [])
# # x = count_arrangements('~~~OXXX', [1, 1, 3], True)
# x = count_arrangements(*test_input[0], 'O', True)
# print(x)