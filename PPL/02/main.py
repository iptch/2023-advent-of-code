from timeit import default_timer as timer
import re


def puzzle_1():
    input_txt = open("input.txt", "r")
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    total = 0
    for line in input_txt:
        game_groups = re.match(r"Game (\d+): (.*)", line)
        number = int(game_groups.group(1))
        draws = game_groups.group(2).split("; ")
        for draw in draws:
            for take in draw.split(", "):
                split = take.split(" ")
                count = int(split[0])
                color = split[1]
                if bag[color] < count:
                    number = 0
        total += number
    return total


def puzzle_2():
    input_txt = open("input.txt", "r")
    total = 0
    for line in input_txt:
        bag = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        game_groups = re.match(r"Game (\d+): (.*)", line)
        draws = game_groups.group(2).split("; ")
        for draw in draws:
            for take in draw.split(", "):
                split = take.split(" ")
                count = int(split[0])
                color = split[1]
                bag[color] = max(bag[color], count)
        total += bag["red"] * bag["green"] * bag["blue"]
    return total


if __name__ == '__main__':
    start1 = timer()
    print(f"Puzzle 1: {puzzle_1()} (in {timer()-start1}sec)")
    start2 = timer()
    print(f"Puzzle 2: {puzzle_2()} (in {timer()-start2}sec)")