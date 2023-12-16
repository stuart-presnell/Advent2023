# https://adventofcode.com/2023/day/16

from collections import OrderedDict

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

O = (0,0)

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
    return None

 
# A record of which points have a beam passing through in which directions, 
# so we don't need to re-process them if the wavefront reaches them again
energised = {(0,0):['E']}
# The wavefront is an ordered dictionary of points; 
# `wavefront[pt]` is a list of directions in which beams are moving through `pt`
# It's ordered so at each step we can `pop` an element from it to advance.
# Initialise every entry to `[]`.
wavefront = OrderedDict.fromkeys(
  [(r,c) for r in range(wd) for c in range(ht)], 
  [])
wavefront[(0,0)] = ['E']

def advance_wave(pt, dir):
  '''Given a point and a direction, advance the beam by one step in that direction, 
  reflecting or splitting as required; 
  put the new point(s) & dir(s) on `wavefront`, and add the points to `energised`.'''
  global energised, wavefront

  new_pt = one_step(pt, dir)
  if not new_pt: # if we've stepped off the edge of the grid, do nothing
    return
  (nr,nc) = new_pt
  match grid[nr][nc]:   # What we do next depends on what we find at `new_pt`
    case '.': 
      energised[new_pt].append(dir)
      wavefront[new_pt].append(dir)
      return
    case '-': 
      if (dir == 'W') | (dir == 'E'):  # If we're hitting `-` at the pointy end, pass through
        return advance_wave(new_pt, dir)
      else:
        
        pass  # TODO:
    case '|': 
      if (dir == 'N') | (dir == 'N'):  # If we're hitting `|` at the pointy end, pass through
        return advance_wave(new_pt, dir)
      else:
        pass  # TODO:
    case '\\': 
      match dir:
        case 'N': pass
        case 'S': pass
        case 'W': pass
        case 'E': pass
    case '/': 
      match dir:
        case 'N': pass
        case 'S': pass
        case 'W': pass
        case 'E': pass
    case _:
      raise ValueError("Wasn't expectng to find " + str(grid[nr][nc]) + " in the grid!")

# print(wavefront)
# print(energised)
# advance_wave((0,2), 'E')
# print(wavefront)
# print(energised)

# while wavefront:
#   (pt, dirs) = wavefront.popitem()
#   for dir in dirs:
#     if dir in energised[pt]: # if we've passed through `pt` in direction `dir`, don't redo it
#       pass
#     else:
#       advance_wave(pt, dir)
# show(energised)

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