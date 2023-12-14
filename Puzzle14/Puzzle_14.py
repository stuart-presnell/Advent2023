# https://adventofcode.com/2022/day/14

# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, parse_nums, 
rotate90, 
# close_bracket, cmp, qsort, Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle14_test.txt")
input      = parse_file_a("Puzzle14_input.txt")

ip = input
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

print(main_a(test_input))  # 136
print(main_a(input))       # 112773

################################
# Part (b)
################################

# def main_b(ip):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 


################################

# TTT.timecheck("Final")