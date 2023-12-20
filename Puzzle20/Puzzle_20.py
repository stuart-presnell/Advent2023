# https://adventofcode.com/2023/day/20

from queue import Queue

# My utility functions
# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, showD, unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = f.read().splitlines()
  f.close()
  ip_file = [line.split(" -> ") for line in ip_file]
  ip_file = [[line[0], line[1].split(", ")] for line in ip_file]
  return ip_file

test_input01 = parse_file_a("Puzzle20_test01.txt")
test_input02 = parse_file_a("Puzzle20_test02.txt")
input      = parse_file_a("Puzzle20_input.txt")

ip = test_input01
# ip = test_input02
# ip = input
show(ip)

################################
# Part (a)
################################

pulse_queue = Queue()

class FlipFlop():
  def __init__(self, name, dests):
    self.name = name
    self.dests = dests
    self.state = False

class Conj():
  def __init__(self, name, dests):
    self.name = name
    self.dests = dests
    self.state = False
    self.memory = {}

class Broadcast():
  def __init__(self, dests):
    self.name = "broadcaster"
    self.dests = dests
    self.state = False

class Button():
  def __init__(self,dests):
    self.name = "button"
    self.dests = dests
    self.state = False



def process_input(ip_file):
  '''Go through the lines of the input, create a module for each line.  Also create a `Button`.'''
  modules = {}
  for [name, dests] in ip_file:
    if (name[0] == '%'):
      modules[name[1:]] = FlipFlop(name[1:], dests)
    elif (name[0] == '&'):
      modules[name[1:]] = Conj(name[1:], dests)
    elif (name == 'broadcaster'):
      modules[name] = Broadcast(dests)
    else:
      raise ValueError("Expected module name to be 'broadcaster' or to start with '%' or '&'.")
  modules["button"] = Button(['broadcaster'])
  return modules

# M = process_input(test_input01)

# M["button"].dests



# def main_a(ip_file):
#   pass

# print(main_a(test_input))  # 
# print(main_a(input))       # 

# TTT.timecheck("Part (a)")  #

################################
# Part (b)
################################

# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################