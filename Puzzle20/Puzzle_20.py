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

# ip = test_input01
# ip = test_input02
ip = input
# show(ip)

################################
# Part (a)
################################

class FlipFlop():
  def __init__(self, name, dests):
    self.type = "FlipFlop"
    self.name = name
    self.dests = dests
    self.state = False
  def receive(self, p):
    if p == 'hi':
      pass  # "If a flip-flop module receives a high pulse, it is ignored and nothing happens."
    elif p == 'lo': # "However, if a flip-flop module receives a low pulse..."
      if not self.state:  # "If it was off, it turns on and sends a high pulse."
        self.state = not self.state
        return 'hi'
      elif self.state: # "If it was on, it turns off and sends a low pulse."
        self.state = not self.state
        return 'lo'

class Conj():
  def __init__(self, name, dests):
    self.type = "Conj"
    self.name = name
    self.dests = dests
    self.state = False
    self.memory = {}
  def receive(self, p):
    pass

class Broadcast():
  def __init__(self, dests):
    self.type = "Broadcast"
    self.name = "broadcaster"
    self.dests = dests
    self.state = False
  def receive(self, p):
    pass

class Button():
  def __init__(self,dests):
    self.type = "Button"
    self.name = "button"
    self.dests = dests
    self.state = False
  def press(self):
    pass

def process_input(ip_file):
  '''Go through the lines of the input, create a module for each line.  Also create a `Button`.'''
  modules = {}
  # First, go throuh all the lines and process just the Conj modules
  for [name, dests] in ip_file:
    if (name[0] == '&'):
      name = name[1:]
      # print("Processing a Conj module called " + name)
      modules[name] = Conj(name, dests)
  
  # Now go through all the lines again and process all the other modules
  # This lets us add `parent` information to the Conj modules so they know what to remember
  for [name, dests] in ip_file:
    if (name[0] == '%'):
      name = name[1:]
      # print("Processing a FlipFlop module called " + name)
      modules[name] = FlipFlop(name, dests)
      for m in dests:
        # print("Checking whether to add myself as a parent to " + m)
        if (m in modules):
          if (modules[m].type == "Conj"):
            # print("Yes, " + name + " is a parent of " + m)
            modules[m].memory[name] = 'lo'    # Add the current module to `m`'s memory, set to 'lo'
    elif (name[0] == '&'):
      name = name[1:]
      # print("ReProcessing a Conj module called " + name)
      for m in dests:
        # print("Checking whether to add myself as a parent to " + m)
        if (m in modules):
          if (modules[m].type == "Conj"):
            # print("Yes, " + name + " is a parent of " + m)
            modules[m].memory[name] = 'lo'    # Add the current module to `m`'s memory, set to 'lo'
    elif (name == 'broadcaster'):
      # print("Processing a Broadcast module called " + name)
      modules[name] = Broadcast(dests)
      for m in dests:
        # print("Checking whether to add myself as a parent to " + m)
        if (m in modules):
          if (modules[m].type == "Conj"):
            # print("Yes, " + name + " is a parent of " + m)
            modules[m].memory[name] = 'lo'    # Add the current module to `m`'s memory, set to 'lo'
    else:
      raise ValueError("Expected module name to be 'broadcaster' or to start with '%' or '&'.")
  modules["button"] = Button(['broadcaster'])
  return modules




# Entries in pulse_queue are pairs `(fr, to, hilo)` 
# recording that a hi/lo pulse has been sent from module `fr` to module `to`
pulse_queue = Queue()

def process_pulse_queue():
  '''While there are still pulses to process, 
  get each module to process its pulses and add its outputs back onto the pulse queue.'''
  while not pulse_queue.empty():
    
    pass



M = process_input(ip)

for k in M:
 if M[k].type == 'Conj':
  print(k,"\t", M[k].memory)
#  (M["button"].type)




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