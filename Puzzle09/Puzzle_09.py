# https://adventofcode.com/2023/day/09

# My utility functions
from utils import (
show,
# chunk_splitlines,
parse_nums,
# rotate90,
# close_bracket
)

from time import perf_counter
TIMING = False
if TIMING: start_time = perf_counter()

################################

f = open("Puzzle09_test.txt")
test_input = f.read().splitlines()
test_input = [parse_nums(line) for line in test_input]
f.close()

f = open("Puzzle09_input.txt")
input = f.read().splitlines()
input = [parse_nums(line) for line in input]
f.close()

# show(test_input)

h1 = test_input[0]
# print(h1)

def diffs(L):
  '''Given a list of n numbers, return a list of their pairwise differences (of length n-1)'''
  return  [L[i+1] - L[i] for i in range(len(L)-1)]

def all_zeros(L):
  return set(L) == {0}

################################
# Part (a)
################################

def next_entry(L):
  # print(L)
  ends = []
  while not all_zeros(L):
    ends.append(L[-1])
    L = diffs(L)
    # print(L)
  return sum(ends)

def main_a(ip):
  print(sum([next_entry(line) for line in ip]))

# main_a(test_input)  # 114
# main_a(input)       # 1887980197


################################
# Part (b)
################################

def alternating_sum(L):
  return(sum([(-1)**i * L[i] for i in range(len(L))]))

def prev_entry(L):
  # print(L)
  starts = []
  while not all_zeros(L):
    starts.append(L[0])
    L = diffs(L)
    # print(L)
  return alternating_sum(starts)

# for line in test_input:
#   print(prev_entry(line))

def main_b(ip):
  print(sum([prev_entry(line) for line in ip]))
    # print(([prev_entry(line) for line in ip]))



main_b(test_input)  # 2
main_b(input)       # 990


################################
if TIMING:
  end_time = perf_counter()
  print()
  print("Time taken: ", (end_time - start_time)*1000, "ms")