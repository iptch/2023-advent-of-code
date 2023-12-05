package puzzles

import (
	"bufio"
	"regexp"
	"strings"
)

func Day4Task1() {
	input := openTextFile("inputs/aoc04.txt")
	scanner := bufio.NewScanner(input)

	sum := 0

	for scanner.Scan() {
		line := scanner.Text()
		winningNumbers := parseWinningNumbers(line)
		ownNumbers := parseOwnNumbers(line)
		gameScore := calculateGameScore(winningNumbers, ownNumbers)
		sum += gameScore
	}

	print(sum)
}

type CardsAndScore struct {
	Cards int
	Score int
}

func Day4Task2() {
	input := openTextFile("inputs/aoc04.txt")
	scanner := bufio.NewScanner(input)

	cardsAndScores := make([]CardsAndScore, 0)

	for scanner.Scan() {
		line := scanner.Text()
		winningNumbers := parseWinningNumbers(line)
		ownNumbers := parseOwnNumbers(line)
		overlap := calculateOverlap(winningNumbers, ownNumbers)

		cardsAndScores = append(cardsAndScores, CardsAndScore{1, overlap})
	}

	for idx, card := range cardsAndScores {
		if card.Score == 0 {
			continue
		}

		for i := 1; i <= card.Score; i++ {
			currentIndex := idx + i

			if currentIndex > len(cardsAndScores)-1 {
				break
			}

			cardsAndScores[currentIndex].Cards += card.Cards
		}
	}

	sum := 0
	for _, card := range cardsAndScores {
		sum += card.Cards
	}

	print(sum)

}

func parseWinningNumbers(in string) []int {
	regex := regexp.MustCompile(`\d+`)
	winningNumbersString := strings.Split(in, "|")[0]

	winningNumbersList := regex.FindAllString(winningNumbersString, -1)

	winningNumbers := make([]int, 0)

	// omit the first number, since it is the Card index
	for _, winner := range winningNumbersList[1:] {
		winningNumbers = append(winningNumbers, stringToNumber(winner))
	}

	return winningNumbers
}

func parseOwnNumbers(in string) []int {
	regex := regexp.MustCompile(`\d+`)
	ownNumbersString := strings.Split(in, "|")[1]

	ownNumbersList := regex.FindAllString(ownNumbersString, -1)

	ownNumbers := make([]int, 0)

	for _, own := range ownNumbersList {
		ownNumbers = append(ownNumbers, stringToNumber(own))
	}

	return ownNumbers
}

func calculateGameScore(winners []int, own []int) int {
	score := 0

	for _, ownNumber := range own {
		if !existsInList(ownNumber, winners) {
			continue
		} else {
			if score == 0 {
				score = 1
			} else {
				score *= 2
			}
		}
	}

	return score
}

func existsInList(number int, list []int) bool {
	for _, entry := range list {
		if entry == number {
			return true
		}
	}

	return false

}

func calculateOverlap(winners []int, own []int) int {
	overlap := 0

	for _, ownNumber := range own {
		if existsInList(ownNumber, winners) {
			overlap++
		}
	}

	return overlap
}
