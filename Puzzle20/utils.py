from time import perf_counter

def chunk_splitlines(s:str) -> list[list[str]]:
  '''Given a string obtained e.g. from `f.read()`, 
  split the file at blank lines, 
  and then split each chunk at newlines'''
  return [x.splitlines() for x in s.split("\n\n")]

def printT(x):
  '''Print input and also show its type'''
  print(x, "\t of type \t", type(x))

def show(x, underline=True):
  '''Given any iterable `x`, print each element of `x` on a separate line'''
  for line in x:
    print(line)
  if underline:
    try:
      num_dashes = len(x[0])
    except: 
      num_dashes = 20
    print("-" * num_dashes)

def showM(M:list[list[int]], max_digits=2):
  '''Display matrix `M` with columns aligned.
  `max_digits` is the largest number of digits in any matrix entry.
  Modified from: https://stackoverflow.com/a/17871279'''
  col_width = max_digits + 2
  format_string = '{:' + str(col_width) + '}'
  print('\n'.join([''.join([format_string.format(item) for item in row]) for row in M]))

def showD(d:dict):
  '''Given a dictionary `d` that might have null values (e.g. if it's a `defaultdict` with default value `[]`), 
  print only the key-value pairs where the value is non-null.'''
  for k in d:
    if d[k]: 
      print(k, "\t:\t", d[k])

# From: https://stackoverflow.com/a/22115957
def unzip(iterable):
    '''Given a list of `k` lists of length `n`, return an iterator of `n` `k`-tuples.
    - e.g. [['a', 1, 10], ['b', 2, 20], ['c', 3, 30], ['d', 4, 40]] ->
         [('a', 'b', 'c', 'd'), (1, 2, 3, 4), (10, 20, 30, 40)].'''
    return zip(*iterable)

def parse_nums(s:str, sep=" ") -> list[int]:
  '''Given a string of the form `"a<sep>b<sep>c<sep>...<sep>z"`, where each entry is a number, 
  return a `list[int]`'''
  op = s.split(sep)
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

def cmp(a:int, b:int) -> int:
  '''Compare two integers: return -1 if a < b, 0 if a == b and +1 if a > b.'''
  return (a > b) - (a < b) 

def qsort(arr, CMP = lambda x,y:x<y):
  '''Given a list `arr : list[A]` 
  [and an optional comparison operator `CMP : A -> A -> bool`, default = `<`],
  sort `arr` according to `CMP` using the quicksort algorithm'''
  if len(arr) <= 1:
    return arr
  else:
    pivot = arr[0]  
    L = qsort([x for x in arr[1:] if     CMP(x, pivot)], CMP)  # elts x < pivot
    R = qsort([x for x in arr[1:] if not CMP(x,pivot)], CMP)   # all other elts
    return L + [pivot] + R

def nwise_cycled(L, n=3):
  '''Given a list `L`, return a list of all consecutive triples, cycling around the end of the list: 
  `[L[0],L[1],L[2]]`,
  `[L[1],L[2],L[3]]`, ..., 
  `[L[-2],L[-1],L[0]]`,
  `[L[-1],L[0],L[1]]`.
  For `n`-tuples instead of triples, pass `n` as an optional argument.'''
  m = len(L)
  if m < n:  # If there are no triples...
    return []
  op = []
  for i in range(m):
    x = [L[(i+k)%m] for k in range(n)]
    op.append(x)
  return op



class Best():
  '''A class to package up the notion of finding the most extreme example of something.
  By default, Best is initialised to `0` and comparision criterion `x > best_so_far`.'''
  def __init__(self, initial_value = 0, criterion = lambda x,y:x>y):
    self.best_so_far = initial_value
    self.criterion = criterion
  def __str__(self) -> str:
    return str(self.best_so_far)
  def update(self, value):
    if self.criterion(value, self.best_so_far):
      self.best_so_far = value
  def reduce(self, L):
    for x in L:
      self.update(x)
    return self.best_so_far


class Timer():
  '''By default, a Timer stays silent and doesn't report timechecks, even when asked.
    Initialise with Timer(True) to get a timer that prints timechecks.'''
  def __init__(self, reporting = False):
    self.reporting = reporting
    self.count = 0  # Count how many timechecks have been requested
    # Check the time when initialised and log this in a list
    self.time_list = [perf_counter()]
  def timecheck(self, name=''):
    if not self.reporting: return
    now = perf_counter()
    elapsed = now - self.time_list[-1]
    timecheck_string = "TIMECHECK " + str(self.count) + ": \t"
    print(timecheck_string + str(elapsed * 1000) + " ms", end='')
    if name:
      print("\t (" + name + ")")
    else:
      print()
    self.count += 1


class Looper():
  '''Given a list that loops, extrapolate the list arbitrarily long by extending the loop.'''
  def __init__(self, L):
    '''This assumes that the sequence `L` is *deterministic*: the first repetition starts a loop.'''
    self.L = L
    for i in range(len(L)):
      # print(i, L[i], L[:i], L[i] in L[:i])
      if L[i] in L[:i]:
        self.loop_start = L.index(L[i])
        self.period = i - self.loop_start
        return
    raise ValueError("Reached end of list without finding a loop")
  def __getitem__(self, idx):
    if idx > self.loop_start + self.period:
      idx = (idx - self.loop_start)%self.period + self.loop_start
    return self.L[idx]
