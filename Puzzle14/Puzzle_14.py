# https://adventofcode.com/2022/day/14

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, parse_nums, 
rotate90, 
# close_bracket, cmp, qsort, Best, 
Timer,
)
TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle14_test.txt")
input      = parse_file_a("Puzzle14_input.txt")

ip = test_input
# ip = input
# show(ip)

################################
# Part (a)
################################

# Roll the rocks north

def roll_row_east(row):
  row = "".join(row)  # Make sure `row` is a string, not a list
  rolled_row = ""
  for block in row.split('#'):
    Os = block.count('O')
    rolled_row = rolled_row + '.' * (len(block)-Os) + 'O' * Os + '#'
  # print(row)
  return (rolled_row[:len(row)])  # If we've added an excess '#', trim it off

def calc_weight_cost(row):
  op = 0
  for i in range(len(row)):
    if row[i] == 'O':
      op += i +1
  return op

def calc_cost(grid):
  return sum([calc_weight_cost(row) for row in grid])

def main_a(ip):
  # First, rotate 90 so we're working on rows instead of columns
  ip = rotate90(ip)  
  # Now our task is to roll the rocks *east*
  # Roll whole grid east
  rolled_grid = [roll_row_east(row) for row in ip]
  return calc_cost(rolled_grid)

# print(main_a(test_input))  # 136
# print(main_a(input))       # 112773

################################
# Part (b)
################################

def plural_s(n):
  return ("s" if n > 0 else "")

def cycle(ip):
  ''' "Each cycle tilts the platform four times 
  so that the rounded rocks roll north, then west, then south, then east." '''
  dirs = ['N', 'W','S', 'E']
  for i in range(4):
    # show(ip)
    # print("Rolling " + dirs[i])
    # First, rotate 90 so we're working on rows instead of columns
    ip = rotate90(ip)  
    ip = [roll_row_east(row) for row in ip]
  return ip

# Calculate the load after 1000000000 (1 billion!) cycles
# Obviously we're not going to run this code for 1 billion cycles
# Evidently there's a loop that we need to detect

def repeat_cycles(grid, max_cycles, verbose = False):
  '''Given a starting grid and a limit on the number of cycles to perform,
  keep running the cycle until we find a loop.'''
  visited_states = [grid]
  for i in range(max_cycles):
    if verbose: print("After " + str(i+1) + " cycle" + ("s" if i > 0 else "") + ":")
    grid = cycle(grid)
    if verbose: show(grid, False)  
    if verbose: print()
    if grid in visited_states:
      return (grid, max_cycles)
    else:
      visited_states.append(grid)
  print("Didn't find a loop after " + str(max_cycles) + " cycle" + plural_s(max_cycles - 1))
  return grid

ip = repeat_cycles(ip, 3)
show(ip)





# def main_b(ip):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 


################################

# TTT.timecheck("Final")