# https://adventofcode.com/2023/day/22

from collections import defaultdict

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
showD, 
# unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer(1)

################################

def altitude(B):
  '''The `z`-coordinate of the lowest block of the brick.'''
  return min(B[2], B[5])

def parse_file_a(filename):
  '''Parse each line of the file as a tuple of 6 integers and sort them into order of altitude.'''
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  op = []
  for line in ip_file:
    line = [item.split(',') for item in line.split('~')]
    line = line[0] + line[1]
    line = [int(n) for n in line]
    line = tuple(line)
    op.append(line)
  # Finally, sort the bricks into order of altitude 
  op.sort(key = lambda L: min(L[2], L[5]))
  return op

test_input = parse_file_a("Puzzle22_test.txt")
input      = parse_file_a("Puzzle22_input.txt")

ip = test_input
# ip = input
# show(ip)

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
  # DONE: Each brick covers some 2D area of the ground
  # TODO: Find the max altitude of all squares covered by the brick; this is where it settles
  # TODO: In each (x,y) position covered by this brick, 
      # update the max altitude information and record the identity of the brick occupying the top.
  # TODO: Record for the current brick the identity numbers of all bricks supporting it.

def squares_covered(B):
  '''Return the set of `(x,y)`-coordinates covered by brick `B`.'''
  (x1,y1,_,x2,y2,_) = B
  return [(x,y) for x in range(x1, x2+1) for y in range(y1, y2+1)]

# At each `(x,y)` position, record the maximum height occupied above that square
# and the identity number (i.e. index in the original list) of the top brick
mho = defaultdict(lambda:[0,None])

def drop_brick(B, i, mho):
  '''Given a brick `B` and the current max-height data `mho`,
  find the height that the brick will settle at
  and return the updated `mho` and the new brick position.'''
  (x1,y1,z1,x2,y2,z2) = B
  brick_tallness = z2-z1
  # Which (x,y) squares are we looking at?
  covered = squares_covered(B)
  # How high is the obstruction below?
  max_height_below = max([mho[x][0] for x in covered])
  # This brick will settle in the next available vertical position
  settle_height = max_height_below + 1
  brick_top = settle_height + brick_tallness
  new_pos = (x1,y1,settle_height, x2,y2,brick_top)
  
  # Use `mho` to work out which bricks are supporting the current brick
  supports = []
  for x in covered:
    if mho[x][0] == max_height_below:  # if the brick is getting support at this position
      supports.append(mho[x][1])       # then record the id of the top brick in this pos

  # Update `mho`: 
  # * the maximum height over each covered square is the top of this brick;
  # * the identity of the brick currently covering this square is the current brick id number
  for x in covered:
    mho[x] = [brick_top, i]
  return (mho, new_pos, supports)


# mho, new_pos, supports = drop_brick(ip[0], 0, mho)
# mho, new_pos, supports = drop_brick(ip[1], 1, mho)
# mho, new_pos, supports = drop_brick(ip[2], 2, mho)
# mho, new_pos, supports = drop_brick(ip[3], 3, mho)
# mho, new_pos, supports = drop_brick(ip[4], 4, mho)
# mho, new_pos, supports = drop_brick(ip[5], 5, mho)
# mho, new_pos, supports = drop_brick(ip[6], 6, mho)
# showD(mho)
# print(new_pos)
# print(supports)


def drop_all_bricks(L):
  '''Given a list of bricks `L`, drop each one with `drop_brick` (starting with an empty `mho`)
  and return a new list of brick positions, plus a list of brick supports.'''
  mho = defaultdict(lambda:[0,None])
  new_positions = []
  supports = []
  for i in range(len(L)):
    (mho, npos, s_list) = drop_brick(L[i], i, mho)
    new_positions.append(npos)
    supports.append(s_list)       # for each i, supports[i] is a list of bricks supporting brick L[i]
  return new_positions, supports

# new_positions, supports = drop_all_bricks(ip)
# show(new_positions)
# show(supports)


def main_a(ip_filename):
  ip = parse_file_a(ip_filename)
  _, supports = drop_all_bricks(ip)
  # show(supports)
  sole_supporters = set()   # The set of bricks that are the only support for some brick above
  for x in supports:    # Run through the support of each brick
    if len(set(x)) == 1:     # If a brick has exactly one supporter
      sole_supporters.add(x[0])  # Add this supporter to `sole_supporters`
  if None in sole_supporters:     # Bricks that land on the ground have `None` as their support
    sole_supporters.remove(None)  # Don't include this as a sole supporter
  # print(sole_supporters)
  return len(ip) - len(sole_supporters)


# XXXX: Work out the dependency graph of bricks sitting on other bricks
# def find_supports(L):
#   '''Given a list of bricks `L`, for each brick work out which other bricks it sits on.'''
#   # Produce a dictionary whose keys are bricks, 
#   # where `support_of[B]` is a list of the bricks `B` sits on.
#   support_of = defaultdict(list)
#   for B in L:
#     h = altitude(B)
#     covered = squares_covered(B)
#     pass  # TODO: Which brick(s) is `B` directly sitting on?
#   return support_of


# # XXXX: Which bricks are the only support of the brick above? Any others can be destroyed.
# def can_be_disintegrated(L):
#   '''Given a list of bricks `L`, return a list of the bricks that are 
#   not the only supporter of any other brick.'''
#   pass





print(main_a("Puzzle22_test.txt"))   # 5
print(main_a("Puzzle22_input.txt"))  # 421
# 612 is too high

# TTT.timecheck("Part (a)")  # ~ 8 ms

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# print(main_b("Puzzle22_test.txt"))  # 
# print(main_b("Puzzle22_input.txt"))       # 

# TTT.timecheck("Part (b)")  #

################################