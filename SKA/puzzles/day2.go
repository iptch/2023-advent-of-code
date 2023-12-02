package puzzles

import (
	"bufio"
	"regexp"
	"strings"
)

var availableCubes = map[string]int{
	"red":   12,
	"green": 13,
	"blue":  14,
}

func Day2Task1() {

	input := openTextFile("inputs/aoc02.txt")

	sum := 0
	gameIdRegex := regexp.MustCompile(`\d+`)
	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		line := scanner.Text()
		gameSegments := strings.Split(line, ":")

		gameID := stringToNumber(gameIdRegex.FindAllString(gameSegments[0], -1)[0])
		gameSets := strings.Split(gameSegments[1], ";")

		if gameSetPossible(gameSets) {
			sum += gameID
		}

	}

	print(sum)
}

func Day2Task2() {
	input := openTextFile("inputs/aoc02.txt")

	sum := 0
	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		minGreen := 0
		minBlue := 0
		minRed := 0

		line := scanner.Text()
		gameSegments := strings.Split(strings.Split(line, ":")[1], ";")
		for _, segment := range gameSegments {
			cubeColorMap := getCubeColorMap(segment)
			minGreen = maximum(minGreen, cubeColorMap["green"])
			minBlue = maximum(minBlue, cubeColorMap["blue"])
			minRed = maximum(minRed, cubeColorMap["red"])
		}
		sum += (minGreen * minBlue * minRed)
	}
	print(sum)
}

func maximum(x int, y int) int {
	if x >= y {
		return x
	} else {
		return y
	}
}

func getCubeColorMap(set string) map[string]int {
	cubeColorMap := make(map[string]int)
	cubeSegments := strings.Split(set, ",")
	digitRegex := regexp.MustCompile(`\d+`)
	wordRegex := regexp.MustCompile(`[a-zA-z]+`)

	for _, segment := range cubeSegments {
		color := wordRegex.FindAllString(segment, -1)[0]
		number := stringToNumber(digitRegex.FindAllString(segment, -1)[0])
		cubeColorMap[color] = number
	}

	return cubeColorMap
}

func cubesAvailable(gameCubes map[string]int) bool {
	for color, number := range gameCubes {
		if number > availableCubes[color] {
			return false
		}
	}

	return true
}

func gameSetPossible(gameSets []string) bool {
	for _, set := range gameSets {
		cubeColorMap := getCubeColorMap(set)
		if !cubesAvailable(cubeColorMap) {
			return false
		}
	}

	return true
}
