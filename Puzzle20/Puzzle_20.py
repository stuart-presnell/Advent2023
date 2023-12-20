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
  def receive(self, p, fr):
    '''Given a pulse with hilo status `p` from sender `fr`,
    process it according to FlipFlop rules
    and return a (possibly empty) list of pulses emitted, to be put on the queue.'''
    if p == 'hi':
      return []  # "If a flip-flop module receives a high pulse, it is ignored and nothing happens."
    elif p == 'lo': # "However, if a flip-flop module receives a low pulse..."
      if not self.state:  # "If it was off, it turns on and sends a high pulse."
        self.state = not self.state
        # Send a `hi` pulse to all dests
        return [(self.name, d, 'hi') for d in self.dests]
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
  def receive(self, p, fr):
    '''Given a pulse with hilo status `p` from sender `fr`,
    process it according to Conj rules
    and return a (possibly empty) list of pulses emitted, to be put on the queue.'''
    # TODO: Write Conj.receive()
    pass

class Broadcast():
  def __init__(self, dests):
    self.type = "Broadcast"
    self.name = "broadcaster"
    self.dests = dests
    self.state = False
  def receive(self, p, fr):
    '''Given a pulse with hilo status `p` from sender `fr`,
    process it according to Broadcast rules
    and return a (possibly empty) list of pulses emitted, to be put on the queue.
    "When broadcaster receives a pulse, it sends the same pulse to all of its destination modules."'''
    return [(self.name, d, p) for d in self.dests]

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
  return modules

def press_button(pq:Queue):
  '''Simulate pressing the BUTTON:
  "When you push the button, a single low pulse is sent directly to the broadcaster module."'''
  pq.put_nowait(('button', 'broadcaster', 'lo'))
  return pq

def show_queue(pq):
  print(pq.queue)

# Entries in pulse_queue are triples `(fr, to, hilo)` 
# recording that a hi/lo pulse has been sent from module `fr` to module `to`
pulse_queue = Queue()

def process_pulse_queue(modules, pq):
  '''While there are still pulses to process, 
  get each module to process its pulses and add its outputs back onto the pulse queue.'''
  while not pq.empty():
    # Get the next pulse from the queue
    (fr, to, hilo) = pq.get_nowait()
    print("Processing a pulse: " + fr + " -" + hilo + "-> " + to)
    # Pick out the module that receives the pulse
    m = modules[to]
    # Send the pulse to `m`, collect any response pulses it replies with
    replies = m.receive(hilo, fr)
    # Put these responses onto the pulse queue
    for pulse in replies:
      pq.put_nowait(pulse)
  print("The pulse queue is now empty")
  return modules

M = process_input(ip)
# show_queue(pulse_queue)

press_button(pulse_queue)
process_pulse_queue(M, pulse_queue)

# (M, pulse_queue) = process_pulse_queue(M, pulse_queue)
# print(M)

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