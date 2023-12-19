# https://adventofcode.com/2023/day/19

# My utility functions
from utils import (
show, 
chunk_splitlines, 
printT, showM, showD, parse_nums, rotate90, 
# close_bracket, cmp, qsort, nwise_cycled,
# Best, 
# Timer,
)
# TTT = Timer()

################################

def parse_file_a(filename):
  f = open(filename)
  ip_file = chunk_splitlines(f.read())
  # .splitlines()
  f.close()
  return ip_file

test_input = parse_file_a("Puzzle19_test.txt")
input      = parse_file_a("Puzzle19_input.txt")

ip = test_input
# ip = input
# show(ip[0])

def process_command(cmd):
  '''Given a single command, such as `'a<2006'`, return lambda 
  that takes a dictionary `d` and checks whether `d['a'] < 2006`.'''
  if '<' in cmd:
    [var, n] = cmd.split('<')
    return (lambda d : d[var] < int(n))
  elif '>' in cmd:
    [var, n] = cmd.split('>')
    return (lambda d : d[var] > int(n))
  elif cmd == 'True':
    return lambda _ : True
  else:
    raise ValueError("Expected either a </> comparison or 'True'.")

def parse_command_line(s):
  '''Given a string such as `'px{a<2006:qkq,m>2090:A,rfg}'` return a command description.'''
  [name, s] = s.split('{')
  s = s[:-1].split(',')
  s = [cmd.split(':') for cmd in s]
  op = []
  for [cmp, dst] in s[:-1]:
    op.append([process_command(cmp),dst])
  last_item = s.pop()[0]
  op.append(['True', last_item])
  return (name, op)


def parse_all_commands(L):
  '''Given a list of command strings, return a dictionary.'''
  d = {}
  for line in L:
    (name, s) = parse_command_line(line)
    d[name] = s
  return d

def parse_machine_part(s):
  '''Given a string such as `'{x=787,m=2655,a=1222,s=2876}'`, return a dictionary.'''
  d = {}
  for item in s[1:-1].split(","):
    [l,n] = item.split('=')
    d[l] = int(n)
  return d

def follow_inst(d, part):
  '''Given a dictionary `d` containing a program of instructions, and a machine part `part`
  (represented as a dictionary), 
  apply the program in `d` to `part` and return either `'A'` or `'R'`.'''
  # "All parts begin in the workflow named `in`."
  current_inst_name = 'in'
  while True:
    if (current_inst_name == 'R') | (current_inst_name == 'A'):
      return current_inst_name
    current_inst = d[current_inst_name]
    for check in current_inst:
      pass

# process_command('a<2006')
# parse_command_line('px{a<2006:qkq,m>2090:A,rfg}')
print(parse_all_commands(ip[0]))
show(ip[0])
# parse_machine_part('{x=787,m=2655,a=1222,s=2876}')

################################
# Part (a)
################################

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