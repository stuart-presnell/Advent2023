# https://adventofcode.com/2023/day/15

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
  ip_file = f.read().split(",")
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle15_test.txt")
input      = parse_file_a("Puzzle15_input.txt")

ip = test_input
# ip = input
# show(ip)


################################
# Part (a)
################################

def HASH_alg(s:str, verbose = False) -> int:
  value = 0
  for char in s:
    if verbose: print(char)
    a = ord(char)
    if verbose: print("ASCII value of " + char + " is " + str(a))
    if verbose: print("Adding " + str(a) + " to " + str(value) + " gives: ", end = '')
    value += a
    if verbose: print(value)
    if verbose: print("Multiplying " + str(value) + " by 17 " + " gives: ", end = '')
    value = value * 17
    if verbose: print(value)
    if verbose: print("Reducing " + str(value) + " mod 256 " + " gives: ", end = '')
    value = value % 256
    if verbose: print(value)
  return value

# print(HASH_alg("HASH")) # 52

def main_a(ip):
  op = 0
  for line in ip:
    x = HASH_alg(line)
    # print(line, "\t becomes \t", x)
    op += x
  return op
  

# print(main_a(test_input))  # 1320
# print(main_a(input))       # 513158

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# Represent the lens boxes as a dictionary whose keys are numbers 0...256, values are lists of lenses.

def process_commands(ip_file):
  '''Given a file of commands, one per line, format them and populate `lens_boxes`.'''
  lens_boxes = {}
  op = []
  for cmd in ip_file:
    cmd = cmd.split('=')
    if len(cmd) == 1:   # if the line ends in '-'
      cmd = [cmd[0][:-1]]
    box = HASH_alg(cmd[0])
    op.append([cmd, box])
    lens_boxes[box] = []
  return (op, lens_boxes)

# (cmd_sequence, lens_boxes) = process_commands(test_input)

def replace_or_insert(box_content, label, fl):
  '''Given a list of lenses and a label, remove a lens with that label from the list if present.'''
  L = box_content.copy()
  for i in range(len(L)):
    if L[i][0] == label:   # If there's already a lens with that label, replace it
      L[i] = [label, fl]
      return L
  # Else if we get to the end of the list without finding the label, add another lens
  L.append([label, fl])
  return L


def try_to_remove(box_content, label):
  L = box_content.copy()
  for lens in L:
    if lens[0] == label:
      L.remove(lens)
      break
  return L


def manipulate_lenses(cmd_sequence, lens_boxes):
  for [cmd, box] in cmd_sequence:
    # print(cmd, " \t ", box)
    if len(cmd) == 2:
      [label, n] = cmd
      fl = int(n)
      lens_boxes[box] = replace_or_insert(lens_boxes[box], label, fl)
    elif len(cmd) == 1:
      [label] = cmd
      lens_boxes[box] = try_to_remove(lens_boxes[box], label)
    else:
      raise ValueError("Expected command to be of length 1 or 2")
  return lens_boxes

def focusing_power(box, pos, fl):
  return (box + 1) * pos * fl

# show(process_commands(test_input))

def main_b(ip_file):
  lb = manipulate_lenses(*process_commands(ip_file))
  # for i in lb:
  #   print(i, lb[i])
  count = 0
  for box in lb:
    for pos in range(len(lb[box])):
      [_, fl] = lb[box][pos]
      count += focusing_power(box, pos+1, fl)
  return count


  

print(main_b(test_input))  # 145
print(main_b(input))       # 200277

# TTT.timecheck("Part (b)")  #

################################