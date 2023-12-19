# https://adventofcode.com/2023/day/19

# My utility functions
from utils import (
show, 
chunk_splitlines, 
# printT, showM, 
showD, 
unzip, 
# parse_nums, rotate90, 
# close_bracket, cmp, qsort, nwise_cycled,
# Best, 
# Timer,
)
# TTT = Timer(1)

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
show(ip[0])

def process_command(cmd):
  '''Given a single command, such as `'a<2006'`, return lambda 
  that takes a dictionary `d` and checks whether `d['a'] < 2006`.'''
  if '<' in cmd:
    [var, n] = cmd.split('<')
    return (lambda d : d[var] < int(n))
  elif '>' in cmd:
    [var, n] = cmd.split('>')
    return (lambda d : d[var] > int(n))
  # elif cmd == 'True':
  #   return lambda _ : True
  else:
    raise ValueError("Expected either a </> comparison or 'True'.")

def parse_command_line_a(s):
  '''Given a string such as `'px{a<2006:qkq,m>2090:A,rfg}'` return a command description.'''
  [name, s] = s.split('{')
  s = s[:-1].split(',')
  s = [cmd.split(':') for cmd in s]
  op = []
  for [cmp, dst] in s[:-1]:
    op.append([process_command(cmp),dst])
  last_item = s.pop()[0]
  op.append([lambda _ : True, last_item])
  return (name, op)


def parse_all_commands(L):
  '''Given a list of command strings, return a dictionary.'''
  d = {}
  for line in L:
    (name, s) = parse_command_line_a(line)
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
      # print("Finally reached " + current_inst_name)
      return current_inst_name
    current_inst = d[current_inst_name]
    # print("Executing instruction " + current_inst_name)
    # print(current_inst)
    for [check, dst] in current_inst:
      if check(part):
        # print("Moving to " + dst)
        current_inst_name = dst
        break


# process_command('a<2006')
# parse_command_line('px{a<2006:qkq,m>2090:A,rfg}')
# show(ip[1])
# p = parse_machine_part('{x=787,m=2655,a=1222,s=2876}')
# print(p)
# print()
# program = parse_all_commands(ip[0])


# follow_inst(program, p)


################################
# Part (a)
################################

def score(part):
  return sum([part[l] for l in ['x', 'm', 'a', 's']])

def main_a(ip_file):
  program = parse_all_commands(ip_file[0])
  parts = [parse_machine_part(item) for item in ip_file[1]]
  # show(parts)
  total_score = 0
  for p in parts:
    if follow_inst(program, p) == 'A':
      # print(score(p))
      total_score += score(p)
  return total_score

# print(main_a(test_input))  # 19114
# print(main_a(input))       # 287054

# TTT.timecheck("Part (a)")  # ~ 5 ms

################################
# Part (b)
################################

# Consider only your list of workflows; 
# the list of part ratings that the Elves wanted you to sort is no longer relevant. 
# How many distinct combinations of ratings will be accepted by the Elves' workflows?

def parse_command_line_b(s):
  '''Given a string such as `'px{a<2006:qkq,m>2090:A,rfg}'`,  
  return a dict of destinations we can go to from here
  where the key for each destination is:
  * the name of this instruction, e.g. 'px', 
  * the list of conditions that we must fail 
  * the condition that must be satisfied:
  e.g. d['qkq'] = ('px', [], 'a<2006')
       d['A']   = ('px', ['a<2006'], 'm>2090')
       d['rfg'] = ('px', ['a<2006', 'm>2090'], 'True')
  '''
  [name, s] = s.split('{')  # e.g. ['px', 'a<2006:qkq,m>2090:A,rfg}']
  s = s[:-1].split(',')     # e.g. ['a<2006:qkq', 'm>2090:A' , 'rfg']
  s = [cmd.split(':') for cmd in s]
  last_item = s.pop()[0]
  s.append(['True', last_item])
  [conds, dsts] = unzip(s)
  # print(conds)
  # print(dsts)
  d = {}
  for i in range(len(dsts)):
    d[dsts[i]] = (name)
  return d
  # for [cmp, dst] in s[:-1]:
  #   # d[dst] = ???
  #   pass
  # last_dst = s[-1][0]
  # d[last_dst] = ????

  # op = []
  # for [cmp, dst] in s[:-1]:
  #   op.append([process_command(cmp),dst])
  # 
  # op.append([lambda _ : True, last_item])
  # return (name, op)

showD(parse_command_line_b('px{a<2006:qkq,m>2090:A,rfg}'))


# def main_b(ip_file):
#   pass

# print(main_b(test_input))  # 
# print(main_b(input))       # 

# TTT.timecheck("Part (b)")  #

################################