# https://adventofcode.com/2023/day/4

import re

# f = open("Puzzle04_test.txt")
f = open("Puzzle04_input.txt")
input = f.read().splitlines()
f.close()

def show(x):
  for line in x:
    print(line)
  print("-" * len(x[0]))
  print()


################################
# Part (a)
################################

# Each card has two lists of numbers separated by a vertical bar (|): 
# a list of winning numbers and then a list of numbers you have.
# You have to figure out which of the numbers you have appear in the list of winning numbers. 
# The first match makes the card worth one point 
# and each match after the first doubles the point value of that card.

# How many points are [the set of cards] worth in total?

# show(input)

def card_wins(card:str):
  '''Given a card, represented as a string, find the list of winning numbers'''
  [card_no, winners, my_numbers] = re.split(r": | \| ", card)
  winners = winners.split()
  my_numbers = my_numbers.split()
  my_wins = filter(lambda x: x in winners, my_numbers)
  return list(my_wins)

def card_score(card:str):
  cw = card_wins(card)
  if len(cw) == 0:
    return 0
  else:
    return 2 ** (len(cw) - 1)

counter = 0
for line in input:
  counter += card_score(line)
# print(counter) # 19855

################################
# Part (b)
################################

# We start with one copy of each card
cards_in_hand = dict.fromkeys(range(1,len(input)+1), 1)

# print(cards_in_hand)

i = 0
for card in input:
  i += 1   # i is the number of the current card
  number_of_wins = len(card_wins(card))
  for x in range(1, number_of_wins+1):
    cards_in_hand[i+x] += cards_in_hand[i]   # for each copy of the current card, we win a copy of the next `number_of_wins` cards

# print(cards_in_hand)
total = sum(list(cards_in_hand.values()))
print(total) # 10378710
