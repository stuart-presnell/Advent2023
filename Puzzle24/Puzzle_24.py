# https://adventofcode.com/2023/day/24

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, 
unzip, 
# parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
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
# show(ip)

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

def xy_hom_coord(pos,vel):
  '''Given a position `(x0,y0,z0)` and a velocity `(vx, vy, vz)`, consider just the `(x,y)` parts.
  The `(x,y)`-trajectory of the hailstone follows a line determined by
  - ax + by + c = 0, where
  - a = vy
  - b = -vx
  - c = y0vx - x0vy

  Return this triple `(a,b,c)`.'''
  (x0,y0,_) = pos
  (vx,vy,_) = vel
  return (vx, -vy, y0*vx - x0*vy)

# for stone in ip:
#   print(stone, "\t", xy_hom_coord(*stone))

def crossing(st1, st2):
  '''Given the trajectories of two stones as homogeneous coordinates, 
  return the crossing point if it exists, or `None` if they do not cross.
  From: https://en.wikipedia.org/wiki/Line–line_intersection#Using_homogeneous_coordinates'''
  (a1,b1,c1) = st1
  (a2,b2,c2) = st2
  cp = a1*b2 - a2*b1
  if cp == 0:
    return None
  else:
    ap = b1*c2 - b2*c1 
    bp = a2*c1 - a1*c2
    x = -bp/cp
    y = -ap/cp
    return (x, y, cp)

def cross_time(p,v,x):
  (x0,_,_) = p
  (vx,_,_) = v
  return (x - x0)/vx


################################
# Part (a)
################################

def cross_or_not(ip, coord_min, coord_max, verbose=False):
  count = 0
  hip = [xy_hom_coord(*stone) for stone in ip]

  for i in range(len(hip)):
    (pos, vel) = ip[i]
    for j in range(i+1, len(hip)):
      C = crossing(hip[i], hip[j])
      if not C:
        if verbose: print("Do not cross")
        continue
      (x,y,cp) = C
      t = cross_time(pos, vel, x)
      if t < 1:  # According to the penultimate example, where t=0.5, apparently t<1 is the past
        if verbose: print("Crossed in the past")
        continue
      if (coord_min <= x <= coord_max) & (coord_min <= y <= coord_max):
        if verbose: print(x,y)
        count += 1
      else:
        if verbose: print("Cross outside zone")
  return count

def cross_or_not_v2(pvh1, pvh2, coord_min, coord_max, verbose=False):
  (p1,v1,h1) = pvh1
  (p2,v2,h2) = pvh2

  C = crossing(h1, h2)
  if not C:
    if verbose: print("Do not cross")
    return False
  (x,y,cp) = C
  t1 = cross_time(p1, v1, x)
  t2 = cross_time(p2, v2, x)
  if verbose: print("Crossing times: ", t1, t2)
  # According to the penultimate example, where t=0.5, apparently t<1 is the past  (???)
  if (t1 < 0) | (t2 < 0):  
    if verbose: print("Crossed in the past")
    return False
  if (coord_min <= x <= coord_max) & (coord_min <= y <= coord_max):
    if verbose: 
      print(x,y)
    return True
  else:
    if verbose: print("Cross outside zone")
    return False

def main_a(ip_filename, coord_min, coord_max, verbose=False):
  count = 0
  ip = parse_file(ip_filename)
  # Unfold the data into a list of positions, velocities, and hom coords
  (P,V) = unzip(ip)
  H = [xy_hom_coord(*stone) for stone in ip]
  PVH = list(zip(P, V, H))
  for i in range(len(PVH)):
    for j in range(i+1, len(PVH)):
      if cross_or_not_v2(PVH[i], PVH[j], coord_min, coord_max, verbose):
        count += 1
  return count

# (cross_or_not(test_input, 7, 27))  # 2

coord_min = 200000000000000
coord_max = 400000000000000
# (cross_or_not(input, coord_min, coord_max))  # 27349 is too high


print(main_a("Puzzle24_test.txt", 7, 27)) # 
print(main_a("Puzzle24_input.txt", coord_min, coord_max)) # 24627

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