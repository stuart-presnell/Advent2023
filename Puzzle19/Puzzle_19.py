# https://adventofcode.com/2023/day/19

from collections import defaultdict
from math import prod

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
  * the tuple of conditions that we must fail 
  * the condition that must be satisfied:
  e.g. d['qkq'] = ('px', (), ('a<2006'))
       d['A']   = ('px', ('a<2006'), ('m>2090'))
       d['rfg'] = ('px', ('a<2006', 'm>2090'), ('True'))
  '''
  [name, s] = s.split('{')  # e.g. ['px', 'a<2006:qkq,m>2090:A,rfg}']
  s = s[:-1].split(',')     # e.g. ['a<2006:qkq', 'm>2090:A' , 'rfg']
  s = [cmd.split(':') for cmd in s]
  last_item = s.pop()[0]
  s.append(['True', last_item])
  [conds, dsts] = unzip(s)
  d = {}
  for i in range(len(dsts)):
    d[dsts[i]] = (name, conds[:i], (conds[i],))
  return d

# showD(parse_command_line_b('px{a<2006:qkq,m>2090:A,rfg}'))

def entry_paths(ip):
  '''Given a list of strings such as `'px{a<2006:qkq,m>2090:A,rfg}'`, 
  return a dictionary whose entry `D[k]` for each state `k`
  is a list of the immediately preceding states that lead to `k`, 
  each annotated with the conditions that must be failed and passed 
  to go from that state to `k`.
  - e.g. `D['A']` includes `('px', ('a<2006',), ('m>2090',))`.'''
  D = defaultdict(list)
  for line in ip:
    pcl = parse_command_line_b(line)
    for dest in pcl:
      D[dest].append(pcl[dest])
    # showD(pcl)
  return D

# E = entry_paths(test_input[0])
# for k in E:
#   print("To get into " + k + ": ")
#   show(E[k])

# show(E['A'])
# print()
# show(E['px'])

def find_accepting_conditions(ip):
  E = entry_paths(ip)
  incomplete_routes_to_A = E['A']
  complete_routes_to_A = []
  while incomplete_routes_to_A:
    rte = incomplete_routes_to_A.pop()
    if rte[0] == 'in':
      # print("This is a route from 'in' to 'A': ")
      # print(rte)
      complete_routes_to_A.append(rte)
      continue
    else:
      (pt, Fail, Pass) = rte
      # print("This is a route from '" + pt +  "' to 'A': ")
      # print(rte)
      for (prev_pt, prev_Fail, prev_Pass) in E[pt]:
        incomplete_routes_to_A.append((prev_pt, prev_Fail + Fail, prev_Pass + Pass))
  return complete_routes_to_A

# x = find_accepting_conditions(test_input[0])
# x = find_accepting_conditions(input[0])
# show(x)

def simplify_conditions(L, PASS = True):
  '''Given a tuple of conditions, e.g. `('a<2006', 'm>2090', 's<537', 'x>2440')`, 
  return a dictionary whose `k` entry is the range of permitted values e.g. `'a' -> [1,2005]`.
  If `PASS = True` then the permitted values are those that satisfy all the given conditions.
  If `PASS = False` then the permitted values are those that fail all the given conditions. (???)
  By default, each range starts at `[1,4000]`.'''
  d = {k : [1,4000] for k in ['x','m','a','s']}
  for cnd in L:
    if cnd == 'True': 
      if PASS:
        # print("Skipping 'True'")
        continue  # Skip 'True'
      else:
        return None   # We can't FAIL a 'True', so there are no permitted values
    # print(cnd)
    k = cnd[0]
    n = int(cnd[2:])
    if PASS:   # If we're trying to PASS all the conditions
      match cnd[1]:
        case '<':
          d[k][1] = min(d[k][1], n-1)
        case '>':
          d[k][0] = max(d[k][0], n+1)
        case _:
          raise ValueError("Expected a comparison")
    else:      # If we're trying to FAIL all the conditions
      match cnd[1]:
        case '<':
          d[k][0] = max(d[k][0], n)
        case '>':
          d[k][1] = min(d[k][1], n)
        case _:
          raise ValueError("Expected a comparison")
  return d

# print(  simplify_conditions(('s<1351', 's>2770'), False)  )
# print(  simplify_conditions(('True', 'm<1801', 'm>838'))  )

def combine_ranges(r1, r2):
  '''Given two ranges `[lo1, hi1]` and `[lo2, hi2]`, return their inersection.'''
  [lo1, hi1] = r1
  [lo2, hi2] = r2
  return [max(lo1, lo2), min(hi1,hi2)]

def capacity(cnd):
  '''Given a dictionary of conditions, 
  e.g. `{'x': [1, 4000], 'm': [839, 1800], 'a': [1, 4000], 's': [1351, 2770]}`
  return the number of values compatible with those conditions.'''
  return prod([cnd[k][1] - cnd[k][0] + 1  for k in cnd])

# print(  capacity({'x': [1, 4000], 'm': [839, 1800], 'a': [1, 4000], 's': [1351, 2770]})  )

# def main_b(ip_file):
#   AC = find_accepting_conditions(ip_file[0])
#   count = 0
#   for (_, Fails, Passes) in AC:
#     # print(Fails, Passes)
#     F = simplify_conditions(Fails, False)
#     P = simplify_conditions(Passes, True)
#     # print(F)
#     # print(P)
#     d = {}
#     for k in ['x','m','a','s']:
#       d[k] = combine_ranges(F[k], P[k])
#     count += capacity(d)
#   return count

# print(main_b(test_input))  #  
# 167 409 079 868 000   -- CORRECT answer
# 140 809 783 868 000   -- my answer :(
# print(main_b(input))       # 

################################
# Trying an alternative approach: start with a region of phase space [1,4000]^4 at 'in', 
# then use the rules to divide and flow this through the graph
# until everything is at 'R' or 'A' (where everything must eventually end up).
# Then total up the region at 'A'.
################################

def parse_command_line_b_v2(s):
  '''Given a string such as `'px{a<2006:qkq,m>2090:A,rfg}'`,  
  return a pair `(name, L)` consisting of the node name `'px'` and a list `L`, 
  where each entry in `L` is a pair `[cnd, dst]`.
  - e.g. `('px',  [['a<2006','qkq'],  ['m>2090','A'],  ['', 'rfg']]  )`
  Note that the last condition will be empty.'''
  [name, s] = s.split('{')  # e.g. ['px', 'a<2006:qkq,m>2090:A,rfg}']
  s = s[:-1].split(',')     # e.g. ['a<2006:qkq', 'm>2090:A' , 'rfg']
  s = [cmd.split(':') for cmd in s]
  last_item = s.pop()[0]
  s.append(['', last_item])
  return (name, s)

def parse_input_commands(ip):
  '''Given a list of strings such as `'px{a<2006:qkq,m>2090:A,rfg}'`,  
  return a dictionary whose keys are the names e.g. `'px'`
  and whose values are the lists of pairs produced by `parse_command_line_b_v2`.'''
  D = {}
  for line in ip:
    (name, s) = parse_command_line_b_v2(line)
    D[name] = s
  return D

# print( 
#   parse_command_line_b_v2('px{a<2006:qkq,m>2090:A,rfg}')
# )

# D = parse_input_commands(test_input[0])
# showD(D)

def split_region(region, condition):
  '''Given a region of phase space, 
  - e.g. {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
  and a `condition` e.g. 'a<2006' (assumed non-empty),
  return the two subregions that satisfy and fail that condition
  - {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 2005], 's': [1, 4000]}
  - {'x': [1, 4000], 'm': [1, 4000], 'a': [2006, 4000], 's': [1, 4000]}
  '''
  PASS = region.copy()
  FAIL = region.copy()
  if '<' in condition:
    [var, N] = condition.split('<')
    N = int(N)
    [lo,hi] = region[var]
    if lo >= N:
      PASS = None
    elif hi < N:
      PASS[var] = [lo,hi]
      FAIL = None
    else:
      PASS[var] = [lo, N-1]
      FAIL[var] = [N, hi]
  elif '>' in condition:
    [var, N] = condition.split('>')
    N = int(N)
    [lo,hi] = region[var]
    if hi <= N:
      PASS = None
    elif lo > N:
      PASS[var] = [lo,hi]
      FAIL = None
    else:
      PASS[var] = [N+1,hi]
      FAIL[var] = [lo, N]
  return (PASS, FAIL)

# r = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}

# (r1, r2) = (split_region(r, 'a<2006'))

# print(r1)
# print(r2)
# print()

# show(split_region(r2, 'a>2005'))

def main_b_v2(ip_file):
  # Get the dictionary mapping node names to rule lists
  D = parse_input_commands(ip_file[0])
  # The initial state has all of phase space at node 'id':
  to_process = [('in', {k : [1,4000] for k in ['x','m','a','s']})]
  # Initially nothing has flowed out to nodes 'A' or 'R'
  A = []
  R = []

  while to_process:
    (node, region) = to_process.pop()   # We have a `region` of phase space concentrated at `node`
    if node == 'A':
      A.append(region)
      continue
    elif node == 'R':
      R.append(region)
      continue

    # Otherwise we're at a non-terminal node, so we want to:
      # split `region` amongst the successor nodes according to the rule
      # append these pairs of nodes and regions back onto `to_process`
    rule_list = D[node]   # get the rule list corresponding to `node`
    for [cnd, dst] in rule_list:
      # Split `region` into PASS and FAIL according to the condition
      if not cnd:  # if the condition is empty, everything in the current region passes
        to_process.append((dst, region))  # Assign the entire region to node `dst`
      else:  
        (PASS, FAIL) = split_region(region, cnd)

      if PASS:
        to_process.append((dst, PASS))  # Assign the PASS region to node `dst`
      if FAIL:  # If there's any more region to process
        region = FAIL
        #  and roll on to the next rule in `rule_list`
  # Now we've processed everything, and all of phase space should be assigned to 'A' or 'R'
  return A


# print(main_b_v2(test_input))  #  
# print(main_b_v2(input))       # 


# TTT.timecheck("Part (b)")  #

################################