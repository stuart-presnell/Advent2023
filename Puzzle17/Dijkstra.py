from math import inf
from PQueue import PQ
from collections import defaultdict

# TODO: Edit `Dijkstra` to record the states visited along the shortest path taken
# https://stackoverflow.com/a/28999743

def Dijkstra(matrix, STARTS, ENDS, ACCESSIBLE_NEIGHBOURS, STEP_COST, verbose = False):
  '''Given a `matrix`, represented as a dictionary whose keys are states,
  and a set/list of `START` states,
  and a (possibly empty) set/list of `END` states,
  with a function `ACCESSIBLE_NEIGHBOURS(matrix, st)` returning a list of states,
  and a function `STEP_COST(matrix, st, st2)` returning an integer,
  run Dijkstra's algorithm to work out the cheapest route from some `START` state 
  to each reachable state, stopping when we reach any of the `END` states (if provided).
  Return this as a dictionary whose keys are states and whose values are integers.'''

  # Assign to every node a tentative distance value, initialised to infinity
  # Store this in a `defaultdict` for quicker lookup, since we don't need the matrix structure
  t_dist = defaultdict(lambda : inf)

  # Give all the starting nodes a distance of 0
  if not STARTS:
    raise ValueError("Need at least one starting point")
  for s in STARTS:
    t_dist[s] = 0

  # Make a Priority Queue of nodes that have not yet been visited.
  # Each item on the queue is a pair `(t, state)`, where `t` is the tentative distance to `state`
  # Being a Priority Queue means we can efficiently pop off the item with the smallest `t`.
  unvisited = PQ()
  for state in matrix:
    unvisited.add_item(state, t_dist[state])

  def is_unvisited(state):
    return unvisited.find_item(state)

  def update_one_step():
    # select the unvisited node that is marked with the smallest tentative distance T; 
    # mark it as visited by popping it from `unvisited`
    (T, st) = unvisited.pop_item_with_priority()
    # If the smallest T of any unvisited node is inf then we've visited every accessible node, 
    # so tell the parent function to break
    if T == inf:  
      return True  # This is collected by the parent function as a variable `FINISHED`
    if verbose: print("Selected point " + str(st) + " which has T = " + str(T)) 
    # Make a list of all the unvisited neighbours of current point `(x,y)`
    unvis_neighbours = [st2 for st2 in ACCESSIBLE_NEIGHBOURS(matrix, st) if is_unvisited(st2)]
    if verbose: print(unvis_neighbours)
    for st2 in unvis_neighbours:
      # for each unvisited neighbour, 
      # reset its tentative distance to T + STEP_COST(here, there) if that's < its current value
      cost = STEP_COST(matrix, st, st2)
      if T + cost < t_dist[st2]: 
        if verbose: print("Resetting " + str(st2) + " to " + str(T+cost))
        t_dist[st2] = T + cost
        # replace the point st2 in `unvisited` with new tentative distance T + cost
        unvisited.add_item(st2, T + cost)
    return False # We don't think we've reached every reachable square yet

  FINISHED = False
  if ENDS:
    # If we have a destination (or set of possible destinations) in mind:
    # Keep taking steps until one of the destinations in ENDS is marked as visited
    # or `update_one_step` reports that it has FINISHED exploring reachable squares
    while (not FINISHED) & all([is_unvisited(x) for x in ENDS]):
      FINISHED = update_one_step()
    return(t_dist)
  else:  
    # If we've passed `ENDS = set()` then walk to every square we can reach
    while (not FINISHED) & (not unvisited.is_empty()):
      FINISHED = update_one_step()
    return(t_dist)


# def example1():
#   M = {(x,y) : 1 for x in range(5) for y in range(3)}
#   STARTS = [(0,0)]
#   ENDS = [(4,2)]

#   def ACCESSIBLE_NEIGHBOURS(matrix, st):
#     (x,y) = st
#     raw = [(x-1, y),(x+1, y),(x, y-1),(x, y+1)]
#     return [pt for pt in raw if pt in matrix]

#   def STEP_COST(matrix, st, st2):
#     return 1

#   return Dijkstra(M, STARTS, ENDS, ACCESSIBLE_NEIGHBOURS, STEP_COST, verbose = False)

# t = example1()
# t[(4,2)]    # 6