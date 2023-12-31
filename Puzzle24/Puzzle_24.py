# https://adventofcode.com/2023/day/24

import numpy as np
from collections import Counter

# My utility functions
from utils import (
show, 
unzip, 
Timer,
)
TTT = Timer(1)

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

# test_input = parse_file("Puzzle24_test.txt")
# input      = parse_file("Puzzle24_input.txt")

# ip = test_input
# ip = input
# show(ip)

# "Look for intersections that happen with an X and Y position 
# each at least 200000000000000 and at most 400000000000000. 
# Disregard the Z axis entirely."


# But we're not going to run a live simulation of the hailstorm!
# A hailstone's path is a straight line in space.
# So compute this line for each hailstone and see which lines intersect.

# Given a point (x0,y0) on a line and a vector (vx,vy) in the direction of the line, 
#   the Symmetric Equation for the line is (x-x0)/vx = (y-y0)/vy
# So given two such lines, they cross at some (x,y) iff this is a solution to both SEs.

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

def cross_or_not_v2(pvh1, pvh2, coord_min, coord_max, verbose=False):
  (p1,v1,h1) = pvh1
  (p2,v2,h2) = pvh2

  C = crossing(h1, h2)
  if not C:
    if verbose: print("Do not cross")
    return False
  (x,y,cp) = C
  # When do the two particles occupy that position?
  t1 = cross_time(p1, v1, x)
  t2 = cross_time(p2, v2, x)
  if verbose: print("Crossing times: ", t1, t2)
  # If either of them occupied that position in the past, return `False`
  if (t1 < 0) | (t2 < 0):  
    if verbose: print("Crossed in the past")
    return False
  # Does the crossing point fall within the given search zone?
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

coord_min = 200000000000000
coord_max = 400000000000000

print(main_a("Puzzle24_test.txt", 7, 27)) # 
print(main_a("Puzzle24_input.txt", coord_min, coord_max)) # 24627

TTT.timecheck("Part (a)")  # ~ 45 ms

################################
# Part (b)
################################

# There is a POS and VEL such that a rock thrown in this way at time t=0
# will intersect (in 3D) every hailstone!

GIVEN_POS = (24, 13, 10)
GIVEN_VEL = (-3, 1, 2)

# T = [5,3,4,6,1]

def animate(pos,vel,n):
  '''Given the `pos`ition and `vel`ocity of a hailstone, 
  return what its `pos` will be in 1 nanosecond (and its `vel`, which is unchanged).'''
  new_pos = tuple([pos[i] + n*vel[i] for i in range(3)])
  return new_pos

# for i in range(5):
#   (p,v) = test_input[i]
#   t = T[i]
#   print(animate(GIVEN_POS,GIVEN_VEL,t) == animate(p,v,t))


# We want to find (PX, PY, VX, VY) for the rock.
# For the rock to collide with a stone having (ax, ay, vx, vy), we require:
    # (PX - ax)/(VX - vx) = (PY - ay)/(VY - vy)
# which gives the equation:
    # (PX.VY - PY.VX) = ax.VY - ay.VX - vx.PY + vy.PX - ax.vy + ay.vx
# We have an equation of this form arising from each stone.
# Thus we have a system of simultaneous equations to solve to get PX, PY, VX, VY.
# We start by eliminating the unknown (PX.VY - PY.VX) from all equations,
# by substracting the first equation from all the others.

def extract_coeffs(coeff, stone):
  '''Given a `stone` with its `pos` and `vel`, and a coefficient position in `{0,1,2}`, 
  (corresponding to x, y, or z), extract the corresponding pair of values (e.g. x, vx).'''
  (pos, vel) = stone
  return pos[coeff], vel[coeff]

def compute_two_pairs(c1, c2, ip_file):
  '''Given `ip_file` containing 5 stones, and `c1`, `c2` in `{0,1,2}` indicating which two of
  `{x,y,z}` we want to compute, return `Vc1, Vc2, Pc1, Pc2`.
  NB: Comments below are written on the basis that `c1=0=x` and `c2=1=y`.
  '''
  (ax0, vx0) = extract_coeffs(c1, ip_file[0])
  (ay0, vy0) = extract_coeffs(c2, ip_file[0])
  e0 = ay0*vx0 - ax0*vy0
  # For each stone, offset the x,y,vx,vy coefficients by subtracting those of stone 0
  M = []
  J = []
  for stone in ip_file[1:]:
    (ax, vx) = extract_coeffs(c1, stone)
    (ay, vy) = extract_coeffs(c2, stone)
    E = ay*vx - ax*vy - e0
    ax -= ax0
    ay -= ay0
    vx -= vx0
    vy -= vy0
    # print (ax, ay, vx, vy)
  # Stone 0 is no longer useful, but now we have N-1 equations of the form
      # A.VX + B.VY + C.PX + D.PY = - E
    A = -ay
    B =  ax
    C =  vy
    D = -vx
    M.append([A,B,C,D])
    J.append(-E)
  # So we want to solve the simultaneous equations M ROCK = J, 
  # where ROCK is the column vector [VX, VY, PX, PY]

  # So let's plug these into a simultaneous equation solver from `numpy`:
  M = np.array(M)
  J = np.array(J)

  ROCK = np.linalg.solve(M,J)
  return (ROCK)

def magic_trajectory(five_stones):
  '''Given a list `five_stones`, each element of which is a pair `[pos, vel]`,
  use `compute_two_pairs` to extract the `POS` and `VEL` of the magic trajectory
  that hits all five stones.'''
  (VX, VY, PX, PY) = compute_two_pairs(0,1,five_stones)
  (VX, VZ, PX, PZ) = compute_two_pairs(0,2,five_stones)
  POS = (round(PX), round(PY), round(PZ))
  VEL = (round(VX), round(VY), round(VZ))
  return POS, VEL

def main_b(ip_filename):
  ip = parse_file(ip_filename)
  # In principle we should get the same results for any set of 5 stones, 
  # but in practice there may be some discrepancies, 
  # so for caution let's look at every consecutive 5-stone run
  op = [magic_trajectory(ip[i:i+5]) for i in range(len(ip) - 4)]
  # and use the modal result, which should be the correct one
  op = Counter(op)
  op = op.most_common(1)
  # Now extract just the values we need
  (PX, PY, PZ) = op[0][0][0]
  # Part (b) asks for the sum of the three coordinates:
  return (PX + PY + PZ)


print(main_b("Puzzle24_test.txt"))  # 47
print(main_b("Puzzle24_input.txt")) # 527310134398221

TTT.timecheck("Part (b)")  # ~ 8 ms

################################