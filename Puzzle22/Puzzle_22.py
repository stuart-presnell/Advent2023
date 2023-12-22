# https://adventofcode.com/2023/day/22

from collections import defaultdict

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def altitude(L):
  '''The `z`-coordinate of the lowest block of the brick.'''
  return min(L[2], L[5])

def parse_file_a(filename):
  '''Parse each line of the file as a list of 6 integers and sort them into order of altitude.'''
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  op = []
  for line in ip_file:
    line = [item.split(',') for item in line.split('~')]
    line = line[0] + line[1]
    line = [int(n) for n in line]
    op.append(line)
  # Finally, sort the bricks into order of altitude 
  op.sort(key = lambda L: min(L[2], L[5]))
  return op

test_input = parse_file_a("Puzzle22_test.txt")
input      = parse_file_a("Puzzle22_input.txt")

ip = test_input
# ip = input
show(ip)

################################
# Part (a)
################################

# Verify that the x- and y- coords are already sorted
def xy_sorted(B):
  (x1,y1,_,x2,y2,_) = B
  return ((x1<=x2) & (y1<=y2))
# all([xy_sorted(B) for B in ip])

# Verify that the bricks are all straight lines, not rectangles of >1 width
def linear(B):
  (x1,y1,_,x2,y2,_) = B
  return ((x1==x2) | (y1==y2))
# print(all([linear(B) for B in ip]))




# TODO: Determine where each brick will settle when they fall
  # TODO: Drop the bricks one by one, starting with the lowest
  # TODO: Each brick covers some 2D area of the ground
  # TODO: Find the max altitude of all squares covered by the brick; this is where it settles
  # TODO: Update the max altitude information and move on to the next brick.

def squares_covered(B):
  '''Return the set of `(x,y)`-coordinates covered by brick `B`.'''
  (x1,y1,_,x2,y2,_) = B
  return [(x,y) for x in range(x1, x2+1) for y in range(y1, y2+1)]

# # At each `(x,y)` position, record the maximum height occupied above that square.
mho = defaultdict(int)

def drop_brick(B, mho):
  '''Given a brick `B` and the current max-height data `mho`,
  find the height that the brick will settle at
  and return the updated `mho` and the new brick position.'''
  (x1,y1,z1,x2,y2,z2) = B
  brick_tallness = z2-z1
  # Which (x,y) squares are we looking at?
  covered = squares_covered(B)
  # How high is the obstruction below?
  max_height_below = max([mho[x] for x in covered])
  # This brick will settle in the next available vertical position
  settle_height = max_height_below + 1
  brick_top = settle_height + brick_tallness
  new_pos = [x1,y1,settle_height, x2,y2,brick_top]
  for x in covered:
    mho[x] = brick_top
  return (mho, new_pos)

def drop_all_bricks(L):
  '''Given a list of bricks `L`, drop each one with `drop_brick` (starting with an empty `mho`)
  and return a new list of brick positions.'''
  pass


# TODO: Work out the dependency graph of bricks sitting on other bricks
# TODO: Which bricks are the only support of the brick above? Any others can be destroyed.

def sits_on(L):
  '''Given a list of bricks `L`, for each brick work out which other bricks it sits on.'''
  pass

def can_be_disintegrated(L):
  '''Given a list of bricks `L`, return a list of the bricks that are 
  not the only supporter of any other brick.'''
  pass



# def main_a(ip_file):
#   pass

# print(main_a("Puzzle22_test.txt"))  # 
# print(main_a("Puzzle22_input.txt"))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# print(main_b("Puzzle22_test.txt"))  # 
# print(main_b("Puzzle22_input.txt"))       # 

# TTT.timecheck("Part (b)")  #

################################