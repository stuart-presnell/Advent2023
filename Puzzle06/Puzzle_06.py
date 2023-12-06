# https://adventofcode.com/2023/day/6

f = open("Puzzle06_test.txt")
# f = open("Puzzle06_input.txt")
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

def rotate90(M):
  '''Given a matrix `M` consisting of a list of strings (or a list of lists), 
  rotate it 90 degrees clockwise'''
  return [list(reversed([M[j][i] for j in range(len(M))]))
            for i in range(len(M[-1]))]

################################

# Your puzzle input lists the time allowed for each race 
# and also the best distance ever recorded in that race. 
# To guarantee you win the grand prize, you need to make sure you go farther in each race 
# than the current record holder.

# Time:      7  15   30
# Distance:  9  40  200
# This document describes three races:

# Each column in this document describes a race, that lasts `Time` ms and the record is `Distance` mm.

# show(input)
input = [parse_nums(line.split(":")[1]) for line in input]
show(input)

input = rotate90(input)
show(input)

# Now formatted as one race per row, [Distance, Time]

################################
# Part (a)
################################


################################
# Part (b)
################################

