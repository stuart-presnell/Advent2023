# https://adventofcode.com/2023/day/6

from math import sqrt, floor, ceil

# f = open("Puzzle06_test.txt")
f = open("Puzzle06_input.txt")
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

input = [parse_nums(line.split(":")[1]) for line in input]
input = rotate90(input)
print("D, T")
show(input)

# Now formatted as one race per row, [Distance, Time]

# Your toy boat has a starting speed of zero millimeters per millisecond. 
# For each whole millisecond you spend at the beginning of the race holding down the button, 
# the boat's speed increases by one millimeter per millisecond.

# Given a target of T ms
# If we hold the button for t ms we'll move at speed t for (T-t) ms, 
# covering distance (T-t) * t mm

def dist_covered(T,t):
  return (T-t) * t

# D = 40
# T = 15

# This describes a parabola; we want to know where it's above a line (T-t) * t > D
# t^2 - Tt + D = 0
# T +- \sqrt(T^2 - 4D) / 2

def solve_quad(T,D):
  rt = sqrt(T**2 - 4*D)
  return ((T - rt)/2, (T + rt)/2)

def round_up(x):
    '''Next integer above x; if x is a whole number in float form, return x+1'''
    return ceil(x) + int(ceil(x) == floor(x))

def round_down(x):
    '''Next integer below x; if x is a whole number in float form, return x-1'''
    return floor(x) - int(ceil(x) == floor(x))

op = []
count = 1
for [D,T] in input:
  # for t in range(T+1):
  #   print(t, dist_covered(T,t))
  # print()
  (lo,hi) = solve_quad(T,D)  # these are the real numbers at which the parabola = D
  #  We need the next integer above lo and the integer below hi
  # print(lo,hi)
  # print(round_up(lo),round_down(hi))
  r = round_down(hi) - round_up(lo) + 1
  op.append(r)
  count = count * r

print(op)
print(count)

# for [D,T] in input:
#   (lo,hi) = solve_quad(T,D)
#   print(floor(hi)-ceil(lo)+1)


################################
# Part (a)
################################

# Determine the number of ways you can beat the record in each race
# What do you get if you multiply these numbers together?

################################
# Part (b)
################################

