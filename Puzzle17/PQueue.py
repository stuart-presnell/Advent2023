# Modified and extended from:
# https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes

from heapq import *
from itertools import count

REMOVED = '<removed-item>'      # placeholder for a removed item

class PQ():
  def __init__(self):
    self.pq = []               # list of entries arranged in a heap
    self.entry_finder = {}     # mapping of items to entries
    self.counter = count()     # unique id
  def to_list(self):
    content = [[p, item] for [p, _, item] in self.pq if item is not REMOVED]
    return(content)
  def show(self):
    print(self.to_list())

  def add_item(self, item, priority=0):
      'Add a new item or update the priority of an existing item'
      if item in self.entry_finder:
          self.remove_item(item)
      id = next(self.counter)
      entry = [priority, id, item]
      self.entry_finder[item] = entry
      heappush(self.pq, entry)

  def remove_item(self, item):
      'Mark an existing item as REMOVED.  Raise KeyError if not found.'
      entry = self.entry_finder.pop(item)
      entry[-1] = REMOVED

  def pop_item(self):
      'Remove and return the lowest priority item. Raise KeyError if empty.'
      while self.pq:
          priority, id, item = heappop(self.pq)
          if item is not REMOVED:
              del self.entry_finder[item]
              return item
      raise KeyError('pop from an empty priority queue')
  
  def pop_item_with_priority(self):
      'Remove and return the lowest priority item. Raise KeyError if empty.'
      while self.pq:
          priority, id, item = heappop(self.pq)
          if item is not REMOVED:
              del self.entry_finder[item]
              return (priority, item)
      raise KeyError('pop from an empty priority queue')
  
  def find_item(self,item):
      return (item in self.entry_finder) & (item is not REMOVED)
  
  def is_empty(self):
      return not [item for item in self.entry_finder if item is not REMOVED]