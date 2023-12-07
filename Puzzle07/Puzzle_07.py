# https://adventofcode.com/2023/day/7

from collections import Counter
from operator import itemgetter

f = open("Puzzle07_test.txt")
test_input = f.read().splitlines()
f.close()

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

# Every hand is exactly one type. From strongest to weakest, they are:
type_name = ["",
"Five of a kind",
"Four of a kind",
"Full house",
"Three of a kind",
"Two pair",
"One pair",
"High card"
]


def compute_winnings(ip, scoring_function):
  '''Given a text input representing hands and bids, 
  and a scoring function assigning a hand type to each hand,
  return the total winnings'''
  # parse each input line as `hand`:list[str] and `bid`:int
  ip = [line.split() for line in ip]
  ip = [[list(hand), int(bid)] for [hand,bid] in ip]
  # make a Counter from each hand, e.g. Counter({'K': 2, '7': 2, '6': 1}), and insert this
  ip = [[hand, Counter(hand), bid] for [hand,bid] in ip]

  # map cards to numerical values
  ip = [[[card_vals[x] for x in hand], ctr, bid] for [hand,ctr,bid] in ip]
  # prepend hand-type values
  ip = [[-scoring_function(ctr), hand,ctr,bid] for [hand,ctr,bid] in ip]

  # Sort the hands, first by hand type, then by highest 1st card, highest 2nd card, etc.
  # `reverse=True`, so the lowest scoring card is placed first
  # From https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
  ip.sort(key = itemgetter(0,1), reverse=True)
  ip.reverse()

  # list the bids in order, each paired with its rank
  winnings_list = enumerate([bid for [_,_,_,bid] in ip], start=1)

  winnings = [rank * bid for (rank,bid) in list(winnings_list)]
  print(sum(winnings))



################################
# Part (a)
################################

def hand_type_a(ctr):
  '''Given the Counter derived from a hand, 
  e.g. Counter({'K': 2, '7': 2, '6': 1})
  return its rank (1 highest, 7 lowest)'''
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

def main_a(ip):
  return compute_winnings(ip, hand_type_a)

main_a(test_input)  # 6440
main_a(input)       # 251216224


################################
# Part (b)
################################

# J cards are now the weakest individual cards
card_vals['J'] = 1

# J cards can pretend to be whatever card is best for the purpose of determining hand type; 
# for example, QJJQ2 is now considered four of a kind. 
# However, for the purpose of breaking ties between two hands of the same type, 
# J is always treated as J, not the card it's pretending to be: 
# JKKK2 is weaker than QQQQ2 because J is weaker than Q.

# This re-scoring function uses the fact that 
# it's always best for all Js to switch to the same other type
def hand_type_b(ctr):
  '''Given the Counter derived from a hand, 
  e.g. Counter({'K': 2, '7': 2, '6': 1})
  return its rank (1 highest, 7 lowest)'''
  if ctr['J'] < 1:        # If 'J' is not in the hand, use the original function
    return hand_type_a(ctr)
  else:
    j = ctr['J']
    possible_types = []
    for k in card_vals.keys():
      temp_ctr = ctr.copy()
      del temp_ctr['J']  # remove the 'J' entry from temp_ctr
      temp_ctr[k] += j       # Let the Js pretend to be of type k
      new_score = hand_type_a(temp_ctr)
      possible_types.append(new_score)  # record what type such a hand would have
    return min(possible_types)


def main_b(ip):
  return compute_winnings(ip, hand_type_b)

main_b(test_input)  # 5905
main_b(input)       # 250825971