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

ip = test_input
# show(ip)

################################
# Part (a)
################################

# Roll the rocks north

# First, rotate 90 so we're working on rows instead of columns
ip = rotate90(ip)  
# Now our task is to roll the rocks *east*

row = "".join(ip[0])

rolled_row = ""
for block in row.split('#'):
  Os = block.count('O')
  rolled_row = rolled_row + '.' * (len(block)-Os) + 'O' * Os + '#'
print(row)
print(rolled_row[:len(row)])  # If we've added an excess '#', trim it off




# def main_a(ip):
#   pass

# print(main_a(test_input))  # 
# print(main_a(input))       # 


################################
# Part (b)
################################

# def main_b(ip):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 


################################

# TTT.timecheck("Final")