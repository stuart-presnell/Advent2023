def chunk_splitlines(s:str) -> list[list[str]]:
  '''Given a string obtained e.g. from `f.read()`, 
  split the file at blank lines, 
  and then split each chunk at newlines'''
  return [x.splitlines() for x in s.split("\n\n")]

def show(x):
  '''Given any iterable `x`, print each element of `x` on a separate line'''
  for line in x:
    print(line)
  try: print("-" * len(x[0]))
  except: print("-" * 5)
  print()

def parse_nums(s:str) -> list[int]:
  '''Given a string of the form `"a b c ... z"`, where each entry is a number, 
  return a `list[int]`'''
  op = s.split()
  op = list(map(int,op))  # This will raise an error if any entry doesn't parse as a number
  return op

def rotate90(M):
  '''Given a matrix `M` consisting of a list of strings (or a list of lists), 
  rotate it 90 degrees clockwise'''
  return [list(reversed([M[j][i] for j in range(len(M))]))
            for i in range(len(M[-1]))]

def close_bracket(s:str) -> str:
  '''Given a string starting with `(`, `[`, or `{`, 
  return the initial substring up to and including the matching closing bracket
  or raise `ValueError` if this cannot be done'''
  closing = {'(':')', '[':']', '{':'}'}   # closing[x] is the matching closing bracket to x
  if len(s) < 1:
    raise ValueError("String is empty, and so does not start with an opening bracket")
  if s[0] not in closing:
    raise ValueError("String does not start with an opening bracket")
  op = s[0]         # the particular kind of opening bracket that s starts with
  cl = closing[op]  # the corresponding closing bracket 
  i = 0             # pointer to a character in the string, indexed from 0
  count = 1         # net number of opening - closing brackets seen so far
  for x in s[1:]:   # step through the remaining characters of the string
    i += 1
    if x == op:
      count += 1
    if x == cl:
      count -= 1
      if count == 0: # if we've found the matching closing bracket
        return s[:i+1]
      elif count < 0: # if we've got a net negative number of brackets
        raise ValueError("More closing brackets than opening brackets")  # UNREACHABLE?
  # if we get here, we've fallen off the end of s without matching the opening bracket
  raise ValueError("Initial opening bracket is not balanced with a matching closing bracket")