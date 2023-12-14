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
# print("Original input: ")
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
      op += i + 1
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

billion = 1000000000

def repeat_cycles(grid, n, verbose = False):
  '''Given a starting grid and a number of cycles to perform,
  run the cycle that many times.'''
  for i in range(n):
    if verbose: print("After " + str(i+1) + " cycle" + ("s" if i > 0 else "") + ":")
    grid = cycle(grid)
    if verbose: show(grid, False)  
    if verbose: print()
  return grid

def detect_loop(grid, max_cycles, verbose = False):
  '''Given a starting grid and a limit on the number of cycles to perform,
  keep running the cycle until we find a loop.'''
  visited_states = [grid]  # After no cycles...
  for i in range(max_cycles):
    if verbose: print("After " + str(i+1) + " cycle" + ("s" if i > 0 else "") + ":")
    grid = cycle(grid)  # Perform one more cycle
    if verbose: show(grid, False)  
    if verbose: print()
    if grid in visited_states:  # If the grid after i cycles is the same as some previous grid
      prev = visited_states.index(grid)
      period = (i+1) - prev
      if verbose: print("Found a loop! The grid after " + str(i+1) + " cycles is the same as after " + str(prev) + " cycles")
      return (visited_states, period, prev)
    else:
      visited_states.append(grid)
  if verbose: print("Didn't find a loop after " + str(max_cycles) + " cycle" + plural_s(max_cycles - 1))
  return grid

# (vs, period, loop_start) = detect_loop(ip.copy(), 1000, verbose = False)
# print(period)
# print(loop_start)

# ip2 = test_input.copy()

# vs = [ip2]  # After no cycles...
# for i in range(1000):
#   ip2 = cycle(ip2)
#   vs.append(ip2)

# print("Grid after defining vs: ")
# show(ip)


# show(vs[:loop_start])
# print(loop_start, loop_start + 1 * period)
# show(vs[loop_start:loop_start + 1 * period])
# print(loop_start + 1 * period, loop_start + 2 * period)
# show(vs[loop_start + 1 * period:loop_start + 2 * period])
# print(loop_start + 2 * period, loop_start + 3 * period)
# show(vs[loop_start + 2 * period:loop_start + 3 * period])


# show(vs)

# print(vs[3])
# k = 3
# print(repeat_cycles(ip, k) == repeat_cycles(ip, k+6))
# print(repeat_cycles(ip.copy(), 3))
# print(repeat_cycles(ip.copy(), 9))
# print(vs[9])
# print(repeat_cycles(ip, 15))
# for i in range(10):
#   print(repeat_cycles(ip, 3 + 6*i))

# 01234567834567834...


# print(vs[9])

# print(loop_start, period)

def reindex(n, loop_start, period):
  return ((n - loop_start) % period) + loop_start

def quick_repeat_cycles(vs, n, loop_start, period):
  return vs[reindex(n, loop_start, period)]


# print(repeat_cycles(ip,9))
# after_billion = quick_repeat_cycles(vs, 1000000000, loop_start, period)
# print(calc_cost(after_billion))

# ip6 = repeat_cycles(ip, 6)
# ip1000 = repeat_cycles(ip, 1000)

# # for x in [ip6, ip1000]:
# #   print(x)


# print(billion%7)

# # print(vs[6+1])
# # quick_repeat_cycles(vs,100,7) == 

# print(repeat_cycles(ip,100))


# calc_cost(repeat_cycles(ip,billion%7))


# print(billion%7)

# show(vs)

# G = test_input.copy()
# for i in range(200):

def calc_cost_b(grid):
  '''`calc_cost` was worked out on the assumption that the grid was rotated 90.
  That's not the case here because we've completed a full cycle, 
  so we need to rotate the grid before calculating.'''
  return calc_cost(rotate90(grid))



def main_b(ip_file, N):
  (vs, period, loop_start) = detect_loop(ip_file.copy(), 1000, verbose = False)
  print("Period = ", period)
  reduced_N = N%period if N%period > loop_start else N%period + period
  cycled_grid = repeat_cycles(ip_file.copy(), reduced_N)
  # k = loop_start + 8
  # print(repeat_cycles(ip_file.copy(), k) == repeat_cycles(ip_file.copy(), k+ 30 * period))
  # cycled_grid = vs[reindex(N, loop_start, period)]
  return (calc_cost_b(cycled_grid))
  

print(main_b(test_input, billion))  # 64
print(main_b(input, billion))       # 
# 98876 is too low
# 102130 is too high



################################

# TTT.timecheck("Final")