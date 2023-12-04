INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def parse_input():
    results = []

    for line in INPUT.split("\n"):
        seen_balls = {}
        line = line.split(": ")[1]
        draws = line.split("; ")
        for draw in draws:
            ball_colors = draw.split(', ')
            for ball_color in ball_colors:
                count, color = ball_color.split(' ')
                if seen_balls.get(color) is None:
                    seen_balls[color] = int(count)
                elif seen_balls[color] < int(count):
                    seen_balls[color] = int(count)

        results.append(seen_balls)
    return results


def possible_game_sums(game_results, content):
    sum = 0

    for i, game_result in enumerate(game_results):
        print(game_result)
        possible = True
        for color in game_result.keys():
            if content.get(color) is None or content[color] < game_result[color]:
                possible = False
                break
        if possible:
            sum += i+1

    return sum


def power_of_minimum(game_results):
    powers = []

    for game_result in game_results:
        power = 1
        for color in game_result.keys():
            power *= game_result[color]
        powers.append(power)

    return powers


if __name__ == '__main__':
    game_results = parse_input()
    content = {'red': 12, 'green': 13, 'blue': 14}

    # print(possible_game_sums(game_results, content))
    print(power_of_minimum(game_results))
    print(sum(power_of_minimum(game_results)))
