import re

# https://adventofcode.com/2023/day/2

# "[You have] a small bag and some cubes which are either red, green, or blue.
# Each time you play this game, he will hide a secret number of cubes of each color in the bag,
# and your goal is to figure out information about the number of cubes."


# test_input : list[str] = [
# "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
# "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
# "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
# "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
# "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
# ]


def parse_outcome(s:str) -> dict[str, int]:
  '''Given a string of the form "x blue, y red, z green" (in some order),
   return a dictionary "{'red': y, 'green': z, 'blue': x} '''
  d = dict.fromkeys(('red', 'green', 'blue'), 0) # Initialise dictionary with all values set to 0
  color_nums:list[str] = s.split(", ")  # e.g. ['1 red', '2 green', '6 blue']
  for elt in color_nums:
    e = elt.split() # e.g. ['1', 'red']
    n:int = int(e[0])  # e.g. 1
    k:str = e[1]       # e.g. 'red'
    d[k] = n
  return d

def parse_game_string(s:str) -> int:
  [gn, rounds] = s.split(": ")
  game_number_str = re.sub("Game ", "", gn)
  game_number = int(game_number_str)
  rounds_list:list[str] = rounds.split("; ")
  parsed_rounds_list = list(map(parse_outcome,rounds_list))
  return (game_number, parsed_rounds_list)


################################
# Part (a)
################################

# Determine which games would have been possible
# if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
# What is the sum of the IDs of those games?

limit = {'red': 12, 'green': 13, 'blue': 14}

def does_not_exceed(test,limit) -> bool:
  '''Given two `dict[str,int]`, check that test[k] <= limit[k] for all k'''
  for k in test:
    if test[k] > limit[k]:
      return False
  return True

def check_game(g, limit):
  '''Given a parsed game string (as a list of dictionaries),
  check that each round in the game does not exceed the limits'''
  checks = map(lambda r : does_not_exceed(r,limit), g)
  return all(checks)


# f = open("Puzzle02_test.txt")
f = open("Puzzle02_input.txt")

sum_of_game_ids = 0
for s in f:
  ps = parse_game_string(s)
  game_number:int = ps[0]
  g:list[dict[str, int]] = ps[1]
  # print(g)
  if check_game(g,limit):
    sum_of_game_ids+= game_number

f.close()

print("sum_of_game_ids = " + str(sum_of_game_ids)) # 2476


################################
# Part (b)
################################

# In each game you played,
# what is the fewest number of cubes of each color that could have been in the bag
# to make the game possible?


# f = open("Puzzle02_test.txt")
f = open("Puzzle02_input.txt")


total_power = 0

for s in f:   # For each line (i.e. each game) in the file
  max_d = dict.fromkeys(('red', 'green', 'blue'), 0)   # Initialise dictionary with all values 0

  ps = parse_game_string(s)
  game : list[dict[str, int]] = ps[1]   # The game, as a list of dicts
  for round in game:
    for k in round:
      max_d[k] = max(max_d[k], round[k])  # If current exceeds best so far, update
  power = max_d['red'] * max_d['green'] * max_d['blue']
  total_power += power
f.close()


print("total_power = " + str(total_power)) # 54911
