# https://adventofcode.com/2023/day/7

from collections import Counter
from operator import itemgetter

# f = open("Puzzle07_test.txt")
f = open("Puzzle07_input.txt")
input = f.read().splitlines()
f.close()

def show(x):
  for line in x:
    print(line)
  print("-" * len(x[0]))
  print()

def parse_nums(s:str) -> list[int]:
  '''Given a string of the form "a b c ... z", where each entry is a number, return a list[int]'''
  op = s.split()
  op = list(map(int,op))  # This will raise an error if any entry doesn't parse as a number
  return op

def rotate90(M):
  '''Given a matrix `M` consisting of a list of strings (or a list of lists), 
  rotate it 90 degrees clockwise'''
  return [list(reversed([M[j][i] for j in range(len(M))]))
            for i in range(len(M[-1]))]

################################

# In Camel Cards, you get a list of hands, and your goal is to order them 
# based on the strength of each hand. 
# A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. 
# The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

card_vals = {str(x):x for x in range(2,10)}
card_vals['T'] = 10
card_vals['J'] = 11
card_vals['Q'] = 12
card_vals['K'] = 13
card_vals['A'] = 14 # Don't forget, aces are high, not low!

# parse each input line as `hand`:list[str] and `bid`:int
input = [line.split() for line in input]
input = [[list(hand),int(bid)] for [hand,bid] in input]
input = [[[card_vals[x] for x in hand], Counter(hand), bid] for [hand,bid] in input]
# show(input)

# Every hand is exactly one type. From strongest to weakest, they are:
# 1:  Five of a kind, 
# where all five cards have the same label: AAAAA
# 2:  Four of a kind, 
# where four cards have the same label and one card has a different label: AA8AA
# 3:  Full house,
#  where three cards have the same label, and the remaining two cards share a different label: 23332
# 4:  Three of a kind, 
# where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 5:  Two pair, 
# where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 6:  One pair, 
# where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 7:  High card, 
# where all cards' labels are distinct: 23456

type_name = ["","Five of a kind","Four of a kind","Full house","Three of a kind","Two pair","One pair","High card"]

def hand_type(ctr):
  '''Given the Counter derived from a hand, return its rank (1 highest, 7 lowest)'''
  counts = sorted(list(ctr.values()))
  match len(ctr):
    case 1:       
      return 1    # Five of a kind (AAAAA)
    case 2:
      if counts == [1,4]:
        return 2  # Four of a kind (2AAAA)
      elif counts == [2,3]:
        return 3  # Full house (22333)
    case 3:
      if counts == [1,1,3]:
        return 4  # Three of a kind (89TTT)
      elif counts == [1,2,2]:
        return 5  # Two pair (22334)
    case 4:       
      return 6    # One pair (234AA)
    case 5:       
      return 7    # High card (23456)

################################
# Part (a)
################################

# # prepend hand-type values
# input = [[-hand_type(ctr), hand,ctr,bid] for [hand,ctr,bid] in input]

# # Sort the hands, first by hand type, then by highest 1st card, highest 2nd card, etc.
# # `reverse=True`, so the lowest scoring card is placed first
# # From https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
# input.sort(key = itemgetter(0,1), reverse=True)
# input.reverse()
# # show(input)

# # list the bids in order, each paired with its rank
# winnings_list = enumerate([bid for [_,_,_,bid] in input], start=1)

# winnings = [rank * bid for (rank,bid) in list(winnings_list)]
# print(sum(winnings)) # 251216224

################################
# Part (b)
################################


