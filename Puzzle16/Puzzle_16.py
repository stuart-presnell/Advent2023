# https://adventofcode.com/2023/day/16

from collections import defaultdict

def showD(d:dict):
  for k in d:
    if d[k]: print(k, ": ", d[k])

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, parse_nums, rotate90, close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle16_test.txt")
input      = parse_file_a("Puzzle16_input.txt")

grid = test_input
# grid = input
show(grid)

ht = len(grid)
wd = len(grid[0])

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

def one_step(pt, dir):
  step = dir_lookup[dir]
  nr = pt[0] + step[0]
  nc = pt[1] + step[1]
  if (0 <= nr < ht) & (0 <= nc < wd):
    return (nr, nc)
  else:
    # print(str((nr,nc)) + " is off the grid, so skip this!")
    return None

 
# A record of which points have a beam passing through in which directions, 
# so we don't need to re-process them if the wavefront reaches them again
# Initialise every entry to `[]`.
# energised = {(r,c):[] for r in range(wd) for c in range(ht)}
energised = defaultdict(list)

# The wavefront is a list of (pt, dir).
# wavefront = defaultdict(list)
# wavefront = {(r,c):[] for r in range(wd) for c in range(ht)}
O = (0,0)
wavefront = [(O, 'E')]

def advance_wave(pt, dir, wavefront, energised):
  '''Given a point and a direction, advance the beam by one step in that direction, 
  reflecting or splitting as required; 
  put the new point(s) & dir(s) on `wavefront`, and add the points to `energised`.'''
  new_pt = one_step(pt, dir)
  if not new_pt: # if we've stepped off the edge of the grid, do nothing
    return (wavefront, energised)
  (nr,nc) = new_pt
  energised[pt].append(dir)
  match grid[nr][nc]:   # What we do next depends on what we find at `new_pt`
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
    case '/': 
      # print("Meeting a '/' at " + str(new_pt))
      match dir:
        case 'N': wavefront.append((new_pt, 'W'))
        case 'S': wavefront.append((new_pt, 'E'))
        case 'W': wavefront.append((new_pt, 'N'))
        case 'E': wavefront.append((new_pt, 'S'))
    case '\\': 
      # print("Meeting a '\\' at " + str(new_pt))
      match dir:
        case 'N': wavefront.append((new_pt, 'E'))
        case 'S': wavefront.append((new_pt, 'W'))
        case 'W': wavefront.append((new_pt, 'S'))
        case 'E': wavefront.append((new_pt, 'N'))
    case _:
      raise ValueError("Wasn't expectng to find " + str(grid[nr][nc]) + " in the grid!")
  # print("After updating at point " + str(new_pt) + " in direction " + str(dir) + " we have: ")
  # print("wavefront")
  # showD(wavefront)
  # print("energised")
  # showD(energised)
  # print()
  return (wavefront, energised)

# print("wavefront")
# showD(wavefront)
# print("energised")
# showD(energised)
# print()

# (pt, dirs) = wavefront.popitem()
# print(pt, dirs)
# # advance_wave((0,0), 'E')
# print()

# print("wavefront")
# showD(wavefront)
# print("energised")
# showD(energised)


while wavefront:
  (pt, dir) = wavefront.pop()
  # print("Now we're at point " + str(pt) + " moving in direction " + str(dir))
  # if we've passed through `pt` in direction `dir`, don't redo it
  if (dir in energised[pt]): 
    # print("We've already examined direction " + str(dir) + " from point " + str(pt) + "; skipping")
    pass
  else:
    (wavefront, energised) = advance_wave(pt, dir, wavefront, energised)

print("wavefront")
showD(wavefront)
print("energised")
showD(energised)

# def main_a(ip):
#   pass

# print(main_a(test_input))  # 
# print(main_a(input))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################