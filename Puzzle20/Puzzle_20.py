# https://adventofcode.com/2023/day/20

from queue import Queue

# My utility functions
# My utility functions
from utils import (
show, 
# chunk_splitlines, printT, showM, 
showD, 
# unzip, parse_nums, rotate90, close_bracket, cmp, qsort, nwise_cycled,
# Best, 
Timer,
Looper
)
TTT = Timer(1)

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
ip = test_input02
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
        return [(self.name, d, 'lo') for d in self.dests]

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
    and return a (possibly empty) list of pulses emitted, to be put on the queue.
    
    "When a pulse is received, the conjunction module first updates its memory for that input. 
    Then, if it remembers high pulses for all inputs, it sends a low pulse; 
    otherwise, it sends a high pulse."'''
    # print("Conj module " + self.name + " received a " + p + " pulse from " + fr)
    self.memory[fr] = p
    # print("Its memory is now: ")
    # showD(self.memory)
    if (all([v == 'hi' for v in self.memory.values()])):
      return [(self.name, d, 'lo') for d in self.dests]
    else:
      return [(self.name, d, 'hi') for d in self.dests]

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

class Output():
  def __init__(self):
    self.type = "Output"
    self.name = "output"
    self.dests = []
    self.state = False
  def receive(self, p, fr):
    '''Output ignores all input pulses'''
    return []

def process_input(ip_file):
  '''Go through the lines of the input, create a module for each line.  Also create a `Button`.'''
  modules = {}
  # First, go through all the lines and process just the Conj modules
  for [name, dests] in ip_file:
    if (name[0] == '&'):
      name = name[1:]
      # print("Processing a Conj module called " + name)
      modules[name] = Conj(name, dests)
  
  # Now go through all the lines again and process all the other transmitting modules
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
    
    # Finally, go through all the lines again, looking for destinations that aren't senders
    for [name, dests] in ip_file:
      for d in dests:
        if d not in modules:
          modules[d] = Output()

  return modules

def press_button(pq:Queue):
  '''Simulate pressing the BUTTON:
  "When you push the button, a single low pulse is sent directly to the broadcaster module."'''
  pq.put_nowait(('button', 'broadcaster', 'lo'))
  return pq

def show_queue(pq):
  print(pq.queue)

def show_module_states(modules, focus=[]):
  '''Print `state` and `memory` of every module in `focus` (or, by default, every module).'''
  if not focus: focus = modules
  print([(m, modules[m].state) for m in focus])
  print([(m, modules[m].memory) for m in focus if modules[m].type == 'Conj'])
  print()

# Entries in pulse_queue are triples `(fr, to, hilo)` 
# recording that a hi/lo pulse has been sent from module `fr` to module `to`
pulse_queue = Queue()

def process_pulse_queue(modules, pq, pulse_count, verbose = False):
  '''While there are still pulses to process, 
  get each module to process its pulses and add its outputs back onto the pulse queue.
  Keep a count in dictionary `pulse_count` of how many `'hi'` and `'lo'` pulses are sent.'''
  while not pq.empty():
    # show_queue(pq)
    # Get the next pulse from the queue
    (fr, to, hilo) = pq.get_nowait()
    pulse_count[hilo] += 1
    if verbose: print(fr + " -" + hilo + "-> " + to)
    # Pick out the module that receives the pulse
    m = modules[to]
    # Send the pulse to `m`, collect any response pulses it replies with
    replies = m.receive(hilo, fr)
    # Put these responses onto the pulse queue
    for pulse in replies:
      pq.put_nowait(pulse)
  if verbose: print()
  return modules, pulse_count

def run_test(ip, n, tracking = [], verbose = False):
  '''Given an input and a number of times to press the button, 
  press the button that many times with optional reporting along the way.
  If `tracking` is set, show the status of all modules in that list
  after each press of the button.'''
  # Initialise the count of hi/lo pulses sent
  P = {hilo : 0 for hilo in ['hi', 'lo']}
  # Define the modules
  M = process_input(ip)

  if verbose: print("Before pressing the button: ")
  if verbose: show_module_states(M)

  for i in range(1,n+1):
    if verbose: print("About to do button press #" + str(i) + ": ")
    press_button(pulse_queue)
    (M,P) = process_pulse_queue(M, pulse_queue, P, verbose)
    if verbose: print("After button press #" + str(i) + ": ")
    if verbose: show_module_states(M)
    if tracking: show_module_states(M, tracking)
  return (M,P)

# (M, P) = run_test(test_input01, 1000)
# (M, P) = run_test(test_input02, 1000)
# (M, P) = run_test(input, 1000)
# show_module_states(M)
# print(P)

# (M, pulse_queue) = process_pulse_queue(M, pulse_queue)
# print(M)

def main_a(ip_file):
  (_, P) = run_test(ip_file, 1000)
  return P['hi'] * P['lo']

# print(main_a(test_input01) == 32000000)  # 32000000
# print(main_a(test_input02) == 11687500)  # 11687500
# print(main_a(input))       # 944750144

# TTT.timecheck("Part (a)")  # ~ 270 ms

################################
# Part (b)
################################

# What is the fewest number of button presses required 
# to deliver a single low pulse to the module named rx?

# rx recieves a pulse only from &kz
# So for rx to get a lo pulse, kz must remember a hi pulse from all its inputs
# &hb -> &sj -> kz
# &hf -> &qq -> kz
# &dl -> &ls -> kz
# &lq -> &bg -> kz

# TODO: Try examining the status of the inputs to `rx` at each cycle, see if there's a repeating pattern with a detectable period.

(M, P) = run_test(input, 1, ['kz', 'sj'])
# show_module_states(M, ['kz'])


# def process_pulse_queue_b(modules, pq, pulse_count, verbose = False):
#   '''While there are still pulses to process, 
#   get each module to process its pulses and add its outputs back onto the pulse queue.
#   Keep a count in dictionary `pulse_count` of how many `'hi'` and `'lo'` pulses are sent.'''
#   while not pq.empty():
#     # show_queue(pq)
#     # Get the next pulse from the queue
#     (fr, to, hilo) = pq.get_nowait()
#     if (to == 'rx') & (hilo == 'lo'):
#       return (None, None)  # If we have a 'lo' pulse to 'rx', ALERT!
#     pulse_count[hilo] += 1
#     if verbose: print(fr + " -" + hilo + "-> " + to)
#     # Pick out the module that receives the pulse
#     m = modules[to]
#     # Send the pulse to `m`, collect any response pulses it replies with
#     replies = m.receive(hilo, fr)
#     # Put these responses onto the pulse queue
#     for pulse in replies:
#       pq.put_nowait(pulse)
#   if verbose: print()
#   return modules, pulse_count

# def main_b(ip):
#   '''Given an input and a number of times to press the button, 
#   press the button that many times with optional reporting along the way.'''
#   number_of_presses = 0
#   # Initialise the count of hi/lo pulses sent
#   P = {hilo : 0 for hilo in ['hi', 'lo']}
#   # Define the modules
#   M = process_input(ip)
#   while M:
#     number_of_presses += 1
#     press_button(pulse_queue)
#     (M,P) = process_pulse_queue(M, pulse_queue, P)
#   return number_of_presses

# main_b(input)


# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################