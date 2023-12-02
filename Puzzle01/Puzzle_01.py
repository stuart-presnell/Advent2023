import re

# https://adventofcode.com/2023/day/1

# "On each line, the calibration value can be found
#  by combining the first digit and the last digit (in that order)
# to form a single two-digit number."

################################
# Part (a)
################################

# test_input : list[str] = [
# "1abc2",        # 12
# "pqr3stu8vwx",  # 38
# "a1b2c3d4e5f",  # 15
# "treb7uchet"    # 77
# ]

# f = open("Puzzle01_test.txt")
f = open("Puzzle01_input.txt")

sum = 0

for s in f:
  digits = re.findall(r"\d", s)
  a = int(digits[0])
  z = int(digits[-1])
  sum += 10*a + z

print("sum = " + str(sum)) # 55538

f.close()


################################
# Part (b)
################################

# test_input : list[str] = [
# "two1nine",
# "eightwothree",
# "abcone2threexyz",
# "xtwone3four",
# "4nineeightseven2",
# "zoneight234",
# "7pqrstsixteen"]

# 29, 83, 13, 24, 42, 14, and 76

def convert_to_number(s:str) -> int:
  '''Given a string that's either a digit '3' or a word 'three', return the corresponding int'''
  d = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}
  p = re.compile(r'(one|two|three|four|five|six|seven|eight|nine)')
  # Match `s` against pattern `p`, look up any match in dictionary `d` and return the value
  # If there's no match in the re search, return `s` unchanged
  x = p.sub(lambda m : d[m.group()], s)
  return int(x)



# f = open("Puzzle01_test_b.txt")
f = open("Puzzle01_input.txt")

sum = 0

# for s in test_input:
for s in f:
  a = re.match(r".*?(one|two|three|four|five|six|seven|eight|nine|\d)", s).group(1)
  z = re.match(r".*(one|two|three|four|five|six|seven|eight|nine|\d)", s).group(1)
  a = convert_to_number(a)
  z = convert_to_number(z)
  # print(s + ": " + str(10*a + z))
  sum += 10*a + z

print("sum = " + str(sum)) # 54875

f.close()
