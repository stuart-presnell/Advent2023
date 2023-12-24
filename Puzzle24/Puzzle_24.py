# https://adventofcode.com/2023/day/24

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def parse_file(filename):
  '''Parse the input file into a list of positions and velocities, 
  each represented as a tuple of three `int`s.'''
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  op = []
  for line in ip_file:
    [pos, vel] = line.split(" @ ")
    pos = tuple([int(x) for x in pos.split(", ")])
    vel = tuple([int(x) for x in vel.split(", ")])
    op.append([pos, vel])
  return op

test_input = parse_file("Puzzle24_test.txt")
input      = parse_file("Puzzle24_input.txt")

ip = test_input
# ip = input
show(ip)

def animate_one_ns(pos,vel):
  '''Given the `pos`ition and `vel`ocity of a hailstone, 
  return what its `pos` will be in 1 nanosecond (and its `vel`, which is unchanged).'''
  new_pos = tuple([pos[i] + vel[i] for i in range(3)])
  return (new_pos, vel)
# animate_one_ns((20, 19, 15), (1, -5, -3))[0] == (21, 14, 12)


# "Look for intersections that happen with an X and Y position 
# each at least 200000000000000 and at most 400000000000000. 
# Disregard the Z axis entirely."


# TODO: But we're not going to run a live simulation of the hailstorm!
# TODO: A hailstone's path is a straight line in space.
# TODO: So compute this line for each hailstone and see which lines intersect.

# TODO: Given a point (x0,y0) on a line and a vector (vx,vy) in the direction of the line, 
#   the Symmetric Equation for the line is (x-x0)/vx = (y-y0)/vy
# TODO: SO given two such lines, they cross at some (x,y) iff this is a solution to both SEs.


################################
# Part (a)
################################

# def main_a(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_a("Puzzle24_test.txt"))  # 
# print(main_a("Puzzle24_input.txt")) # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_filename):
#   ip = parse_file(ip_filename)
#   pass

# print(main_b("Puzzle24_test.txt"))  # 
# print(main_b("Puzzle24_input.txt")) # 

# TTT.timecheck("Part (b)")  #

################################