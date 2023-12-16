# https://adventofcode.com/2023/day/16

from collections import defaultdict

def showD(d:dict):
  for k in d:
    if d[k]: print(k, ": ", d[k])

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, parse_nums, rotate90, close_bracket, cmp, qsort, 
Best, 
Timer,
)
TTT = Timer(1)

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle16_test.txt")
input      = parse_file_a("Puzzle16_input.txt")
energised_correct = parse_file_a("energised_correct_test.txt")

# grid = test_input
# grid = input
# show(energised_correct)

################################
# Part (a)
################################

# How to step in each cardinal direction (change in row, change in column)
dir_lookup = {
  'N':(-1,0),
  'S':( 1,0),
  'W':(0,-1),
  'E':(0, 1)
}


def advance_wave(G, pt, dir, wavefront, energised):
  '''Given a point and a direction, advance the beam by one step in that direction, 
  reflecting or splitting as required; 
  put the new point(s) & dir(s) on `wavefront`, and add the points to `energised`.'''
  ht = len(G)
  wd = len(G[0])
  def one_step(pt, dir):
    step = dir_lookup[dir]
    nr = pt[0] + step[0]
    nc = pt[1] + step[1]
    if (0 <= nr < ht) & (0 <= nc < wd):
      return (nr, nc)
    else:
      # print(str((nr,nc)) + " is off the grid, so skip this!")
      return None

  new_pt = one_step(pt, dir)
  if not new_pt: # if we've stepped off the edge of the grid, do nothing
    return (wavefront, energised)
  (nr,nc) = new_pt
  energised[pt].append(dir)
  match G[nr][nc]:   # What we do next depends on what we find at `new_pt`
    case '.': 
      # print("Meeting a '.' at " + str(new_pt))
      wavefront.append((new_pt, dir))
    case '-': 
      # print("Meeting a '-' at " + str(new_pt))
      if (dir == 'W') | (dir == 'E'):  # If we're hitting `-` at the pointy end, pass through
        wavefront.append((new_pt, dir))
      else:  # otherwise, propagate waves to 'W' and 'E' from this position
        wavefront.append((new_pt, 'W'))
        wavefront.append((new_pt, 'E'))
    case '|': 
      # print("Meeting a '|' at " + str(new_pt))
      if (dir == 'N') | (dir == 'S'):  # If we're hitting `|` at the pointy end, pass through
        wavefront.append((new_pt, dir))
      else:  # otherwise, propagate waves to 'N' and 'S' from this position
        wavefront.append((new_pt, 'N'))
        wavefront.append((new_pt, 'S'))
    case '\\': 
      # print("Meeting a '\\' at " + str(new_pt))
      match dir:
        case 'N': wavefront.append((new_pt, 'W'))
        case 'S': wavefront.append((new_pt, 'E'))
        case 'W': wavefront.append((new_pt, 'N'))
        case 'E': wavefront.append((new_pt, 'S'))
    case '/': 
      # print("Meeting a '/' at " + str(new_pt))
      match dir:
        case 'N': wavefront.append((new_pt, 'E'))
        case 'S': wavefront.append((new_pt, 'W'))
        case 'W': wavefront.append((new_pt, 'S'))
        case 'E': wavefront.append((new_pt, 'N'))
    case _:
      raise ValueError("Wasn't expectng to find " + str(G[nr][nc]) + " in the grid!")
  # print("After updating at point " + str(new_pt) + " in direction " + str(dir) + " we have: ")
  return (wavefront, energised)


def fire_laser(G, pt, dir):
  '''Given a grid `G` of optical elements, a starting point `pt` just off the grid, 
  and a direction `dir` in which to fire the laser, 
  simulate the bouncing of the laser beam around the grid
  and return the number of squares the laser passed through.'''
  # A record of which points have a beam passing through in which directions, 
  # so we don't need to re-process them if the wavefront reaches them again
  energised = defaultdict(list)

  # The wavefront is a list of (pt, dir).
  wavefront = [(pt, dir)]

  while wavefront:
    # print("wavefront: " + str(wavefront))
    (pt, dir) = wavefront.pop()
    # print("Now we're at point " + str(pt) + " moving in direction " + str(dir))
    # if we've passed through `pt` in direction `dir`, don't redo it
    if (dir in energised[pt]): 
      # print("We've already examined direction " + str(dir) + " from point " + str(pt) + "; skipping")
      pass
    else:
      (wavefront, energised) = advance_wave(G, pt, dir, wavefront, energised)
  
  # We started just off the grid, so remove this off-grid square before we finish
  del energised[pt]
  # print(energised)
  # EG = ["".join(['#' if (row, col) in energised else '.' for col in range(len(G[0]))]) 
  #       for row in range(len(G))]
  # show(EG)
  # print(EG == energised_correct)
  return len(energised)

def main_a(G):
  O = (0,-1)  # start just to the left of the top left corner
  return fire_laser(G, O, 'E')

print(main_a(test_input))  # 46
print(main_a(input))       # 7060

TTT.timecheck("Part (a)")  # ~ 15 ms

################################
# Part (b)
################################

# Starting the beam in the fourth tile from the left in the top row, 51 tiles are energized
# Ob = (-1,3)
# print(fire_laser(test_input, Ob, 'S'))  # 51

def main_b(G):
  ht = len(G)
  wd = len(G[0])
  greatest_energy = Best()
  # # Fire lasers from left
  greatest_energy.reduce([fire_laser(G, (r, -1), 'E') for r in range(ht)])
  # Fire lasers from right
  greatest_energy.reduce([fire_laser(G, (r, wd), 'W') for r in range(ht)])
  # # Fire lasers from top
  greatest_energy.reduce([fire_laser(G, (-1, c), 'S') for c in range(wd)])
  # # Fire lasers from bottom
  greatest_energy.reduce([fire_laser(G, (ht, c), 'N') for c in range(wd)])
  return greatest_energy.best_so_far

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################